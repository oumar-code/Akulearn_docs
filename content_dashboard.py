#!/usr/bin/env python3
"""
Content Management Dashboard
Comprehensive overview and management of the content creation pipeline
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import argparse
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import pandas as pd

class ContentManagementDashboard:
    """Comprehensive content management and analytics dashboard"""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.content_dir = os.path.join(self.workspace_path, "content")
        self.reports_dir = os.path.join(self.workspace_path, "reports")
        self.templates_dir = os.path.join(self.workspace_path, "content_templates")
        self.imports_dir = os.path.join(self.workspace_path, "content_imports")

        # Create directories if they don't exist
        for dir_path in [self.content_dir, self.reports_dir, self.templates_dir, self.imports_dir]:
            os.makedirs(dir_path, exist_ok=True)

        self.content_database = self._load_content_database()

    def _load_content_database(self) -> List[Dict[str, Any]]:
        """Load all content from various sources"""

        content_items = []

        # Load from content directory
        if os.path.exists(self.content_dir):
            for file in os.listdir(self.content_dir):
                if file.endswith('.json'):
                    try:
                        with open(os.path.join(self.content_dir, file), 'r', encoding='utf-8') as f:
                            content = json.load(f)
                            if isinstance(content, dict):
                                content_items.append(content)
                            elif isinstance(content, list):
                                content_items.extend(content)
                    except Exception as e:
                        print(f"Warning: Could not load {file}: {e}")

        # Load from sample content files
        sample_files = ['content_data.json', 'sample_content.json', 'test_content.json']
        for sample_file in sample_files:
            if os.path.exists(sample_file):
                try:
                    with open(sample_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            content_items.extend(data)
                        elif isinstance(data, dict) and 'content' in data:
                            content_items.append(data)
                except Exception as e:
                    print(f"Warning: Could not load {sample_file}: {e}")

        return content_items

    def generate_comprehensive_report(self, output_file: str = None) -> Dict[str, Any]:
        """Generate a comprehensive content management report"""

        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(self.reports_dir, f'content_dashboard_report_{timestamp}.json')

        report = {
            'report_timestamp': datetime.now().isoformat(),
            'content_overview': self._analyze_content_overview(),
            'quality_metrics': self._analyze_quality_metrics(),
            'subject_distribution': self._analyze_subject_distribution(),
            'content_gaps': self._identify_content_gaps(),
            'recent_activity': self._analyze_recent_activity(),
            'recommendations': self._generate_recommendations(),
            'performance_indicators': self._calculate_performance_indicators()
        }

        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"📊 Comprehensive report generated: {output_file}")
        return report

    def _analyze_content_overview(self) -> Dict[str, Any]:
        """Analyze overall content statistics"""

        total_content = len(self.content_database)
        content_types = Counter(item.get('content_type', 'unknown') for item in self.content_database)
        subjects = Counter(item.get('subject', 'unknown') for item in self.content_database)
        difficulty_levels = Counter(item.get('difficulty', 'unknown') for item in self.content_database)

        # Content length statistics
        content_lengths = [len(item.get('content', '')) for item in self.content_database if item.get('content')]
        avg_length = sum(content_lengths) / len(content_lengths) if content_lengths else 0

        # Creation methods
        creation_methods = Counter(item.get('creation_method', 'unknown') for item in self.content_database)

        return {
            'total_content_items': total_content,
            'content_types': dict(content_types),
            'subjects': dict(subjects),
            'difficulty_distribution': dict(difficulty_levels),
            'average_content_length': round(avg_length, 2),
            'creation_methods': dict(creation_methods),
            'content_with_summaries': sum(1 for item in self.content_database if item.get('summary')),
            'content_with_examples': sum(1 for item in self.content_database if item.get('worked_examples') or item.get('practice_problems')),
            'content_with_nigerian_context': sum(1 for item in self.content_database if item.get('cultural_notes'))
        }

    def _analyze_quality_metrics(self) -> Dict[str, Any]:
        """Analyze content quality metrics"""

        quality_scores = []

        for item in self.content_database:
            # Simple quality scoring based on available fields
            score = 0
            max_score = 100

            # Required fields (40 points)
            required_fields = ['title', 'subject', 'topic', 'content', 'content_type']
            filled_required = sum(1 for field in required_fields if item.get(field))
            score += (filled_required / len(required_fields)) * 40

            # Optional fields (40 points)
            optional_fields = ['summary', 'learning_objectives', 'key_concepts', 'worked_examples',
                             'practice_problems', 'exam_tips', 'prerequisites']
            filled_optional = sum(1 for field in optional_fields if item.get(field))
            score += (filled_optional / len(optional_fields)) * 40

            # Nigerian context (10 points)
            content_text = item.get('content', '')
            if isinstance(content_text, list):
                content_text = ' '.join(str(x) for x in content_text)
            if item.get('cultural_notes') or 'nigeria' in content_text.lower():
                score += 10

            # Content length appropriateness (10 points)
            if isinstance(content_text, str):
                content_length = len(content_text)
            else:
                content_length = 0
            content_type = item.get('content_type', 'study_guide')

            if content_type == 'summary' and 100 <= content_length <= 1000:
                score += 10
            elif content_type == 'reference' and 200 <= content_length <= 2500:
                score += 10
            elif content_type in ['study_guide', 'tutorial'] and 500 <= content_length <= 5000:
                score += 10
            elif content_length > 100:  # Generic minimum
                score += 5

            quality_scores.append(min(100, score))

        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

        # Quality distribution
        quality_distribution = {
            'excellent': sum(1 for s in quality_scores if s >= 80),
            'good': sum(1 for s in quality_scores if 60 <= s < 80),
            'fair': sum(1 for s in quality_scores if 40 <= s < 60),
            'poor': sum(1 for s in quality_scores if s < 40)
        }

        return {
            'average_quality_score': round(avg_quality, 2),
            'quality_distribution': quality_distribution,
            'highest_quality_score': max(quality_scores) if quality_scores else 0,
            'lowest_quality_score': min(quality_scores) if quality_scores else 0,
            'quality_variance': round(sum((x - avg_quality) ** 2 for x in quality_scores) / len(quality_scores), 2) if quality_scores else 0
        }

    def _analyze_subject_distribution(self) -> Dict[str, Any]:
        """Analyze content distribution across subjects"""

        subject_stats = defaultdict(lambda: {
            'total': 0,
            'by_type': defaultdict(int),
            'by_difficulty': defaultdict(int),
            'average_quality': 0,
            'topics_covered': set()
        })

        for item in self.content_database:
            subject = item.get('subject', 'Unknown')
            subject_stats[subject]['total'] += 1
            subject_stats[subject]['by_type'][item.get('content_type', 'unknown')] += 1
            subject_stats[subject]['by_difficulty'][item.get('difficulty', 'unknown')] += 1
            subject_stats[subject]['topics_covered'].add(item.get('topic', 'unknown'))

        # Calculate average quality per subject
        for subject in subject_stats:
            subject_items = [item for item in self.content_database if item.get('subject') == subject]
            if subject_items:
                # Simple quality calculation
                avg_quality = sum(len(item.get('content', '')) > 200 for item in subject_items) / len(subject_items) * 100
                subject_stats[subject]['average_quality'] = round(avg_quality, 2)

            # Convert set to list for JSON serialization
            subject_stats[subject]['topics_covered'] = list(subject_stats[subject]['topics_covered'])
            subject_stats[subject]['by_type'] = dict(subject_stats[subject]['by_type'])
            subject_stats[subject]['by_difficulty'] = dict(subject_stats[subject]['by_difficulty'])

        return dict(subject_stats)

    def _identify_content_gaps(self) -> Dict[str, Any]:
        """Identify gaps in content coverage"""

        gaps = {
            'missing_subjects': [],
            'underrepresented_topics': [],
            'missing_difficulty_levels': [],
            'content_type_gaps': [],
            'quality_gaps': []
        }

        # Expected subjects for Nigerian curriculum
        expected_subjects = ['Mathematics', 'English', 'Physics', 'Chemistry', 'Biology',
                           'Geography', 'Economics', 'History', 'Literature', 'Computer Science']

        current_subjects = set(item.get('subject', '').title() for item in self.content_database)
        gaps['missing_subjects'] = [s for s in expected_subjects if s not in current_subjects]

        # Check topic coverage per subject
        subject_topics = defaultdict(set)
        for item in self.content_database:
            subject = item.get('subject', '').title()
            topic = item.get('topic', '')
            if topic:
                subject_topics[subject].add(topic)

        # Expected topics for key subjects (simplified)
        expected_topics = {
            'Mathematics': ['Algebra', 'Geometry', 'Trigonometry', 'Calculus', 'Statistics'],
            'Physics': ['Mechanics', 'Electricity', 'Magnetism', 'Optics', 'Thermodynamics'],
            'Chemistry': ['Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry', 'Biochemistry'],
            'Biology': ['Cell Biology', 'Genetics', 'Ecology', 'Human Physiology', 'Evolution']
        }

        for subject, expected in expected_topics.items():
            covered = subject_topics.get(subject, set())
            missing = [t for t in expected if t not in covered]
            if missing:
                gaps['underrepresented_topics'].append({
                    'subject': subject,
                    'missing_topics': missing,
                    'coverage_percentage': len(covered) / len(expected) * 100
                })

        # Difficulty distribution
        difficulties = Counter(item.get('difficulty', 'unknown') for item in self.content_database)
        if difficulties.get('advanced', 0) < difficulties.get('basic', 0) * 0.3:
            gaps['missing_difficulty_levels'].append('Advanced level content underrepresented')

        # Content type balance
        content_types = Counter(item.get('content_type', 'unknown') for item in self.content_database)
        if content_types.get('exercise', 0) < content_types.get('study_guide', 0) * 0.2:
            gaps['content_type_gaps'].append('Need more practice exercises and quizzes')

        return gaps

    def _analyze_recent_activity(self) -> Dict[str, Any]:
        """Analyze recent content creation and modification activity"""

        # Since we don't have actual timestamps, simulate based on file modification times
        recent_files = []

        for root, dirs, files in os.walk(self.workspace_path):
            for file in files:
                if file.endswith('.json') and any(keyword in file for keyword in ['content', 'sample', 'test']):
                    file_path = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(file_path)
                        recent_files.append({
                            'file': file,
                            'modified': datetime.fromtimestamp(mtime).isoformat(),
                            'age_days': (datetime.now() - datetime.fromtimestamp(mtime)).days
                        })
                    except:
                        pass

        # Sort by modification time
        recent_files.sort(key=lambda x: x['modified'], reverse=True)

        # Activity summary
        activity = {
            'recent_files': recent_files[:10],  # Last 10 modified files
            'files_modified_today': sum(1 for f in recent_files if f['age_days'] == 0),
            'files_modified_this_week': sum(1 for f in recent_files if f['age_days'] <= 7),
            'files_modified_this_month': sum(1 for f in recent_files if f['age_days'] <= 30)
        }

        return activity

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on analysis"""

        recommendations = []

        overview = self._analyze_content_overview()
        quality = self._analyze_quality_metrics()
        gaps = self._identify_content_gaps()

        # Content volume recommendations
        if overview['total_content_items'] < 100:
            recommendations.append("Focus on expanding content volume - aim for at least 500 comprehensive content items")

        # Quality recommendations
        if quality['average_quality_score'] < 70:
            recommendations.append("Prioritize content quality improvement - use AI enhancement and validation tools")

        # Subject balance recommendations
        subject_dist = overview['subjects']
        total_items = overview['total_content_items']
        for subject, count in subject_dist.items():
            if subject != 'unknown' and count / total_items < 0.05:  # Less than 5%
                recommendations.append(f"Increase coverage for {subject} - currently underrepresented")

        # Gap-based recommendations
        if gaps['missing_subjects']:
            recommendations.append(f"Add content for missing subjects: {', '.join(gaps['missing_subjects'])}")

        if gaps['underrepresented_topics']:
            for gap in gaps['underrepresented_topics'][:3]:  # Top 3
                recommendations.append(f"Add topics for {gap['subject']}: {', '.join(gap['missing_topics'])}")

        # Nigerian context recommendations
        nigerian_context_pct = overview['content_with_nigerian_context'] / overview['total_content_items'] * 100
        if nigerian_context_pct < 50:
            recommendations.append("Add Nigerian cultural context and examples to more content items")

        # Content type balance
        if overview['content_types'].get('exercise', 0) < overview['content_types'].get('study_guide', 0) * 0.3:
            recommendations.append("Create more practice exercises and interactive content")

        return recommendations[:10]  # Limit to top 10 recommendations

    def _calculate_performance_indicators(self) -> Dict[str, Any]:
        """Calculate key performance indicators"""

        overview = self._analyze_content_overview()
        quality = self._analyze_quality_metrics()

        kpis = {
            'content_completeness_index': round(
                (overview['content_with_summaries'] + overview['content_with_examples']) /
                (overview['total_content_items'] * 2) * 100, 2
            ),
            'cultural_relevance_index': round(
                overview['content_with_nigerian_context'] / overview['total_content_items'] * 100, 2
            ),
            'quality_index': quality['average_quality_score'],
            'subject_diversity_index': round(
                len([s for s in overview['subjects'].keys() if s != 'unknown']) / 10 * 100, 2  # Assuming 10 core subjects
            ),
            'content_type_diversity_index': round(
                len(overview['content_types']) / 6 * 100, 2  # Assuming 6 content types
            )
        }

        # Overall performance score
        kpis['overall_performance_score'] = round(sum(kpis.values()) / len(kpis), 2)

        return kpis

    def display_dashboard(self, report_file: str = None):
        """Display an interactive dashboard in the terminal"""

        if report_file and os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
        else:
            report = self.generate_comprehensive_report()

        print("🎯 Akulearn Content Management Dashboard")
        print("=" * 60)

        # Overview Section
        overview = report['content_overview']
        print("📊 CONTENT OVERVIEW")
        print(f"   Total Content Items: {overview['total_content_items']}")
        print(f"   Subjects Covered: {len(overview['subjects'])}")
        print(f"   Content Types: {len(overview['content_types'])}")
        print(".2f")
        print(f"   With Nigerian Context: {overview['content_with_nigerian_context']}")

        # Quality Section
        quality = report['quality_metrics']
        print("\n⭐ QUALITY METRICS")
        print(".2f")
        print(f"   Excellent: {quality['quality_distribution']['excellent']}")
        print(f"   Good: {quality['quality_distribution']['good']}")
        print(f"   Fair: {quality['quality_distribution']['fair']}")
        print(f"   Poor: {quality['quality_distribution']['poor']}")

        # Performance Indicators
        kpis = report['performance_indicators']
        print("\n📈 KEY PERFORMANCE INDICATORS")
        print(".2f")
        print(".2f")
        print(".2f")
        print(".2f")
        print(".2f")
        print(".2f")
        # Subject Distribution
        subjects = report['subject_distribution']
        print("\n📚 SUBJECT DISTRIBUTION")
        sorted_subjects = sorted(subjects.items(), key=lambda x: x[1]['total'], reverse=True)
        for subject, stats in sorted_subjects[:8]:  # Top 8 subjects
            print(f"   {subject}: {stats['total']} items ({stats['average_quality']:.1f}% avg quality)")

        # Content Gaps
        gaps = report['content_gaps']
        if gaps['missing_subjects']:
            print("\n⚠️  MISSING SUBJECTS")
            for subject in gaps['missing_subjects']:
                print(f"   • {subject}")

        if gaps['underrepresented_topics']:
            print("\n📝 UNDERREPRESENTED TOPICS")
            for gap in gaps['underrepresented_topics'][:3]:
                print(f"   • {gap['subject']}: {', '.join(gap['missing_topics'])}")

        # Recommendations
        recommendations = report['recommendations']
        if recommendations:
            print("\n💡 TOP RECOMMENDATIONS")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"   {i}. {rec}")

        print(f"\n📄 Full report saved to: {report_file or 'content_dashboard_report.json'}")

    def export_visualizations(self, report_data: Dict[str, Any], output_dir: str = None):
        """Export visualizations of the dashboard data"""

        if not output_dir:
            output_dir = os.path.join(self.reports_dir, 'visualizations')
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Subject distribution pie chart
            subjects = report_data['subject_distribution']
            subject_names = list(subjects.keys())[:8]  # Top 8
            subject_counts = [subjects[s]['total'] for s in subject_names]

            plt.figure(figsize=(10, 6))
            plt.pie(subject_counts, labels=subject_names, autopct='%1.1f%%')
            plt.title('Content Distribution by Subject')
            plt.savefig(os.path.join(output_dir, 'subject_distribution.png'))
            plt.close()

            # Quality distribution bar chart
            quality = report_data['quality_metrics']['quality_distribution']
            plt.figure(figsize=(8, 5))
            plt.bar(quality.keys(), quality.values(), color=['green', 'blue', 'orange', 'red'])
            plt.title('Content Quality Distribution')
            plt.ylabel('Number of Items')
            plt.savefig(os.path.join(output_dir, 'quality_distribution.png'))
            plt.close()

            # Performance indicators radar chart
            kpis = report_data['performance_indicators']
            kpi_names = [k.replace('_', ' ').title() for k in kpis.keys() if k != 'overall_performance_score']
            kpi_values = [kpis[k] for k in kpis.keys() if k != 'overall_performance_score']

            angles = [n / float(len(kpi_names)) * 2 * 3.14159 for n in range(len(kpi_names))]
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
            kpi_values += kpi_values[:1]
            ax.plot(angles, kpi_values)
            ax.fill(angles, kpi_values, alpha=0.25)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(kpi_names)
            ax.set_title('Performance Indicators')
            plt.savefig(os.path.join(output_dir, 'performance_radar.png'))
            plt.close()

            print(f"📊 Visualizations exported to: {output_dir}")

        except ImportError:
            print("⚠️  Matplotlib not available - skipping visualizations")
        except Exception as e:
            print(f"⚠️  Error creating visualizations: {e}")

def main():
    """Command-line interface for content management dashboard"""

    dashboard = ContentManagementDashboard()

    parser = argparse.ArgumentParser(description='Content Management Dashboard')
    parser.add_argument('--generate-report', action='store_true', help='Generate comprehensive report')
    parser.add_argument('--display-dashboard', action='store_true', help='Display interactive dashboard')
    parser.add_argument('--export-visualizations', action='store_true', help='Export data visualizations')
    parser.add_argument('--report-file', type=str, help='Specific report file to use/display')
    parser.add_argument('--output-dir', type=str, help='Output directory for reports/visualizations')

    args = parser.parse_args()

    if args.generate_report:
        report_file = args.report_file or f"content_dashboard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        if args.output_dir:
            report_file = os.path.join(args.output_dir, os.path.basename(report_file))

        report = dashboard.generate_comprehensive_report(report_file)
        print("✅ Report generated successfully!")

    elif args.display_dashboard:
        report_file = args.report_file
        dashboard.display_dashboard(report_file)

    elif args.export_visualizations:
        if args.report_file and os.path.exists(args.report_file):
            with open(args.report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
        else:
            report_data = dashboard.generate_comprehensive_report()

        dashboard.export_visualizations(report_data, args.output_dir)

    else:
        # Interactive dashboard
        print("🎯 Akulearn Content Management Dashboard")
        print("=" * 50)

        while True:
            print("\nOptions:")
            print("1. Generate comprehensive report")
            print("2. Display dashboard")
            print("3. Export visualizations")
            print("4. Quick statistics")
            print("5. Exit")

            choice = input("\nSelect option (1-5): ").strip()

            if choice == "1":
                report_file = input("Report filename (or press Enter for auto-generated): ").strip()
                if not report_file:
                    report_file = f"content_dashboard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

                dashboard.generate_comprehensive_report(report_file)
                print(f"✅ Report saved to: {report_file}")

            elif choice == "2":
                report_file = input("Report file to display (or press Enter for latest): ").strip()
                if not report_file:
                    # Find latest report
                    report_files = [f for f in os.listdir('.') if f.startswith('content_dashboard_report_') and f.endswith('.json')]
                    if report_files:
                        report_file = max(report_files, key=lambda x: os.path.getmtime(x))
                    else:
                        print("No report files found. Generating new report...")
                        report_file = dashboard.generate_comprehensive_report()

                dashboard.display_dashboard(report_file)

            elif choice == "3":
                report_file = input("Report file for visualizations (or press Enter for latest): ").strip()
                if not report_file:
                    report_files = [f for f in os.listdir('.') if f.startswith('content_dashboard_report_') and f.endswith('.json')]
                    if report_files:
                        report_file = max(report_files, key=lambda x: os.path.getmtime(x))
                        with open(report_file, 'r', encoding='utf-8') as f:
                            report_data = json.load(f)
                    else:
                        report_data = dashboard.generate_comprehensive_report()
                else:
                    with open(report_file, 'r', encoding='utf-8') as f:
                        report_data = json.load(f)

                output_dir = input("Output directory (or press Enter for default): ").strip()
                dashboard.export_visualizations(report_data, output_dir or None)

            elif choice == "4":
                # Quick statistics
                overview = dashboard._analyze_content_overview()
                quality = dashboard._analyze_quality_metrics()
                kpis = dashboard._calculate_performance_indicators()

                print("\n📊 QUICK STATISTICS")
                print(f"   Total Content: {overview['total_content_items']}")
                print(".2f")
                print(".2f")
                print(".2f")
                print(f"   Subjects: {len(overview['subjects'])}")
                print(f"   Content Types: {len(overview['content_types'])}")

            elif choice == "5":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid option")

if __name__ == "__main__":
    main()