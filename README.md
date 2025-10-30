# BusLog - Business Logic Documentation Tool

**Visualize and document your codebase workflows with AI**

BusLog is a lightweight, language-agnostic CLI tool that helps developers document, visualize, and understand business logic in any codebase. It leverages AI agents (Claude, Cursor, Windsurf, etc.) to automatically detect and document workflows, then presents them in an interactive web interface.

## Features

- **Language Agnostic**: Works with any programming language or framework
- **AI-Powered**: Generates prompts for your favorite AI coding assistant
- **Lightweight**: Just markdown files and JSON - version control friendly
- **Interactive Visualization**: Web interface with collapsible sections and Mermaid diagrams
- **Zero Lock-in**: All documentation stored as readable markdown files
- **Solo-Friendly**: Perfect for solo developers and small teams

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/buslog.git
cd buslog

# Install dependencies
pip install -e .
```

## Quick Start

```bash
# Initialize BusLog in your project
buslog init

# Add a new workflow manually
buslog add user-authentication

# List all workflows
buslog list

# Launch web interface
buslog serve
```

## How It Works

1. **Initialize**: `buslog init` creates a `.business-logic/` folder with templates
2. **Analyze**: Use the generated AI prompt with your coding assistant to detect workflows
3. **Document**: AI or you create structured markdown files for each workflow
4. **Visualize**: Launch the web interface to browse and enrich your documentation
5. **Collaborate**: Commit `.business-logic/` to Git and share with your team

## Workflow Structure

Each workflow is documented in markdown with:
- **Description**: What the workflow does
- **Triggers**: API endpoints, events, CLI commands
- **Components**: Files, functions, external APIs, libraries
- **Flow Diagram**: Mermaid.js visualization
- **Dependencies**: Related workflows
- **Annotations**: Team notes and comments

## Tech Stack

- **CLI**: Python + Typer
- **Web Server**: FastAPI
- **Frontend**: Vanilla JS + Mermaid.js
- **Storage**: Markdown + JSON

## Roadmap

- [ ] v0.1: Core CLI and web interface
- [ ] v0.2: Advanced AI prompt generation
- [ ] v0.3: Multi-repo support
- [ ] v0.4: Export to various formats (PDF, HTML)
- [ ] v1.0: Stable release

## Contributing

Contributions welcome! This project is in active development.

## License

MIT License - See LICENSE file for details

## Author

Created by **PoulpYBifle** (contact@sachapreneur.fr)

---

*Generated with [Claude Code](https://claude.com/claude-code)*
