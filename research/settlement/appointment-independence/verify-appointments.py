"""Reconcile the original decree lists and the authored appointment comparison."""

from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path


class DecreeParagraphs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.paragraphs = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.current = []

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == "p" and self.current is not None:
            self.paragraphs.append(" ".join("".join(self.current).split()))
            self.current = None


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-appointment-independence-and-concurrent-vacancies"
)
observations = json.loads((edition / "observations.json").read_text())
reported = observations["spanish_interim_scope"]
originals = edition / "original-sources"
assert (originals / "boe-2021-4907.pdf").read_bytes().startswith(b"%PDF-")
assert date.fromisoformat(reported["law_published"]) < date.fromisoformat(
    reported["council_appointment_decrees_dated"]
)
assert reported["supreme_court_vacancies_reported"] == 27
assert reported["all_pending_judicial_appointments_reported"] == 99
assert observations["downstream_person_level_hearing_effect"] is None
for chamber, decree_number in (("congress", 755), ("senate", 756)):
    parser = DecreeParagraphs()
    document = (originals / f"boe-{chamber}-appointment-2024.html").read_text()
    assert f"Real Decreto {decree_number}/2024, de 24 de julio" in document
    parser.feed(document)
    start = next(i for i, p in enumerate(parser.paragraphs) if p.startswith("Vengo en nombrar"))
    end = next(i for i, p in enumerate(parser.paragraphs) if p.startswith("Dado en Palma"))
    names = [p for p in parser.paragraphs[start:end] if p.startswith(("Don ", "Doña "))]
    assert len(set(names)) == reported[f"{chamber}_decree_nominees"] == 10


def possible(available, threshold):
    """Test only the fixed vote and category bounds after lawful alternates."""
    return sum(available) >= threshold and all(count > 0 for count in available)


ordinary = (6, 3, 3)
core = (3, 3, 3)
five_core_missing = (1, 1, 2)
core_lay_missing = (3, 3, 0)
assert sum(five_core_missing) == 4
assert not possible(five_core_missing, 6)
assert not possible((4, 1, 2), 8)
assert sum(core_lay_missing) == 6
assert not possible(core_lay_missing, 6)
assert sum((6, 3, 0)) == 9
assert not possible((6, 3, 0), 8)
assert possible(ordinary, 8)
assert possible(core, 6)
assert (sum(ordinary), sum(ordinary) + sum(core), sum(ordinary) + 2 * sum(core)) == (
    12,
    21,
    30,
)
print("Spanish decrees: 10 council appointments from each parliamentary source.")
print("Authored case: 4 core and 7 shared ordinary votes after five core losses.")
print("Separate ordinary formation preserves the ordinary vote path if separately staffed.")
