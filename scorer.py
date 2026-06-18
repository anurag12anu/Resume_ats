import re
from collections import Counter
from difflib import SequenceMatcher


class ATSScorer:
    """Score resumes based on job description matching."""
    
    def __init__(self):
        self.technical_keywords = {
            'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'swift',
            'kotlin', 'rust', 'golang', 'scala', 'r', 'matlab', 'sql', 'html',
            'css', 'react', 'angular', 'vue', 'nodejs', 'django', 'flask',
            'spring', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'git', 'linux', 'windows', 'mac', 'agile', 'scrum', 'jira',
            'machine learning', 'deep learning', 'ai', 'tensorflow', 'pytorch',
            'pandas', 'numpy', 'scikit-learn', 'data science', 'analytics',
            'api', 'rest', 'graphql', 'json', 'xml', 'mongodb', 'postgresql',
            'mysql', 'redis', 'elasticsearch', 'ci/cd', 'devops'
        }
        
        self.soft_skills = {
            'communication', 'leadership', 'teamwork', 'problem-solving',
            'critical thinking', 'creativity', 'adaptability', 'time management',
            'collaboration', 'negotiation', 'presentation', 'analytical',
            'project management', 'organization', 'attention to detail'
        }
    
    def score_resume(self, resume_text, job_description):
        """Calculate ATS score for a resume against job description."""
        scores = {}
        
        # Keyword matching score
        scores['keyword_match'] = self._calculate_keyword_match(resume_text, job_description)
        
        # Technical skills score
        scores['technical_skills'] = self._calculate_technical_skills(resume_text, job_description)
        
        # Soft skills score
        scores['soft_skills'] = self._calculate_soft_skills(resume_text, job_description)
        
        # Experience match score
        scores['experience_relevance'] = self._calculate_experience_match(resume_text, job_description)
        
        # Format and structure score
        scores['format_quality'] = self._calculate_format_quality(resume_text)
        
        # Calculate weighted ATS score
        overall_score = (
            scores['keyword_match'] * 0.35 +
            scores['technical_skills'] * 0.25 +
            scores['soft_skills'] * 0.15 +
            scores['experience_relevance'] * 0.15 +
            scores['format_quality'] * 0.10
        )
        
        scores['ats_score'] = round(overall_score, 2)
        
        return scores
    
    def _calculate_keyword_match(self, resume_text, job_description):
        """Calculate keyword match percentage."""
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Extract meaningful keywords from job description
        job_keywords = self._extract_meaningful_words(job_lower)
        
        # Count matches
        matches = sum(1 for keyword in job_keywords if keyword in resume_lower)
        
        if len(job_keywords) == 0:
            return 0
        
        match_percentage = (matches / len(job_keywords)) * 100
        return min(100, match_percentage)
    
    def _calculate_technical_skills(self, resume_text, job_description):
        """Calculate technical skills match."""
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Find required skills in job description
        required_skills = []
        for skill in self.technical_keywords:
            if skill in job_lower:
                required_skills.append(skill)
        
        if not required_skills:
            return 50  # Default score if no technical skills specified
        
        # Count matches in resume
        matches = sum(1 for skill in required_skills if skill in resume_lower)
        
        return (matches / len(required_skills)) * 100
    
    def _calculate_soft_skills(self, resume_text, job_description):
        """Calculate soft skills match."""
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Find required soft skills in job description
        required_skills = []
        for skill in self.soft_skills:
            if skill in job_lower:
                required_skills.append(skill)
        
        if not required_skills:
            return 50  # Default score if no soft skills specified
        
        # Count matches in resume
        matches = sum(1 for skill in required_skills if skill in resume_lower)
        
        return (matches / len(required_skills)) * 100
    
    def _calculate_experience_match(self, resume_text, job_description):
        """Calculate experience relevance based on years mentioned."""
        years_pattern = r'\b(\d{1,2})\s*(?:\+|\-)?.*(?:years?|yrs?)\b'
        
        resume_years = re.findall(years_pattern, resume_text, re.IGNORECASE)
        job_years = re.findall(years_pattern, job_description, re.IGNORECASE)
        
        if not job_years:
            return 50  # Default if no years specified
        
        if not resume_years:
            return 30  # Low score if no experience years mentioned
        
        # Convert to integers
        max_resume_years = max(int(y) for y in resume_years)
        required_years = int(job_years[0])
        
        # Calculate match
        if max_resume_years >= required_years:
            return 100
        else:
            return (max_resume_years / required_years) * 100
    
    def _calculate_format_quality(self, resume_text):
        """Evaluate resume formatting quality."""
        score = 100
        
        # Check for minimum length
        if len(resume_text.strip()) < 100:
            score -= 30
        
        # Check for line breaks and structure
        lines = resume_text.split('\n')
        if len(lines) < 5:
            score -= 20
        
        # Check for bullet points or organization
        if resume_text.count('-') < 5 and resume_text.count('•') < 5:
            score -= 10
        
        # Check for contact information (email or phone)
        if '@' not in resume_text and '(' not in resume_text:
            score -= 10
        
        return max(0, score)
    
    def _extract_meaningful_words(self, text):
        """Extract meaningful words from text."""
        # Remove special characters and split
        words = re.findall(r'\b[a-z]{3,}\b', text)
        
        # Remove common stop words
        stop_words = {
            'the', 'and', 'for', 'with', 'that', 'from', 'are', 'have', 'has',
            'was', 'were', 'been', 'being', 'this', 'can', 'could', 'would',
            'should', 'may', 'might', 'must', 'will', 'your', 'our', 'their',
            'job', 'role', 'position', 'seeking', 'looking', 'candidate'
        }
        
        return list(set(w for w in words if w not in stop_words))
    
    def get_missing_keywords(self, resume_text, job_description):
        """Identify keywords from job description missing in resume."""
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        job_keywords = self._extract_meaningful_words(job_lower)
        
        missing = [kw for kw in job_keywords if kw not in resume_lower]
        
        return missing[:10]  # Return top 10 missing keywords
    
    def generate_report(self, resume_text, job_description, contact_info=None, ats_only=False):
        """Generate a comprehensive ATS analysis report.

        If `ats_only` is True, return a minimal report with only the ATS score
        nested under `scores` for compatibility: `{'scores': {'ats_score': X}}`.
        """
        scores = self.score_resume(resume_text, job_description)

        if ats_only:
            # Minimal report containing only the ATS score
            return {'scores': {'ats_score': scores['ats_score']}}

        missing_keywords = self.get_missing_keywords(resume_text, job_description)
        
        report = {
            'scores': scores,
            'missing_keywords': missing_keywords,
            'contact_info': contact_info or {},
            'recommendations': self._generate_recommendations(scores, missing_keywords)
        }
        
        return report
    
    def _generate_recommendations(self, scores, missing_keywords):
        """Generate improvement recommendations."""
        recommendations = []
        
        if scores['keyword_match'] < 70:
            recommendations.append("Increase keyword matches from job description")
        
        if scores['technical_skills'] < 70:
            recommendations.append("Add more relevant technical skills")
        
        if scores['soft_skills'] < 70:
            recommendations.append("Highlight soft skills mentioned in job description")
        
        if scores['experience_relevance'] < 70:
            recommendations.append("Emphasize relevant experience and years of work")
        
        if scores['format_quality'] < 80:
            recommendations.append("Improve resume formatting and structure")
        
        if missing_keywords:
            recommendations.append(f"Consider adding these keywords: {', '.join(missing_keywords[:5])}")
        
        return recommendations
