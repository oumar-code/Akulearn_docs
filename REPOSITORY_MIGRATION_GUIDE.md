# Repository Structure & GitHub Setup Guide

## Overview
This document provides instructions to separate personal portfolio and company (VersaTech) assets into dedicated GitHub repositories for better branding, discoverability, and customer acquisition.

---

## Current Structure (Akulearn_docs - Monorepo)

```
Akulearn_docs/ (main project repo)
├── personal_portfolio/
│   ├── README.md (bio, skills, services)
│   ├── case_studies/
│   │   ├── akulearn.md (2,800 words - DevOps/MLOps)
│   │   ├── voice_dataset.md (2,500 words - NLP/ethics)
│   │   └── geospatial_mapping.md (2,400 words - QGIS/Power BI)
│   └── kaggle/
│       └── assyrian_translation_baseline.ipynb (seq2seq demo)
├── versatech_profile/
│   └── README.md (company positioning, services)
├── marketing/
│   ├── social_posts.md (8 launch posts)
│   └── SOCIAL_POSTING_SCHEDULE.md (7-day calendar)
├── src/backend/ (FastAPI - 40+ endpoints)
├── wave3_content_database.json (42 lessons - production)
└── [content generation scripts, docs, etc.]
```

---

## Target Structure (3 Separate Repos)

### 1. **personal-portfolio** (Public)
**Purpose**: Showcase technical skills, case studies, Kaggle work; attract remote opportunities  
**URL**: `https://github.com/oumar-code/personal-portfolio`

**Structure**:
```
personal-portfolio/
├── README.md
│   - Hero section: "AI/NLP Engineer | EdTech Pioneer | Kaggle Competitor"
│   - 3 featured projects (Akulearn, Voice, Geospatial)
│   - Quick stats (42 lessons, 8,500 recordings, 77% gap coverage)
│   - Contact: email, Calendly link, GitHub repos
├── projects/
│   ├── akulearn/
│   │   ├── README.md (case study content)
│   │   ├── architecture-diagram.png
│   │   └── pipeline-code-samples.md
│   ├── voice-dataset/
│   │   ├── README.md (case study content)
│   │   └── ethics-framework.md
│   └── geospatial-mapping/
│       ├── README.md (case study content)
│       └── qgis-snapshots/ (screenshots)
├── kaggle/
│   ├── assyrian-translation/
│   │   └── notebook.ipynb (competition entry)
│   └── README.md (leaderboard links, approach summaries)
├── blog/ (optional - future technical posts)
│   └── README.md (archive of published articles)
├── cv.pdf (resume/CV)
└── LICENSE (MIT or similar)
```

**SEO Keywords**: NLP engineer, EdTech, Kaggle, DevOps, multilingual AI, Nigerian tech

---

### 2. **versatech-site** (Public)
**Purpose**: Company homepage, service offerings, case studies; B2B customer acquisition  
**URL**: `https://github.com/oumar-code/versatech-site`

**Structure**:
```
versatech-site/
├── README.md (company overview, quick start)
├── index.html (landing page or Next.js /pages/index)
├── docs/
│   ├── SERVICES.md (6 service pillars with pricing)
│   ├── CASE_STUDIES.md (Akulearn, Voice, Geospatial - B2B angle)
│   ├── SECTORS.md (EdTech, Healthcare, Public Sector, Fintech, Telco)
│   ├── TEAM.md (Founder/team bios)
│   └── FAQ.md (Common questions)
├── website/ (optional Next.js or static site)
│   ├── components/
│   ├── pages/
│   │   ├── index.tsx (hero + services)
│   │   ├── services.tsx (detailed service cards)
│   │   ├── cases.tsx (case study gallery)
│   │   ├── blog.tsx (tech content, thought leadership)
│   │   └── contact.tsx (Calendly embed)
│   └── styles/
├── assets/
│   ├── logo-versatech.svg
│   ├── service-icons/ (6 icons for pillars)
│   └── case-study-images/
├── package.json (Next.js dependencies if applicable)
└── LICENSE
```

**SEO Keywords**: AI solutions, EdTech platform, NLP consulting, MLOps, Nigeria

---

## Migration Steps

### Phase 1: Repository Setup (GitHub UI)

#### 1a. Create **personal-portfolio** repo
```bash
# On GitHub:
- New repo → name: "personal-portfolio"
- Public
- Add README.md
- MIT License
- .gitignore: Python
```

#### 1b. Create **versatech-site** repo
```bash
# On GitHub:
- New repo → name: "versatech-site"
- Public
- Add README.md
- MIT License
```

---

### Phase 2: Local Setup & Content Migration

#### 2a. Clone your new personal-portfolio repo
```bash
cd ~/repos  # or your projects folder
git clone https://github.com/oumar-code/personal-portfolio.git
cd personal-portfolio
```

#### 2b. Copy case study content
```bash
# From Akulearn_docs
cp ~/Documents/Akulearn_docs/personal_portfolio/README.md ./
mkdir -p projects/akulearn projects/voice-dataset projects/geospatial-mapping
cp ~/Documents/Akulearn_docs/personal_portfolio/case_studies/akulearn.md ./projects/akulearn/README.md
cp ~/Documents/Akulearn_docs/personal_portfolio/case_studies/voice_dataset.md ./projects/voice-dataset/README.md
cp ~/Documents/Akulearn_docs/personal_portfolio/case_studies/geospatial_mapping.md ./projects/geospatial-mapping/README.md
```

#### 2c. Copy Kaggle notebook
```bash
mkdir -p kaggle/assyrian-translation
cp ~/Documents/Akulearn_docs/personal_portfolio/kaggle/assyrian_translation_baseline.ipynb ./kaggle/assyrian-translation/notebook.ipynb
```

#### 2d. Create Kaggle README
```markdown
# Kaggle Competitions

## Active Competitions

### Assyrian Cuneiform Translation
- **Notebook**: [assyrian-translation/notebook.ipynb](assyrian-translation/notebook.ipynb)
- **Status**: Training mT5-small baseline
- **Approach**: Multilingual seq2seq with transformers
- **Leaderboard**: [Link to competition]
- **Relevant Skills**: Low-resource NLP, translation, transfer learning
```

---

#### 2e. Commit and push to personal-portfolio
```bash
git add .
git commit -m "Initial portfolio: case studies, Kaggle notebook, professional bio"
git push -u origin main
```

---

#### 2f. Clone versatech-site
```bash
git clone https://github.com/oumar-code/versatech-site.git
cd versatech-site
```

#### 2g. Copy company content
```bash
# Copy VersaTech README
cp ~/Documents/Akulearn_docs/versatech_profile/README.md ./

# Create docs structure
mkdir -p docs
cat > docs/SERVICES.md << 'EOF'
# VersaTech Services

## 1. AI Strategy & Architecture
Custom AI/ML strategy for enterprises, startups, and NGOs.
- Technical assessment
- Roadmap development
- Tool selection (TensorFlow, PyTorch, etc.)
- **Typical Cost**: ₦500k-₦2M (fixed project)

## 2. Scalable Infrastructure
MLOps and DevOps pipeline setup.
- GitHub Actions CI/CD
- Docker containerization
- Kubernetes orchestration (optional)
- MLflow experiment tracking
- **Typical Cost**: ₦1M-₦5M (implementation + training)

## 3. Automation & Workflow Optimization
Custom Python scripts, business process automation.
- PDF/document processing
- Data pipeline automation
- ETL workflows
- **Typical Cost**: ₦300k-₦1M per project

## 4. Multilingual NLP & Voice Solutions
ASR/TTS, translation, language-specific NLP.
- Fine-tuning for underrepresented languages (Hausa, Yoruba, etc.)
- Voice dataset creation and labeling
- **Typical Cost**: ₦2M-₦8M (depending on scale)

## 5. EdTech Platform Development
Curriculum mapping, content generation, deployment.
- AI-powered content creation
- Localized learning systems
- Offline-first design
- **Typical Cost**: ₦3M-₦15M (MVP to production)

## 6. Geospatial Analytics & BI
QGIS, Power BI, spatial analysis, policy impact.
- Opportunity mapping
- Capacity analysis
- Interactive dashboards
- **Typical Cost**: ₦1.5M-₦5M per project

---

## Package Discounts
- **Full-Stack (AI + Infra + EdTech)**: 20% discount
- **Multi-Year**: 15% discount (years 2+)
- **Non-Profit/NGO**: 25% discount

---

**Schedule Consultation**: [Calendly link]
EOF
```

#### 2h. Create sector-specific docs
```bash
cat > docs/SECTORS.md << 'EOF'
# Industries We Serve

## Education & EdTech
- **Problem**: Low teacher capacity, lack of quality, accessible content
- **Solution**: Akulearn platform (42 lessons, ₦300/student/month)
- **Proof**: 1k beta → 65k target (Q4 2026)

## Healthcare
- **Problem**: Data fragmentation, diagnostic consistency
- **Solution**: AI-powered clinical decision support, data integration
- **Proof**: [Healthcare case study - coming soon]

## Public Sector & Policy
- **Problem**: Data silos, geographic blind spots
- **Solution**: Geospatial analytics, dashboards for policy makers
- **Proof**: UNDP Geosp study (77% gaps identified, ₦500M approved)

## Telecommunications
- **Problem**: Rural connectivity, last-mile delivery
- **Solution**: Offline-first apps, solar-powered kits, CDN optimization
- **Proof**: [Telco partnership case study - coming soon]

## Financial Services
- **Problem**: Credit risk assessment, fraud detection
- **Solution**: Custom ML models, real-time inference
- **Proof**: [Fintech case study - coming soon]
EOF
```

#### 2i. Commit and push versatech-site
```bash
git add .
git commit -m "Initial VersaTech site: services, sectors, case studies"
git push -u origin main
```

---

### Phase 3: Update References

#### 3a. Update personal_portfolio/README.md (in both places)
```markdown
[At top of README]
## Portfolio Repository
- **Full Projects**: [personal-portfolio](https://github.com/oumar-code/personal-portfolio)
- **Company**: [VersaTech](https://github.com/oumar-code/versatech-site)
- **Main Project**: [Akulearn](https://github.com/oumar-code/Akulearn_docs)
```

#### 3b. Update versatech_profile/README.md
```markdown
[At top of README]
## VersaTech Repository
- **Website**: [versatech-site](https://github.com/oumar-code/versatech-site)
- **Founder Portfolio**: [personal-portfolio](https://github.com/oumar-code/personal-portfolio)
- **Flagship Product**: [Akulearn_docs](https://github.com/oumar-code/Akulearn_docs)
```

#### 3c. Update Akulearn_docs README
```markdown
[Add section]
## Related Repositories
- **VersaTech Company**: https://github.com/oumar-code/versatech-site
- **Founder Portfolio**: https://github.com/oumar-code/personal-portfolio
```

---

### Phase 4: Pin Repos on GitHub Profile

Go to [https://github.com/oumar-code](https://github.com/oumar-code) → Edit profile → Pin repositories:
1. personal-portfolio
2. versatech-site
3. Akulearn_docs

---

## Website Options (versatech-site)

### Option A: Static HTML (Quick, 1-2 hours)
- Bootstrap + HTML/CSS
- Host on GitHub Pages (free)
- Example: [versatech-site/index.html](./index.html)

### Option B: Next.js (Production, 4-6 hours)
```bash
cd versatech-site
npx create-next-app@latest --typescript --tailwind
# Build pages: index, services, cases, blog, contact
# Calendly embed in contact page
npm run build && npm run start
```

### Option C: Markdown-based (Medium, 2-3 hours)
- Use Jekyll/Hugo to convert markdown docs to HTML site
- Example: GitHub's built-in Pages with Jekyll theme

**Recommendation**: Start with Option A (HTML), upgrade to Option B (Next.js) in Q2 2026

---

## Calendly Integration

Once you have Calendly account:

### Add to personal-portfolio/README.md
```markdown
## Schedule a Consultation
Looking to discuss AI/NLP opportunities? [Book a 30-minute call](https://calendly.com/oumar-code/consultation)
```

### Add to versatech-site
```markdown
## Get in Touch
Interested in VersaTech services? [Schedule a strategy session](https://calendly.com/oumar-code/consultation)
```

### Add to all case studies
```markdown
---
**Interested in similar solutions for your organization?**
[Schedule a consultation](https://calendly.com/oumar-code/consultation) to discuss your specific needs.
```

---

## SEO & Discoverability

### personal-portfolio GitHub
- **Repo Description**: "AI/NLP Engineer portfolio: EdTech, low-resource translation, geospatial analytics"
- **Topics**: `nlp`, `machine-learning`, `edtech`, `kaggle`, `portfolio`, `case-studies`
- **Website URL**: (blank for now, add when live)

### versatech-site GitHub
- **Repo Description**: "VersaTech: Custom AI/ML solutions for EdTech, healthcare, public sector"
- **Topics**: `ai`, `machine-learning`, `edtech`, `mlops`, `nigeria`, `africa`
- **Website URL**: (add when GitHub Pages live)

---

## Timeline

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| 1 | Create 2 new repos | 5 min | ⏳ TODO |
| 2a | Clone & setup local repos | 5 min | ⏳ TODO |
| 2b-g | Copy content & commit | 15 min | ⏳ TODO |
| 3 | Update cross-references | 10 min | ⏳ TODO |
| 4 | Pin repos on profile | 2 min | ⏳ TODO |
| 5 | Create website (Option A) | 1-2 hrs | ⏳ TODO |
| 6 | Add Calendly links | 10 min | ⏳ TODO |
| 7 | Post on social media | 5-7 days | ⏳ TODO |

**Total**: ~2-4 hours for complete setup + website

---

## Post-Launch Maintenance

### Weekly (Every Monday)
- [ ] Update Akulearn lesson count in all READMEs
- [ ] Sync new case studies or blog posts across repos

### Monthly (First Friday)
- [ ] Update GitHub profile stats (followers, contributions)
- [ ] Review and respond to GitHub issues/DMs
- [ ] Update Kaggle leaderboard screenshots

### Quarterly
- [ ] Quarterly case studies or client wins
- [ ] Update service pricing/availability
- [ ] Blog post on recent projects or industry insights

---

## Questions?

This guide is meant to be customizable. Feel free to:
- Rename repos (e.g., `umar-portfolio`, `versatech-ai`)
- Add additional projects or case studies
- Host on custom domain instead of GitHub Pages
- Integrate blog, testimonials, or team member profiles

**Last Updated**: January 3, 2026  
**Next Review**: January 17, 2026 (after launch)
