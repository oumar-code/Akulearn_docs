"""
Akulearn Skills CLI
Command-line interface for managing and executing agent skills
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from skills.skill_orchestrator import SkillOrchestrator
except ImportError:
    print("Error: Could not import SkillOrchestrator. Make sure you're in the correct directory.")
    sys.exit(1)


class SkillsCLI:
    """Command-line interface for Akulearn skills"""
    
    def __init__(self):
        self.orchestrator = SkillOrchestrator()
        
    def list_skills(self, args):
        """List available skills"""
        skills = self.orchestrator.list_skills(category=args.category)
        
        if args.json:
            print(json.dumps(skills, indent=2))
            return
        
        if not skills:
            print("No skills found.")
            return
        
        print(f"\n{'=' * 80}")
        print(f"  Available Skills ({len(skills)})")
        print(f"{'=' * 80}\n")
        
        # Group by category if not filtering
        if not args.category:
            by_category = {}
            for skill in skills:
                cat = skill['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(skill)
            
            for category, cat_skills in sorted(by_category.items()):
                cat_info = self.orchestrator.skill_categories.get(category, {})
                cat_name = cat_info.get('name', category)
                print(f"\n📂 {cat_name}")
                print(f"   {cat_info.get('description', '')}")
                print("-" * 80)
                
                for skill in cat_skills:
                    print(f"\n  ID: {skill['id']}")
                    print(f"  Name: {skill['name']}")
                    print(f"  Description: {skill['description']}")
                    print(f"  Complexity: {skill['complexity']}")
                    print(f"  Duration: {skill['estimated_duration']}")
        else:
            for skill in skills:
                print(f"\nID: {skill['id']}")
                print(f"Name: {skill['name']}")
                print(f"Description: {skill['description']}")
                print(f"Complexity: {skill['complexity']}")
                print(f"Duration: {skill['estimated_duration']}")
                print("-" * 80)
    
    def show_skill(self, args):
        """Show detailed information about a skill"""
        skill = self.orchestrator.get_skill(args.skill)
        
        if not skill:
            print(f"Error: Skill '{args.skill}' not found")
            return
        
        if args.json:
            print(json.dumps(skill, indent=2))
            return
        
        print(f"\n{'=' * 80}")
        print(f"  Skill: {skill['name']}")
        print(f"{'=' * 80}\n")
        
        print(f"ID: {skill['id']}")
        print(f"Category: {skill['category']}")
        print(f"Complexity: {skill['complexity']}")
        print(f"Estimated Duration: {skill['estimated_duration']}")
        print(f"\nDescription:")
        print(f"  {skill['description']}")
        
        print(f"\nRequired Context:")
        for req in skill['required_context']:
            print(f"  • {req}")
        
        if skill.get('optional_context'):
            print(f"\nOptional Context:")
            for opt in skill['optional_context']:
                print(f"  • {opt}")
        
        print(f"\nTools Used:")
        for tool in skill['tools']:
            print(f"  • {tool}")
        
        if skill.get('dependencies'):
            print(f"\nDependencies:")
            for dep in skill['dependencies']:
                print(f"  • {dep}")
        
        print(f"\nOutput Format: {skill['output_format']}")
        
        instruction_file = skill.get('instruction_template')
        if instruction_file:
            print(f"\nInstruction Template: {instruction_file}")
    
    def execute_skill(self, args):
        """Execute a skill"""
        # Parse context
        context = {}
        if args.context:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in context: {e}")
                return
        
        # Add individual context parameters
        if args.subject:
            context['subject'] = args.subject
        if args.grade_level:
            context['grade_level'] = args.grade_level
        if args.topic:
            context['topic'] = args.topic
        if args.curriculum:
            context['curriculum_standard'] = args.curriculum
        
        # Validate before execution
        if not args.force:
            is_valid, errors = self.orchestrator.validate_context(args.skill, context)
            if not is_valid:
                print("❌ Context validation failed:")
                for error in errors:
                    print(f"  • {error}")
                print("\nUse --force to skip validation")
                return
        
        print(f"\n🚀 Executing skill: {args.skill}")
        if args.dry_run:
            print("   (Dry run mode - no actual execution)")
        print()
        
        # Execute
        result = self.orchestrator.execute_skill(
            args.skill,
            context,
            dry_run=args.dry_run
        )
        
        # Display result
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
            return
        
        status_emoji = {
            'success': '✅',
            'failed': '❌',
            'partial': '⚠️',
            'cancelled': '🚫'
        }
        
        print(f"\n{'=' * 80}")
        print(f"  Execution Result")
        print(f"{'=' * 80}\n")
        
        print(f"Status: {status_emoji.get(result.status.value, '❓')} {result.status.value.upper()}")
        print(f"Duration: {result.duration_seconds:.2f}s")
        
        if result.error_message:
            print(f"\n❌ Error: {result.error_message}")
        
        if result.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in result.warnings:
                print(f"  • {warning}")
        
        if result.artifacts:
            print(f"\n📦 Artifacts:")
            for artifact in result.artifacts:
                print(f"  • {artifact}")
        
        if not args.dry_run and result.output:
            print(f"\n📊 Output:")
            if isinstance(result.output, (list, dict)):
                print(json.dumps(result.output, indent=2))
            else:
                print(result.output)
    
    def execute_workflow(self, args):
        """Execute a workflow"""
        # Parse context
        context = {}
        if args.context:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in context: {e}")
                return
        
        workflow = self.orchestrator.skill_workflows.get(args.workflow)
        if not workflow:
            print(f"Error: Workflow '{args.workflow}' not found")
            return
        
        print(f"\n🔄 Executing workflow: {workflow['name']}")
        print(f"   {workflow['description']}")
        print(f"   Steps: {len(workflow['steps'])}\n")
        
        # Execute
        results = self.orchestrator.execute_workflow(
            args.workflow,
            context,
            stop_on_error=not args.continue_on_error
        )
        
        # Display results
        if args.json:
            print(json.dumps([r.to_dict() for r in results], indent=2))
            return
        
        print(f"\n{'=' * 80}")
        print(f"  Workflow Results")
        print(f"{'=' * 80}\n")
        
        for i, result in enumerate(results, 1):
            status_emoji = {
                'success': '✅',
                'failed': '❌',
                'partial': '⚠️'
            }
            
            print(f"Step {i}: {result.skill_id}")
            print(f"  Status: {status_emoji.get(result.status.value, '❓')} {result.status.value}")
            print(f"  Duration: {result.duration_seconds:.2f}s")
            if result.warnings:
                print(f"  Warnings: {len(result.warnings)}")
            print()
        
        success_count = sum(1 for r in results if r.status.value == 'success')
        print(f"Completed: {success_count}/{len(results)} steps successful")
    
    def list_workflows(self, args):
        """List available workflows"""
        workflows = self.orchestrator.skill_workflows
        
        if args.json:
            print(json.dumps(workflows, indent=2))
            return
        
        print(f"\n{'=' * 80}")
        print(f"  Available Workflows ({len(workflows)})")
        print(f"{'=' * 80}\n")
        
        for wf_id, workflow in workflows.items():
            print(f"ID: {wf_id}")
            print(f"Name: {workflow['name']}")
            print(f"Description: {workflow['description']}")
            print(f"Steps: {len(workflow['steps'])}")
            
            if args.verbose:
                print("\nWorkflow Steps:")
                for i, step in enumerate(workflow['steps'], 1):
                    print(f"  {i}. {step['skill']}: {step['description']}")
            
            print("-" * 80)
    
    def show_history(self, args):
        """Show execution history"""
        history = self.orchestrator.get_execution_history(
            skill_id=args.skill,
            limit=args.limit
        )
        
        if args.json:
            print(json.dumps(history, indent=2))
            return
        
        if not history:
            print("No execution history found.")
            return
        
        print(f"\n{'=' * 80}")
        print(f"  Execution History ({len(history)} results)")
        print(f"{'=' * 80}\n")
        
        for entry in history:
            print(f"Skill: {entry['skill_id']}")
            print(f"Execution ID: {entry['execution_id']}")
            print(f"Status: {entry['status']}")
            print(f"Duration: {entry['duration_seconds']:.2f}s")
            
            if entry.get('error_message'):
                print(f"Error: {entry['error_message']}")
            
            if entry.get('warnings'):
                print(f"Warnings: {len(entry['warnings'])}")
            
            print("-" * 80)
    
    def show_stats(self, args):
        """Show execution statistics"""
        stats = self.orchestrator.get_skill_statistics()
        
        if args.json:
            print(json.dumps(stats, indent=2))
            return
        
        print(f"\n{'=' * 80}")
        print(f"  Execution Statistics")
        print(f"{'=' * 80}\n")
        
        print(f"Total Executions: {stats['total_executions']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Average Duration: {stats['average_duration']:.2f}s")
        
        if stats['most_used_skill']:
            print(f"\nMost Used Skill:")
            print(f"  {stats['most_used_skill']} ({stats['most_used_skill_count']} times)")
        
        if args.verbose and stats.get('skill_usage'):
            print(f"\nSkill Usage:")
            for skill_id, count in sorted(
                stats['skill_usage'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                print(f"  {skill_id}: {count} times")
        
        if args.export:
            if self.orchestrator.export_execution_log(args.export):
                print(f"\n✅ Statistics exported to: {args.export}")
            else:
                print(f"\n❌ Failed to export statistics")
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n" + "=" * 80)
        print("  Akulearn Skills Interactive Mode")
        print("=" * 80)
        print("\nType 'help' for available commands, 'exit' to quit\n")
        
        while True:
            try:
                command = input("skills> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye!")
                    break
                
                if command.lower() == 'help':
                    self.print_interactive_help()
                    continue
                
                # Parse and execute command
                parts = command.split()
                if parts[0] == 'list':
                    args = argparse.Namespace(category=None, json=False)
                    if len(parts) > 1:
                        args.category = parts[1]
                    self.list_skills(args)
                
                elif parts[0] == 'show':
                    if len(parts) < 2:
                        print("Usage: show <skill_id>")
                        continue
                    args = argparse.Namespace(skill=parts[1], json=False)
                    self.show_skill(args)
                
                elif parts[0] == 'workflows':
                    args = argparse.Namespace(json=False, verbose=False)
                    self.list_workflows(args)
                
                elif parts[0] == 'history':
                    args = argparse.Namespace(skill=None, limit=10, json=False)
                    self.show_history(args)
                
                elif parts[0] == 'stats':
                    args = argparse.Namespace(json=False, verbose=False, export=None)
                    self.show_stats(args)
                
                else:
                    print(f"Unknown command: {parts[0]}")
                    print("Type 'help' for available commands")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def print_interactive_help(self):
        """Print help for interactive mode"""
        print("\nAvailable Commands:")
        print("  list [category]          - List all skills or filter by category")
        print("  show <skill_id>          - Show detailed info about a skill")
        print("  workflows                - List available workflows")
        print("  history                  - Show execution history")
        print("  stats                    - Show execution statistics")
        print("  help                     - Show this help message")
        print("  exit, quit, q            - Exit interactive mode")
        print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Akulearn Skills CLI - Manage and execute agent skills',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List skills command
    list_parser = subparsers.add_parser('list', help='List available skills')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Show skill command
    show_parser = subparsers.add_parser('show', help='Show skill details')
    show_parser.add_argument('skill', help='Skill ID')
    show_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Execute skill command
    exec_parser = subparsers.add_parser('execute', help='Execute a skill')
    exec_parser.add_argument('skill', help='Skill ID')
    exec_parser.add_argument('--context', help='Context as JSON string')
    exec_parser.add_argument('--subject', help='Subject name')
    exec_parser.add_argument('--grade-level', help='Grade level')
    exec_parser.add_argument('--topic', help='Topic name')
    exec_parser.add_argument('--curriculum', help='Curriculum standard')
    exec_parser.add_argument('--dry-run', action='store_true', help='Validate without executing')
    exec_parser.add_argument('--force', action='store_true', help='Skip validation')
    exec_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Workflow commands
    workflow_parser = subparsers.add_parser('workflow', help='Execute a workflow')
    workflow_parser.add_argument('workflow', help='Workflow ID')
    workflow_parser.add_argument('--context', help='Context as JSON string')
    workflow_parser.add_argument('--continue-on-error', action='store_true',
                                help='Continue workflow on errors')
    workflow_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    workflows_parser = subparsers.add_parser('workflows', help='List workflows')
    workflows_parser.add_argument('--json', action='store_true', help='Output as JSON')
    workflows_parser.add_argument('--verbose', '-v', action='store_true',
                                 help='Show workflow steps')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show execution history')
    history_parser.add_argument('--skill', help='Filter by skill ID')
    history_parser.add_argument('--limit', type=int, default=10, help='Number of results')
    history_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show execution statistics')
    stats_parser.add_argument('--json', action='store_true', help='Output as JSON')
    stats_parser.add_argument('--verbose', '-v', action='store_true',
                            help='Show detailed statistics')
    stats_parser.add_argument('--export', help='Export to file')
    
    # Interactive mode
    subparsers.add_parser('interactive', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = SkillsCLI()
    
    if args.command == 'list':
        cli.list_skills(args)
    elif args.command == 'show':
        cli.show_skill(args)
    elif args.command == 'execute':
        cli.execute_skill(args)
    elif args.command == 'workflow':
        cli.execute_workflow(args)
    elif args.command == 'workflows':
        cli.list_workflows(args)
    elif args.command == 'history':
        cli.show_history(args)
    elif args.command == 'stats':
        cli.show_stats(args)
    elif args.command == 'interactive':
        cli.interactive_mode()


if __name__ == '__main__':
    main()
