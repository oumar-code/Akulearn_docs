# Content Generation Instructions

## Skill: Curriculum Content Generator

### Objective
Generate comprehensive, curriculum-aligned educational content for Nigerian secondary school students following NERDC, WAEC, and CAP standards.

### Context Requirements
- **subject**: The subject area (e.g., Mathematics, Physics, Chemistry, Biology, English)
- **grade_level**: Target grade level (JSS1-3, SS1-3)
- **topic**: Main topic or unit
- **curriculum_standard**: NERDC, WAEC, or CAP

### Content Generation Guidelines

#### 1. Lesson Structure
Each lesson should include:
- **Learning Objectives**: Clear, measurable objectives aligned with curriculum standards
- **Prerequisites**: Required prior knowledge
- **Key Concepts**: Main ideas and definitions
- **Explanations**: Detailed, step-by-step explanations with examples
- **Practice Questions**: Progressive difficulty levels
- **Real-World Applications**: Nigerian context examples
- **Summary**: Recap of key points

#### 2. Content Quality Standards
- **Accuracy**: All content must be factually correct and curriculum-aligned
- **Clarity**: Use simple, age-appropriate language
- **Cultural Relevance**: Use Nigerian examples, contexts, and scenarios
- **Engagement**: Include interesting facts, stories, or applications
- **Visual Support**: Suggest diagrams, charts, or illustrations where helpful

#### 3. Question Types to Include
- **Multiple Choice**: 4 options, one correct answer
- **Short Answer**: Brief responses testing understanding
- **Problem Solving**: Step-by-step worked examples
- **Application**: Real-world scenario questions
- **Critical Thinking**: Analysis and evaluation questions

#### 4. Difficulty Progression
- **Foundation**: Basic concepts and recall
- **Intermediate**: Application and understanding
- **Advanced**: Analysis and problem-solving

#### 5. Nigerian Context Integration
Always incorporate:
- Local currency (Naira) in financial problems
- Nigerian locations, names, and scenarios
- Culturally relevant examples
- Local industry and business contexts
- WAEC/NECO exam question styles

### Output Format
Generate structured JSON with:
```json
{
  "lesson_id": "unique_identifier",
  "subject": "subject_name",
  "grade_level": "level",
  "topic": "topic_name",
  "curriculum_alignment": ["NERDC", "WAEC"],
  "learning_objectives": [],
  "prerequisites": [],
  "content": {
    "introduction": "text",
    "main_content": [],
    "examples": [],
    "practice_questions": [],
    "summary": "text"
  },
  "metadata": {
    "estimated_duration": "minutes",
    "difficulty_level": "foundation|intermediate|advanced",
    "keywords": []
  }
}
```

### Best Practices
1. **Start Simple**: Begin with foundational concepts before advancing
2. **Build Progressively**: Each section should build on previous knowledge
3. **Check Alignment**: Verify all content matches curriculum standards
4. **Include Solutions**: Provide detailed solutions for all practice questions
5. **Test Understanding**: Include checkpoints throughout the lesson

### Quality Checklist
- [ ] All learning objectives are measurable
- [ ] Content is age-appropriate
- [ ] Nigerian context is integrated
- [ ] Examples are clear and relevant
- [ ] Questions have varying difficulty levels
- [ ] Solutions are provided and accurate
- [ ] Curriculum standards are explicitly referenced
- [ ] Language is simple and accessible
- [ ] Visual aids are suggested where appropriate
- [ ] Real-world applications are included
