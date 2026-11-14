"""Verify scoped source markers and the authored income and cash comparison."""

from decimal import Decimal
from html import unescape
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-income-timing-and-usable-resources"
)
observed = json.loads((edition / "observations.json").read_text())
originals = edition / "original-sources"
judgment = unescape((originals / "johnson-2020-ewca-778.html").read_text())
guidance = unescape((originals / "uk-earnings-guidance.html").read_text())
assert "[2020] EWCA Civ 778" in judgment
assert "22 June 2020" in judgment
assert "losing £500 over a year" in judgment
assert "Once a year, you’ll have an assessment period with 2 paydays" in guidance
assert observed["johnson_court_of_appeal"]["respondents"] == 4
assert observed["johnson_court_of_appeal"]["witness_reported_annual_loss_gbp_approx"] == 500
assert observed["government_guidance"]["described_monthly_period_paydays"] == 2
assert observed["measured_whole_population_payment_and_outcome_effect"] is None

need = 100
disregard = 20
taper = Decimal("0.5")


def award(assessment_earnings):
    return max(0, need - taper * max(0, assessment_earnings - disregard))


stable = (award(100), award(100))
raw = (award(200), award(0))
matched = (award(100), award(100))
assert stable == matched == (60, 60)
assert raw == (10, 100)
assert sum(matched) - sum(raw) == 10

cohort = 100
cash_difference = tuple(cohort * (new - old) for new, old in zip(matched, raw))
assert cash_difference == (5000, -4000)
assert sum(cash_difference) == 1000

already_received_award = award(100)
missed_wage_correction = award(0) - already_received_award
assert missed_wage_correction == 40
assert 100 - 60 == missed_wage_correction

print("Observed scope: four respondents and an official shorter-cycle example.")
print("Authored awards: matching restores 60 then 60, versus raw 10 then 100.")
print("For 100 cases: +5,000 early, -4,000 later, +1,000 total.")
print("A genuinely missed wage leaves 40 due after the forecast award.")
