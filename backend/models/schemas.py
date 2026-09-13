from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class ComponentScore(BaseModel):
    formatting: float
    keywords: float
    component: float
    skill_validation: float
    ats_compatibility: float

class JDComparison(BaseModel):
    match_percentage: float
    semantic_similarity: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    skills_gap: List[str]

class SkillValidationDetails(BaseModel):
    validated: List[Dist[str, Any]] = []    #[{'still': str, 'projects': [str]}]
    unvalidated: List[str] = []             #['Flask', 'A/B Testing', ...]
    total: int = 0
    validated_count: int = 0
    validated_pct: float = 0.0

class IssueDetail(BaseModel):
    issue_title: str
    severity_level: str
    ats_impact: str
    explanation: str
    where_it_appears: str
    how_to_fix: str
    action_items: List[str] = []           #['Update resume with new skills', 'Add project details', ...]
    example_improvement: str

class AnalysisResponse(BaseModel):
    ATS_score: float
    component_scores: ComponentScore
    issues_summary: List[str]
    detailed_feedback: List[IssueDetail]
    jd_match_analysis: Optional[JDComparison] = None
    skill_validation_details: Optional[SkillValidationDetails] = None

    ats_score: float
    keyword_match: float = 0.0
    

