from typing import List, Optional
from pydantic import BaseModel, Field


class Parties(BaseModel):
    petitioner: Optional[str] = Field(default="N/A", description="Name of petitioner / appellant / plaintiff")
    respondent: Optional[str] = Field(default="N/A", description="Name of respondent / defendant")


class EvidenceItem(BaseModel):
    page: int = Field(..., description="1-indexed page number in the original PDF")
    text: str = Field(..., description="Exact excerpt or snippet from the court judgment text")
    field: str = Field(..., description="The field supported by this evidence (parties, legalProvisions, issues, outcome, etc.)")


class AnalysisResponse(BaseModel):
    caseType: Optional[str] = Field(default="N/A", description="Type of case e.g. Civil, Criminal, Constitutional")
    parties: Parties = Field(default_factory=Parties, description="Extracted petitioner and respondent names")
    legalProvisions: List[str] = Field(default_factory=list, description="Sections, statutes, acts cited in the document")
    issues: List[str] = Field(default_factory=list, description="Core legal issues or points framed by the court")
    summary: Optional[str] = Field(default="", description="Detailed, evidence-grounded numbered summary of the judgment's main points")
    outcome: Optional[str] = Field(default="N/A", description="Final judicial outcome, ruling, order, or N/A if interim")
    evidence: List[EvidenceItem] = Field(default_factory=list, description="Clickable evidence citations supporting extracted facts")
    error: Optional[str] = Field(default=None, description="Error message if analysis failed, else null")
    pageCount: Optional[int] = Field(default=0, description="Total number of pages processed")
    processingTimeMs: Optional[float] = Field(default=0.0, description="Inference and extraction duration in milliseconds")


class HealthResponse(BaseModel):
    status: str
    model: str
    ready: bool
    engine: str = "Ollama"
    ollama_url: str
    available_models: List[str] = []
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
