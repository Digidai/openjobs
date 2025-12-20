#!/usr/bin/env python3
"""
从 XML 源获取职位信息并更新 README.md
每次运行展示 100 条职位，根据时间轮换
"""

import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime, timezone
import re

XML_URL = "https://www.openjobs-ai.com/xml/jobs-detail-2025-12-part29.xml"
README_PATH = "README.md"
JOBS_PER_PAGE = 100
ROTATION_HOURS = 6

def fetch_xml(url):
    """获取 XML 内容"""
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; OpenJobs/1.0)'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8')

def parse_jobs(xml_content):
    """解析 XML 提取职位信息"""
    # 移除命名空间以简化解析
    xml_content = re.sub(r'\sxmlns[^"]*"[^"]*"', '', xml_content)
    xml_content = re.sub(r'<(/?)image:', r'<\1image_', xml_content)

    root = ET.fromstring(xml_content)
    jobs = []

    for url_elem in root.findall('.//url'):
        loc = url_elem.find('loc')
        image = url_elem.find('.//image_image')
        caption = image.find('image_caption') if image is not None else None

        if loc is not None and caption is not None:
            job_url = loc.text.strip()
            caption_text = caption.text.strip() if caption.text else ""

            # 解析 caption: "Job Title at Company in Location"
            # 格式通常是: "Title at Company in City, State"
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
                'url': job_url
            })

    return jobs

def get_rotation_offset(total_jobs):
    """根据当前时间计算轮换偏移量"""
    now = datetime.now(timezone.utc)
    # 计算从某个固定时间点开始的 6 小时周期数
    epoch = datetime(2025, 1, 1, tzinfo=timezone.utc)
    hours_since_epoch = (now - epoch).total_seconds() / 3600
    rotation_period = int(hours_since_epoch / ROTATION_HOURS)

    # 计算偏移量，确保不超过总数
    offset = (rotation_period * JOBS_PER_PAGE) % max(total_jobs, 1)
    return offset

def generate_readme(jobs):
    """生成 README.md 内容"""
    total_jobs = len(jobs)
    offset = get_rotation_offset(total_jobs)

    # 获取当前轮次的 100 条职位
    selected_jobs = []
    for i in range(JOBS_PER_PAGE):
        idx = (offset + i) % total_jobs
        selected_jobs.append(jobs[idx])

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    readme = f"""# OpenJobs - Latest Job Postings

> Auto-updated job listings from [OpenJobs-AI](https://www.openjobs-ai.com)

**Last Updated:** {now}
**Showing:** {len(selected_jobs)} of {total_jobs} jobs (rotates every 6 hours)

---

## Latest Jobs

| # | Job Title | Company | Location | Link |
|---|-----------|---------|----------|------|
"""

    for i, job in enumerate(selected_jobs, 1):
        # 转义 Markdown 特殊字符
        title = job['title'].replace('|', '\\|')
        company = job['company'].replace('|', '\\|')
        location = job['location'].replace('|', '\\|')

        readme += f"| {i} | {title} | {company} | {location} | [链接]({job['url']}) |\n"

    readme += """
---

## About

This repository automatically fetches and displays the latest job postings from OpenJobs-AI.

- Updates every 6 hours via GitHub Actions
- Shows 100 jobs per rotation
- Jobs rotate to show different listings over time

## Source

Data from: [OpenJobs-AI](https://www.openjobs-ai.com)
"""

    return readme

def main():
    print("Fetching XML data...")
    xml_content = fetch_xml(XML_URL)

    print("Parsing jobs...")
    jobs = parse_jobs(xml_content)
    print(f"Found {len(jobs)} jobs")

    print("Generating README...")
    readme_content = generate_readme(jobs)

    print(f"Writing to {README_PATH}...")
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("Done!")

if __name__ == "__main__":
    main()
