"""
Pydantic Models for Nigerian Government Knowledge Graph
=======================================================

Type-safe models for all nodes and relationships in the graph.
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any, Literal
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl, validator


# ============================================================================
# ENUMS
# ============================================================================

class GovernmentLevel(str, Enum):
    """Level of government."""
    FEDERAL = "federal"
    STATE = "state"
    LOCAL = "local"


class ProjectStatus(str, Enum):
    """Project execution status."""
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    STALLED = "stalled"
    ABANDONED = "abandoned"


class VerificationStatus(str, Enum):
    """Data verification status."""
    VERIFIED = "verified"
    REPORTED = "reported"
    DISPUTED = "disputed"
    PENDING = "pending"


class NewsSourceType(str, Enum):
    """Type of news source."""
    NEWSPAPER = "newspaper"
    TV = "tv"
    ONLINE = "online"
    RADIO = "radio"


class SocialPlatform(str, Enum):
    """Social media platform."""
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"


# ============================================================================
# BASE NODE MODEL
# ============================================================================

class NodeBase(BaseModel):
    """Base model for all graph nodes."""
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }


# ============================================================================
# GOVERNMENT STRUCTURE NODES
# ============================================================================

class MinistryNode(NodeBase):
    """Federal or State Ministry."""
    name: str = Field(..., description="Official name of ministry")
    sector: str = Field(..., description="Sector (e.g., Health, Education, Finance)")
    budget_annual: Optional[float] = Field(None, description="Annual budget in NGN")
    minister: Optional[str] = Field(None, description="Current minister name")
    established: Optional[date] = Field(None, description="Date established")
    website: Optional[HttpUrl] = Field(None, description="Official website")
    level: GovernmentLevel = Field(GovernmentLevel.FEDERAL, description="Government level")
    state: Optional[str] = Field(None, description="State name (if state-level)")
    description: Optional[str] = Field(None, description="Ministry mandate/description")


class AgencyNode(NodeBase):
    """Government Agency or Parastatal."""
    name: str = Field(..., description="Official name")
    acronym: Optional[str] = Field(None, description="Common acronym (e.g., NAFDAC)")
    type: str = Field(..., description="Agency type (e.g., regulatory, service delivery)")
    mandate: Optional[str] = Field(None, description="Official mandate")
    budget_annual: Optional[float] = Field(None, description="Annual budget in NGN")
    director_general: Optional[str] = Field(None, description="Current DG/CEO name")
    established: Optional[date] = Field(None, description="Date established")
    website: Optional[HttpUrl] = Field(None, description="Official website")
    employees_count: Optional[int] = Field(None, description="Number of employees")
    level: GovernmentLevel = Field(GovernmentLevel.FEDERAL, description="Government level")
    state: Optional[str] = Field(None, description="State name (if state-level)")


class StateNode(NodeBase):
    """Nigerian State."""
    name: str = Field(..., description="State name")
    capital: str = Field(..., description="State capital")
    governor: Optional[str] = Field(None, description="Current governor")
    population: Optional[int] = Field(None, description="Population estimate")
    budget_annual: Optional[float] = Field(None, description="Annual budget in NGN")
    geopolitical_zone: str = Field(
        ...,
        description="Geopolitical zone (NC, NE, NW, SE, SS, SW)"
    )
    area_sqkm: Optional[float] = Field(None, description="Area in square kilometers")


# ============================================================================
# FINANCIAL NODES
# ============================================================================

class BudgetNode(NodeBase):
    """Budget Allocation."""
    year: int = Field(..., description="Budget year")
    amount: float = Field(..., description="Amount in NGN")
    currency: str = Field("NGN", description="Currency code")
    allocation_date: Optional[date] = Field(None, description="Date allocated")
    utilization_rate: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Percentage utilized (0-100)"
    )
    category: Optional[str] = Field(None, description="Budget category (capital, recurrent)")
    source: Optional[str] = Field(None, description="Source of funds")


# ============================================================================
# PROJECT & IMPACT NODES
# ============================================================================

class ProjectNode(NodeBase):
    """Government Project."""
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    status: ProjectStatus = Field(ProjectStatus.PLANNED, description="Current status")
    cost_budgeted: Optional[float] = Field(None, description="Budgeted cost in NGN")
    cost_actual: Optional[float] = Field(None, description="Actual cost in NGN")
    start_date: Optional[date] = Field(None, description="Start date")
    completion_date: Optional[date] = Field(None, description="Expected/actual completion")
    location: Optional[str] = Field(None, description="Project location")
    state: Optional[str] = Field(None, description="State where project is located")
    progress_percentage: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Progress percentage (0-100)"
    )
    contractor: Optional[str] = Field(None, description="Main contractor")


class OutcomeNode(NodeBase):
    """Measurable Outcome."""
    name: str = Field(..., description="Outcome name")
    description: Optional[str] = Field(None, description="Outcome description")
    metric_type: str = Field(..., description="Type of metric (e.g., people served, km built)")
    value: float = Field(..., description="Measured value")
    unit: str = Field(..., description="Unit of measurement")
    measurement_date: date = Field(..., description="Date measured")
    beneficiaries_count: Optional[int] = Field(None, description="Number of beneficiaries")
    verification_status: VerificationStatus = Field(
        VerificationStatus.REPORTED,
        description="Verification status"
    )


class ServiceNode(NodeBase):
    """Public Service."""
    name: str = Field(..., description="Service name")
    type: str = Field(..., description="Service type")
    beneficiaries_annual: Optional[int] = Field(None, description="Annual beneficiaries")
    quality_score: Optional[float] = Field(
        None,
        ge=0,
        le=10,
        description="Quality score (0-10)"
    )
    accessibility_rating: Optional[float] = Field(
        None,
        ge=0,
        le=10,
        description="Accessibility rating (0-10)"
    )
    cost_per_beneficiary: Optional[float] = Field(None, description="Cost per person served")


# ============================================================================
# NEWS & MEDIA NODES
# ============================================================================

class NewsArticleNode(NodeBase):
    """News Article."""
    title: str = Field(..., description="Article title")
    source: str = Field(..., description="News source name")
    url: HttpUrl = Field(..., description="Article URL")
    published_date: datetime = Field(..., description="Publication date/time")
    content: Optional[str] = Field(None, description="Article content/excerpt")
    author: Optional[str] = Field(None, description="Article author")
    sentiment: Optional[float] = Field(
        None,
        ge=-1,
        le=1,
        description="Sentiment score (-1 to 1)"
    )
    bias_score: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        description="Bias score (0=neutral, 1=highly biased)"
    )
    credibility_score: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        description="Credibility score (0-1)"
    )
    topics: Optional[List[str]] = Field(default_factory=list, description="Extracted topics")
    entities_mentioned: Optional[List[str]] = Field(
        default_factory=list,
        description="Government entities mentioned"
    )
    fact_check_status: Optional[str] = Field(None, description="Fact-check result")


class NewsSourceNode(NodeBase):
    """News Media Source."""
    name: str = Field(..., description="Source name")
    type: NewsSourceType = Field(..., description="Type of news source")
    url: Optional[HttpUrl] = Field(None, description="Website URL")
    political_leaning: Optional[str] = Field(
        None,
        description="Political leaning (left, center, right)"
    )
    credibility_rating: Optional[float] = Field(
        None,
        ge=0,
        le=10,
        description="Overall credibility (0-10)"
    )
    bias_rating: Optional[float] = Field(
        None,
        ge=0,
        le=10,
        description="Overall bias rating (0=unbiased, 10=highly biased)"
    )
    founded: Optional[date] = Field(None, description="Year founded")
    ownership: Optional[str] = Field(None, description="Ownership information")


class SocialTrendNode(NodeBase):
    """Social Media Trend."""
    topic: str = Field(..., description="Trend topic/hashtag")
    platform: SocialPlatform = Field(..., description="Social media platform")
    volume: int = Field(..., description="Number of mentions/posts")
    sentiment: Optional[float] = Field(
        None,
        ge=-1,
        le=1,
        description="Average sentiment (-1 to 1)"
    )
    started_date: datetime = Field(..., description="When trend started")
    peak_date: Optional[datetime] = Field(None, description="Peak activity date")
    related_hashtags: Optional[List[str]] = Field(
        default_factory=list,
        description="Related hashtags"
    )
    geographic_focus: Optional[List[str]] = Field(
        default_factory=list,
        description="States/regions involved"
    )
    engagement_rate: Optional[float] = Field(None, description="Engagement rate")


class PublicSentimentNode(NodeBase):
    """Aggregated Public Sentiment."""
    topic: str = Field(..., description="Topic of sentiment")
    date: date = Field(..., description="Measurement date")
    score: float = Field(..., ge=-1, le=1, description="Sentiment score (-1 to 1)")
    sample_size: int = Field(..., description="Number of data points")
    sources: List[str] = Field(..., description="Data sources")
    demographics: Optional[Dict[str, Any]] = Field(
        None,
        description="Demographic breakdown"
    )
    confidence_interval: Optional[float] = Field(None, description="Statistical confidence")


# ============================================================================
# ECONOMIC INDICATOR NODES
# ============================================================================

class EconomicIndicatorNode(NodeBase):
    """Economic Indicator."""
    name: str = Field(..., description="Indicator name (e.g., Inflation Rate)")
    value: float = Field(..., description="Indicator value")
    date: date = Field(..., description="Measurement date")
    source: str = Field(..., description="Data source (e.g., CBN, NBS)")
    category: str = Field(
        ...,
        description="Category (monetary, fiscal, trade, employment)"
    )
    unit: Optional[str] = Field(None, description="Unit (%, NGN, etc.)")
    previous_value: Optional[float] = Field(None, description="Previous period value")


# ============================================================================
# RELATIONSHIP MODELS
# ============================================================================

class RelationshipBase(BaseModel):
    """Base model for relationships."""
    
    class Config:
        arbitrary_types_allowed = True


class OversightRelationship(RelationshipBase):
    """Ministry oversees Agency."""
    established_date: Optional[date] = None
    oversight_level: Optional[str] = None  # "direct", "supervisory", "regulatory"


class BudgetAllocationRelationship(RelationshipBase):
    """Budget allocation relationship."""
    allocated_date: date
    purpose: Optional[str] = None
    conditions: Optional[List[str]] = None


class ProjectImplementationRelationship(RelationshipBase):
    """Agency implements project."""
    role: str  # "lead", "partner", "contractor"
    responsibility: Optional[str] = None


class ImpactRelationship(RelationshipBase):
    """Project/service impacts outcome."""
    impact_level: Optional[str] = None  # "direct", "indirect", "contributing"
    evidence: Optional[str] = None


class NewsMentionRelationship(RelationshipBase):
    """News article mentions entity."""
    context: Optional[str] = None  # "positive", "negative", "neutral", "mixed"
    prominence: Optional[int] = None  # 1-10, how prominently mentioned


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class GraphQuery(BaseModel):
    """Generic graph query request."""
    cypher: str = Field(..., description="Cypher query string")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    limit: int = Field(100, ge=1, le=10000)


class GraphResponse(BaseModel):
    """Generic graph query response."""
    data: List[Dict[str, Any]]
    count: int
    query_time_ms: Optional[float] = None


class InsightQuery(BaseModel):
    """Natural language query for GraphRAG."""
    question: str = Field(..., description="User's question")
    context: Optional[List[str]] = Field(
        default_factory=list,
        description="Additional context"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Filters (state, ministry, date range, etc.)"
    )


class InsightResponse(BaseModel):
    """Response from GraphRAG system."""
    answer: str = Field(..., description="Generated answer")
    sources: List[str] = Field(default_factory=list, description="Data sources used")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    supporting_data: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Supporting graph data"
    )
    visualization_hint: Optional[str] = Field(
        None,
        description="Suggested visualization type"
    )


# ============================================================================
# BATCH IMPORT MODELS
# ============================================================================

class BatchImportRequest(BaseModel):
    """Batch data import request."""
    node_type: str = Field(..., description="Type of nodes to import")
    data: List[Dict[str, Any]] = Field(..., description="List of node data")
    merge_on: Optional[str] = Field(None, description="Property to merge on")


class BatchImportResponse(BaseModel):
    """Batch import result."""
    imported_count: int
    failed_count: int
    errors: Optional[List[str]] = None
    duration_seconds: float
