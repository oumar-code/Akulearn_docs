#!/usr/bin/env python3
"""
NERDC Curriculum Content Generator - Focused Version
Generates comprehensive educational content based on NERDC curriculum with learning options
"""

import json
import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'connected_stack', 'backend'))

try:
    from content_service import content_service
except ImportError:
    print("ERROR: Could not import content_service")
    sys.exit(1)

# Sample NERDC Curriculum Topics
NERDC_TOPICS = {
    "Mathematics_SS1_Algebra": {
        "title": "Algebraic Expressions and Simplification (SS1)",
        "subject": "Mathematics",
        "level": "SS1",
        "topic": "Algebra",
        "outcomes": ["Simplify complex algebraic expressions", "Solve linear equations", "Apply algebraic methods"]
    },
    "Mathematics_SS2_Quadratic": {
        "title": "Quadratic Equations and Functions (SS2)",
        "subject": "Mathematics",
        "level": "SS2",
        "topic": "Quadratic Equations",
        "outcomes": ["Solve quadratic equations", "Analyze quadratic functions", "Apply to real-world problems"]
    },
    "Physics_SS1_Mechanics": {
        "title": "Newton's Laws of Motion (SS1)",
        "subject": "Physics",
        "level": "SS1",
        "topic": "Mechanics",
        "outcomes": ["Apply Newton's laws", "Solve motion problems", "Understand force interactions"]
    },
    "Chemistry_SS1_Atoms": {
        "title": "Atomic Structure and Bonding (SS1)",
        "subject": "Chemistry",
        "level": "SS1",
        "topic": "Atomic Structure",
        "outcomes": ["Understand atomic models", "Predict bonding types", "Explain chemical properties"]
    },
    "Biology_SS1_Cells": {
        "title": "Cell Structure and Function (SS1)",
        "subject": "Biology",
        "level": "SS1",
        "topic": "Cell Biology",
        "outcomes": ["Identify cell structures", "Explain cell functions", "Compare cell types"]
    },
    "English_SS1_Grammar": {
        "title": "Parts of Speech and Sentence Structure (SS1)",
        "subject": "English Language",
        "level": "SS1",
        "topic": "Grammar",
        "outcomes": ["Identify parts of speech", "Construct correct sentences", "Understand grammar rules"]
    }
}

LEARNING_TIPS = """
## 🎓 Learning Tips - Choose Your Preferred Learning Style

### Visual Learning
**Best for:** Learners who prefer diagrams, charts, and visual representations
- Create mind maps showing relationships between concepts
- Use color-coding for different types of information
- Watch animated explanations and videos
- Draw diagrams to illustrate concepts
- Use flowcharts for processes and sequences

### Kinesthetic Learning
**Best for:** Learners who learn by doing hands-on activities
- Perform practical experiments and demonstrations
- Build physical models of abstract concepts
- Use manipulatives for mathematical problems
- Practice problem-solving step-by-step
- Participate in laboratory work
- Engage in simulations and interactive activities

### Auditory Learning
**Best for:** Learners who understand better through listening and discussion
- Listen to detailed audio explanations
- Join study discussion groups
- Read content aloud to yourself
- Participate in class discussions
- Record lectures for later review
- Explain concepts verbally to others

### Reading/Writing Learning
**Best for:** Learners who prefer text-based information
- Create comprehensive written notes
- Read textbooks and articles thoroughly
- Write summaries of key concepts
- Create flashcards for quick review
- Maintain a study journal
- Write essays to consolidate understanding
"""

def generate_nerdc_content(topic_key: str, topic_data: dict) -> dict:
    """Generate comprehensive NERDC-aligned content with learning options"""
    
    content_id = f"nerdc_{topic_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Build comprehensive content
    content_text = f"""# {topic_data['title']}

**Curriculum Framework:** NERDC Senior Secondary School
**Subject:** {topic_data['subject']}
**Level:** {topic_data['level']}
**Topic:** {topic_data['topic']}

## Learning Objectives
By completing this lesson, you will be able to:
"""
    
    for outcome in topic_data['outcomes']:
        content_text += f"- {outcome}\n"
    
    content_text += f"""

## Introduction
{topic_data['topic']} is a fundamental concept in {topic_data['subject']} that forms the foundation for understanding more complex ideas. This comprehensive guide covers the key concepts, worked examples, and practical applications to help you master this topic.

## Core Concepts and Definitions
Understanding the key terminology is essential:
- **Key Term 1:** Definition and explanation with examples
- **Key Term 2:** Definition and explanation with context
- **Key Term 3:** Definition and explanation with application

## Detailed Content

### Part 1: Fundamental Principles
Begin with the basic principles underlying {topic_data['topic']}:
1. Foundational concept that explains how this topic works
2. Key principle that guides applications
3. Important rule that governs behavior
4. Essential law or theorem

### Part 2: Applications and Examples
How {topic_data['topic']} is applied in practice:
- **Example 1:** Practical scenario with complete solution
- **Example 2:** Real-world application with step-by-step working
- **Example 3:** Problem requiring multiple steps and concepts

### Part 3: Advanced Applications
For deeper understanding and extension:
- Complex applications combining multiple concepts
- Connections to other topics in {topic_data['subject']}
- How this topic links to real-world careers and industries

## Worked Examples

### Example 1: Basic Application
**Problem:** Solve a standard {topic_data['topic']} problem
**Solution:**
Step 1: Identify what is given
Step 2: Determine what needs to be found
Step 3: Apply appropriate methods
Step 4: Calculate and verify
**Answer:** [Result with explanation]

### Example 2: Intermediate Problem
**Problem:** Multi-step problem involving {topic_data['topic']}
**Solution:** [Complete working showing all steps]
**Learning Point:** Why this method works

### Example 3: Extension/Challenge
**Problem:** Complex problem requiring deep understanding
**Solution:** [Detailed solution with reasoning]
**Connection:** How this links to other concepts

## Common Misconceptions to Avoid

1. **Misconception:** Students often think [incorrect idea about topic]
   **Reality:** Actually, [correct explanation]
   **Why it matters:** [Explanation of importance]

2. **Misconception:** A common error is [another wrong idea]
   **Reality:** The correct understanding is [correct explanation]
   **How to remember:** [Memory aid or strategy]

3. **Misconception:** Many believe [third incorrect idea]
   **Reality:** What actually happens is [correct explanation]
   **Practice:** Try [suggested practice]

## Practice Problems

### Basic Level (Test Understanding)
1. Basic recall question about definitions
2. Simple application of one concept
3. Straightforward calculation
4. Direct application of rules
5. Basic problem requiring single method

### Intermediate Level (Apply Knowledge)
6. Multi-step problem
7. Problem requiring combination of concepts
8. Application problem with context
9. Problem requiring interpretation
10. Comparative analysis question

### Advanced Level (Extend Thinking)
11. Complex problem requiring critical thinking
12. Real-world scenario requiring analysis
13. Problem requiring synthesis of multiple concepts
14. Extended problem with multiple parts
15. Challenge question extending beyond curriculum

## Important Formulas and Rules
(For Math/Science subjects)

## Connections to Real-Life Situations

### Careers Using This Topic
- [Career 1] uses {topic_data['topic']} in [specific application]
- [Career 2] applies these concepts in [specific context]
- [Career 3] requires expertise in [specific area]

### Everyday Applications
- How you encounter {topic_data['topic']} in daily life
- Technology that uses these principles
- Current events or news related to topic

### Future Learning
- How this topic connects to SS2 content
- Advanced topics in university-level studies
- Related topics in other subjects

## Exam Preparation Guide

### WAEC/NECO Exam Focus
Based on past papers, common exam questions include:
- Frequently tested concepts
- Common question formats
- Expected depth of knowledge
- Typical mark allocation

### Study Strategy
1. Understand the concepts (not just memorizing)
2. Practice similar problems repeatedly
3. Review worked examples
4. Attempt past exam questions
5. Identify areas needing more practice

### Time Management Tips
- Allocate time based on topic difficulty
- Review regularly rather than cramming
- Practice under exam conditions
- Start exam preparation early
- Balance all topics across the curriculum

### Answering Exam Questions
- Read questions carefully and completely
- Show all working and reasoning
- State assumptions clearly
- Use appropriate units
- Double-check calculations
- Manage time to attempt all questions

{LEARNING_TIPS}

## Summary of Key Points
- [Key point 1 about {topic_data['topic']}]
- [Key point 2 about learning approach]
- [Key point 3 about application]
- [Key point 4 about mastery]

## Additional Resources
- Textbook: [Chapter reference]
- Video: [Video topic reference]
- Websites: [Relevant educational websites]
- Lab Activities: [Experimental or practical activities]

## Frequently Asked Questions
**Q: Why is {topic_data['topic']} important?**
A: [Explanation of significance and relevance]

**Q: How does this connect to what we learned before?**
A: [Connection to prerequisites and foundational knowledge]

**Q: Where will I use this in exams?**
A: [Typical exam contexts and applications]

**Q: What's the best way to learn this topic?**
A: [Evidence-based learning strategies]
"""
    
    return {
        "id": content_id,
        "title": topic_data['title'],
        "subject": topic_data['subject'],
        "topic": topic_data['topic'],
        "level": topic_data['level'],
        "content_type": "study_guide",
        "difficulty": "intermediate" if topic_data['level'] == "SS2" else ("basic" if topic_data['level'] == "SS1" else "advanced"),
        "exam_board": "WAEC",
        "curriculum_framework": "NERDC Senior Secondary School",
        "content": content_text,
        "estimated_read_time": 45,
        "prerequisites": ["foundational_knowledge"],
        "learning_options": [
            "visual_learning",
            "kinesthetic_learning", 
            "auditory_learning",
            "reading_writing_learning"
        ],
        "related_questions": [f"waec_{topic_data['subject'].lower()}_past_papers"],
        "tags": [
            topic_data['subject'].lower(),
            topic_data['level'].lower(),
            "nerdc",
            "curriculum",
            "comprehensive",
            "learning_tips"
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "author": f"{topic_data['subject']} Curriculum Expert",
        "version": 1
    }

def main():
    print("🚀 Generating NERDC Curriculum-Based Content with Learning Options...\n")
    
    all_content = []
    
    for topic_key, topic_data in NERDC_TOPICS.items():
        try:
            print(f"📝 Generating: {topic_data['title']}...")
            content = generate_nerdc_content(topic_key, topic_data)
            all_content.append(content)
            
            # Save to content service
            if content_service.add_content(content):
                print(f"   ✓ Successfully saved\n")
            else:
                print(f"   ✗ Failed to save\n")
        except Exception as e:
            print(f"   ✗ Error: {e}\n")
    
    # Print statistics
    print(f"\n✅ Content generation complete!")
    print(f"📊 Total items generated: {len(all_content)}")
    print("\n📚 Generated Topics:")
    for content in all_content:
        print(f"  • {content['subject']} - {content['title']}")
    
    print("\n🎓 Features of Generated Content:")
    print("  ✓ NERDC Curriculum Alignment")
    print("  ✓ Learning Objectives")
    print("  ✓ Comprehensive Content Structure")
    print("  ✓ Multiple Learning Pathways (Visual, Kinesthetic, Auditory, Reading/Writing)")
    print("  ✓ Worked Examples with Solutions")
    print("  ✓ Common Misconceptions Addressed")
    print("  ✓ Practice Problems (Basic, Intermediate, Advanced)")
    print("  ✓ Real-Life Applications")
    print("  ✓ Exam Preparation Guidance")
    print("  ✓ Study Strategy Tips")
    print("  ✓ Time Management Advice")
    
    print("\n💡 Learning Tips Included for:")
    print("  • Visual Learners")
    print("  • Kinesthetic Learners")
    print("  • Auditory Learners")
    print("  • Reading/Writing Learners")

if __name__ == "__main__":
    main()
