# Akulearn Agent Skills System

## Overview

The Akulearn Agent Skills System is a comprehensive framework for defining, managing, and executing specialized AI agent tasks across the educational platform. This system integrates with VS Code's agent capabilities to provide custom, context-aware automation for content generation, validation, deployment, and analysis tasks.

## Architecture

### Core Components

1. **Skill Definitions** (`skill_definitions.json`)
   - Registry of 15+ predefined skills
   - Structured metadata for each skill
   - Category organization
   - Workflow definitions

2. **Skill Orchestrator** (`skill_orchestrator.py`)
   - Skill execution engine
   - Context validation
   - Dependency management
   - Execution tracking and history
   - Statistics and reporting

3. **Instruction Templates** (`instructions/*.md`)
   - Detailed guidelines for each skill category
   - Best practices and quality standards
   - Output format specifications
   - Context-specific requirements

4. **CLI Interface** (`akulearn_skills.py`)
   - Command-line access to skills
   - Interactive mode
   - Workflow execution
   - History and statistics viewing

## Available Skills

### Content Generation
- **curriculum_content_generator** - Generate comprehensive lessons
- **batch_content_generator** - Bulk content creation
- **diagnostic_test_generator** - Create assessment tests
- **flashcard_generator** - Generate flashcards
- **multimedia_asset_generator** - Create visual assets
- **curriculum_expander** - Expand curriculum coverage

### Analysis & Quality
- **curriculum_coverage_analyzer** - Analyze curriculum gaps
- **content_validator** - Validate content quality
- **progress_tracker** - Track generation progress
- **content_strategy_planner** - Plan content strategy

### Deployment & Operations
- **deployment_orchestrator** - Manage deployments
- **csv_data_importer** - Import CSV data

### Content Enrichment
- **youtube_content_suggester** - Suggest video resources
- **learning_path_optimizer** - Optimize learning paths
- **exam_scraper** - Import past questions

## Usage

### Command Line

```bash
# List all skills
python src/backend/akulearn_skills.py list

# List skills by category
python src/backend/akulearn_skills.py list --category content_generation

# Show skill details
python src/backend/akulearn_skills.py show curriculum_content_generator

# Execute a skill
python src/backend/akulearn_skills.py execute curriculum_content_generator \
    --subject Mathematics \
    --grade-level SS1 \
    --topic "Quadratic Equations" \
    --curriculum NERDC

# Execute with JSON context
python src/backend/akulearn_skills.py execute curriculum_content_generator \
    --context '{"subject": "Physics", "grade_level": "SS2", "topic": "Motion"}'

# Dry run (validate without executing)
python src/backend/akulearn_skills.py execute curriculum_content_generator \
    --subject Chemistry \
    --grade-level JSS3 \
    --topic "Atoms" \
    --dry-run

# List workflows
python src/backend/akulearn_skills.py workflows

# Execute a workflow
python src/backend/akulearn_skills.py workflow complete_content_pipeline \
    --context '{"subject": "Biology", "grade_level": "SS1"}'

# View execution history
python src/backend/akulearn_skills.py history --limit 20

# View statistics
python src/backend/akulearn_skills.py stats --verbose

# Export execution log
python src/backend/akulearn_skills.py stats --export logs/execution_log.json

# Interactive mode
python src/backend/akulearn_skills.py interactive
```

### Python API

```python
from skills.skill_orchestrator import SkillOrchestrator

# Initialize orchestrator
orchestrator = SkillOrchestrator()

# List skills
skills = orchestrator.list_skills(category='content_generation')

# Get skill details
skill = orchestrator.get_skill('curriculum_content_generator')

# Execute a skill
context = {
    'subject': 'Mathematics',
    'grade_level': 'SS1',
    'topic': 'Quadratic Equations',
    'curriculum_standard': 'NERDC'
}

result = orchestrator.execute_skill('curriculum_content_generator', context)

if result.status.value == 'success':
    print(f"Success! Duration: {result.duration_seconds}s")
    print(f"Output: {result.output}")
else:
    print(f"Failed: {result.error_message}")

# Execute a workflow
results = orchestrator.execute_workflow(
    'complete_content_pipeline',
    context,
    stop_on_error=True
)

# View statistics
stats = orchestrator.get_skill_statistics()
print(f"Total executions: {stats['total_executions']}")
print(f"Success rate: {stats['success_rate']}%")
```

## Predefined Workflows

### 1. Complete Content Pipeline
End-to-end content creation workflow:
1. Analyze curriculum coverage
2. Plan content strategy
3. Generate content
4. Validate content
5. Generate multimedia assets
6. Deploy content
7. Track progress

### 2. Rapid Topic Expansion
Quick content expansion for specific topics:
1. Generate core content
2. Create flashcards
3. Generate diagnostic tests
4. Add video resources
5. Validate all content

### 3. Coverage Gap Resolution
Identify and resolve curriculum gaps:
1. Identify coverage gaps
2. Expand coverage
3. Validate expanded content
4. Track gap resolution

## Skill Categories

- **Content Generation** - Creating educational content
- **Analysis & Reporting** - Analyzing curriculum and coverage
- **Quality Assurance** - Validating content quality
- **Deployment** - Deploying content and updates
- **Data Processing** - Importing and processing data
- **Assessment** - Creating tests and assessments
- **Content Enrichment** - Enhancing with additional resources
- **Planning & Strategy** - Strategic planning
- **Data Acquisition** - Acquiring external content
- **Monitoring & Tracking** - Progress tracking
- **Optimization** - Optimizing learning experiences

## Integration with VS Code Agent

The skills system is designed to integrate with VS Code's agent capabilities:

1. **Custom Instructions**: Each skill has detailed instruction templates that can be used by Copilot
2. **Context Awareness**: Skills understand platform context and requirements
3. **Tool Mapping**: Skills map to existing Python scripts and tools
4. **Workflow Orchestration**: Complex multi-step workflows are automated
5. **Quality Standards**: Built-in validation and quality checks

## Extending the System

### Adding a New Skill

1. Add skill definition to `skill_definitions.json`:
```json
{
  "skills": {
    "your_skill_id": {
      "id": "your_skill_id",
      "name": "Your Skill Name",
      "description": "What the skill does",
      "category": "content_generation",
      "complexity": "medium",
      "required_context": ["param1", "param2"],
      "optional_context": ["param3"],
      "tools": ["your_tool.py"],
      "output_format": "json",
      "estimated_duration": "5-10 minutes",
      "dependencies": [],
      "instruction_template": "your_instructions.md"
    }
  }
}
```

2. Create instruction template in `instructions/your_instructions.md`

3. Ensure your tool script accepts context parameters as command-line arguments

### Creating a New Workflow

Add workflow definition to `skill_definitions.json`:
```json
{
  "skill_workflows": {
    "your_workflow_id": {
      "name": "Your Workflow Name",
      "description": "What the workflow accomplishes",
      "steps": [
        {
          "skill": "skill_id_1",
          "description": "What this step does"
        },
        {
          "skill": "skill_id_2",
          "description": "What this step does"
        }
      ]
    }
  }
}
```

## Best Practices

1. **Validate Context**: Always validate required parameters before execution
2. **Handle Errors**: Use try-except blocks and provide meaningful error messages
3. **Track Progress**: Update execution history and statistics
4. **Document Everything**: Keep instruction templates up to date
5. **Test Workflows**: Test complete workflows before production use
6. **Monitor Performance**: Track execution times and success rates
7. **Use Dry Runs**: Test with --dry-run before actual execution
8. **Export Logs**: Regularly export execution logs for analysis

## Troubleshooting

### Skill Not Found
- Check skill ID spelling in `skill_definitions.json`
- Ensure skill definition is properly formatted

### Context Validation Failed
- Verify all required context parameters are provided
- Check parameter names match skill definition
- Use --force to skip validation (not recommended)

### Tool Execution Failed
- Verify tool script exists and is executable
- Check tool script accepts required parameters
- Review tool script logs for specific errors

### Workflow Stops Early
- Check if stop_on_error is enabled
- Review individual skill execution results
- Use --continue-on-error for workflows that should complete despite errors

## Future Enhancements

- [ ] Web-based dashboard for skill management
- [ ] Real-time execution monitoring
- [ ] Skill scheduling and automation
- [ ] Advanced analytics and insights
- [ ] Skill version management
- [ ] Collaborative skill development
- [ ] Integration with CI/CD pipelines
- [ ] Performance optimization recommendations

## Support

For issues or questions:
1. Check execution logs and statistics
2. Review instruction templates for guidance
3. Use --verbose flag for detailed output
4. Export execution log for debugging
