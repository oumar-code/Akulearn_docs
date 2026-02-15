"""
Akulearn Skill Orchestrator
Manages and executes custom AI agent skills for educational content generation,
analysis, validation, and deployment tasks.
"""

import json
import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SkillStatus(Enum):
    """Status of skill execution"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIAL = "partial"


@dataclass
class SkillContext:
    """Context for skill execution"""
    skill_id: str
    parameters: Dict[str, Any]
    workspace_root: str
    execution_id: str
    timestamp: str
    dependencies_met: bool = True
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SkillResult:
    """Result of skill execution"""
    skill_id: str
    execution_id: str
    status: SkillStatus
    output: Any
    duration_seconds: float
    error_message: Optional[str] = None
    warnings: List[str] = None
    artifacts: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.artifacts is None:
            self.artifacts = []

    def to_dict(self):
        result = asdict(self)
        result['status'] = self.status.value
        return result


class SkillOrchestrator:
    """
    Orchestrates execution of custom agent skills across the Akulearn platform
    """
    
    def __init__(self, workspace_root: Optional[str] = None):
        """
        Initialize the skill orchestrator
        
        Args:
            workspace_root: Root directory of the workspace
        """
        self.workspace_root = workspace_root or self._detect_workspace_root()
        self.skills_dir = Path(self.workspace_root) / "src" / "backend" / "skills"
        self.definitions_path = self.skills_dir / "skill_definitions.json"
        self.instructions_dir = self.skills_dir / "instructions"
        
        # Load skill definitions
        self.skills = self._load_skill_definitions()
        self.skill_categories = self.skills.get('skill_categories', {})
        self.skill_workflows = self.skills.get('skill_workflows', {})
        
        # Execution tracking
        self.execution_history: List[SkillResult] = []
        self.active_executions: Dict[str, SkillContext] = {}
        
        logger.info(f"SkillOrchestrator initialized with {len(self.skills.get('skills', {}))} skills")

    def _detect_workspace_root(self) -> str:
        """Detect workspace root directory"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "src" / "backend").exists():
                return str(current)
            current = current.parent
        return str(Path.cwd())

    def _load_skill_definitions(self) -> Dict:
        """Load skill definitions from JSON file"""
        try:
            with open(self.definitions_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Skill definitions not found at {self.definitions_path}")
            return {"skills": {}, "skill_categories": {}, "skill_workflows": {}}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing skill definitions: {e}")
            return {"skills": {}, "skill_categories": {}, "skill_workflows": {}}

    def list_skills(self, category: Optional[str] = None) -> List[Dict]:
        """
        List available skills, optionally filtered by category
        
        Args:
            category: Optional category filter
            
        Returns:
            List of skill definitions
        """
        skills = self.skills.get('skills', {})
        skill_list = []
        
        for skill_id, skill_def in skills.items():
            if category is None or skill_def.get('category') == category:
                skill_list.append({
                    'id': skill_id,
                    'name': skill_def.get('name'),
                    'description': skill_def.get('description'),
                    'category': skill_def.get('category'),
                    'complexity': skill_def.get('complexity'),
                    'estimated_duration': skill_def.get('estimated_duration')
                })
        
        return skill_list

    def get_skill(self, skill_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific skill
        
        Args:
            skill_id: ID of the skill
            
        Returns:
            Skill definition or None if not found
        """
        return self.skills.get('skills', {}).get(skill_id)

    def validate_context(self, skill_id: str, context: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate that required context is provided for a skill
        
        Args:
            skill_id: ID of the skill
            context: Context parameters
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        skill = self.get_skill(skill_id)
        if not skill:
            return False, [f"Skill '{skill_id}' not found"]
        
        errors = []
        required_context = skill.get('required_context', [])
        
        for req in required_context:
            if req not in context or context[req] is None:
                errors.append(f"Missing required context parameter: '{req}'")
        
        return len(errors) == 0, errors

    def check_dependencies(self, skill_id: str) -> Tuple[bool, List[str]]:
        """
        Check if skill dependencies are satisfied
        
        Args:
            skill_id: ID of the skill
            
        Returns:
            Tuple of (dependencies_met, list_of_missing_dependencies)
        """
        skill = self.get_skill(skill_id)
        if not skill:
            return False, [f"Skill '{skill_id}' not found"]
        
        dependencies = skill.get('dependencies', [])
        missing = []
        
        # Check if dependency skills exist
        for dep_id in dependencies:
            if not self.get_skill(dep_id):
                missing.append(f"Dependency skill '{dep_id}' not found")
        
        return len(missing) == 0, missing

    def _get_tool_path(self, tool_name: str) -> Optional[Path]:
        """
        Get the full path to a tool script
        
        Args:
            tool_name: Name of the tool file
            
        Returns:
            Path to the tool or None if not found
        """
        # Check in workspace root
        tool_path = Path(self.workspace_root) / tool_name
        if tool_path.exists():
            return tool_path
        
        # Check in src/backend
        tool_path = Path(self.workspace_root) / "src" / "backend" / tool_name
        if tool_path.exists():
            return tool_path
        
        return None

    def _execute_python_tool(self, tool_path: Path, context: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        Execute a Python tool with given context
        
        Args:
            tool_path: Path to the Python script
            context: Context parameters
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            # Prepare command
            cmd = [sys.executable, str(tool_path)]
            
            # Convert context to command line arguments
            for key, value in context.items():
                if isinstance(value, bool):
                    if value:
                        cmd.append(f"--{key}")
                elif isinstance(value, (list, dict)):
                    cmd.extend([f"--{key}", json.dumps(value)])
                else:
                    cmd.extend([f"--{key}", str(value)])
            
            # Execute
            logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            return False, "", "Tool execution timeout (1 hour)"
        except Exception as e:
            return False, "", str(e)

    def _execute_shell_script(self, script_path: Path, context: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        Execute a shell script with given context
        
        Args:
            script_path: Path to the shell script
            context: Context parameters
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            # Make script executable on Unix systems
            if sys.platform != 'win32':
                os.chmod(script_path, 0o755)
            
            # Prepare environment variables from context
            env = os.environ.copy()
            for key, value in context.items():
                env[key.upper()] = str(value)
            
            # Execute
            if sys.platform == 'win32':
                # Use PowerShell on Windows
                cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(script_path)]
            else:
                cmd = [str(script_path)]
            
            logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                env=env,
                timeout=3600
            )
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except Exception as e:
            return False, "", str(e)

    def execute_skill(
        self,
        skill_id: str,
        context: Dict[str, Any],
        dry_run: bool = False
    ) -> SkillResult:
        """
        Execute a skill with given context
        
        Args:
            skill_id: ID of the skill to execute
            context: Context parameters for the skill
            dry_run: If True, validate but don't actually execute
            
        Returns:
            SkillResult object with execution results
        """
        start_time = datetime.now()
        execution_id = f"{skill_id}_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"Starting skill execution: {skill_id} (ID: {execution_id})")
        
        # Get skill definition
        skill = self.get_skill(skill_id)
        if not skill:
            return SkillResult(
                skill_id=skill_id,
                execution_id=execution_id,
                status=SkillStatus.FAILED,
                output=None,
                duration_seconds=0,
                error_message=f"Skill '{skill_id}' not found"
            )
        
        # Validate context
        is_valid, errors = self.validate_context(skill_id, context)
        if not is_valid:
            return SkillResult(
                skill_id=skill_id,
                execution_id=execution_id,
                status=SkillStatus.FAILED,
                output=None,
                duration_seconds=0,
                error_message=f"Context validation failed: {', '.join(errors)}"
            )
        
        # Check dependencies
        deps_met, missing_deps = self.check_dependencies(skill_id)
        if not deps_met:
            return SkillResult(
                skill_id=skill_id,
                execution_id=execution_id,
                status=SkillStatus.FAILED,
                output=None,
                duration_seconds=0,
                error_message=f"Dependencies not met: {', '.join(missing_deps)}"
            )
        
        if dry_run:
            return SkillResult(
                skill_id=skill_id,
                execution_id=execution_id,
                status=SkillStatus.SUCCESS,
                output={"message": "Dry run successful", "skill": skill},
                duration_seconds=0
            )
        
        # Create skill context
        skill_context = SkillContext(
            skill_id=skill_id,
            parameters=context,
            workspace_root=self.workspace_root,
            execution_id=execution_id,
            timestamp=start_time.isoformat(),
            dependencies_met=deps_met
        )
        self.active_executions[execution_id] = skill_context
        
        # Execute tools
        tools = skill.get('tools', [])
        outputs = []
        warnings = []
        artifacts = []
        overall_success = True
        
        for tool_name in tools:
            tool_path = self._get_tool_path(tool_name)
            if not tool_path:
                warnings.append(f"Tool '{tool_name}' not found")
                continue
            
            # Execute based on file type
            if tool_name.endswith('.py'):
                success, stdout, stderr = self._execute_python_tool(tool_path, context)
            elif tool_name.endswith('.sh'):
                success, stdout, stderr = self._execute_shell_script(tool_path, context)
            else:
                warnings.append(f"Unsupported tool type: {tool_name}")
                continue
            
            if success:
                outputs.append({
                    'tool': tool_name,
                    'output': stdout,
                    'success': True
                })
                logger.info(f"Tool '{tool_name}' executed successfully")
            else:
                outputs.append({
                    'tool': tool_name,
                    'output': stdout,
                    'error': stderr,
                    'success': False
                })
                warnings.append(f"Tool '{tool_name}' failed: {stderr[:200]}")
                overall_success = False
                logger.warning(f"Tool '{tool_name}' failed")
        
        # Calculate duration
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Determine final status
        if overall_success:
            status = SkillStatus.SUCCESS
        elif len(outputs) > 0 and any(o.get('success') for o in outputs):
            status = SkillStatus.PARTIAL
        else:
            status = SkillStatus.FAILED
        
        # Create result
        result = SkillResult(
            skill_id=skill_id,
            execution_id=execution_id,
            status=status,
            output=outputs,
            duration_seconds=duration,
            warnings=warnings,
            artifacts=artifacts
        )
        
        # Update tracking
        self.execution_history.append(result)
        if execution_id in self.active_executions:
            del self.active_executions[execution_id]
        
        logger.info(f"Skill execution completed: {skill_id} ({status.value}) in {duration:.2f}s")
        
        return result

    def execute_workflow(
        self,
        workflow_id: str,
        context: Dict[str, Any],
        stop_on_error: bool = True
    ) -> List[SkillResult]:
        """
        Execute a predefined workflow consisting of multiple skills
        
        Args:
            workflow_id: ID of the workflow to execute
            context: Context parameters (shared across all skills)
            stop_on_error: If True, stop workflow on first error
            
        Returns:
            List of SkillResult objects for each step
        """
        workflow = self.skill_workflows.get(workflow_id)
        if not workflow:
            logger.error(f"Workflow '{workflow_id}' not found")
            return []
        
        logger.info(f"Starting workflow: {workflow.get('name')} ({workflow_id})")
        
        results = []
        steps = workflow.get('steps', [])
        
        for i, step in enumerate(steps, 1):
            skill_id = step.get('skill')
            step_description = step.get('description', '')
            
            logger.info(f"Workflow step {i}/{len(steps)}: {step_description}")
            
            result = self.execute_skill(skill_id, context)
            results.append(result)
            
            if stop_on_error and result.status == SkillStatus.FAILED:
                logger.error(f"Workflow stopped due to error in step {i}")
                break
        
        logger.info(f"Workflow completed: {workflow_id}")
        return results

    def get_execution_history(
        self,
        skill_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get execution history, optionally filtered by skill
        
        Args:
            skill_id: Optional skill ID filter
            limit: Maximum number of results to return
            
        Returns:
            List of execution results
        """
        history = self.execution_history
        
        if skill_id:
            history = [r for r in history if r.skill_id == skill_id]
        
        # Return most recent first
        history = sorted(history, key=lambda r: r.execution_id, reverse=True)
        
        return [r.to_dict() for r in history[:limit]]

    def get_skill_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about skill executions
        
        Returns:
            Dictionary with statistics
        """
        total_executions = len(self.execution_history)
        if total_executions == 0:
            return {
                'total_executions': 0,
                'success_rate': 0,
                'average_duration': 0,
                'most_used_skill': None
            }
        
        successful = sum(1 for r in self.execution_history if r.status == SkillStatus.SUCCESS)
        total_duration = sum(r.duration_seconds for r in self.execution_history)
        
        # Count skill usage
        skill_usage = {}
        for result in self.execution_history:
            skill_usage[result.skill_id] = skill_usage.get(result.skill_id, 0) + 1
        
        most_used = max(skill_usage.items(), key=lambda x: x[1]) if skill_usage else (None, 0)
        
        return {
            'total_executions': total_executions,
            'success_rate': (successful / total_executions) * 100,
            'average_duration': total_duration / total_executions,
            'most_used_skill': most_used[0],
            'most_used_skill_count': most_used[1],
            'skill_usage': skill_usage
        }

    def export_execution_log(self, output_path: str) -> bool:
        """
        Export execution history to JSON file
        
        Args:
            output_path: Path to output file
            
        Returns:
            True if successful
        """
        try:
            data = {
                'exported_at': datetime.now().isoformat(),
                'workspace_root': self.workspace_root,
                'statistics': self.get_skill_statistics(),
                'execution_history': [r.to_dict() for r in self.execution_history]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Execution log exported to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting execution log: {e}")
            return False


def main():
    """Command-line interface for skill orchestrator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Akulearn Skill Orchestrator')
    parser.add_argument('command', choices=['list', 'execute', 'workflow', 'history', 'stats'],
                      help='Command to execute')
    parser.add_argument('--skill', help='Skill ID')
    parser.add_argument('--workflow', help='Workflow ID')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--context', help='Context parameters as JSON string')
    parser.add_argument('--dry-run', action='store_true', help='Validate without executing')
    parser.add_argument('--limit', type=int, default=10, help='Limit for history results')
    parser.add_argument('--export', help='Export path for logs')
    
    args = parser.parse_args()
    
    orchestrator = SkillOrchestrator()
    
    if args.command == 'list':
        skills = orchestrator.list_skills(category=args.category)
        print(f"\n=== Available Skills ({len(skills)}) ===\n")
        for skill in skills:
            print(f"ID: {skill['id']}")
            print(f"Name: {skill['name']}")
            print(f"Category: {skill['category']}")
            print(f"Description: {skill['description']}")
            print(f"Estimated Duration: {skill['estimated_duration']}")
            print("-" * 80)
    
    elif args.command == 'execute':
        if not args.skill:
            print("Error: --skill required for execute command")
            return
        
        context = {}
        if args.context:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError:
                print("Error: Invalid JSON in --context")
                return
        
        result = orchestrator.execute_skill(args.skill, context, dry_run=args.dry_run)
        print(f"\n=== Execution Result ===")
        print(f"Skill: {result.skill_id}")
        print(f"Status: {result.status.value}")
        print(f"Duration: {result.duration_seconds:.2f}s")
        if result.error_message:
            print(f"Error: {result.error_message}")
        if result.warnings:
            print(f"Warnings: {', '.join(result.warnings)}")
    
    elif args.command == 'workflow':
        if not args.workflow:
            print("Error: --workflow required for workflow command")
            return
        
        context = {}
        if args.context:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError:
                print("Error: Invalid JSON in --context")
                return
        
        results = orchestrator.execute_workflow(args.workflow, context)
        print(f"\n=== Workflow Results ({len(results)} steps) ===")
        for i, result in enumerate(results, 1):
            print(f"\nStep {i}: {result.skill_id}")
            print(f"  Status: {result.status.value}")
            print(f"  Duration: {result.duration_seconds:.2f}s")
    
    elif args.command == 'history':
        history = orchestrator.get_execution_history(skill_id=args.skill, limit=args.limit)
        print(f"\n=== Execution History ({len(history)} results) ===\n")
        for entry in history:
            print(f"Skill: {entry['skill_id']}")
            print(f"Execution ID: {entry['execution_id']}")
            print(f"Status: {entry['status']}")
            print(f"Duration: {entry['duration_seconds']:.2f}s")
            print("-" * 80)
    
    elif args.command == 'stats':
        stats = orchestrator.get_skill_statistics()
        print(f"\n=== Execution Statistics ===")
        print(f"Total Executions: {stats['total_executions']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Average Duration: {stats['average_duration']:.2f}s")
        print(f"Most Used Skill: {stats['most_used_skill']} ({stats.get('most_used_skill_count', 0)} times)")
        
        if args.export:
            orchestrator.export_execution_log(args.export)
            print(f"\nLog exported to: {args.export}")


if __name__ == '__main__':
    main()
