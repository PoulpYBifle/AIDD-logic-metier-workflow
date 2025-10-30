"""
Web Server

FastAPI server for the BusLog web interface.
"""

import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from buslog.core.workflow_manager import WorkflowManager


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application.
    """
    app = FastAPI(
        title="BusLog",
        description="Business Logic Documentation Tool",
        version="0.1.0",
    )

    # Setup paths
    web_dir = Path(__file__).parent
    static_dir = web_dir / "static"
    templates_dir = web_dir / "templates"

    # Create directories if they don't exist
    static_dir.mkdir(exist_ok=True)
    templates_dir.mkdir(exist_ok=True)

    # Mount static files if directory exists and has files
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Setup templates
    templates = Jinja2Templates(directory=str(templates_dir))

    # Initialize workflow manager
    manager = WorkflowManager()

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Render the main page."""
        try:
            workflows = manager.list_workflows()
            config = manager.get_config()

            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "workflows": workflows,
                    "project_name": config.get("project_name", "Unknown Project"),
                    "total_workflows": len(workflows),
                },
            )
        except Exception as e:
            return HTMLResponse(
                content=f"<h1>Error loading BusLog</h1><p>{str(e)}</p>", status_code=500
            )

    @app.get("/api/workflows")
    async def get_workflows():
        """Get all workflows as JSON."""
        workflows = manager.list_workflows()
        return JSONResponse(content={"workflows": workflows})

    @app.get("/api/workflows/{workflow_name}")
    async def get_workflow(workflow_name: str):
        """Get a specific workflow's content."""
        workflow_path = manager.workflows_path / f"{workflow_name}.md"

        if not workflow_path.exists():
            raise HTTPException(status_code=404, detail="Workflow not found")

        content = workflow_path.read_text(encoding="utf-8")
        return JSONResponse(content={"name": workflow_name, "content": content})

    @app.get("/api/config")
    async def get_config():
        """Get BusLog configuration."""
        config = manager.get_config()
        return JSONResponse(content=config)

    @app.post("/api/workflows/{workflow_name}/annotations")
    async def save_annotations(workflow_name: str, request: Request):
        """Save annotations for a workflow."""
        try:
            data = await request.json()
            annotations = data.get("annotations", [])

            # Save annotations to JSON file
            annotations_dir = manager.buslog_path / "annotations"
            annotations_dir.mkdir(exist_ok=True)

            annotation_file = annotations_dir / f"{workflow_name}.json"
            annotation_file.write_text(
                json.dumps(annotations, indent=2, ensure_ascii=False), encoding="utf-8"
            )

            return JSONResponse(content={"success": True})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    @app.get("/api/workflows/{workflow_name}/annotations")
    async def get_annotations(workflow_name: str):
        """Get annotations for a workflow."""
        annotations_file = manager.buslog_path / "annotations" / f"{workflow_name}.json"

        if not annotations_file.exists():
            return JSONResponse(content={"annotations": []})

        annotations = json.loads(annotations_file.read_text(encoding="utf-8"))
        return JSONResponse(content={"annotations": annotations})

    @app.get("/workflow/{workflow_name}", response_class=HTMLResponse)
    async def view_workflow(request: Request, workflow_name: str):
        """Render a single workflow page."""
        workflow_path = manager.workflows_path / f"{workflow_name}.md"

        if not workflow_path.exists():
            return HTMLResponse(content="<h1>Workflow not found</h1>", status_code=404)

        content = workflow_path.read_text(encoding="utf-8")

        # Load annotations if they exist
        annotations_file = manager.buslog_path / "annotations" / f"{workflow_name}.json"
        annotations = []
        if annotations_file.exists():
            annotations = json.loads(annotations_file.read_text(encoding="utf-8"))

        return templates.TemplateResponse(
            "workflow.html",
            {
                "request": request,
                "workflow_name": workflow_name,
                "workflow_content": content,
                "annotations": annotations,
            },
        )

    return app


def start_server(host: str = "127.0.0.1", port: int = 8080):
    """Start the web server.

    Args:
        host: Host to bind to.
        port: Port to listen on.
    """
    app = create_app()
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
