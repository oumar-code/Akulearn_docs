# Content Validation Instructions

## Skill: Content Quality Validator

### Objective
Validate educational content for quality, accuracy, completeness, and curriculum alignment to ensure high standards across the Akulearn platform.

### Validation Categories

#### 1. Curriculum Alignment Validation
- Verify content matches specified curriculum standards (NERDC/WAEC/CAP)
- Check learning objectives align with curriculum requirements
- Ensure topics are age-appropriate for grade level
- Validate prerequisite knowledge requirements

#### 2. Content Quality Validation
- **Accuracy**: Verify factual correctness of all information
- **Completeness**: Ensure all required sections are present
- **Clarity**: Check language is clear and age-appropriate
- **Structure**: Validate proper lesson organization
- **Consistency**: Check for consistent terminology and formatting

#### 3. Question Validation
- Verify all questions have correct answers
- Check answer options are plausible and non-ambiguous
- Ensure questions test stated learning objectives
- Validate difficulty level matches grade level
- Confirm solutions are provided and accurate

#### 4. Cultural Relevance Validation
- Verify Nigerian context in examples and scenarios
- Check currency references use Naira
- Validate names and locations are appropriate
- Ensure cultural sensitivity in all content

#### 5. Technical Validation
- Verify JSON structure is valid
- Check all required fields are present
- Validate data types are correct
- Ensure IDs are unique and properly formatted

### Validation Rules

#### Critical Errors (Must Fix)
- Factually incorrect information
- Missing required sections
- Invalid JSON structure
- Misaligned curriculum standards
- Incorrect answer keys
- Inappropriate content for age group

#### Warnings (Should Fix)
- Missing optional enhancements
- Inconsistent formatting
- Limited Nigerian context
- Sparse examples or explanations
- Missing visual aid suggestions

#### Suggestions (Nice to Have)
- Additional practice questions
- More real-world applications
- Enhanced multimedia suggestions
- Cross-curricular connections

### Validation Process

1. **Schema Validation**
   - Validate JSON structure
   - Check all required fields exist
   - Verify data types

2. **Content Review**
   - Read through all text content
   - Check for clarity and accuracy
   - Verify examples are correct

3. **Question Assessment**
   - Review all questions and answers
   - Verify difficulty progression
   - Check solution accuracy

4. **Curriculum Check**
   - Confirm alignment with standards
   - Verify learning objectives
   - Check grade-level appropriateness

5. **Cultural Review**
   - Assess Nigerian context integration
   - Check for cultural sensitivity
   - Verify localization

### Output Format

Generate validation report:
```json
{
  "validation_id": "unique_id",
  "content_id": "content_identifier",
  "timestamp": "ISO_timestamp",
  "overall_status": "pass|fail|warning",
  "score": 0-100,
  "errors": [
    {
      "severity": "critical|warning|suggestion",
      "category": "category_name",
      "message": "description",
      "location": "field_path",
      "suggestion": "how_to_fix"
    }
  ],
  "summary": {
    "total_checks": 0,
    "passed": 0,
    "warnings": 0,
    "errors": 0
  },
  "recommendations": []
}
```

### Quality Metrics

- **Completeness Score**: % of required fields present
- **Accuracy Score**: % of factually correct content
- **Alignment Score**: % match with curriculum standards
- **Engagement Score**: Quality of examples and applications
- **Localization Score**: Nigerian context integration level

### Auto-Fix Capabilities

When `auto_fix` is enabled:
- Fix JSON formatting issues
- Standardize terminology
- Add missing required fields with placeholders
- Correct common spelling errors
- Format currency to Naira

### Best Practices

1. **Be Thorough**: Check every section and field
2. **Be Constructive**: Provide actionable suggestions
3. **Be Consistent**: Apply rules uniformly
4. **Be Fair**: Consider content context and objectives
5. **Be Educational**: Help improve content creator skills

### Validation Checklist

- [ ] JSON structure is valid
- [ ] All required fields are present
- [ ] Learning objectives are clear and measurable
- [ ] Content is factually accurate
- [ ] Examples are relevant and correct
- [ ] Questions have valid answers
- [ ] Difficulty level is appropriate
- [ ] Nigerian context is integrated
- [ ] Language is clear and age-appropriate
- [ ] Curriculum alignment is verified
- [ ] Visual aids are suggested
- [ ] Real-world applications are included
- [ ] Solutions are complete and accurate
