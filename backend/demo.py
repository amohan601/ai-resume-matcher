from extraction.file_content_extraction import extract_text
from backend.process.match_score_resume import score_match
def main():
    print("Hello from backend!")
    extracted_data = extract_text("/Users/amohan/personal/anj/personal-projects/agent-projects/resume-matcher/backend/tests/fixtures/resume.pdf")
    print("Extracted data chars:", extracted_data[:20] )

    extracted_job_description = extract_text("/Users/amohan/personal/anj/personal-projects/agent-projects/resume-matcher/backend/tests/fixtures/job_description.txt")
    print("Extracted job description chars:", extracted_job_description[:20] )

    match_result = score_match(extracted_data, extracted_job_description)


if __name__ == "__main__":
    main()
