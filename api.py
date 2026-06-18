import shutil
import tempfile
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from parser import ResumeParser
from scorer import ATSScorer


class Scores(BaseModel):
    overall: float
    keyword_match: float
    technical_skills: float
    soft_skills: float
    experience_relevance: float
    format_quality: float


class ATSReport(BaseModel):
    scores: Scores
    missing_keywords: List[str]
    contact_info: dict
    recommendations: List[str]


class FileAnalysisResult(BaseModel):
    filename: str
    report: ATSReport


app = FastAPI(
    title="Resume ATS Analyzer API",
    description="Upload a resume and job description to analyze ATS compatibility. Swagger UI is available at /docs.",
    version="1.0.0"
)

parser = ResumeParser()
scorer = ATSScorer()
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}


def _save_upload_file(upload_file: UploadFile) -> str:
    suffix = Path(upload_file.filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(upload_file.file, tmp)
        return tmp.name


def _analyze_file_path(file_path: str, job_description: str) -> dict:
    try:
        resume_text = parser.parse_file(file_path)
        contact_info = parser.extract_contact_info(resume_text)
        report = scorer.generate_report(resume_text, job_description, contact_info)
        return report
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/analyze", response_model=ATSReport)
async def analyze_resume(file: UploadFile = File(...), job_description: str = Form(...)):
    """Analyze a single resume file against a job description."""
    temp_path = _save_upload_file(file)
    try:
        report = _analyze_file_path(temp_path, job_description)
        return report
    finally:
        try:
            Path(temp_path).unlink()
        except OSError:
            pass


@app.post("/analyze/batch", response_model=List[FileAnalysisResult])
async def analyze_batch(files: List[UploadFile] = File(...), job_description: str = Form(...)):
    """Analyze multiple resume files in a single request."""
    results = []

    for file in files:
        temp_path = _save_upload_file(file)
        try:
            report = _analyze_file_path(temp_path, job_description)
            results.append({
                'filename': file.filename,
                'report': report
            })
        finally:
            try:
                Path(temp_path).unlink()
            except OSError:
                pass

    return results
