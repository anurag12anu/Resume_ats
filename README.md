# Resume ATS Analyzer

A Python-based tool to analyze resumes against job descriptions and calculate an ATS (Applicant Tracking System) compatibility score.

## Features

- **Resume Parsing**: Support for PDF, DOCX, and TXT formats
- **ATS Scoring**: Calculate overall compatibility score (0-100)
- **Detailed Analysis**:
  - Keyword matching
  - Technical skills assessment
  - Soft skills detection
  - Experience relevance evaluation
  - Format quality check
- **Contact Information Extraction**: Automatically extract email, phone, and LinkedIn
- **Recommendations**: Get actionable suggestions to improve resume
- **Batch Processing**: Analyze multiple resumes at once
- **Interactive Mode**: Easy-to-use command-line interface

## Installation

1. Clone or download this project
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Recommended)

Simply run the application:

```bash
python app.py
```

Then:

1. Paste the job description
2. Provide the path to a resume file or folder containing resumes
3. View the ATS analysis report

### Command Line Mode

```bash
python app.py <resume_path> <job_description_file>
```

Example:

```bash
python app.py resumes/john_doe.pdf job_description.txt
```

Or for batch analysis:

```bash
python app.py resumes/ job_description.txt
```

## Output Report

The analyzer provides:

- **Overall Score**: 0-100 rating
- **Component Scores**:
  - Keyword Match: % of job description keywords found in resume
  - Technical Skills: Match against technical requirements
  - Soft Skills: Match against soft skill requirements
  - Experience Relevance: Experience level alignment
  - Format Quality: Resume structure assessment

- **Missing Keywords**: Keywords from job description not in resume
- **Recommendations**: Specific improvements to boost ATS score
- **Contact Information**: Extracted email, phone, LinkedIn

## Score Interpretation

- **75-100**: Excellent match ✅
- **50-74**: Good potential ⚠️
- **Below 50**: Needs improvement ❌

## How It Works

1. **Parsing**: Extracts text from resume file
2. **Scoring**: Compares resume content against job description
3. **Analysis**: Identifies strengths and gaps
4. **Recommendations**: Suggests improvements

## File Structure

```
Resume_ATS_CHECKER/
├── app.py           # Main application
├── parser.py        # Resume file parsing
├── scorer.py        # ATS scoring engine
├── requirements.txt # Python dependencies
├── README.md        # This file
└── resumes/         # Folder for resume files
```

## Supported Formats

- PDF (.pdf)
- DOCX (.docx)
- TXT (.txt)

## Tips for Higher ATS Scores

1. **Use Keywords**: Include keywords from the job description
2. **Structured Format**: Use clear sections (Experience, Skills, Education)
3. **Technical Skills**: Explicitly list relevant technologies and tools
4. **Quantify Experience**: Mention years of experience
5. **Contact Info**: Include email and phone number
6. **Relevant Content**: Tailor content to the job description

## Troubleshooting

**Q: PDF parsing not working?**

- Ensure PyPDF2 is installed: `pip install PyPDF2`
- Some PDFs may be scanned images; consider converting to text first

**Q: DOCX file not recognized?**

- Install python-docx: `pip install python-docx`

**Q: Module not found error?**

- Reinstall dependencies: `pip install -r requirements.txt`

## License

Free to use for personal and commercial purposes.

## Contributing

Feel free to fork and improve this project!
