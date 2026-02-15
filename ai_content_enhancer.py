#!/usr/bin/env python3
"""
AI-Powered Content Enhancement System
Uses AI services to improve, expand, and enhance educational content
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import argparse
import re
from collections import defaultdict

class AIContentEnhancer:
    """AI-powered content enhancement and improvement system"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.enhancement_history = []
        self.templates = self._load_enhancement_templates()

    def _load_enhancement_templates(self) -> Dict[str, str]:
        """Load AI enhancement templates for different improvement types"""

        return {
            'expand_content': """
You are an expert educational content creator. Expand the following {subject} content to be more comprehensive and engaging.

Original Content:
{content}

Topic: {topic}
Subject: {subject}
Content Type: {content_type}
Current Quality Score: {quality_score}/100

Please expand this content by:
1. Adding more detailed explanations
2. Including additional examples and worked solutions
3. Adding relevant diagrams or visual descriptions
4. Including common mistakes and how to avoid them
5. Adding practice questions or exercises
6. Including real-world applications, especially Nigerian context where relevant

Enhanced Content:""",

            'improve_structure': """
You are an expert educational content creator. Restructure and improve the organization of the following content.

Original Content:
{content}

Subject: {subject}
Topic: {topic}

Please restructure this content by:
1. Creating clear section headers
2. Organizing information logically (introduction → main concepts → examples → practice → summary)
3. Adding smooth transitions between sections
4. Ensuring consistent formatting and style
5. Making the content more scannable and readable

Restructured Content:""",

            'add_nigerian_context': """
You are an expert in Nigerian education and cultural context. Add relevant Nigerian examples and cultural context to the following educational content.

Original Content:
{content}

Subject: {subject}
Topic: {topic}

Please enhance this content by:
1. Adding Nigerian examples and case studies
2. Including relevant cultural references
3. Connecting concepts to Nigerian economic, social, or geographical contexts
4. Adding local applications and relevance
5. Including Nigerian examination perspectives (WAEC, NECO, JAMB)
6. Maintaining the original educational value while making it more relatable

Enhanced Content with Nigerian Context:""",

            'generate_practice_questions': """
You are an expert question writer for {subject}. Generate practice questions and exercises for the following topic.

Topic: {topic}
Subject: {subject}
Content Summary: {summary}

Please generate:
1. 5-10 multiple choice questions with explanations
2. 3-5 short answer questions
3. 2-3 essay questions
4. 1 practical/application question

Include answer keys and marking schemes where appropriate.

Practice Questions:""",

            'create_summary': """
You are an expert at creating concise educational summaries. Create a comprehensive summary of the following content.

Original Content:
{content}

Subject: {subject}
Topic: {topic}

Please create a summary that includes:
1. Key learning objectives
2. Main concepts and definitions
3. Important formulas or principles (if applicable)
4. Essential examples
5. Key takeaways and applications

Summary:""",

            'fix_errors': """
You are an expert proofreader and content validator. Review and correct the following educational content.

Original Content:
{content}

Subject: {subject}
Topic: {topic}

Please:
1. Correct any factual errors
2. Fix grammatical and spelling mistakes
3. Improve clarity and precision
4. Ensure mathematical/scientific accuracy
5. Maintain appropriate educational level

Corrected Content:""",

            'add_multimedia_suggestions': """
You are an expert in educational multimedia. Suggest multimedia elements for the following content.

Content Summary: {summary}
Subject: {subject}
Topic: {topic}

Please suggest:
1. Images, diagrams, or charts that would help explain concepts
2. Videos or animations that could demonstrate processes
3. Interactive elements or simulations
4. Audio explanations or pronunciations
5. Links to relevant online resources

Multimedia Suggestions:""",

            'generate_learning_objectives': """
You are an expert curriculum developer. Create clear, measurable learning objectives for the following content.

Content Summary: {summary}
Subject: {subject}
Topic: {topic}
Target Audience: Senior Secondary School Students (WAEC/NECO level)

Please create learning objectives that:
1. Start with action verbs (define, explain, solve, analyze, etc.)
2. Are specific and measurable
3. Cover different cognitive levels (knowledge, comprehension, application, analysis)
4. Are appropriate for the content level

Learning Objectives:"""
        }

    def enhance_content(self, content: Dict[str, Any], enhancement_type: str = 'expand_content',
                       use_ai: bool = True) -> Dict[str, Any]:
        """Enhance content using AI or rule-based methods"""

        enhancement_result = {
            'original_content': content.copy(),
            'enhancement_type': enhancement_type,
            'enhancement_timestamp': datetime.now().isoformat(),
            'enhanced_content': {},
            'improvements_made': [],
            'quality_improvement': 0,
            'ai_used': use_ai
        }

        if use_ai and self.api_key:
            enhanced_content = self._enhance_with_ai(content, enhancement_type)
        else:
            enhanced_content = self._enhance_with_rules(content, enhancement_type)

        if enhanced_content:
            enhancement_result['enhanced_content'] = enhanced_content
            enhancement_result['improvements_made'] = self._analyze_improvements(content, enhanced_content)
            enhancement_result['quality_improvement'] = self._calculate_quality_improvement(content, enhanced_content)

        return enhancement_result

    def _enhance_with_ai(self, content: Dict[str, Any], enhancement_type: str) -> Optional[Dict[str, Any]]:
        """Enhance content using AI services"""

        if not self.api_key:
            print("⚠️  No API key provided - falling back to rule-based enhancement")
            return self._enhance_with_rules(content, enhancement_type)

        try:
            # This would integrate with actual AI service (OpenAI, etc.)
            # For now, simulate AI enhancement

            template = self.templates.get(enhancement_type, self.templates['expand_content'])

            # Prepare prompt variables
            prompt_vars = {
                'content': content.get('content', ''),
                'subject': content.get('subject', 'General'),
                'topic': content.get('topic', 'General Topic'),
                'content_type': content.get('content_type', 'study_guide'),
                'summary': content.get('summary', content.get('content', '')[:200] + '...'),
                'quality_score': 75  # Would be calculated
            }

            # Format the prompt
            prompt = template.format(**prompt_vars)

            # Simulate AI response (replace with actual API call)
            ai_response = self._simulate_ai_response(prompt, enhancement_type)

            # Parse and structure the AI response
            enhanced_content = self._parse_ai_response(ai_response, content, enhancement_type)

            return enhanced_content

        except Exception as e:
            print(f"❌ AI enhancement failed: {str(e)}")
            return self._enhance_with_rules(content, enhancement_type)

    def _simulate_ai_response(self, prompt: str, enhancement_type: str) -> str:
        """Simulate AI response for development/testing"""

        # This is a placeholder - replace with actual AI API calls

        if enhancement_type == 'expand_content':
            return """
# Enhanced Content: Solving Quadratic Equations

## Introduction
Quadratic equations are polynomial equations of degree 2, written in the form ax² + bx + c = 0, where a ≠ 0. These equations are fundamental in mathematics and appear frequently in physics, engineering, and real-world problem-solving.

## Methods of Solution

### 1. Factorization Method
To solve ax² + bx + c = 0 by factorization:

**Step 1:** Ensure the equation is in standard form
**Step 2:** Factor the quadratic expression
**Step 3:** Apply the zero product property
**Step 4:** Solve the resulting linear equations

#### Worked Example 1:
Solve x² + 5x + 6 = 0

**Solution:**
x² + 5x + 6 = (x + 2)(x + 3) = 0
x + 2 = 0 or x + 3 = 0
x = -2 or x = -3

#### Worked Example 2:
Solve 2x² + 7x + 3 = 0

**Solution:**
2x² + 7x + 3 = (2x + 1)(x + 3) = 0
2x + 1 = 0 or x + 3 = 0
x = -1/2 or x = -3

### 2. Quadratic Formula
For ax² + bx + c = 0, the solutions are:
x = [-b ± √(b² - 4ac)] / 2a

#### Worked Example:
Solve x² - 4x - 5 = 0

**Solution:**
a = 1, b = -4, c = -5
x = [4 ± √(16 + 20)] / 2
x = [4 ± √36] / 2
x = [4 ± 6] / 2
x = 5 or x = -1

## Applications in Nigerian Context

### Agricultural Applications
Farmers use quadratic equations to maximize crop yields. For example, calculating optimal fertilizer quantities or irrigation schedules often involves quadratic relationships.

### Business Applications
Small business owners solve quadratic equations when determining maximum profit points or break-even analysis for their enterprises.

## Common Mistakes to Avoid

1. Forgetting that a ≠ 0 (if a = 0, it's not quadratic)
2. Incorrectly applying the zero product property
3. Making sign errors in the quadratic formula
4. Not checking solutions by substitution

## Practice Exercises

1. Solve: x² + 8x + 15 = 0
2. Solve: 3x² - x - 2 = 0
3. Find the roots of 2x² + 5x - 3 = 0
4. A farmer finds that his profit P in naira is given by P = -2n² + 120n - 100, where n is the number of bags of fertilizer. Find the number of bags that maximizes profit.

## Summary
Quadratic equations can be solved by factorization, completing the square, or the quadratic formula. Each method has its advantages, with factorization being preferred when possible. Understanding these methods is crucial for advanced mathematics and real-world applications.
"""

        elif enhancement_type == 'add_nigerian_context':
            return """
## Nigerian Context and Applications

### WAEC Examination Focus
WAEC frequently tests quadratic equations in both objective and theory questions. Students should master factorization and the quadratic formula, as these appear in Paper 1 (Objectives) and Paper 2 (Essay).

### Real-World Nigerian Examples

#### Agricultural Optimization
A cocoa farmer in Ondo State finds that his revenue R from selling cocoa is R = -0.5x² + 50x - 100, where x is the number of hectares farmed. To maximize revenue, he needs to solve the quadratic equation for the vertex.

#### Business Profit Maximization
A small-scale entrepreneur selling pure water in Lagos calculates profit using P = -2n² + 180n - 500, where n is the number of sachets sold daily. The maximum profit occurs at the vertex of this parabola.

#### Construction and Engineering
Civil engineers working on Nigerian roads use quadratic equations to calculate optimal beam designs and load distributions for bridges across the Niger River.

### Cultural Relevance
In Nigerian traditional mathematics, similar concepts appear in Islamic geometric patterns and architectural designs found in Kano and Zaria. The parabolic shapes in these designs reflect the same mathematical principles.

### Economic Applications
Central Bank of Nigeria economists use quadratic models to analyze inflation curves and economic growth patterns, helping to predict and manage economic cycles.
"""

        elif enhancement_type == 'generate_practice_questions':
            return """
## Practice Questions: Quadratic Equations

### Multiple Choice Questions

1. Solve x² + 7x + 12 = 0
   a) x = -3, -4
   b) x = 3, 4
   c) x = -3, 4
   d) x = 3, -4

2. Find the roots of 2x² - 5x - 3 = 0
   a) x = 3, -1/2
   b) x = -3, 1/2
   c) x = 3, 1/2
   d) x = -3, -1/2

3. The quadratic equation x² - 6x + 9 = 0 has:
   a) Two distinct real roots
   b) One repeated real root
   c) No real roots
   d) Complex roots

### Short Answer Questions

1. Solve by factorization: x² + 10x + 21 = 0
2. Use the quadratic formula to solve: x² - 4x - 12 = 0
3. Find the discriminant of 3x² + 2x - 1 = 0 and determine the nature of roots

### Essay Questions

1. Compare and contrast the three methods of solving quadratic equations (factorization, completing the square, quadratic formula). Give examples of when each method is most appropriate.

2. A Nigerian farmer finds that his maize yield Y is given by Y = -0.1x² + 8x + 20, where x is the amount of fertilizer in bags. Find the amount of fertilizer that maximizes yield and calculate the maximum yield.

### Practical Application

A soft drink company in Kano wants to maximize profit from selling minerals. Their profit function is P = -5n² + 300n - 1000, where n is the number of crates sold. Using calculus or completing the square, find:
a) The number of crates that maximizes profit
b) The maximum profit
c) Interpret your results in the context of Nigerian business

## Answer Key

### Multiple Choice
1. a) x = -3, -4
2. a) x = 3, -1/2
3. b) One repeated real root

### Short Answer
1. (x + 3)(x + 7) = 0 → x = -3, -7
2. x = [4 ± √(16 + 48)]/2 = [4 ± √64]/2 = [4 ± 8]/2 → x = 6, -2
3. Discriminant = 4 + 12 = 16 > 0, two distinct real roots

### Essay (Sample Answers)
1. Factorization is quickest when factors are obvious. Quadratic formula works for all equations. Completing the square shows the vertex form.

2. Vertex at x = -b/2a = -8/-0.2 = 40 bags, Maximum yield = 340 bags
"""

        else:
            return "Enhanced content would appear here based on AI processing."

    def _parse_ai_response(self, ai_response: str, original_content: Dict[str, Any],
                          enhancement_type: str) -> Dict[str, Any]:
        """Parse AI response and integrate with original content"""

        enhanced_content = original_content.copy()

        if enhancement_type == 'expand_content':
            # Replace the main content
            enhanced_content['content'] = ai_response.strip()
            enhanced_content['version'] = original_content.get('version', 1) + 1

        elif enhancement_type == 'add_nigerian_context':
            # Append Nigerian context to existing content
            original = original_content.get('content', '')
            enhanced_content['content'] = original + '\n\n' + ai_response.strip()
            enhanced_content['cultural_notes'] = ai_response.strip()

        elif enhancement_type == 'generate_practice_questions':
            # Add practice questions
            enhanced_content['practice_problems'] = ai_response.strip()

        elif enhancement_type == 'create_summary':
            enhanced_content['summary'] = ai_response.strip()

        elif enhancement_type == 'improve_structure':
            enhanced_content['content'] = ai_response.strip()

        elif enhancement_type == 'fix_errors':
            enhanced_content['content'] = ai_response.strip()

        elif enhancement_type == 'add_multimedia_suggestions':
            enhanced_content['multimedia_links'] = ai_response.strip()

        elif enhancement_type == 'generate_learning_objectives':
            enhanced_content['learning_objectives'] = ai_response.strip()

        # Update metadata
        enhanced_content['last_enhanced'] = datetime.now().isoformat()
        enhanced_content['enhancement_type'] = enhancement_type

        return enhanced_content

    def _enhance_with_rules(self, content: Dict[str, Any], enhancement_type: str) -> Dict[str, Any]:
        """Rule-based content enhancement when AI is not available"""

        enhanced_content = content.copy()

        if enhancement_type == 'expand_content':
            enhanced_content = self._rule_expand_content(content)

        elif enhancement_type == 'add_nigerian_context':
            enhanced_content = self._rule_add_nigerian_context(content)

        elif enhancement_type == 'generate_practice_questions':
            enhanced_content = self._rule_generate_questions(content)

        elif enhancement_type == 'create_summary':
            enhanced_content = self._rule_create_summary(content)

        elif enhancement_type == 'improve_structure':
            enhanced_content = self._rule_improve_structure(content)

        return enhanced_content

    def _rule_expand_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based content expansion"""

        enhanced = content.copy()
        original_content = content.get('content', '')

        # Add standard sections if missing
        expansions = []

        if '## Introduction' not in original_content and '## Intro' not in original_content:
            expansions.append("## Introduction\n\nProvide a brief overview of the topic and its importance.\n")

        if '## Key Concepts' not in original_content:
            expansions.append("## Key Concepts\n\n- Concept 1\n- Concept 2\n- Concept 3\n")

        if '## Examples' not in original_content and '## Example' not in original_content:
            expansions.append("## Examples\n\n### Example 1\n\nStep-by-step solution here.\n")

        if '## Practice' not in original_content:
            expansions.append("## Practice Questions\n\n1. Practice question 1\n2. Practice question 2\n")

        if '## Summary' not in original_content:
            expansions.append("## Summary\n\nKey takeaways and important points.\n")

        enhanced['content'] = original_content + '\n\n' + '\n\n'.join(expansions)
        return enhanced

    def _rule_add_nigerian_context(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Add Nigerian context using rules"""

        enhanced = content.copy()
        subject = content.get('subject', '').lower()

        nigerian_contexts = {
            'mathematics': """
## Nigerian Context
Mathematics is essential for various careers in Nigeria including engineering, banking, and teaching. WAEC and NECO examinations test mathematical proficiency for university admission.

### Applications in Nigerian Economy
- Agricultural optimization (crop yields, fertilizer calculations)
- Business profit maximization
- Construction and engineering calculations
- Banking and financial modeling""",

            'physics': """
## Nigerian Applications
Physics principles are applied in:
- Oil and gas industry operations
- Telecommunications infrastructure
- Renewable energy projects (solar, wind)
- Medical equipment in Nigerian hospitals
- Construction of roads and bridges""",

            'chemistry': """
## Nigerian Chemical Industry
- Petroleum refining and petrochemicals
- Pharmaceutical manufacturing
- Fertilizer production for agriculture
- Soap and detergent manufacturing
- Food processing and preservation""",

            'biology': """
## Nigerian Biological Sciences
- Tropical disease research (malaria, Ebola)
- Agricultural biotechnology
- Conservation of Nigerian wildlife
- Public health and epidemiology
- Environmental impact studies"""
        }

        context = nigerian_contexts.get(subject, """
## Nigerian Educational Context
This topic is part of the Nigerian secondary school curriculum and is tested in WAEC, NECO, and JAMB examinations. Understanding these concepts is essential for higher education and career opportunities in Nigeria.""")

        enhanced['content'] = content.get('content', '') + '\n\n' + context
        enhanced['cultural_notes'] = context

        return enhanced

    def _rule_generate_questions(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate practice questions using rules"""

        enhanced = content.copy()
        subject = content.get('subject', '').lower()
        topic = content.get('topic', '').lower()

        # Generic question templates
        question_templates = {
            'mathematics': [
                f"What is the solution to a basic {topic} problem?",
                f"Explain the steps to solve {topic} equations.",
                f"Find the value of x in this {topic} equation.",
                f"Calculate the {topic} for the following values."
            ],
            'physics': [
                f"Explain how {topic} works in real-world applications.",
                f"Calculate the {topic} given these values.",
                f"What are the units for {topic}?",
                f"Describe an experiment demonstrating {topic}."
            ],
            'chemistry': [
                f"What happens during {topic} reactions?",
                f"Write the balanced equation for {topic}.",
                f"Explain the properties of {topic}.",
                f"Describe the laboratory procedure for {topic}."
            ],
            'biology': [
                f"Explain the process of {topic} in organisms.",
                f"What are the main components of {topic}?",
                f"Describe how {topic} affects living systems.",
                f"Compare {topic} in different organisms."
            ]
        }

        questions = question_templates.get(subject, [
            f"What are the key concepts in {topic}?",
            f"Explain {topic} in your own words.",
            f"What are some examples of {topic}?",
            f"Why is {topic} important?"
        ])

        enhanced['practice_problems'] = '\n'.join(f"{i+1}. {q}" for i, q in enumerate(questions))
        return enhanced

    def _rule_create_summary(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary using rules"""

        enhanced = content.copy()
        content_text = content.get('content', '')

        # Extract key sentences (simple rule-based approach)
        sentences = re.split(r'[.!?]+', content_text)
        key_sentences = []

        for sentence in sentences[:10]:  # First 10 sentences
            sentence = sentence.strip()
            if len(sentence) > 20 and not sentence.startswith('#'):
                key_sentences.append(sentence)

        summary = ' '.join(key_sentences[:3]) if key_sentences else "Summary of key concepts and applications."

        enhanced['summary'] = summary
        return enhanced

    def _rule_improve_structure(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Improve content structure using rules"""

        enhanced = content.copy()
        content_text = content.get('content', '')

        # Add basic structure if missing
        if not content_text.startswith('#'):
            content_text = f"# {content.get('title', 'Content')}\n\n{content_text}"

        # Ensure sections are properly formatted
        sections_to_add = ['## Introduction', '## Main Content', '## Examples', '## Summary']

        for section in sections_to_add:
            if section not in content_text:
                content_text += f"\n\n{section}\n\nContent for {section.lower()} section."

        enhanced['content'] = content_text
        return enhanced

    def _analyze_improvements(self, original: Dict[str, Any], enhanced: Dict[str, Any]) -> List[str]:
        """Analyze what improvements were made"""

        improvements = []

        # Content length
        orig_len = len(original.get('content', ''))
        enh_len = len(enhanced.get('content', ''))

        if enh_len > orig_len * 1.5:
            improvements.append("Content significantly expanded")
        elif enh_len > orig_len * 1.2:
            improvements.append("Content moderately expanded")

        # New fields added
        new_fields = set(enhanced.keys()) - set(original.keys())
        if new_fields:
            improvements.append(f"Added fields: {', '.join(new_fields)}")

        # Structure improvements
        if '##' in enhanced.get('content', '') and '##' not in original.get('content', ''):
            improvements.append("Added structured sections")

        # Nigerian context
        if 'cultural_notes' in enhanced and 'cultural_notes' not in original:
            improvements.append("Added cultural/Nigerian context")

        return improvements

    def _calculate_quality_improvement(self, original: Dict[str, Any], enhanced: Dict[str, Any]) -> int:
        """Calculate quality improvement score"""

        improvement_score = 0

        # Length improvement
        orig_len = len(original.get('content', ''))
        enh_len = len(enhanced.get('content', ''))

        if enh_len > orig_len:
            improvement_score += min(20, (enh_len - orig_len) // 50)

        # Structure improvement
        orig_sections = original.get('content', '').count('##')
        enh_sections = enhanced.get('content', '').count('##')

        if enh_sections > orig_sections:
            improvement_score += (enh_sections - orig_sections) * 5

        # New metadata
        new_fields = set(enhanced.keys()) - set(original.keys())
        improvement_score += len(new_fields) * 3

        # Nigerian context
        if 'cultural_notes' in enhanced and not original.get('cultural_notes'):
            improvement_score += 10

        return min(50, improvement_score)  # Cap at 50 points

    def batch_enhance_content(self, content_list: List[Dict[str, Any]],
                            enhancement_types: List[str] = None,
                            use_ai: bool = True) -> Dict[str, Any]:
        """Batch enhance multiple content items"""

        if not enhancement_types:
            enhancement_types = ['expand_content', 'add_nigerian_context']

        batch_results = {
            'batch_timestamp': datetime.now().isoformat(),
            'total_items': len(content_list),
            'enhancement_types': enhancement_types,
            'ai_used': use_ai,
            'results': [],
            'summary': {
                'successful_enhancements': 0,
                'failed_enhancements': 0,
                'average_quality_improvement': 0,
                'total_improvements_made': 0
            }
        }

        total_quality_improvement = 0

        for i, content in enumerate(content_list):
            print(f"Enhancing content {i+1}/{len(content_list)}: {content.get('title', 'Untitled')}")

            item_results = []

            for enhancement_type in enhancement_types:
                try:
                    result = self.enhance_content(content, enhancement_type, use_ai)
                    item_results.append(result)

                    if result.get('enhanced_content'):
                        batch_results['summary']['successful_enhancements'] += 1
                        total_quality_improvement += result.get('quality_improvement', 0)
                    else:
                        batch_results['summary']['failed_enhancements'] += 1

                except Exception as e:
                    print(f"❌ Enhancement failed for {enhancement_type}: {str(e)}")
                    batch_results['summary']['failed_enhancements'] += 1

            batch_results['results'].append({
                'original_content_id': content.get('id', f'item_{i+1}'),
                'title': content.get('title', 'Untitled'),
                'enhancement_results': item_results
            })

        # Calculate averages
        successful = batch_results['summary']['successful_enhancements']
        if successful > 0:
            batch_results['summary']['average_quality_improvement'] = total_quality_improvement / successful

        return batch_results

def main():
    """Command-line interface for AI content enhancement"""

    enhancer = AIContentEnhancer()

    parser = argparse.ArgumentParser(description='AI-Powered Content Enhancement System')
    parser.add_argument('--enhance-file', type=str, help='Enhance single content file (JSON)')
    parser.add_argument('--batch-enhance', type=str, help='Batch enhance content from JSON file')
    parser.add_argument('--enhancement-type', type=str, default='expand_content',
                       choices=['expand_content', 'improve_structure', 'add_nigerian_context',
                               'generate_practice_questions', 'create_summary', 'fix_errors',
                               'add_multimedia_suggestions', 'generate_learning_objectives'],
                       help='Type of enhancement to apply')
    parser.add_argument('--enhancement-types', type=str, help='Comma-separated list of enhancement types for batch processing')
    parser.add_argument('--no-ai', action='store_true', help='Use rule-based enhancement instead of AI')
    parser.add_argument('--output-file', type=str, help='Output file for enhancement results')

    args = parser.parse_args()

    if args.enhance_file:
        # Enhance single file
        if not os.path.exists(args.enhance_file):
            print(f"❌ File not found: {args.enhance_file}")
            return

        with open(args.enhance_file, 'r', encoding='utf-8') as f:
            content = json.load(f)

        print(f"🔄 Enhancing content: {content.get('title', 'Untitled')}")
        print(f"📋 Enhancement type: {args.enhancement_type}")

        result = enhancer.enhance_content(content, args.enhancement_type, not args.no_ai)

        if result.get('enhanced_content'):
            print("✅ Enhancement successful!"            print(f"📊 Quality improvement: +{result['quality_improvement']} points")
            print(f"🔧 Improvements made: {', '.join(result['improvements_made'])}")

            # Save result
            output_file = args.output_file or f"enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 Enhanced content saved to: {output_file}")

        else:
            print("❌ Enhancement failed")

    elif args.batch_enhance:
        # Batch enhance
        if not os.path.exists(args.batch_enhance):
            print(f"❌ File not found: {args.batch_enhance}")
            return

        with open(args.batch_enhance, 'r', encoding='utf-8') as f:
            content_list = json.load(f)

        if not isinstance(content_list, list):
            print("❌ Batch enhancement file must contain a list of content items")
            return

        # Parse enhancement types
        if args.enhancement_types:
            enhancement_types = [t.strip() for t in args.enhancement_types.split(',')]
        else:
            enhancement_types = [args.enhancement_type]

        print(f"🔄 Batch enhancing {len(content_list)} content items")
        print(f"📋 Enhancement types: {', '.join(enhancement_types)}")
        print(f"🤖 AI enabled: {not args.no_ai}")

        results = enhancer.batch_enhance_content(content_list, enhancement_types, not args.no_ai)

        print("📊 Batch Enhancement Summary:"        print(f"📁 Total items: {results['summary']['total_items']}")
        print(f"✅ Successful: {results['summary']['successful_enhancements']}")
        print(f"❌ Failed: {results['summary']['failed_enhancements']}")
        print(f"📊 Avg quality improvement: {results['summary']['average_quality_improvement']:.1f} points")

        # Save results
        output_file = args.output_file or f"batch_enhancement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"💾 Batch results saved to: {output_file}")

    else:
        # Interactive mode
        print("🤖 AI-Powered Content Enhancement System")
        print("=" * 50)

        while True:
            print("\nOptions:")
            print("1. Enhance single content file")
            print("2. Batch enhance content files")
            print("3. Exit")

            choice = input("\nSelect option (1-3): ").strip()

            if choice == "1":
                file_path = input("Content file path (JSON): ").strip()
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)

                    print(f"Available enhancement types:")
                    types = ['expand_content', 'improve_structure', 'add_nigerian_context',
                            'generate_practice_questions', 'create_summary', 'fix_errors',
                            'add_multimedia_suggestions', 'generate_learning_objectives']

                    for i, t in enumerate(types, 1):
                        print(f"{i}. {t}")

                    type_choice = input("Select enhancement type (number): ").strip()
                    try:
                        enhancement_type = types[int(type_choice) - 1]
                        use_ai = input("Use AI enhancement? (y/n): ").strip().lower() == 'y'

                        result = enhancer.enhance_content(content, enhancement_type, use_ai)

                        if result.get('enhanced_content'):
                            print("✅ Enhancement successful!")
                            output_file = input("Save to file (or press Enter for default): ").strip()
                            if not output_file:
                                output_file = f"enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

                            with open(output_file, 'w', encoding='utf-8') as f:
                                json.dump(result, f, indent=2, ensure_ascii=False)
                            print(f"💾 Saved to: {output_file}")
                        else:
                            print("❌ Enhancement failed")

                    except (ValueError, IndexError):
                        print("❌ Invalid selection")
                else:
                    print("❌ File not found")

            elif choice == "2":
                file_path = input("Batch content file path (JSON array): ").strip()
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_list = json.load(f)

                    if isinstance(content_list, list):
                        enhancement_types = input("Enhancement types (comma-separated, or Enter for defaults): ").strip()
                        if not enhancement_types:
                            enhancement_types = ['expand_content', 'add_nigerian_context']
                        else:
                            enhancement_types = [t.strip() for t in enhancement_types.split(',')]

                        use_ai = input("Use AI enhancement? (y/n): ").strip().lower() == 'y'

                        results = enhancer.batch_enhance_content(content_list, enhancement_types, use_ai)
                        print(f"📊 Enhanced {len(content_list)} items successfully")

                        output_file = input("Save batch results to file (or press Enter for default): ").strip()
                        if not output_file:
                            output_file = f"batch_enhancement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(results, f, indent=2, ensure_ascii=False)
                        print(f"💾 Saved to: {output_file}")
                    else:
                        print("❌ File must contain a JSON array")
                else:
                    print("❌ File not found")

            elif choice == "3":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid option")

if __name__ == "__main__":
    main()