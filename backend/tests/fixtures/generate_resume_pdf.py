"""Regenerate the sample resume.pdf test fixture.

Run with: uv run python tests/fixtures/generate_resume_pdf.py

fpdf2 is a dev-only dependency — it exists purely to produce this fixture,
the app itself never writes PDFs. The content here is intentionally shaped
to exercise the matcher later: it matches on Python/FastAPI/LangChain and
falls short on Kubernetes/AWS and years of experience.
"""

from pathlib import Path

from fpdf import FPDF

RESUME_TEXT = """Jane Doe
Software Engineer
jane.doe@example.com | (555) 123-4567 | Austin, TX

EXPERIENCE

Backend Engineer, Acme Corp (2022 - 2025)
- Built and maintained REST APIs with Python and FastAPI
- Implemented LLM-powered resume screening features using LangChain
- Wrote unit and integration tests with pytest, kept coverage above 90%
- Collaborated with a team of 4 engineers in an agile environment

Software Engineer Intern, Widget Inc (2021 - 2022)
- Automated internal reporting scripts in Python
- Migrated a legacy Flask service to FastAPI

SKILLS

Python, FastAPI, LangChain, PostgreSQL, Docker, Git, REST APIs

EDUCATION

B.S. Computer Science, State University, 2021
"""


def generate(output_path: Path) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 6, RESUME_TEXT)
    pdf.output(str(output_path))


if __name__ == "__main__":
    generate(Path(__file__).parent / "resume.pdf")
    print(f"Wrote {Path(__file__).parent / 'resume.pdf'}")
