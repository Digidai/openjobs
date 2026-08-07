(function () {
  "use strict";

  const form = document.querySelector("[data-scorecard]");
  const total = document.querySelector("[data-score-total]");
  const verdict = document.querySelector("[data-score-verdict]");
  const printButton = document.querySelector("[data-print]");

  if (!form || !total || !verdict) return;

  const verdictFor = (score, completed) => {
    if (completed < 8) return "Score every dimension to see a pilot recommendation.";
    if (score <= 8) return "Stop. The evidence or control model is not ready for a live pilot.";
    if (score <= 16) return "Proceed only with a narrow, reversible pilot and explicit stop conditions.";
    return "Pilot-ready. Validate the claims against a recent role and your own baseline.";
  };

  const update = () => {
    const checked = Array.from(form.querySelectorAll("input[type='radio']:checked"));
    const score = checked.reduce((sum, input) => sum + Number(input.value), 0);
    total.textContent = `${score}/24`;
    verdict.textContent = verdictFor(score, checked.length);
  };

  form.addEventListener("change", update);
  printButton?.addEventListener("click", () => window.print());
  update();
})();
