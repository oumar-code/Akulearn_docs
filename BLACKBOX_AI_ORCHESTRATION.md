# Blackbox AI Orchestration Strategy (VS Code)

Purpose: Operationalize Blackbox AI in VS Code as a multi-role collaborator to accelerate content generation and platform development, aligned with `CONTENT_POPULATION_STRATEGY.md`.

## Roles & Responsibilities

Use Blackbox AI as distinct role personas. Prompt each role explicitly with scope, inputs, outputs, constraints, and acceptance criteria.

- Subject Matter Expert (SME)
  - Scope: Curriculum alignment, topic breakdowns, learning objectives, culturally relevant examples
  - Inputs: NERDC syllabus, existing content templates, subject outlines
  - Outputs: Structured outlines, objective trees, glossary, example sets
  - Constraints: NERDC alignment, Nigerian context, age-appropriate language
  - Acceptance: Coverage completeness, accuracy, local relevance

- Full Stack / Mobile / VR Developer
  - Scope: Interactive modules, code assets, simulations, web/mobile/VR features
  - Inputs: SME outlines, UI specs, tech stacks (React/Node/Django/WebXR)
  - Outputs: Implementable components, code examples, interactive demos, WebXR scenes
  - Constraints: Performance (<2s), cross-device compatibility, secure patterns
  - Acceptance: Runs locally, passes lint/tests, adheres to architecture

- UI/UX Designer
  - Scope: Information architecture, component specs, accessibility, motion guidelines
  - Inputs: Use cases, personas, SME content structures
  - Outputs: UX flows, UI specs (tokens, components), accessibility checklist
  - Constraints: WCAG 2.1 AA, mobile-first, low bandwidth support
  - Acceptance: Heuristic review, contrast ratios, keyboard operability

- Quality Assurance (QA)
  - Scope: Test plans, cases, automation, content validation
  - Inputs: Requirements, SME outputs, developer components
  - Outputs: Test matrices, automated tests, validation reports
  - Constraints: Accuracy verification, performance targets, security baselines
  - Acceptance: Pass/fail criteria aligned to Success Metrics and QA Framework

- DevOps Engineer
  - Scope: CI/CD, environments, observability, content pipelines
  - Inputs: Repo structure, Dockerfiles, `docker-compose-neo4j.yaml`
  - Outputs: Pipelines, IaC snippets, monitoring dashboards, backup plans
  - Constraints: Secure secrets handling, reproducible builds, rollbacks
  - Acceptance: Green pipelines, health checks, traceability

## Orchestration Workflow (Weekly Sprints)

1. Plan (SME + UX)
   - Select subjects/topics per `Phase` in `CONTENT_POPULATION_STRATEGY.md`
   - Produce outline, learning objectives, UX flows
2. Build (Dev + DevOps)
   - Generate code assets, simulations, content import scripts
   - Provision environments (Dev, Staging) and Neo4j as needed
3. Validate (QA + SME)
   - Run tests, accuracy checks, accessibility review
   - Approve for publishing
4. Publish (DevOps)
   - Commit, tag, deploy, monitor
5. Learn (All)
   - Analyze metrics, iterate on content and features

## Prompt Templates (Copy/Paste into Blackbox)

> SME Prompt
```
Role: Subject Matter Expert (Nigerian NERDC Curriculum)
Goal: Produce WAEC-aligned, culturally relevant content outlines for [Subject > Topic].
Inputs: `CONTENT_POPULATION_STRATEGY.md`, NERDC syllabus, existing JSON/CSV.
Outputs: JSON with fields: subject, topic, subtopics[], learning_objectives[], prerequisites[], examples[], glossary[].
Constraints: Age-appropriate, Nigerian context, avoid copyrighted text; write original summaries.
Acceptance: Coverage ≥95% of syllabus items for topic, clarity, example variety.
```

> Developer Prompt (Web/Mobile/VR)
```
Role: Full Stack + Mobile + VR Developer
Goal: Implement interactive module for [Subject > Topic].
Inputs: SME JSON outline, UI/UX spec, tech stack (React/Django/WebXR).
Outputs: Minimal runnable component(s), code examples, README with run steps.
Constraints: Performance <2s load, accessible controls, secure patterns.
Acceptance: Component runs locally, lint/tests pass, documented.
```

> UI/UX Prompt
```
Role: UI/UX Designer
Goal: Define IA + component spec for [Module].
Inputs: SME outline, target device constraints.
Outputs: IA tree, component list with properties, accessibility checklist (WCAG 2.1 AA), content layout templates.
Constraints: Mobile-first, low-bandwidth, color contrast ≥ 4.5:1.
Acceptance: Clear flows, accessible interactions, consistent tokens.
```

> QA Prompt
```
Role: QA Engineer
Goal: Validate content + component for [Module].
Inputs: Requirements, SME outline, developer outputs.
Outputs: Test plan, cases, automated tests (where applicable), validation report.
Constraints: Accuracy cross-check, performance targets, security baselines.
Acceptance: All critical tests pass; defects categorized with severity.
```

> DevOps Prompt
```
Role: DevOps Engineer
Goal: CI/CD + environment setup for content + components.
Inputs: Repo structure, Dockerfile, docker-compose-neo4j.yaml, requirements.txt.
Outputs: Pipeline YAML, environment configs, monitoring hooks, backup policy.
Constraints: Secrets security, reproducibility, rollbacks.
Acceptance: Green pipeline; deploy + health checks verified.
```

## AI Content Generation Pipeline (Aligned to Strategy)

- Source: SME generates structured outlines (JSON/CSV)
- Transform: Use `content_templates.py` and `comprehensive_content_populator.py` to render study guides, flashcards, encyclopedias
- Enrich: Link to `knowledge_graph_neo4j.py` for prerequisites/related content
- Validate: QA runs accuracy + readability checks against QA Framework
- Publish: DevOps commits + deploys; track metrics in Success Metrics

## File/Folder Conventions

- `content/ai_generated/<subject>/<topic>/*.json` — SME outlines
- `content/ai_rendered/<subject>/<topic>/*.md|.json` — Rendered outputs
- `tests/content_validation/*` — QA scripts
- `pipelines/*` — DevOps configs

## Guardrails (Policy & Quality)

- Original writing only; avoid copying textbooks or paid sources
- Cite datasets and public sources (NBS, World Bank) when used
- Enforce WCAG 2.1 AA; add Nigerian examples and context
- Use small, iterative PRs; all content must pass validation checks

## First Sprint (2 weeks)

- Subjects: Mathematics (Algebra), Physics (Mechanics)
- Deliverables:
  - SME outlines (10 topics total)
  - 10 study guides + 50 practice problems
  - 2 interactive demos (equations solver; motion simulator)
  - QA validation + accessibility checklist
  - CI pipeline to render + publish content artifacts

## How to Use in VS Code

1. Open Blackbox AI panel
2. Paste role prompt; provide the current subject/topic and inputs
3. Save outputs under `content/ai_generated/...`
4. Run render scripts to produce study guides
5. Submit PR; QA reviews; DevOps deploys

## Optional: Automation Hooks

- Create tasks to run generators:
```
python comprehensive_content_populator.py --subject Mathematics --topic Algebra
python comprehensive_content_populator.py --subject Physics --topic Mechanics
```

- Link rendered content to Neo4j:
```
python knowledge_graph_neo4j.py
```

This strategy keeps AI productive, accountable, and aligned with `CONTENT_POPULATION_STRATEGY.md`, while ensuring quality, accessibility, and local relevance. 