Analyze the current codebase using BusLog and document all business logic workflows.

## Instructions

1. **Initialize BusLog** if not already done:
   - Check: `python -m buslog.cli list`
   - Init if needed: `python -m buslog.cli init`

2. **Analyze the codebase** to identify workflows:
   - Look for API endpoints (routes, controllers)
   - Find event handlers and listeners
   - Locate background jobs and scheduled tasks
   - Identify database operations and transactions

3. **Document each workflow** you find:
   - Create workflow: `python -m buslog.cli add workflow-name`
   - Edit `.business-logic/workflows/workflow-name.md`
   - Include: description, triggers, files, dependencies, flow diagram

4. **For each workflow, document**:
   - **Description**: Business purpose (what problem it solves)
   - **Déclencheurs**: Entry points (endpoints, events, commands)
   - **Fichiers**: All files involved with line numbers
   - **APIs Externes**: External services called
   - **Services Internes**: Internal services/repositories used
   - **Librairies**: Third-party packages and their role
   - **Flux d'Exécution**: Mermaid diagram showing the flow
   - **Dépendances Métier**: Related workflows

5. **Present the results**:
   - List all workflows documented
   - Show where documentation is saved
   - Provide command to view: `python -m buslog.cli serve`

## Expected Output

```
✅ BusLog Analysis Complete

Documented [N] workflows:
1. [Workflow Name] - [Brief description]
2. [Workflow Name] - [Brief description]
...

📁 Documentation: .business-logic/workflows/
🌐 View: python -m buslog.cli serve (http://localhost:8080)
```

## Tips

- Be thorough: trace the complete execution path
- Include all files, even utilities and helpers
- Add Mermaid diagrams for visual understanding
- Document business rules and edge cases
- Use line numbers for easy code navigation
