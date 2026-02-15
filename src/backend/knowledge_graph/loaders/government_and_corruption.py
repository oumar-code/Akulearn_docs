"""Government agencies, corruption, debt, NGO, and conflict data loaders."""

import logging
import uuid
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class GovernmentDataLoader:
    """Load Nigerian government entities into knowledge graph."""
    
    # Official Federal Ministries
    FEDERAL_MINISTRIES = [
        {
            "id": str(uuid.uuid4()),
            "name": "Federal Ministry of Health",
            "sector": "Health",
            "budget_annual": 500_000_000_000,
            "minister": "Muhammad Ali Pate",
            "established": "2019-06-21",
            "website": "https://www.health.gov.ng",
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Federal Ministry of Finance",
            "sector": "Finance",
            "budget_annual": 2_000_000_000_000,
            "minister": "Wale Edun",
            "established": "1999-05-29",
            "website": "https://www.fmf.gov.ng",
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Federal Ministry of Agriculture and Food Security",
            "sector": "Agriculture",
            "budget_annual": 300_000_000_000,
            "minister": "Abubakar Kyari",
            "established": "1999-05-29",
            "website": "https://www.fmard.gov.ng",
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Federal Ministry of Education",
            "sector": "Education",
            "budget_annual": 800_000_000_000,
            "minister": "Tahir Mamman",
            "established": "1999-05-29",
            "website": "https://education.gov.ng",
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Federal Ministry of Interior",
            "sector": "Interior Security",
            "budget_annual": 400_000_000_000,
            "minister": "Olubunmi Tunji-Ojo",
            "established": "1999-05-29",
            "website": "https://www.moi.gov.ng",
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Federal Ministry of Power",
            "sector": "Energy",
            "budget_annual": 600_000_000_000,
            "minister": "Adebayo Adelabu",
            "established": "2007",
            "website": "https://www.power.gov.ng",
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Federal Ministry of Transportation",
            "sector": "Transportation",
            "budget_annual": 500_000_000_000,
            "minister": "Sa'id Dada",
            "established": "1999-05-29",
            "website": "https://www.transport.gov.ng",
            "level": "federal"
        },
    ]
    
    # Key Anti-Corruption Agencies
    ANTI_CORRUPTION_AGENCIES = [
        {
            "id": str(uuid.uuid4()),
            "name": "Economic and Financial Crimes Commission",
            "acronym": "EFCC",
            "type": "Anti-Corruption",
            "mandate": "Combat financial crimes and corruption",
            "budget_annual": 50_000_000_000,
            "director_general": "Iman Azazi",
            "established": "2002",
            "website": "https://www.efcc.gov.ng",
            "employees_count": 1200,
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Independent Corrupt Practices Commission",
            "acronym": "ICPC",
            "type": "Anti-Corruption",
            "mandate": "Enforce anti-corruption laws",
            "budget_annual": 40_000_000_000,
            "director_general": "Musa Adamu Kyari",
            "established": "2000",
            "website": "https://icpc.gov.ng",
            "employees_count": 800,
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Nigerian Police Force",
            "acronym": "NPF",
            "type": "Law Enforcement",
            "mandate": "Maintain law and order",
            "budget_annual": 800_000_000_000,
            "established": "1861",
            "website": "https://www.npf.gov.ng",
            "employees_count": 371800,
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Department of State Services",
            "acronym": "DSS",
            "type": "Security",
            "mandate": "State security and intelligence",
            "budget_annual": 200_000_000_000,
            "established": "1961",
            "employees_count": 5000,
            "level": "federal"
        },
    ]
    
    # Key Regulatory & Implementation Agencies
    REGULATORY_AGENCIES = [
        {
            "id": str(uuid.uuid4()),
            "name": "National Agency for Food and Drug Administration and Control",
            "acronym": "NAFDAC",
            "type": "Regulatory",
            "mandate": "Regulate food, drugs, cosmetics",
            "budget_annual": 30_000_000_000,
            "director_general": "Mojisola Adeyeye",
            "established": "1993",
            "website": "https://www.nafdac.gov.ng",
            "employees_count": 5000,
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Nigerian National Petroleum Corporation",
            "acronym": "NNPC",
            "type": "State Enterprise",
            "mandate": "Manage petroleum resources",
            "budget_annual": 5_000_000_000_000,
            "established": "1977",
            "website": "https://www.nnpc.ng",
            "employees_count": 10000,
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Central Bank of Nigeria",
            "acronym": "CBN",
            "type": "Monetary Authority",
            "mandate": "Manage monetary policy",
            "budget_annual": 500_000_000_000,
            "established": "1959",
            "website": "https://www.cbn.gov.ng",
            "employees_count": 4000,
            "level": "federal"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "National Bureau of Statistics",
            "acronym": "NBS",
            "type": "Research & Statistics",
            "mandate": "Collect and publish national statistics",
            "budget_annual": 20_000_000_000,
            "established": "1966",
            "website": "https://nigerianstat.gov.ng",
            "employees_count": 2000,
            "level": "federal"
        },
    ]
    
    @staticmethod
    def get_all_government_entities() -> List[Dict[str, Any]]:
        """Get all predefined government entities."""
        return (
            GovernmentDataLoader.FEDERAL_MINISTRIES +
            GovernmentDataLoader.ANTI_CORRUPTION_AGENCIES +
            GovernmentDataLoader.REGULATORY_AGENCIES
        )
    
    @staticmethod
    def get_ministries() -> List[Dict[str, Any]]:
        """Get federal ministries."""
        return GovernmentDataLoader.FEDERAL_MINISTRIES
    
    @staticmethod
    def get_agencies() -> List[Dict[str, Any]]:
        """Get government agencies."""
        return (
            GovernmentDataLoader.ANTI_CORRUPTION_AGENCIES +
            GovernmentDataLoader.REGULATORY_AGENCIES
        )


class CorruptionDataLoader:
    """Load corruption case data."""
    
    SAMPLE_CASES = [
        {
            "id": str(uuid.uuid4()),
            "case_id": "EFCC/2023/001",
            "title": "Fuel Subsidy Fraud Case - Dangote Group",
            "description": "Investigation into alleged fuel subsidy fraud involving major oil companies",
            "status": "ongoing",
            "value_involved": 250_000_000_000,
            "reporting_agency": "EFCC",
            "date_reported": "2023-06-15",
            "source": "EFCC Official Records",
            "credibility_score": 0.95
        },
        {
            "id": str(uuid.uuid4()),
            "case_id": "ICPC/2023/045",
            "title": "N2.8 billion Highway Contract Scam",
            "description": "Federal road project awarded but funds misappropriated",
            "status": "concluded",
            "value_involved": 2_800_000_000,
            "reporting_agency": "ICPC",
            "date_reported": "2022-10-20",
            "date_concluded": "2023-12-10",
            "verdict": "Guilty",
            "sentence_years": 5,
            "source": "ICPC Official Records",
            "credibility_score": 0.98
        },
        {
            "id": str(uuid.uuid4()),
            "case_id": "EFCC/2024/012",
            "title": "COVID-19 Relief Fund Embezzlement",
            "description": "Diversion of pandemic relief funds meant for vulnerable populations",
            "status": "ongoing",
            "value_involved": 1_200_000_000,
            "reporting_agency": "EFCC",
            "date_reported": "2021-03-05",
            "source": "EFCC Official Records",
            "credibility_score": 0.92
        },
    ]
    
    @staticmethod
    def get_sample_cases() -> List[Dict[str, Any]]:
        """Get sample corruption cases."""
        return CorruptionDataLoader.SAMPLE_CASES


class DebtDataLoader:
    """Load African debt data."""
    
    AFRICAN_DEBTS = [
        {
            "id": str(uuid.uuid4()),
            "country": "Nigeria",
            "creditor": "World Bank",
            "amount": 15_000_000_000,
            "currency": "USD",
            "interest_rate": 1.5,
            "taken_date": "2015-01-15",
            "purpose": "Infrastructure development",
            "status": "active"
        },
        {
            "id": str(uuid.uuid4()),
            "country": "Nigeria",
            "creditor": "International Monetary Fund",
            "amount": 3_600_000_000,
            "currency": "USD",
            "interest_rate": 2.0,
            "taken_date": "2023-03-10",
            "purpose": "Economic stabilization",
            "status": "active"
        },
        {
            "id": str(uuid.uuid4()),
            "country": "Nigeria",
            "creditor": "China",
            "amount": 5_500_000_000,
            "currency": "USD",
            "interest_rate": 5.0,
            "taken_date": "2014-01-01",
            "purpose": "Railway and infrastructure projects",
            "status": "active"
        },
        {
            "id": str(uuid.uuid4()),
            "country": "Ghana",
            "creditor": "International Monetary Fund",
            "amount": 3_000_000_000,
            "currency": "USD",
            "interest_rate": 1.5,
            "taken_date": "2023-06-01",
            "purpose": "Debt restructuring",
            "status": "active"
        },
        {
            "id": str(uuid.uuid4()),
            "country": "Kenya",
            "creditor": "China",
            "amount": 9_000_000_000,
            "currency": "USD",
            "interest_rate": 4.5,
            "taken_date": "2017-01-01",
            "purpose": "Standard Gauge Railway",
            "status": "active"
        },
    ]
    
    @staticmethod
    def get_african_debts() -> List[Dict[str, Any]]:
        """Get African debt records."""
        return DebtDataLoader.AFRICAN_DEBTS


class NGODataLoader:
    """Load NGO data."""
    
    KEY_NGOS = [
        {
            "id": str(uuid.uuid4()),
            "name": "BudgIT",
            "acronym": "BudgIT",
            "mission": "Promote fiscal transparency and accountability in governance",
            "focus_areas": ["transparency", "fiscal_accountability", "governance"],
            "founded_date": "2011-08-01",
            "headquarters": "Abuja, Nigeria",
            "countries_active": ["Nigeria"],
            "annual_budget": 500_000_000,
            "credibility_rating": 0.95,
            "transparency_score": 0.98,
            "website": "https://www.budgit.org"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "SERAP",
            "acronym": "SERAP",
            "mission": "Promote socio-economic rights and accountability",
            "focus_areas": ["human_rights", "accountability", "justice"],
            "founded_date": "2004-01-01",
            "headquarters": "Lagos, Nigeria",
            "countries_active": ["Nigeria", "Ghana", "Kenya"],
            "annual_budget": 2_000_000_000,
            "credibility_rating": 0.96,
            "transparency_score": 0.97,
            "website": "https://www.serap.org.ng"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Transparency International",
            "acronym": "TI",
            "mission": "Combat corruption and promote transparency",
            "focus_areas": ["anti_corruption", "transparency", "governance"],
            "founded_date": "1993-01-01",
            "headquarters": "Berlin, Germany",
            "countries_active": ["Nigeria", "Kenya", "Ghana", "South Africa", "Egypt"],
            "annual_budget": 50_000_000_000,
            "credibility_rating": 0.99,
            "transparency_score": 0.99,
            "website": "https://www.transparency.org"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Save the Children",
            "acronym": "StC",
            "mission": "Provide humanitarian aid and development to children",
            "focus_areas": ["child_welfare", "education", "health"],
            "founded_date": "1919-01-01",
            "headquarters": "London, UK",
            "countries_active": ["Nigeria", "Kenya", "Somalia", "South Sudan", "Ethiopia"],
            "annual_budget": 2_000_000_000,
            "credibility_rating": 0.94,
            "transparency_score": 0.96,
            "website": "https://www.savethechildren.org"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Action Against Hunger",
            "acronym": "AAH",
            "mission": "Fight hunger and malnutrition",
            "focus_areas": ["hunger", "malnutrition", "food_security"],
            "founded_date": "1979-01-01",
            "headquarters": "Paris, France",
            "countries_active": ["Nigeria", "Niger", "Mali", "Burkina Faso", "Somalia"],
            "annual_budget": 800_000_000,
            "credibility_rating": 0.93,
            "transparency_score": 0.95,
            "website": "https://www.actionagainsthunger.org"
        },
    ]
    
    @staticmethod
    def get_key_ngos() -> List[Dict[str, Any]]:
        """Get key NGOs."""
        return NGODataLoader.KEY_NGOS


class ConflictDataLoader:
    """Load global conflict data."""
    
    CONFLICTS = [
        {
            "id": str(uuid.uuid4()),
            "name": "Boko Haram Insurgency (Nigeria)",
            "type": "insurgency",
            "description": "Islamic extremist insurgency in northeastern Nigeria",
            "start_date": "2002-01-01",
            "status": "active",
            "primary_location": "Northeastern Nigeria",
            "affected_countries": ["Nigeria", "Niger", "Cameroon", "Chad"],
            "parties_involved": ["Boko Haram", "ISWAP", "Nigerian Military"],
            "death_toll": 350000,
            "displaced_persons": 2_900_000,
            "economic_impact": 29_000_000_000
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Darfur Conflict (Sudan)",
            "type": "armed",
            "description": "Ongoing armed conflict in Darfur region",
            "start_date": "2003-01-01",
            "status": "dormant",
            "primary_location": "Darfur, Sudan",
            "affected_countries": ["Sudan", "Chad"],
            "parties_involved": ["Janjaweed", "Sudanese Government"],
            "death_toll": 300000,
            "displaced_persons": 2_700_000,
            "economic_impact": 10_000_000_000
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Somali Civil War",
            "type": "armed",
            "description": "Prolonged armed conflict in Somalia",
            "start_date": "1991-01-01",
            "status": "active",
            "primary_location": "Somalia",
            "affected_countries": ["Somalia", "Kenya", "Ethiopia"],
            "parties_involved": ["Al-Shabaab", "Somali Government", "AMISOM"],
            "death_toll": 500000,
            "displaced_persons": 3_000_000,
            "economic_impact": 15_000_000_000
        },
    ]
    
    @staticmethod
    def get_conflicts() -> List[Dict[str, Any]]:
        """Get conflict records."""
        return ConflictDataLoader.CONFLICTS


class SocialIssueDataLoader:
    """Load social issue data."""
    
    ISSUES = [
        {
            "id": str(uuid.uuid4()),
            "topic": "Out-of-School Children",
            "category": "almajiri",
            "description": "Children not enrolled in formal education, including Almajiri system",
            "severity": "critical",
            "affected_population": 15_000_000,
            "affected_regions": ["Northern Nigeria", "Northern Cameroon"],
            "tracking_start_date": "2010-01-01",
            "recent_incidents": 45
        },
        {
            "id": str(uuid.uuid4()),
            "topic": "Child Marriage",
            "category": "gender_inequality",
            "description": "Early and forced marriage of children, particularly girls",
            "severity": "high",
            "affected_population": 2_000_000,
            "affected_regions": ["Northern Nigeria", "Parts of West Africa"],
            "tracking_start_date": "2015-01-01",
            "recent_incidents": 120
        },
        {
            "id": str(uuid.uuid4()),
            "topic": "Gender-Based Violence",
            "category": "gender_inequality",
            "description": "Violence against women and girls",
            "severity": "high",
            "affected_population": 5_000_000,
            "affected_regions": ["Nigeria", "Africa"],
            "tracking_start_date": "2010-01-01",
            "recent_incidents": 200
        },
        {
            "id": str(uuid.uuid4()),
            "topic": "Child Labour",
            "category": "child_labor",
            "description": "Economic exploitation of children",
            "severity": "high",
            "affected_population": 10_000_000,
            "affected_regions": ["Sub-Saharan Africa"],
            "tracking_start_date": "2010-01-01",
            "recent_incidents": 300
        },
    ]
    
    @staticmethod
    def get_social_issues() -> List[Dict[str, Any]]:
        """Get social issue records."""
        return SocialIssueDataLoader.ISSUES
