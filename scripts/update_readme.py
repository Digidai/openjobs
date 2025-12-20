#!/usr/bin/env python3
"""
从 XML 源获取职位信息并更新 README.md
动态发现最新数据源，每次运行展示 100 条职位，根据时间轮换
"""

import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime, timezone
import re
import os

SITEMAP_URL = "https://www.openjobs-ai.com/xml/sitemap.xml"
README_PATH = "README.md"
HTML_PATH = "public/index.html"
JOBS_PER_PAGE = 100
ROTATION_HOURS = 6
DEFAULT_LOGO = "https://www.openjobs-ai.com/logo.png"

def fetch_xml(url):
    """获取 XML 内容"""
    print(f"  Fetching: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; OpenJobs/1.0)'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8')

def clean_xml_namespaces(xml_content):
    """移除 XML 命名空间以简化解析"""
    xml_content = re.sub(r'\sxmlns[^"]*"[^"]*"', '', xml_content)
    xml_content = re.sub(r'<(/?)image:', r'<\1image_', xml_content)
    return xml_content

def get_latest_month_index():
    """从 sitemap.xml 获取最新月份的索引文件 URL"""
    print("Step 1: Finding latest month index...")
    xml_content = fetch_xml(SITEMAP_URL)
    xml_content = clean_xml_namespaces(xml_content)

    root = ET.fromstring(xml_content)

    # 查找所有 sitemap-index-YYYY-MM.xml 格式的 URL
    month_indexes = []
    for sitemap in root.findall('.//sitemap'):
        loc = sitemap.find('loc')
        if loc is not None and loc.text:
            url = loc.text.strip()
            # 匹配 sitemap-index-YYYY-MM.xml 格式
            match = re.search(r'sitemap-index-(\d{4})-(\d{2})\.xml$', url)
            if match:
                year, month = int(match.group(1)), int(match.group(2))
                month_indexes.append((year, month, url))

    if not month_indexes:
        raise ValueError("No month index files found in sitemap.xml")

    # 按年月排序，获取最新的
    month_indexes.sort(key=lambda x: (x[0], x[1]), reverse=True)
    latest = month_indexes[0]
    print(f"  Found latest month: {latest[0]}-{latest[1]:02d}")
    return latest[2]

def get_latest_part_url(month_index_url):
    """从月份索引获取最新的 part 文件 URL"""
    print("Step 2: Finding latest part file...")
    xml_content = fetch_xml(month_index_url)
    xml_content = clean_xml_namespaces(xml_content)

    root = ET.fromstring(xml_content)

    # 查找所有 jobs-detail-YYYY-MM-partN.xml 格式的 URL
    part_files = []
    for sitemap in root.findall('.//sitemap'):
        loc = sitemap.find('loc')
        if loc is not None and loc.text:
            url = loc.text.strip()
            # 匹配 jobs-detail-YYYY-MM-partN.xml 格式
            match = re.search(r'jobs-detail-\d{4}-\d{2}-part(\d+)\.xml$', url)
            if match:
                part_num = int(match.group(1))
                part_files.append((part_num, url))

    if not part_files:
        raise ValueError("No part files found in month index")

    # 按 part 编号排序，获取最大的（最新的）
    part_files.sort(key=lambda x: x[0], reverse=True)
    latest = part_files[0]
    print(f"  Found latest part: part{latest[0]}")
    return latest[1]

def get_latest_jobs_url():
    """获取最新的职位数据 XML URL"""
    month_index_url = get_latest_month_index()
    jobs_url = get_latest_part_url(month_index_url)
    return jobs_url

def parse_jobs(xml_content):
    """解析 XML 提取职位信息"""
    xml_content = clean_xml_namespaces(xml_content)
    root = ET.fromstring(xml_content)
    jobs = []

    for url_elem in root.findall('.//url'):
        loc = url_elem.find('loc')
        image = url_elem.find('.//image_image')
        caption = image.find('image_caption') if image is not None else None
        image_loc = image.find('image_loc') if image is not None else None

        if loc is not None and caption is not None:
            job_url = loc.text.strip()
            caption_text = caption.text.strip() if caption.text else ""
            logo_url = image_loc.text.strip() if image_loc is not None and image_loc.text else DEFAULT_LOGO

            # 解析 caption: "Job Title at Company in Location"
            parts = caption_text.split(' at ')
            if len(parts) >= 2:
                title = parts[0].strip()
                rest = ' at '.join(parts[1:])

                # 分离公司和地点
                location_parts = rest.split(' in ')
                if len(location_parts) >= 2:
                    company = location_parts[0].strip()
                    location = ' in '.join(location_parts[1:]).strip()
                else:
                    company = rest.strip()
                    location = "-"
            else:
                title = caption_text
                company = "-"
                location = "-"

            jobs.append({
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'logo': logo_url
            })

    return jobs

def get_rotation_offset(total_jobs):
    """根据当前时间计算轮换偏移量"""
    now = datetime.now(timezone.utc)
    epoch = datetime(2025, 1, 1, tzinfo=timezone.utc)
    hours_since_epoch = (now - epoch).total_seconds() / 3600
    rotation_period = int(hours_since_epoch / ROTATION_HOURS)
    offset = (rotation_period * JOBS_PER_PAGE) % max(total_jobs, 1)
    return offset

def generate_readme(jobs, source_url):
    """生成 README.md 内容"""
    total_jobs = len(jobs)
    offset = get_rotation_offset(total_jobs)

    selected_jobs = []
    for i in range(min(JOBS_PER_PAGE, total_jobs)):
        idx = (offset + i) % total_jobs
        selected_jobs.append(jobs[idx])

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%B %d, %Y")

    readme = f"""# Latest Job Openings

Discover {total_jobs:,}+ career opportunities from top companies. Whether you're looking for remote work, tech roles, healthcare positions, or entry-level jobs — find your next opportunity here.

**{date_str}** · Featuring jobs in Engineering, Healthcare, Sales, Finance, and more.

---

| Job Title | Company | Apply |
|-----------|---------|:-----:|
"""

    for job in selected_jobs:
        title = job['title'].replace('|', '\\|')
        company = job['company'].replace('|', '\\|')
        logo = job.get('logo', DEFAULT_LOGO)
        readme += f"| {title} | <img src=\"{logo}\" width=\"20\" height=\"20\" alt=\"\"> {company} | [View]({job['url']}) |\n"

    readme += f"""
---

Browse all jobs at [OpenJobs AI](https://www.openjobs-ai.com/deepsearch) · Updated daily
"""

    return readme

def generate_html(jobs, source_url):
    """生成 HTML 页面 - 卡片布局，与 README 表格布局差异化"""
    total_jobs = len(jobs)
    # 使用不同的偏移量，展示不同的职位
    offset = get_rotation_offset(total_jobs) + 50

    # 展示 50 个职位（与 README 的 100 个不同）
    html_jobs_count = 50
    selected_jobs = []
    for i in range(min(html_jobs_count, total_jobs)):
        idx = (offset + i) % total_jobs
        selected_jobs.append(jobs[idx])

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%b %d, %Y")

    jobs_cards = ""
    for job in selected_jobs:
        title = job['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        company = job['company'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        logo = job.get('logo', DEFAULT_LOGO)
        jobs_cards += f"""    <a href="{job['url']}" class="card" target="_blank" rel="noopener">
      <div class="card-title">{title}</div>
      <div class="card-company"><img src="{logo}" alt="" class="logo">{company}</div>
    </a>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OpenJobs · Find Your Next Career</title>
  <meta name="description" content="Browse {total_jobs:,}+ open positions. New jobs added daily from leading employers across tech, healthcare, finance, and more.">
  <link rel="canonical" href="https://www.openjobs-ai.com/">
  <style>
    :root {{ --primary: #2563eb; --bg: #f8fafc; --card-bg: #fff; --text: #1e293b; --muted: #64748b; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 2rem 1rem; }}
    header {{ text-align: center; margin-bottom: 2rem; }}
    h1 {{ font-size: 1.75rem; font-weight: 700; margin-bottom: 0.5rem; }}
    .subtitle {{ color: var(--muted); font-size: 1rem; }}
    .stats {{ display: flex; justify-content: center; gap: 2rem; margin: 1.5rem 0; font-size: 0.875rem; color: var(--muted); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }}
    .card {{ display: block; background: var(--card-bg); border-radius: 12px; padding: 1.25rem; text-decoration: none; color: inherit; border: 1px solid #e2e8f0; transition: all 0.2s; }}
    .card:hover {{ border-color: var(--primary); box-shadow: 0 4px 12px rgba(37,99,235,0.1); transform: translateY(-2px); }}
    .card-title {{ font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem; color: var(--text); line-height: 1.4; }}
    .card-company {{ font-size: 0.85rem; color: var(--muted); display: flex; align-items: center; gap: 0.5rem; }}
    .logo {{ width: 20px; height: 20px; border-radius: 4px; object-fit: contain; flex-shrink: 0; }}
    footer {{ text-align: center; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0; color: var(--muted); font-size: 0.875rem; }}
    footer a {{ color: var(--primary); text-decoration: none; }}
    @media (max-width: 640px) {{ .stats {{ flex-direction: column; gap: 0.5rem; }} .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Find Your Next Career</h1>
      <p class="subtitle">Curated job openings from top employers</p>
      <div class="stats">
        <span>{total_jobs:,}+ positions</span>
        <span>Updated {date_str}</span>
        <span>{html_jobs_count} featured below</span>
      </div>
    </header>

    <div class="grid">
{jobs_cards}    </div>

    <footer>
      <p>Explore more opportunities at <a href="https://www.openjobs-ai.com/deepsearch">OpenJobs AI</a></p>
    </footer>
  </div>
</body>
</html>
"""
    return html

def main():
    print("=" * 50)
    print("OpenJobs Updater")
    print("=" * 50)

    # 动态发现最新数据源
    jobs_url = get_latest_jobs_url()

    print("Step 3: Fetching job listings...")
    xml_content = fetch_xml(jobs_url)

    print("Step 4: Parsing jobs...")
    jobs = parse_jobs(xml_content)
    print(f"  Found {len(jobs)} jobs")

    print("Step 5: Generating README.md...")
    readme_content = generate_readme(jobs, jobs_url)
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("Step 6: Generating HTML for Cloudflare Pages...")
    os.makedirs(os.path.dirname(HTML_PATH), exist_ok=True)
    html_content = generate_html(jobs, jobs_url)
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("=" * 50)
    print("Done! Generated README.md and public/index.html")

if __name__ == "__main__":
    main()
