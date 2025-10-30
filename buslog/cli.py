"""
BusLog CLI - Command Line Interface

Main entry point for the BusLog tool.
"""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from buslog.core.prompt_generator import PromptGenerator
from buslog.core.workflow_manager import WorkflowManager
from buslog.web.server import start_server

app = typer.Typer(
    name="buslog",
    help="Business Logic Documentation Tool - Visualize and document your codebase workflows",
    add_completion=False,
)

console = Console()


@app.command()
def init(
    project_name: str | None = typer.Option(None, "--name", "-n", help="Project name"),
    force: bool = typer.Option(False, "--force", "-f", help="Force re-initialization"),
):
    """
    Initialize BusLog in the current project.
    Creates .business-logic/ folder with templates and configuration.
    """
    console.print("[bold blue]>> Initializing BusLog...[/bold blue]")

    manager = WorkflowManager()

    if manager.is_initialized() and not force:
        console.print("[yellow]! BusLog is already initialized in this project.[/yellow]")
        console.print("[dim]Use --force to re-initialize[/dim]")
        return

    try:
        manager.initialize(project_name=project_name, force=force)
        console.print("[bold green][OK] BusLog initialized successfully![/bold green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("  1. Run [cyan]buslog analyze[/cyan] to generate an AI prompt")
        console.print("  2. Use the prompt with your AI assistant (Claude, Cursor, etc.)")
        console.print("  3. Run [cyan]buslog serve[/cyan] to view documentation")
        console.print("  4. Use [cyan]buslog add <workflow-name>[/cyan] to add workflows manually")
    except Exception as e:
        console.print(f"[bold red]❌ Error during initialization: {e}[/bold red]")
        sys.exit(1)


@app.command()
def add(
    workflow_name: str = typer.Argument(
        ..., help="Name of the workflow (e.g., user-authentication)"
    ),
):
    """
    Create a new workflow documentation file.
    """
    manager = WorkflowManager()

    if not manager.is_initialized():
        console.print(
            "[bold red][ERROR] BusLog is not initialized. Run 'buslog init' first.[/bold red]"
        )
        sys.exit(1)

    try:
        workflow_path = manager.add_workflow(workflow_name)
        console.print(f"[bold green][OK] Workflow created:[/bold green] {workflow_path}")
        console.print(
            "\n[dim]Edit the file to document your workflow, then run 'buslog serve' to view it.[/dim]"
        )
    except FileExistsError:
        console.print(f"[yellow]! Workflow '{workflow_name}' already exists.[/yellow]")
    except Exception as e:
        console.print(f"[bold red][ERROR] Error creating workflow: {e}[/bold red]")
        sys.exit(1)


@app.command()
def list():
    """
    List all documented workflows.
    """
    manager = WorkflowManager()

    if not manager.is_initialized():
        console.print(
            "[bold red][ERROR] BusLog is not initialized. Run 'buslog init' first.[/bold red]"
        )
        sys.exit(1)

    workflows = manager.list_workflows()

    if not workflows:
        console.print("[yellow]No workflows found. Use 'buslog add <name>' to create one.[/yellow]")
        return

    table = Table(title="Business Logic Workflows")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("File", style="dim")
    table.add_column("Status", style="green")

    for workflow in workflows:
        table.add_row(workflow["name"], workflow["file"], "[OK] Active")

    console.print(table)
    console.print(f"\n[dim]Total: {len(workflows)} workflow(s)[/dim]")


@app.command()
def analyze(
    output: Path | None = typer.Option(None, "--output", "-o", help="Output file for the prompt"),
):
    """
    Generate an AI prompt to analyze the codebase for business logic workflows.
    """
    manager = WorkflowManager()

    if not manager.is_initialized():
        console.print(
            "[bold red][ERROR] BusLog is not initialized. Run 'buslog init' first.[/bold red]"
        )
        sys.exit(1)

    console.print("[bold blue]>> Generating AI analysis prompt...[/bold blue]")

    try:
        generator = PromptGenerator()
        prompt = generator.generate_analysis_prompt()

        if output:
            output.write_text(prompt, encoding="utf-8")
            console.print(f"[bold green][OK] Prompt saved to:[/bold green] {output}")
        else:
            console.print("\n[bold cyan]" + "=" * 80 + "[/bold cyan]")
            console.print(prompt)
            console.print("[bold cyan]" + "=" * 80 + "[/bold cyan]\n")

        console.print("[dim]Copy this prompt and use it with your AI coding assistant.[/dim]")
    except Exception as e:
        console.print(f"[bold red][ERROR] Error generating prompt: {e}[/bold red]")
        sys.exit(1)


@app.command()
def serve(
    port: int = typer.Option(8080, "--port", "-p", help="Port to run the server on"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind the server to"),
):
    """
    Start the web interface to view and edit workflows.
    """
    manager = WorkflowManager()

    if not manager.is_initialized():
        console.print(
            "[bold red][ERROR] BusLog is not initialized. Run 'buslog init' first.[/bold red]"
        )
        sys.exit(1)

    console.print("[bold blue]>> Starting BusLog web interface...[/bold blue]")
    console.print(f"[dim]Server will be available at: http://{host}:{port}[/dim]")
    console.print("[dim]Press CTRL+C to stop the server[/dim]\n")

    try:
        start_server(host=host, port=port)
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped.[/yellow]")
    except Exception as e:
        console.print(f"[bold red][ERROR] Error starting server: {e}[/bold red]")
        sys.exit(1)


@app.command()
def version():
    """
    Show BusLog version information.
    """
    from buslog import __author__, __version__

    console.print(f"[bold]BusLog[/bold] version [cyan]{__version__}[/cyan]")
    console.print(f"[dim]Created by {__author__}[/dim]")


if __name__ == "__main__":
    app()
