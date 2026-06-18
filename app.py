#!/usr/bin/env python3
"""
Resume ATS Analyzer
Analyzes resumes against job descriptions to determine ATS compatibility score.
"""

import sys
from pathlib import Path
from parser import ResumeParser
from scorer import ATSScorer


class ResumeATSAnalyzer:
    """Main application for analyzing resumes."""
    
    def __init__(self):
        self.parser = ResumeParser()
        self.scorer = ATSScorer()
    
    def analyze_resume(self, resume_path, job_description):
        """Analyze a single resume against job description."""
        try:
            # Parse resume
            resume_text = self.parser.parse_file(resume_path)
            
            # Extract contact info
            contact_info = self.parser.extract_contact_info(resume_text)
            
            # Generate ATS report
            report = self.scorer.generate_report(resume_text, job_description, contact_info)
            
            return report
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_batch(self, resumes_dir, job_description):
        """Analyze multiple resumes in a directory."""
        resumes_path = Path(resumes_dir)
        results = []
        
        supported_extensions = {'.pdf', '.docx', '.txt'}
        
        for resume_file in resumes_path.glob('*'):
            if resume_file.suffix.lower() in supported_extensions:
                report = self.analyze_resume(str(resume_file), job_description)
                results.append({
                    'filename': resume_file.name,
                    'report': report
                })
        
        return results
    
    def print_report(self, filename, report):
        """Pretty print analysis report."""
        if 'error' in report:
            print(f"\n❌ Error analyzing {filename}: {report['error']}")
            return
        
        print(f"\n{'='*60}")
        print(f"📄 Resume: {filename}")
        print(f"{'='*60}")
        
        # Print scores
        scores = report['scores']
        print("\n📊 ATS Scores:")
        print(f"  Overall Score: {scores['overall']}/100 {'🟢' if scores['overall'] >= 75 else '🟡' if scores['overall'] >= 50 else '🔴'}")
        print(f"  Keyword Match: {scores['keyword_match']:.1f}%")
        print(f"  Technical Skills: {scores['technical_skills']:.1f}%")
        print(f"  Soft Skills: {scores['soft_skills']:.1f}%")
        print(f"  Experience Relevance: {scores['experience_relevance']:.1f}%")
        print(f"  Format Quality: {scores['format_quality']:.1f}%")
        
        # Print contact info
        if report['contact_info']:
            print("\n📞 Contact Information:")
            if report['contact_info'].get('email'):
                print(f"  Email: {report['contact_info']['email']}")
            if report['contact_info'].get('phone'):
                print(f"  Phone: {report['contact_info']['phone']}")
            if report['contact_info'].get('linkedin'):
                print(f"  LinkedIn: {report['contact_info']['linkedin']}")
        
        # Print missing keywords
        if report['missing_keywords']:
            print("\n❌ Missing Keywords:")
            print(f"  {', '.join(report['missing_keywords'][:10])}")
        
        # Print recommendations
        if report['recommendations']:
            print("\n💡 Recommendations:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        print()
    
    def interactive_mode(self):
        """Interactive mode for analyzing resumes."""
        print("📋 Resume ATS Analyzer")
        print("=" * 60)
        
        # Get job description
        print("\nPaste your job description (press Enter twice when done):")
        lines = []
        while True:
            try:
                line = input()
                if line == "":
                    if lines and lines[-1] == "":
                        lines.pop()  # Remove last empty line
                        break
                lines.append(line)
            except EOFError:
                break
        
        job_description = "\n".join(lines)
        
        if not job_description.strip():
            print("Error: No job description provided")
            return
        
        # Get resume path
        resume_path = input("\nEnter resume file path (or folder for batch): ").strip()
        
        if not resume_path:
            print("Error: No resume path provided")
            return
        
        resume_path = Path(resume_path)
        
        if not resume_path.exists():
            print(f"Error: Path not found: {resume_path}")
            return
        
        # Analyze
        if resume_path.is_file():
            print("\n🔍 Analyzing resume...")
            report = self.analyze_resume(str(resume_path), job_description)
            self.print_report(resume_path.name, report)
        elif resume_path.is_dir():
            print(f"\n🔍 Analyzing resumes in {resume_path}...")
            results = self.analyze_batch(str(resume_path), job_description)
            
            if not results:
                print(f"No resume files found in {resume_path}")
                return
            
            # Sort by score
            results.sort(
                key=lambda x: x['report'].get('scores', {}).get('overall', 0),
                reverse=True
            )
            
            # Print all results
            for result in results:
                self.print_report(result['filename'], result['report'])
            
            # Print summary
            print(f"\n{'='*60}")
            print(f"📊 Summary: Analyzed {len(results)} resumes")
            print(f"{'='*60}")


def main():
    """Main entry point."""
    analyzer = ResumeATSAnalyzer()
    
    if len(sys.argv) > 2:
        # Command line mode
        resume_path = sys.argv[1]
        job_file = sys.argv[2]
        
        try:
            with open(job_file, 'r') as f:
                job_description = f.read()
        except FileNotFoundError:
            print(f"Error: Job description file not found: {job_file}")
            return
        
        if Path(resume_path).is_file():
            report = analyzer.analyze_resume(resume_path, job_description)
            analyzer.print_report(Path(resume_path).name, report)
        elif Path(resume_path).is_dir():
            results = analyzer.analyze_batch(resume_path, job_description)
            for result in results:
                analyzer.print_report(result['filename'], result['report'])
    else:
        # Interactive mode
        analyzer.interactive_mode()


if __name__ == "__main__":
    main()
