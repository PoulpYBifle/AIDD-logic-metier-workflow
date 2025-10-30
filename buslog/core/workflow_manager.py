"""
Workflow Manager

Handles CRUD operations for business logic workflows.
"""

import json
from datetime import datetime
from pathlib import Path


class WorkflowManager:
    """Manages business logic workflow documentation."""

    BUSLOG_DIR = ".business-logic"
    WORKFLOWS_DIR = "workflows"
    CONFIG_FILE = "config.json"
    INDEX_FILE = "index.md"

    def __init__(self, project_root: Path | None = None):
        """Initialize WorkflowManager.

        Args:
            project_root: Root directory of the project. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()
        self.buslog_path = self.project_root / self.BUSLOG_DIR
        self.workflows_path = self.buslog_path / self.WORKFLOWS_DIR
        self.config_path = self.buslog_path / self.CONFIG_FILE
        self.index_path = self.buslog_path / self.INDEX_FILE

    def is_initialized(self) -> bool:
        """Check if BusLog is initialized in the project."""
        return (
            self.buslog_path.exists() and self.config_path.exists() and self.workflows_path.exists()
        )

    def initialize(self, project_name: str | None = None, force: bool = False) -> None:
        """Initialize BusLog structure in the project.

        Args:
            project_name: Name of the project. Defaults to directory name.
            force: Force re-initialization even if already exists.
        """
        if self.is_initialized() and not force:
            raise FileExistsError("BusLog is already initialized")

        # Create directories
        self.buslog_path.mkdir(exist_ok=True)
        self.workflows_path.mkdir(exist_ok=True)

        # Detect project name
        if not project_name:
            project_name = self.project_root.name

        # Create config.json
        config = {
            "project_name": project_name,
            "version": "0.1.0",
            "created_at": datetime.now().isoformat(),
            "languages": self._detect_languages(),
            "frameworks": [],
            "workflows": [],
            "settings": {
                "auto_detect": False,
                "mermaid_theme": "default",
                "show_line_numbers": True,
                "collapse_by_default": False,
            },
            "metadata": {"repository": "", "main_branch": "main", "authors": []},
        }

        self.config_path.write_text(
            json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Create index.md
        index_content = self._generate_index(project_name)
        self.index_path.write_text(index_content, encoding="utf-8")

    def add_workflow(self, workflow_name: str) -> Path:
        """Create a new workflow documentation file.

        Args:
            workflow_name: Name of the workflow (kebab-case recommended).

        Returns:
            Path to the created workflow file.

        Raises:
            FileExistsError: If workflow already exists.
        """
        # Sanitize workflow name
        safe_name = workflow_name.lower().replace(" ", "-")
        workflow_path = self.workflows_path / f"{safe_name}.md"

        if workflow_path.exists():
            raise FileExistsError(f"Workflow '{safe_name}' already exists")

        # Load template
        template_path = Path(__file__).parent.parent / "templates" / "workflow.md"
        template = template_path.read_text(encoding="utf-8")

        # Replace placeholders
        workflow_title = workflow_name.replace("-", " ").title()
        content = template.format(
            workflow_name=workflow_title,
            created_date=datetime.now().strftime("%Y-%m-%d"),
            modified_date=datetime.now().strftime("%Y-%m-%d"),
            author="",
            date=datetime.now().strftime("%Y-%m-%d"),
        )

        # Write workflow file
        workflow_path.write_text(content, encoding="utf-8")

        # Update config
        self._add_workflow_to_config(safe_name)

        return workflow_path

    def list_workflows(self) -> list[dict[str, str]]:
        """List all workflows in the project.

        Returns:
            List of workflow information dictionaries.
        """
        if not self.workflows_path.exists():
            return []

        workflows = []
        for workflow_file in self.workflows_path.glob("*.md"):
            workflows.append(
                {
                    "name": workflow_file.stem.replace("-", " ").title(),
                    "file": workflow_file.name,
                    "path": str(workflow_file),
                }
            )

        return sorted(workflows, key=lambda w: w["name"])

    def get_config(self) -> dict:
        """Get the current BusLog configuration.

        Returns:
            Configuration dictionary.
        """
        if not self.config_path.exists():
            return {}

        return json.loads(self.config_path.read_text(encoding="utf-8"))

    def _detect_languages(self) -> list[str]:
        """Detect programming languages in the project.

        Returns:
            List of detected languages.
        """
        language_extensions = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".go": "Go",
            ".rs": "Rust",
            ".rb": "Ruby",
            ".php": "PHP",
            ".cs": "C#",
            ".cpp": "C++",
            ".c": "C",
        }

        detected = set()

        for ext, lang in language_extensions.items():
            if list(self.project_root.rglob(f"*{ext}")):
                detected.add(lang)

        return sorted(detected)

    def _generate_index(self, project_name: str) -> str:
        """Generate index.md content.

        Args:
            project_name: Name of the project.

        Returns:
            Index markdown content.
        """
        template_path = Path(__file__).parent.parent / "templates" / "index.md"
        template = template_path.read_text(encoding="utf-8")

        return template.format(
            project_name=project_name,
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"),
            total_workflows=0,
            critical_count=0,
            api_count=0,
            last_analysis="Never",
        )

    def _add_workflow_to_config(self, workflow_name: str) -> None:
        """Add a workflow to the configuration.

        Args:
            workflow_name: Name of the workflow.
        """
        config = self.get_config()

        if workflow_name not in config.get("workflows", []):
            config.setdefault("workflows", []).append(workflow_name)

            self.config_path.write_text(
                json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8"
            )
