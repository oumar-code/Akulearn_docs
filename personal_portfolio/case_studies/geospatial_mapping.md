# Case Study: Zamfara Education Mapping - Geospatial Analysis for Policy

## Overview
**Project**: Tertiary Education Access Mapping for Northwest Nigeria  
**Organization**: United Nations Development Programme (UNDP)  
**Timeline**: May 2024 – April 2025 (12-month internship)  
**Role**: Data Analyst (Geospatial Focus), Policy Support  
**Stack**: Power BI, SQL (PostgreSQL), QGIS, Python (GeoPandas, Folium), Excel

## Problem Statement
Northwest Nigeria (Zamfara, Sokoto, Katsina, Kebbi, Jigawa) faces:
- Unknown distribution of tertiary institutions (universities, polytechnics, colleges of education)
- No data on coverage gaps in rural vs urban areas
- Policy decisions made without spatial analysis
- Students travel 100+ km to nearest institution → high dropout rates

## Solution: Comprehensive Geospatial Database + Interactive Dashboards

### 1. Data Collection & Integration
- **Primary Sources**: 
  - National Universities Commission (NUC) registry (federal/state/private)
  - National Board for Technical Education (NBTE) polytechnic list
  - State Ministries of Education (colleges of education)
- **Manual Geocoding**: 80% of institutions lacked GPS coordinates → field verification via Google Maps + local contacts
- **Attribute Data**: Enrollment capacity, programs offered, infrastructure (labs, libraries, hostels)

### 2. Spatial Analysis (QGIS + Python)
Key questions answered:
- **Coverage Gaps**: Which LGAs (Local Government Areas) lack tertiary institutions within 50km?
- **Capacity Mismatch**: Where do high-population zones have insufficient enrollment capacity?
- **Transport Analysis**: How many students face 2+ hour commutes?

### 3. Interactive Power BI Dashboards
Built 3 stakeholder-specific views:
- **Policy Makers**: Coverage heatmaps, population-vs-capacity scatter plots, priority LGA rankings
- **Education Planners**: Institution details (programs, capacity, infrastructure scores)
- **Public/Students**: Institution finder with distance calculator, program search

## Technical Approach

### Geospatial Workflow
```python
# Sample distance analysis (GeoPandas)
import geopandas as gpd
from shapely.geometry import Point

# Load institutions and LGAs
institutions = gpd.read_file("institutions.geojson")
lgas = gpd.read_file("lgas.shp")

# Calculate nearest institution for each LGA centroid
lgas['nearest_distance_km'] = lgas.geometry.apply(
    lambda centroid: institutions.distance(centroid).min() / 1000
)

# Identify underserved LGAs (>50km to nearest institution)
underserved = lgas[lgas['nearest_distance_km'] > 50]
print(f"Underserved LGAs: {len(underserved)}")
```

### SQL Queries (Capacity Analysis)
```sql
-- Population vs enrollment capacity by state
SELECT 
    s.state_name,
    s.population,
    SUM(i.enrollment_capacity) AS total_capacity,
    (s.population / SUM(i.enrollment_capacity)) AS ratio_pop_to_capacity
FROM states s
LEFT JOIN institutions i ON s.state_id = i.state_id
GROUP BY s.state_name, s.population
ORDER BY ratio_pop_to_capacity DESC;
```

## Key Findings

### Coverage Gaps (Quantified)
| State | Total LGAs | LGAs with Institution | Underserved LGAs (>50km) |
|-------|------------|----------------------|-------------------------|
| Zamfara | 14 | 3 (21%) | 11 (79%) |
| Sokoto | 23 | 5 (22%) | 18 (78%) |
| Katsina | 34 | 8 (24%) | 26 (76%) |
| **Total** | **71** | **16 (23%)** | **55 (77%)** |

### Capacity Mismatch
- **Zamfara**: 4.5M population → 25,000 enrollment capacity → 180:1 ratio (national avg: 120:1)
- **Implication**: 60,000 qualified students/year compete for 5,000 slots

### Infrastructure Quality
- 40% of institutions lack functional labs (science/engineering programs suffer)
- 60% have <50% hostel capacity → students commute/rent expensive private housing

## Policy Impact

### Immediate Actions (2024-2025)
1. **New Institution Planning**: UNDP recommended 12 new colleges of education (prioritized by our gap analysis)
2. **Transport Subsidies**: Zamfara State approved ₦500M for student shuttle buses (routes based on our distance data)
3. **Capacity Expansion**: 3 polytechnics received funding for 5,000 additional slots (targeted to high-ratio LGAs)

### Long-Term Strategy (2026-2030)
- **Digital Education**: UNDP piloting distance learning programs in underserved LGAs (informed by our infrastructure audit)
- **Public-Private Partnerships**: Dashboards shared with private investors → 2 new private universities planned for Zamfara

## Technical Deliverables

1. **Geospatial Database**: PostgreSQL with PostGIS extensions (71 LGAs, 35 institutions, 1,000+ attributes)
2. **Power BI Dashboards**: 15+ interactive visuals, published to UNDP's internal portal
3. **QGIS Project Files**: Reproducible maps for future updates
4. **Policy Brief**: 20-page report with maps, charts, recommendations (presented to State Commissioners of Education)

## Skills Demonstrated

- **Geospatial Analysis**: QGIS, GeoPandas, spatial joins, buffer analysis, distance calculations
- **Data Engineering**: ETL pipelines (Excel/CSV → cleaned PostgreSQL), data validation scripts
- **Visualization**: Power BI (DAX measures, interactive filters, drill-down hierarchies)
- **Stakeholder Communication**: Translated technical findings into policy-friendly language

## Lessons Learned

1. **Data Gaps Are the Norm**: 50% of initial data required manual verification/correction
2. **Maps Speak Louder Than Tables**: Policy makers engaged 3x more with visual heatmaps vs raw numbers
3. **Context Matters**: National averages hide regional disparities; state-level analysis essential
4. **Field Experience Informs Product**: This project inspired Akulearn's focus on low-bandwidth delivery for rural students

## Recognition
- **UNDP Internal Award**: "Most Impactful Intern Project 2024"
- **Field Research Foundation**: Documented pain points → informed Akulearn's rural education features

## Next Steps (Post-UNDP)

### Applying Learnings to Akulearn
- **School Mapping Module**: Help administrators identify underserved schools for pilot deployments
- **Offline Sync Strategy**: Prioritize low-connectivity LGAs for solar kit distribution

### Broader Geospatial + EdTech Vision
- **National EdTech Map**: Replicate analysis for all 36 Nigerian states (identify 500k+ underserved students)
- **Real-Time Dashboards**: Partner with Ministries to update institution data quarterly

## Contact & Consulting
- **Geospatial Analytics**: Available for education mapping, health facility analysis, infrastructure planning
- **Power BI/SQL/QGIS Training**: Offer workshops for NGOs/government teams
- **Email**: lumarabubakarb2018@gmail.com | **Phone**: +234 9038650851
- **Schedule Consultation**: [Add Calendly link]

## Related Projects
- Akulearn (used geospatial insights to prioritize pilot states)
- Zamfara Schistosomiasis Study (HND research project, Python-driven prevalence analysis)
