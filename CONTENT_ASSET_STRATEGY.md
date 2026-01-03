# Content Asset Generation Strategy for Akulearn
**Date**: January 2, 2026  
**Status**: Planning Phase  
**Goal**: Create intuitive, high-quality educational assets using MCP integrations

---

## 🎯 Vision
Build a comprehensive library of educational content assets that are:
- **Contextually Relevant**: Tailored to Nigerian students (WAEC, NECO, JAMB)
- **Culturally Appropriate**: Use Nigerian names, locations, currency, examples
- **Visually Engaging**: Rich multimedia (diagrams, videos, interactive content)
- **Pedagogically Sound**: Aligned with learning objectives and curriculum standards

---

## 📊 Current State Analysis

### Existing Content (27 items across 7 subjects)
- Biology: 2 items (Cell Biology, Ecology)
- Chemistry: 4 items (Hydrocarbons, Kinetics, Biochemistry)
- Economics: 1 item (Demand & Supply)
- English: 2 items (Comprehension, Grammar)
- Geography: 1 item (Weather & Climate)
- Mathematics: 8 items (Coordinate Geometry, Calculus, Probability)
- Physics: 9 items (Energy, Circuits, Optics, Thermodynamics)

### Content Gaps Identified
1. **Missing Subjects**: History, Literature, Computer Science, Commerce, Government
2. **Insufficient Depth**: Most subjects have < 5 topics covered
3. **Missing Asset Types**:
   - No diagrams or illustrations
   - No practice questions with solutions
   - No video content
   - No interactive simulations
   - No cultural context examples

---

## 🔬 Research Phase: MCP-Driven Content Discovery

### Phase 1: Curriculum Mapping (Week 1-2)
**Tools**: Brave Search MCP, Wikipedia MCP, GitHub MCP

#### Research Tasks:
1. **WAEC Syllabus Scraping**
   - Use Brave Search to fetch official WAEC syllabus documents
   - Extract topic lists for all subjects
   - Map to current content database
   - Identify coverage gaps

2. **NECO & JAMB Standards**
   - Compare requirements across exam boards
   - Find overlapping topics (efficiency gain)
   - Note unique requirements per board

3. **Nigerian Curriculum Standards**
   - Federal Ministry of Education guidelines
   - State-specific variations
   - Common misconceptions and difficult topics

**Deliverable**: `curriculum_mapping.json` with complete topic hierarchy

### Phase 2: Content Quality Benchmarking (Week 2-3)
**Tools**: Web Search MCP, GitHub MCP (check competitors)

#### Research Questions:
- What makes educational content "intuitive"?
- How do top Nigerian ed-tech platforms structure content?
- What multimedia formats have highest engagement?
- What's the optimal content length for SS2 students?

#### Competitive Analysis:
- uLesson content structure
- Prepclass content format
- Khan Academy (adapt for Nigerian context)
- BBC Bitesize (adapt pedagogy)

**Deliverable**: `content_quality_standards.md` with best practices

### Phase 3: Asset Type Definition (Week 3-4)
**Tools**: Image Generation MCP, YouTube MCP

#### Asset Categories to Research:

1. **Text-Based Assets**
   - Study guides (current: ✅)
   - Reference materials (current: ✅)
   - Practice problems (current: ⚠️ limited)
   - Worked examples (current: ⚠️ limited)
   - Exam tips (current: ✅)

2. **Visual Assets** (NEW)
   - Diagrams (Physics circuits, Chemistry structures)
   - Infographics (History timelines, Geography maps)
   - Illustrations (Biology diagrams, Literature character maps)
   - Charts/Graphs (Economics data, Math functions)

3. **Interactive Assets** (NEW)
   - Quizzes with instant feedback
   - Flashcards for memorization
   - Interactive simulations (Physics experiments)
   - Code playgrounds (Computer Science)

4. **Multimedia Assets** (NEW)
   - Video lessons (5-10 min segments)
   - Audio explanations (for accessibility)
   - Animated concepts (complex topics)

**Deliverable**: `asset_type_catalog.json` with specifications

---

## 🏗️ Content Asset Generation Framework

### Asset Type 1: Enhanced Study Guides
**Status**: Current format needs enrichment

**Enhancement Plan**:
```json
{
  "current_format": "Markdown text with sections",
  "enhancements": [
    "Add inline diagrams using Image Generation MCP",
    "Include real-world Nigerian examples (currency, locations)",
    "Embed curated YouTube videos",
    "Add practice problems with step-by-step solutions",
    "Include cultural context notes"
  ],
  "mcp_integration": ["Brave Search", "Wikipedia", "Image Gen", "YouTube"]
}
```

### Asset Type 2: Visual Diagrams Library
**Status**: Not started

**Generation Strategy**:
1. **Physics Diagrams** (Circuit diagrams, Force diagrams, Ray diagrams)
   - Use Image Generation MCP with physics-specific prompts
   - Generate SVG format for scalability
   - Store in `assets/diagrams/physics/`

2. **Chemistry Structures** (Molecular structures, Reaction diagrams)
   - Use ChemDraw-style prompts
   - Generate organic chemistry structures
   - Store in `assets/diagrams/chemistry/`

3. **Biology Illustrations** (Cell diagrams, Body systems, Ecology food chains)
   - Use anatomical illustration style
   - Include labels in clear fonts
   - Store in `assets/diagrams/biology/`

4. **Math Graphs** (Function plots, Geometric shapes, Statistical charts)
   - Use matplotlib/plotly for programmatic generation
   - Interactive where possible
   - Store in `assets/diagrams/mathematics/`

**Tool**: Image Generation MCP + Python scripting

### Asset Type 3: Practice Question Banks
**Status**: Not started

**Generation Strategy**:
- Use Brave Search to find past WAEC/NECO questions
- Generate similar questions using pattern analysis
- Create worked solutions with explanations
- Difficulty levels: Basic → Intermediate → Advanced → Exam-Level

**Structure**:
```json
{
  "question_id": "physics_mechanics_001",
  "subject": "Physics",
  "topic": "Mechanics",
  "difficulty": "intermediate",
  "question": "A car of mass 1000kg...",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "B",
  "worked_solution": "Step 1: Identify given values...",
  "explanation": "This question tests Newton's second law...",
  "exam_board": "WAEC",
  "year": "2024"
}
```

### Asset Type 4: Video Content Curation
**Status**: Not started

**Curation Strategy**:
1. Use YouTube MCP to search for Nigerian educational content
2. Filter by:
   - Relevance to curriculum
   - Video quality (min 720p)
   - Nigerian accent/context (where applicable)
   - Length (5-15 minutes optimal)
3. Create video library with timestamps for key concepts
4. Embed in study guides at relevant sections

**Categories**:
- Concept explanations (theory)
- Worked examples (problem-solving)
- Exam techniques (test-taking strategies)
- Real-world applications (motivation)

---

## 📋 Research Checklist

### Before Content Generation Starts:
- [ ] **Curriculum Mapping Complete**
  - [ ] WAEC syllabus mapped (all subjects)
  - [ ] NECO requirements documented
  - [ ] JAMB UTME topics listed
  - [ ] Topic priority ranking created

- [ ] **Quality Standards Defined**
  - [ ] Content length guidelines (per topic type)
  - [ ] Reading level verification (SS2 = 16-17 years)
  - [ ] Cultural relevance checklist
  - [ ] Accuracy verification process

- [ ] **Asset Specifications Ready**
  - [ ] Image format standards (SVG, PNG, WebP)
  - [ ] Video format requirements (MP4, max file size)
  - [ ] Audio specifications (if needed)
  - [ ] Interactive element guidelines

- [ ] **MCP Integrations Tested**
  - [ ] Brave Search API working
  - [ ] Image Generation producing quality outputs
  - [ ] YouTube API returning relevant results
  - [ ] Database MCP ready for asset storage

- [ ] **Content Creator Training**
  - [ ] How to use MCP tools for research
  - [ ] Asset quality standards
  - [ ] Nigerian context guidelines
  - [ ] Review and approval workflow

---

## 🚀 Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
**Research Focus**: Curriculum mapping and standards
**Deliverables**:
- Complete curriculum map for all subjects
- Content quality standards document
- Nigerian context guidelines
- Asset type specifications

### Phase 2: Pilot Generation (Weeks 3-4)
**Focus**: Generate 5 complete lessons per subject using MCPs
**Assets per Lesson**:
- Enhanced study guide (with diagrams)
- 10 practice questions with solutions
- 2-3 curated video links
- Key concepts flashcards
- Cultural context examples

**Subjects**: Biology, Chemistry, Physics, Mathematics, Economics

### Phase 3: Scale-Up (Weeks 5-8)
**Focus**: Generate 20 lessons per subject
**Total Target**: 100 lessons across 5 subjects

### Phase 4: Expansion (Weeks 9-12)
**New Subjects**: History, Literature, Government, Commerce, Computer Science
**Target**: 15 lessons per new subject = 75 additional lessons

### Phase 5: Multimedia Enhancement (Weeks 13-16)
**Focus**: Add rich media to existing content
- Generate custom diagrams for all science topics
- Create video content or curate from Nigerian creators
- Build interactive quizzes
- Add audio narrations for accessibility

---

## 🎨 Asset Intuitive Design Principles

### Principle 1: Cultural Relevance
✅ **Do**:
- Use Nigerian names (Ada, Chidi, Fatima, Emeka)
- Reference Nigerian locations (Lagos, Abuja, Kano, Port Harcourt)
- Use Naira (₦) for Economics examples
- Include Nigerian historical context

❌ **Don't**:
- Use foreign names or contexts exclusively
- Assume universal cultural knowledge
- Ignore regional variations

### Principle 2: Visual Clarity
✅ **Do**:
- Use high contrast for diagrams
- Large, readable fonts (min 14px)
- Clear labels and legends
- Consistent color schemes per subject

❌ **Don't**:
- Overload diagrams with information
- Use tiny text in images
- Mix too many colors

### Principle 3: Progressive Complexity
✅ **Do**:
- Start with simple examples
- Build to complex problems gradually
- Provide scaffolding (step-by-step)
- Include "Try This" practice at each level

❌ **Don't**:
- Jump to advanced concepts without foundation
- Assume prior knowledge
- Skip intermediate steps

### Principle 4: Multi-Modal Learning
✅ **Do**:
- Provide text explanations
- Add visual diagrams
- Include video alternatives
- Offer practice problems
- Give real-world applications

❌ **Don't**:
- Rely on only one format
- Ignore different learning styles

---

## 📊 Success Metrics

### Content Quality Metrics:
- **Coverage**: % of curriculum topics covered (Target: 80% by Q2 2026)
- **Accuracy**: % of content verified by subject experts (Target: 100%)
- **Engagement**: Average time spent per content item (Target: 12+ min)
- **Completion**: % of students completing lessons (Target: 70%+)

### Asset Quality Metrics:
- **Visual Assets**: Number of custom diagrams (Target: 500+)
- **Practice Questions**: Question bank size (Target: 2000+)
- **Video Library**: Curated videos per subject (Target: 50+)
- **Cultural Relevance**: % with Nigerian context (Target: 90%+)

### User Feedback Metrics:
- **Likes**: Average likes per content (Target: 80%+)
- **Student Ratings**: Average rating (Target: 4.5/5)
- **Teacher Feedback**: Curriculum alignment score (Target: 95%+)

---

## 🛠️ Tools and Technologies

### Content Generation:
- **Python Scripts**: Automated content generation pipelines
- **MCP Integrations**: Brave Search, Wikipedia, YouTube, Image Gen
- **AI Assistance**: ChatGPT/Claude for content drafting
- **Human Review**: Subject matter experts for verification

### Asset Management:
- **GitHub**: Version control for all content
- **Cloud Storage**: Google Drive or AWS S3 for multimedia
- **Database**: PostgreSQL for structured content storage
- **CDN**: Fast delivery of images/videos

### Quality Control:
- **Grammarly**: Language quality checks
- **Plagiarism Detector**: Ensure originality
- **Curriculum Validator**: Match against exam board requirements
- **A/B Testing**: Test different content formats

---

## 💡 Next Immediate Actions

1. **Set Up MCP Integrations** (This Week)
   - Activate Brave Search MCP
   - Test Wikipedia MCP for content fetching
   - Configure Image Generation MCP
   - Set up YouTube MCP

2. **Start Curriculum Research** (Next 2 Days)
   - Fetch WAEC syllabus for all subjects
   - Create topic inventory
   - Identify priority topics (exam frequency analysis)

3. **Generate Pilot Assets** (Next Week)
   - Create 5 enhanced study guides with diagrams
   - Generate 50 practice questions
   - Curate 20 educational videos

4. **Build Asset Pipeline** (Next 2 Weeks)
   - Automate content generation workflow
   - Create asset review dashboard
   - Set up content delivery infrastructure

---

**Next Step**: Activate MCP integrations and begin curriculum mapping research?
