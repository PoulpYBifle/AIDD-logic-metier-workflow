"""
Code Analyzer

Performs static analysis of codebases to detect patterns and structures.
"""

import re
from pathlib import Path


class CodeAnalyzer:
    """Analyzes code structure and patterns."""

    def __init__(self, project_root: Path | None = None):
        """Initialize CodeAnalyzer.

        Args:
            project_root: Root directory of the project. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()

    def analyze_structure(self) -> dict:
        """Analyze the overall project structure.

        Returns:
            Dictionary with project structure information.
        """
        return {
            "languages": self._detect_languages(),
            "frameworks": self._detect_frameworks(),
            "file_count": self._count_files(),
            "entry_points": self._find_entry_points(),
        }

    def _detect_languages(self) -> list[str]:
        """Detect programming languages in the project.

        Returns:
            List of detected languages.
        """
        language_extensions = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".jsx": "React",
            ".tsx": "React/TypeScript",
            ".java": "Java",
            ".go": "Go",
            ".rs": "Rust",
            ".rb": "Ruby",
            ".php": "PHP",
            ".cs": "C#",
            ".cpp": "C++",
            ".c": "C",
            ".swift": "Swift",
            ".kt": "Kotlin",
        }

        detected = {}

        for ext, lang in language_extensions.items():
            files = list(self.project_root.rglob(f"*{ext}"))
            if files:
                detected[lang] = len(files)

        return [lang for lang, _ in sorted(detected.items(), key=lambda x: x[1], reverse=True)]

    def _detect_frameworks(self) -> list[str]:
        """Detect frameworks used in the project.

        Returns:
            List of detected frameworks.
        """
        frameworks = []

        # Check for common framework indicators
        indicators = {
            "FastAPI": ["from fastapi import", "import fastapi"],
            "Django": ["from django.", "import django"],
            "Flask": ["from flask import", "import flask"],
            "Express": ["require('express')", "from 'express'"],
            "React": ["from 'react'", "import React"],
            "Vue": ["from 'vue'", "import Vue"],
            "Angular": ["@angular/", "import { Component }"],
            "Spring": ["@SpringBootApplication", "org.springframework"],
            "Rails": ["class.*< ApplicationController", "Rails.application"],
        }

        for framework, patterns in indicators.items():
            if self._search_patterns(patterns):
                frameworks.append(framework)

        return frameworks

    def _count_files(self) -> dict[str, int]:
        """Count files by type.

        Returns:
            Dictionary with file counts.
        """
        counts = {
            "total": 0,
            "source": 0,
            "test": 0,
            "config": 0,
        }

        for file in self.project_root.rglob("*"):
            if file.is_file() and not self._is_excluded(file):
                counts["total"] += 1

                if file.suffix in [".py", ".js", ".ts", ".java", ".go", ".rs"]:
                    counts["source"] += 1

                if "test" in file.name.lower() or "test" in str(file.parent).lower():
                    counts["test"] += 1

                if file.suffix in [".json", ".yaml", ".yml", ".toml", ".ini", ".env"]:
                    counts["config"] += 1

        return counts

    def _find_entry_points(self) -> list[dict[str, str]]:
        """Find potential entry points in the codebase.

        Returns:
            List of entry point information.
        """
        entry_points = []

        # Search for common entry point patterns
        patterns = {
            "API Endpoint": [
                r"@app\.(get|post|put|delete|patch)\(['\"]([^'\"]+)",
                r"@router\.(get|post|put|delete|patch)\(['\"]([^'\"]+)",
                r"app\.(get|post|put|delete|patch)\(['\"]([^'\"]+)",
            ],
            "CLI Command": [
                r"@click\.command\(\)",
                r"@typer\.command\(\)",
                r"def main\(",
            ],
            "Event Handler": [
                r"@event\.",
                r"\.on\(['\"]([^'\"]+)",
                r"addEventListener\(['\"]([^'\"]+)",
            ],
        }

        for entry_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = self._search_pattern_in_files(pattern)
                for file, match in matches:
                    entry_points.append(
                        {
                            "type": entry_type,
                            "file": str(file.relative_to(self.project_root)),
                            "match": match,
                        }
                    )

        return entry_points

    def _search_patterns(self, patterns: list[str]) -> bool:
        """Search for patterns in source files.

        Args:
            patterns: List of string patterns to search for.

        Returns:
            True if any pattern is found.
        """
        for file in self.project_root.rglob("*"):
            if file.is_file() and not self._is_excluded(file):
                try:
                    content = file.read_text(encoding="utf-8")
                    if any(pattern in content for pattern in patterns):
                        return True
                except Exception:
                    continue

        return False

    def _search_pattern_in_files(self, pattern: str) -> list[tuple]:
        """Search for a regex pattern in source files.

        Args:
            pattern: Regex pattern to search for.

        Returns:
            List of (file, match) tuples.
        """
        matches = []

        for file in self.project_root.rglob("*"):
            if file.is_file() and not self._is_excluded(file):
                try:
                    content = file.read_text(encoding="utf-8")
                    for match in re.finditer(pattern, content):
                        matches.append((file, match.group(0)))
                except Exception:
                    continue

        return matches

    def _is_excluded(self, path: Path) -> bool:
        """Check if a path should be excluded from analysis.

        Args:
            path: Path to check.

        Returns:
            True if path should be excluded.
        """
        excluded_patterns = [
            ".git",
            ".venv",
            "venv",
            "node_modules",
            "__pycache__",
            ".pytest_cache",
            "dist",
            "build",
            ".business-logic",
        ]

        path_str = str(path)
        return any(pattern in path_str for pattern in excluded_patterns)
