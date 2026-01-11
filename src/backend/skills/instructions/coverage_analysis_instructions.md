# Coverage Analysis Instructions

## Skill: Curriculum Coverage Analyzer

### Objective
Analyze and report on curriculum coverage across NERDC, WAEC, and CAP standards to identify gaps and prioritize content creation.

### Analysis Scope

#### Curriculum Standards
- **NERDC**: Nigerian Educational Research and Development Council curriculum
- **WAEC**: West African Examinations Council syllabus
- **CAP**: Computer-Aided Personalized learning standards

#### Subjects to Analyze
- Mathematics (JSS1-3, SS1-3)
- English Language
- Sciences (Physics, Chemistry, Biology)
- Social Studies
- Commercial Subjects
- Arts and Humanities

### Analysis Dimensions

#### 1. Topic Coverage
- Count of topics defined in curriculum
- Count of topics with content in platform
- Percentage coverage by subject
- Percentage coverage by grade level
- Missing topics list

#### 2. Content Depth
- Lessons per topic
- Questions per topic
- Examples per concept
- Practice exercises available
- Multimedia assets present

#### 3. Content Quality
- Validation status
- Curriculum alignment score
- Content completeness
- Question quality metrics
- Student engagement data

#### 4. Assessment Coverage
- Practice questions available
- Diagnostic tests created
- Past questions coverage
- Question type variety
- Difficulty level distribution

### Coverage Metrics

#### Primary Metrics
- **Overall Coverage**: % of curriculum topics with content
- **Subject Coverage**: % coverage per subject
- **Grade Coverage**: % coverage per grade level
- **Standard Coverage**: % coverage per curriculum standard

#### Secondary Metrics
- **Content Depth Score**: Average lessons per topic
- **Question Density**: Average questions per topic
- **Multimedia Coverage**: % topics with visual aids
- **Assessment Readiness**: % topics with complete assessments

#### Quality Metrics
- **Validation Rate**: % content that passed validation
- **Alignment Score**: Average curriculum alignment score
- **Engagement Score**: Student interaction metrics
- **Completion Rate**: Student lesson completion rates

### Analysis Process

#### Step 1: Data Collection
1. Load curriculum standards from database
2. Query platform content database
3. Retrieve validation reports
4. Collect usage analytics
5. Gather assessment data

#### Step 2: Coverage Calculation
1. Map content to curriculum topics
2. Calculate coverage percentages
3. Identify missing topics
4. Assess content depth
5. Evaluate quality metrics

#### Step 3: Gap Identification
1. List topics with no content
2. List topics with insufficient content
3. Identify quality issues
4. Note missing assessments
5. Flag outdated content

#### Step 4: Priority Assignment
1. Rank gaps by importance
2. Consider WAEC exam frequency
3. Factor in student demand
4. Assess difficulty to create
5. Account for dependencies

#### Step 5: Report Generation
1. Compile coverage statistics
2. Generate gap lists
3. Create visualizations
4. Provide recommendations
5. Export actionable data

### Output Format

```json
{
  "analysis_id": "unique_id",
  "timestamp": "ISO_timestamp",
  "curriculum_standard": "NERDC|WAEC|CAP",
  "scope": {
    "subjects": [],
    "grade_levels": [],
    "total_topics": 0
  },
  "coverage_summary": {
    "overall_coverage_percent": 0.0,
    "topics_with_content": 0,
    "topics_without_content": 0,
    "topics_partial_content": 0
  },
  "by_subject": {
    "subject_name": {
      "coverage_percent": 0.0,
      "topics_total": 0,
      "topics_covered": 0,
      "average_depth_score": 0.0
    }
  },
  "by_grade_level": {
    "JSS1": {
      "coverage_percent": 0.0,
      "topics_total": 0,
      "topics_covered": 0
    }
  },
  "gaps": [
    {
      "subject": "subject_name",
      "grade_level": "level",
      "topic": "topic_name",
      "priority": "high|medium|low",
      "reason": "description"
    }
  ],
  "quality_metrics": {
    "validation_rate": 0.0,
    "average_alignment_score": 0.0,
    "content_completeness": 0.0
  },
  "recommendations": [
    {
      "action": "action_type",
      "target": "target_area",
      "priority": "high|medium|low",
      "estimated_effort": "time_estimate",
      "description": "detailed_recommendation"
    }
  ]
}
```

### Gap Prioritization Criteria

#### High Priority
- Topics in current WAEC syllabus
- Foundation topics for advanced learning
- High student demand topics
- Topics with zero content
- Critical exam topics

#### Medium Priority
- Supporting topics
- Enrichment content
- Topics with partial coverage
- Standard practice topics
- Moderate exam frequency

#### Low Priority
- Advanced optional topics
- Supplementary content
- Topics with good coverage
- Low exam frequency
- Specialized topics

### Visualization Guidelines

Create visual reports including:

1. **Coverage Heatmap**: Subject × Grade Level grid
2. **Trend Charts**: Coverage over time
3. **Priority Matrix**: Importance vs. Effort
4. **Depth Analysis**: Content density by topic
5. **Quality Dashboard**: Validation and alignment scores

### Actionable Recommendations

#### For Content Gaps
- List specific topics to create
- Suggest batch generation approach
- Estimate time and resources
- Identify dependencies
- Recommend creation order

#### For Quality Issues
- List content needing review
- Suggest validation improvements
- Recommend updates needed
- Identify alignment issues

#### For Assessment Gaps
- Specify question requirements
- Suggest test creation priorities
- Recommend question types
- Identify exam focus areas

### Best Practices

1. **Regular Analysis**: Run weekly or after major content updates
2. **Compare Standards**: Analyze across all curriculum standards
3. **Track Progress**: Monitor coverage improvement over time
4. **Focus on Quality**: Don't sacrifice quality for coverage
5. **Consider Usage**: Factor in actual student needs
6. **Update Curriculum**: Keep standards database current
7. **Validate Results**: Cross-check with curriculum documents
8. **Share Insights**: Communicate findings to content team

### Common Analysis Patterns

#### Pattern 1: Foundational Gaps
- Junior secondary topics missing
- Impacts senior secondary learning
- **Action**: Prioritize JSS1-2 content

#### Pattern 2: Exam-Critical Gaps
- High-frequency WAEC topics missing
- **Action**: Immediate content creation

#### Pattern 3: Uneven Distribution
- Some subjects well-covered, others sparse
- **Action**: Balance content creation efforts

#### Pattern 4: Depth vs. Breadth
- Many topics, shallow coverage
- **Action**: Deepen existing content before expanding

### Integration with Other Skills

- **Content Generator**: Feed gaps to content creation
- **Batch Generator**: Use for bulk content planning
- **Validator**: Ensure quality during gap filling
- **Progress Tracker**: Monitor gap resolution
- **Strategy Planner**: Input for content strategy

### Success Criteria

- Coverage increases over time
- Gaps are identified accurately
- Priorities align with student needs
- Recommendations are actionable
- Analysis informs content strategy
- Reports are clear and useful
