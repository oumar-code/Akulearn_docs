# Data Ingestion Pipeline Implementation Guide

## Overview

The Nigerian Government Transparency Knowledge Graph data ingestion pipeline is designed to:

1. **Load government entities** (ministries, agencies, officials)
2. **Track corruption cases** (EFCC, ICPC investigations and convictions)
3. **Monitor African debt** (loans, creditors, sustainability)
4. **Catalog NGOs** (civil society organizations, programs, focus areas)
5. **Map global conflicts** (armed conflicts, parties, casualties)
6. **Track social issues** (Almajiri, gender inequality, child labor, hunger)
7. **Monitor news coverage** (bias detection, sentiment analysis, fact-checking)
8. **Analyze social media trends** (trending topics, sentiment tracking)

## Architecture

### Directory Structure

```
src/backend/knowledge_graph/
├── __init__.py
├── neo4j_client.py              # Neo4j connection and query execution
├── models.py                    # Pydantic data models
├── schema_manager.py            # Schema creation and management
├── cypher_queries.py            # Pre-built Cypher queries
│
├── loaders/                     # Data loading modules
│   ├── __init__.py
│   ├── government_and_corruption.py  # Government & EFCC/ICPC data
│   ├── news_loader.py               # News & social media
│   └── orchestrator.py              # Orchestrates all ingestion
│
├── validators/                  # Data validation
│   ├── __init__.py
│   └── data_validator.py        # Entity and batch validation
│
├── analysis/                    # Intelligence layer
│   ├── __init__.py
│   └── intelligence.py          # Bias, sentiment, trend analysis
│
└── requirements.txt             # Python dependencies
```

### Data Flow

```
Raw Data Sources
    ↓
Loaders (government_and_corruption.py, news_loader.py)
    ↓
Validators (data_validator.py)
    ↓
Analysis Engines (intelligence.py)
    ↓
Neo4j Client (neo4j_client.py)
    ↓
Neo4j Database
```

## Core Components

### 1. Data Loaders

#### GovernmentDataLoader
Provides federal ministries, agencies, and official hierarchies:

```python
from loaders import GovernmentDataLoader

# Get all government entities
entities = GovernmentDataLoader.get_all_government_entities()

# Get specific entity types
ministries = GovernmentDataLoader.get_ministries()
agencies = GovernmentDataLoader.get_agencies()
```

**Entities:**
- Federal Ministries (Health, Finance, Agriculture, Education, etc.)
- Anti-Corruption Agencies (EFCC, ICPC, Police, DSS)
- Regulatory Agencies (NAFDAC, NNPC, CBN, NBS)

#### CorruptionDataLoader
Load corruption investigations and convictions:

```python
from loaders import CorruptionDataLoader

cases = CorruptionDataLoader.get_sample_cases()
# Returns: case_id, status, value_involved, verdict, sentence_years
```

**Tracks:**
- EFCC investigations
- ICPC cases
- Conviction records
- Fund recovery amounts

#### DebtDataLoader
Track African countries' debt obligations:

```python
from loaders import DebtDataLoader

debts = DebtDataLoader.get_african_debts()
# Returns: country, creditor, amount, interest_rate, status
```

**Coverage:**
- Nigeria, Ghana, Kenya, and other African nations
- Creditors: World Bank, IMF, China, bilateral creditors
- Tracks: amount, interest rates, maturity dates, purposes

#### NGODataLoader
Civil society organizations and their work:

```python
from loaders import NGODataLoader

ngos = NGODataLoader.get_key_ngos()
# Returns: BudgIT, SERAP, Transparency International, Save the Children, AAH
```

**Includes:**
- Mission statements
- Focus areas
- Countries active
- Credibility ratings

#### ConflictDataLoader
Global security conflicts and their impact:

```python
from loaders import ConflictDataLoader

conflicts = ConflictDataLoader.get_conflicts()
# Returns: Boko Haram, Darfur, Somalia, etc.
```

**Tracks:**
- Conflict parties
- Death tolls
- Displaced persons
- Economic impacts

#### SocialIssueDataLoader
Critical social challenges:

```python
from loaders import SocialIssueDataLoader

issues = SocialIssueDataLoader.get_social_issues()
# Returns: Almajiri, child marriage, GBV, child labor
```

### 2. News & Media Loaders

#### NewsSourceRegistry
Comprehensive list of Nigerian and African news outlets:

```python
from loaders.news_loader import NewsSourceRegistry

nigerian = NewsSourceRegistry.get_nigerian_sources()  # 14 outlets
african = NewsSourceRegistry.get_african_sources()    # 4 outlets
all_sources = NewsSourceRegistry.get_all_sources()    # 18 outlets
```

**Nigerian Sources:**
- Newspapers: The Punch, Vanguard, Guardian, ThisDay, Daily Trust, BusinessDay
- Online: Premium Times, The Cable, Sahara Reporters, Peoples Gazette, Nairametrics
- TV: Channels, Arise, TVC

**Features:**
- Political leaning classification
- Credibility ratings (0.73-0.92)
- Bias ratings (-1 to +1)
- Founded dates

#### NewsArticleLoader
Sample news articles with analysis:

```python
from loaders.news_loader import NewsArticleLoader

articles = NewsArticleLoader.get_sample_articles()
# Returns: title, source, content, sentiment, bias_score
```

#### SocialMediaTrendLoader
Social media trend tracking:

```python
from loaders.news_loader import SocialMediaTrendLoader

trends = SocialMediaTrendLoader.get_sample_trends()
# Returns: topic, platform, volume, sentiment, hashtags
```

**Topics Tracked:**
- Fuel subsidy removal
- Naira devaluation
- Government corruption
- Insecurity
- Food prices and hunger
- Gender-based violence
- Education crisis

### 3. Data Validation

```python
from validators import DataValidator

# Validate single entity
is_valid, errors = DataValidator.validate_entity(
    {"id": "123", "name": "Ministry of Health"},
    "Ministry"
)

# Validate batch
valid_entities, invalid_entities = DataValidator.validate_batch(
    entities_list,
    "Agency"
)

# Check data quality
quality = DataValidator.check_data_quality(entities)
# Returns: completeness_percentage, avg_fields_per_entity
```

### 4. Intelligence Analysis

#### BiasDetector
Analyze media bias:

```python
from analysis import BiasDetector

bias_analysis = BiasDetector.analyze_bias(
    article_content,
    source_name
)
# Returns: bias_score, sentiment, keyword counts

# Compare coverage
comparison = BiasDetector.compare_coverage(
    article_group,
    topic
)
# Returns: bias range, average bias, sources compared
```

#### SentimentAnalyzer
Calculate sentiment scores:

```python
from analysis import SentimentAnalyzer

sentiment = SentimentAnalyzer.calculate_sentiment(text)
# Returns: -1.0 (very negative) to +1.0 (very positive)
```

#### TrendAnalyzer
Analyze and predict trends:

```python
from analysis import TrendAnalyzer

trend_analysis = TrendAnalyzer.analyze_trend(trend_data)
# Returns: current_volume, peak_volume, avg_volume, trend_direction

predictions = TrendAnalyzer.predict_trend_trajectory(
    recent_volumes,
    days_ahead=7
)
# Returns: predicted volumes for next 7 days
```

#### CorruptionAnalyzer
Analyze corruption patterns:

```python
from analysis import CorruptionAnalyzer

burden = CorruptionAnalyzer.calculate_corruption_burden(
    cases,
    agency_name
)
# Returns: total_cases, total_amount, conviction_rate

high_risk = CorruptionAnalyzer.identify_high_risk_agencies(
    cases,
    threshold=3
)
# Returns: agencies with 3+ corruption cases
```

#### DebtAnalyzer
Analyze debt sustainability:

```python
from analysis import DebtAnalyzer

burden = DebtAnalyzer.calculate_debt_burden(
    country_name,
    debts,
    gdp
)
# Returns: total_debt, debt_to_gdp_ratio, avg_interest_rate

at_risk = DebtAnalyzer.identify_debt_crisis_risk(
    countries,
    threshold_ratio=60.0
)
# Returns: countries with debt-to-GDP > 60%
```

### 5. Data Ingestion Orchestrator

Main orchestrator coordinating all ingestion:

```python
from loaders.orchestrator import DataIngestionOrchestrator
from neo4j_client import Neo4jClient
import asyncio

async def ingest():
    client = Neo4jClient(
        uri="neo4j+s://xxx.databases.neo4j.io",
        username="neo4j",
        password="password"
    )
    
    orchestrator = DataIngestionOrchestrator(client)
    
    # Ingest everything
    result = await orchestrator.ingest_full_knowledge_graph()
    
    # Get report
    report = orchestrator.get_validation_report()
    
    client.close()

asyncio.run(ingest())
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r src/backend/knowledge_graph/requirements.txt
```

### 2. Set Up Neo4j AuraDB

```bash
# Go to https://auradb.neo4j.io and create free instance
# Copy connection details:
# - URI: neo4j+s://xxx.databases.neo4j.io
# - Username: neo4j
# - Password: (generated)
```

### 3. Configure Environment

```bash
# .env file
NEO4J_URI=neo4j+s://xxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEWSAPI_KEY=your_newsapi_key
TWITTER_BEARER_TOKEN=your_bearer_token
```

### 4. Run Initial Ingestion

```python
from src.backend.knowledge_graph.loaders.orchestrator import DataIngestionOrchestrator
from src.backend.knowledge_graph.neo4j_client import Neo4jClient
import asyncio

client = Neo4jClient(
    uri="neo4j+s://xxx.databases.neo4j.io",
    username="neo4j",
    password="password"
)

orchestrator = DataIngestionOrchestrator(client)
result = await orchestrator.ingest_full_knowledge_graph()

print(result)
client.close()
```

## Extending the System

### Add Custom Data Loaders

```python
# Create new_loader.py in loaders/
from typing import List, Dict, Any

class CustomDataLoader:
    SAMPLE_DATA = [
        {"id": "1", "name": "Example", ...},
    ]
    
    @staticmethod
    def get_data() -> List[Dict[str, Any]]:
        return CustomDataLoader.SAMPLE_DATA

# Update loaders/__init__.py to export it
```

### Add Custom Analysis

```python
# Create new_analysis.py in analysis/
from typing import Dict, Any

class CustomAnalyzer:
    @staticmethod
    def analyze(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Your analysis logic
        return results

# Update analysis/__init__.py to export it
```

### Add Real Data Sources

```python
# In loaders/news_loader.py NewsAggregator class
@staticmethod
async def fetch_from_news_api(query, sources, language, days_back):
    # Implement with newsapi.org
    # Returns: articles
    pass

@staticmethod
async def fetch_from_twitter(query, days_back):
    # Implement with tweepy and Twitter API v2
    # Returns: tweets
    pass
```

## Data Quality Considerations

1. **Validation**: All entities validated before insertion
2. **Deduplication**: Duplicate records removed based on key fields
3. **Data Completeness**: Tracked and reported
4. **Credibility Scoring**: News sources rated 0.73-0.99
5. **Bias Detection**: Political leaning classified
6. **Fact-Checking**: Integration points prepared for verification

## Scheduled Updates

Set up APScheduler for automated updates:

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# Daily news update
scheduler.add_job(
    update_news_articles,
    'cron',
    hour=0,
    minute=0,
    id='daily_news'
)

# Weekly government data sync
scheduler.add_job(
    sync_government_data,
    'cron',
    day_of_week='monday',
    hour=1,
    id='weekly_govt'
)

# Monthly corruption case update
scheduler.add_job(
    update_corruption_cases,
    'cron',
    day=1,
    hour=2,
    id='monthly_corruption'
)

scheduler.start()
```

## Performance Optimization

1. **Batch Operations**: Use `batch_create_nodes` and `batch_create_relationships`
2. **Indexing**: Automatically created on key fields
3. **Connection Pooling**: Max 50 connections (configurable)
4. **Query Optimization**: Pre-built Cypher queries in `cypher_queries.py`
5. **Caching**: Redis integration for frequent queries

## Monitoring & Logging

```python
import logging

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Structured logging
logger.info("Ingestion started", extra={
    "entity_type": "Ministry",
    "count": 100
})
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection timeout | Verify URI, username, password |
| Validation errors | Check `validation_report` in orchestrator |
| Memory issues | Reduce batch sizes, increase timeout |
| Duplicate entities | Run deduplication before ingestion |
| News parsing fails | Check BeautifulSoup selectors, website structure |

## Resources

- **Neo4j Documentation**: https://neo4j.com/docs/
- **Cypher Guide**: https://neo4j.com/docs/cypher-manual/
- **AuraDB Setup**: https://auradb.neo4j.io/
- **NewsAPI**: https://newsapi.org/
- **Twitter API v2**: https://developer.twitter.com/

---

**Status**: Complete data ingestion pipeline ready for deployment
**Last Updated**: January 2026
**Version**: 1.0.0
