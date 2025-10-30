"""
Prompt Generator

Generates AI prompts for analyzing codebases and detecting business logic workflows.
"""

import json
from pathlib import Path


class PromptGenerator:
    """Generates prompts for AI coding assistants."""

    def __init__(self, project_root: Path | None = None):
        """Initialize PromptGenerator.

        Args:
            project_root: Root directory of the project. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()
        self.buslog_path = self.project_root / ".business-logic"

    def generate_analysis_prompt(self) -> str:
        """Generate a prompt for analyzing the codebase.

        Returns:
            Formatted prompt string for AI analysis.
        """
        # Load config if exists
        config_path = self.buslog_path / "config.json"
        if config_path.exists():
            config = json.loads(config_path.read_text(encoding="utf-8"))
            project_name = config.get("project_name", self.project_root.name)
            languages = config.get("languages", [])
        else:
            project_name = self.project_root.name
            languages = []

        # Detect entry points
        entry_points = self._detect_entry_points()

        prompt = f"""# Business Logic Workflow Analysis

You are analyzing the codebase of **{project_name}** to document its business logic workflows.

## Project Context

- **Project Name**: {project_name}
- **Languages**: {", ".join(languages) if languages else "Auto-detect"}
- **Entry Points**: {len(entry_points)} detected

## Your Task

Analyze this codebase and identify distinct **business logic workflows**. For each workflow:

1. **Identify the workflow** - What business process does it represent?
2. **Find entry points** - API endpoints, event handlers, CLI commands, scheduled jobs
3. **Map components** - Which files, functions, and classes are involved?
4. **Track dependencies**:
   - External APIs called
   - Third-party libraries used
   - Internal services/modules used
5. **Create a flow diagram** - Use Mermaid.js syntax to visualize the flow
6. **Document relationships** - Which workflows trigger or depend on others?

## Output Format

For each workflow, create a markdown file in `.business-logic/workflows/<workflow-name>.md` using this structure:

```markdown
# Workflow: [Workflow Name]

## Description
[What this workflow does from a business perspective]

## Déclencheurs
- **Endpoint**: `[HTTP method] /api/path`
- **Event**: `[event.name]`
- **CLI**: `[command]`

## Composants Utilisés

### Fichiers
- `path/to/file.ext:10-45` - [What this file does in the workflow]

### APIs Externes
- **Service Name** (`api.example.com/endpoint`) - [Purpose]

### Services Internes
- `ServiceName` - [Purpose]

### Librairies Tierces
- `package-name` (v1.0.0) - [How it's used]

## Flux d'Exécution

```mermaid
graph TD
    A[Start Point] --> B{{Decision}}
    B -->|Path 1| C[Action]
    B -->|Path 2| D[Action]
    C --> E[End]
    D --> E
```

## Dépendances Métier

### Déclenche
- `other-workflow` - [When/Why]

### Requis par
- `other-workflow` - [When/Why]

## Notes & Annotations

_Key points, gotchas, or important business rules_
```

## Detected Entry Points

{self._format_entry_points(entry_points)}

## Analysis Guidelines

1. **Focus on business value** - Not every function is a workflow
2. **Look for these patterns**:
   - API route handlers (REST, GraphQL endpoints)
   - Event listeners/handlers
   - Scheduled tasks (cron jobs)
   - CLI commands
   - Message queue consumers
   - Background jobs

3. **Identify external interactions**:
   - HTTP API calls to external services
   - Database operations (especially complex transactions)
   - File system operations
   - Email/SMS sending
   - Payment processing
   - Authentication/authorization flows

4. **Map data flows** - How does data move through the system?

5. **Note business rules** - Special conditions, validations, or constraints

## Getting Started

Begin by exploring the entry points listed above. For each one, trace the code execution path and identify the business purpose.

Start with the most critical or frequently-used workflows first (authentication, core data operations, payment flows, etc.).

## Questions to Ask

- What problem does this code solve for the end user?
- What happens if this workflow fails?
- Which external systems does this interact with?
- What are the success/failure conditions?
- Are there any business rules or constraints?

Good luck! Create comprehensive, well-documented workflows that will help developers understand the business logic at a glance.
"""

        return prompt

    def _detect_entry_points(self) -> list[dict]:
        """Detect potential entry points in the codebase.

        Returns:
            List of entry point information.
        """
        entry_points = []

        # Common patterns for different languages
        patterns = {
            "Python FastAPI/Flask": ["@app.", "@router.", "@bp.route"],
            "JavaScript/TypeScript Express": ["app.get", "app.post", "router.get", "router.post"],
            "Python Django": ["def get(", "def post(", "path("],
            "CLI Commands": ["@click.", "@typer.", "argparse"],
            "Event Handlers": ["@event.", ".on(", "addEventListener"],
            "Scheduled Jobs": ["@cron", "@schedule", "cron.schedule"],
        }

        for pattern_name, keywords in patterns.items():
            for keyword in keywords:
                # Simple search in Python files (can be extended)
                for file_path in self.project_root.rglob("*.py"):
                    if file_path.is_file() and ".venv" not in str(file_path):
                        try:
                            content = file_path.read_text(encoding="utf-8")
                            if keyword in content:
                                entry_points.append(
                                    {
                                        "type": pattern_name,
                                        "file": str(file_path.relative_to(self.project_root)),
                                        "pattern": keyword,
                                    }
                                )
                                break  # One match per file per pattern
                        except Exception:
                            continue

        return entry_points

    def _format_entry_points(self, entry_points: list[dict]) -> str:
        """Format entry points for display in prompt.

        Args:
            entry_points: List of entry point information.

        Returns:
            Formatted string.
        """
        if not entry_points:
            return "_No entry points detected. You'll need to explore the codebase manually._"

        formatted = []
        grouped = {}

        # Group by type
        for ep in entry_points:
            ep_type = ep["type"]
            if ep_type not in grouped:
                grouped[ep_type] = []
            grouped[ep_type].append(ep["file"])

        # Format
        for ep_type, files in grouped.items():
            formatted.append(f"### {ep_type}")
            for file in files[:5]:  # Limit to 5 per type
                formatted.append(f"- `{file}`")
            if len(files) > 5:
                formatted.append(f"- _(+{len(files) - 5} more)_")
            formatted.append("")

        return "\n".join(formatted)
