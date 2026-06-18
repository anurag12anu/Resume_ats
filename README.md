<<<<<<< HEAD

# Resume ATS Analyzer

A Python tool for analyzing resumes against job descriptions and calculating an ATS (Applicant Tracking System) compatibility score.

## Features

- Resume parsing for PDF, DOCX, and TXT files
- ATS compatibility scoring with component breakdown
- Keyword matching and missing keyword detection
- Technical and soft skills matching
- Experience relevance scoring and format quality checks
- Contact information extraction (email, phone, LinkedIn)
- Batch resume analysis
- Interactive CLI mode and FastAPI endpoint

## Installation

1. Clone or download this project.
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

> Recommended: use the included virtual environment at `.venv` if available.

## Usage

### Interactive CLI Mode

Run the main application:

```bash
python app.py
```

Then:

1. Paste the job description (optional).
2. Enter a resume file path or a directory containing resumes.
3. View the generated ATS analysis report.

### Command Line Mode

Run the analyzer with a resume path:

```bash
python app.py <resume_path>
```

Optionally provide a job description file:

```bash
python app.py <resume_path> <job_description_file>
```

To print only the ATS score:

```bash
python app.py <resume_path> --ats-only
python app.py <resume_path> <job_description_file> --ats-only
```

Examples:

```bash
python app.py resumes/john_doe.pdf
python app.py resumes/ job_description.txt
python app.py resumes/john_doe.pdf --ats-only
```

For batch directories, the output prints one score per file:

```bash
python app.py resumes/ --ats-only
```

### FastAPI Mode

Start the API server:

```bash
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

Then open the interactive docs at:

- `http://127.0.0.1:8000/docs`

The API now accepts an optional `job_description` field.
By default the API returns only the ATS score (minimal response). To request the full report,
include the form field `ats_only=false` when posting to `/analyze` or `/analyze/batch`.
If no job description is supplied, the resume is still analyzed with generic scoring.

## What the Report Includes

- **ATS Score**: ATS compatibility rating from 0 to 100
- **Component Scores**:
  - Keyword Match
  - Technical Skills
  - Soft Skills
  - Experience Relevance
  - Format Quality
- **Missing Keywords**: Notable job description keywords absent from the resume (when a job description is provided)
- **Recommendations**: Suggested improvements
- **Contact Information**: Extracted email, phone, and LinkedIn

## Supported Formats

- `.pdf`
- `.docx`
- `.txt`

## Project Structure

```
Resume_ATS_CHECKER/
├── api.py             # FastAPI API endpoints
├── app.py             # Main CLI application
├── parser.py          # Resume parsing and contact extraction
├── scorer.py          # ATS scoring logic and report generation
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
└── resumes/           # Resume files for batch analysis
```

## Notes

- The `resumes/` folder is expected to contain the files you want to analyze.
- If you run `python app.py resumes job_description.txt` and no results appear, verify that `resumes/` contains supported files.

## Troubleshooting

- If PDF parsing fails, ensure `PyPDF2` is installed.
- If DOCX parsing fails, ensure `python-docx` is installed.
- If an unsupported file type is used, add one of the supported formats.
- If a path is not found, verify the file or folder path is correct.

## Tips for Better ATS Scores

- Use job description keywords exactly as written.
- Include relevant technical skills and tools.
- Highlight experience with years and project results.
- Keep resume format structured and readable.
- Add contact information clearly at the top.

## License

Free to use for personal and commercial purposes.

## Contributing

# Contributions are welcome. Feel free to fork, improve the scoring logic, add support for new resume formats, or enhance the API.

# Resume_ats

> > > > > > > 7f63ca9b1cd3f1ed0a27760f3bdf2329db2b04ce
