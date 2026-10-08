from extraction.file_content_extraction import extract_text


def test_extract_text_from_pdf():
    text = extract_text("tests/fixtures/resume.pdf")
    assert "Jane Doe" in text


def test_extract_text_from_docx():
    text = extract_text("tests/fixtures/resume.docx")
    assert "Jane Doe" in text


def test_extract_text_from_txt():
    text = extract_text("tests/fixtures/job_description.txt")
    assert "Senior Backend Engineer" in text
