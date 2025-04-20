from pydantic import BaseModel
from typing import List, Optional, Dict

class IdeaGenerationRequest(BaseModel):
    """Request model for generating startup ideas."""
    constraints: Optional[str] = None
    industry: Optional[str] = None
    technology_focus: Optional[str] = None

class ValidationRequest(BaseModel):
    """Request model for validating a startup idea."""
    idea: str

class IdeasResponse(BaseModel):
    """Response model for generated ideas."""
    ideas: List[Dict[str, str]]

class ValidationResponse(BaseModel):
    """Response model for validation results."""
    market_analysis: str
    technical_evaluation: str
    business_plan: str
