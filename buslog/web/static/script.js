/**
 * BusLog - Client-side JavaScript
 */

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('BusLog initialized');
});

/**
 * Toggle workflow visibility
 * @param {string} workflowName - Name of the workflow to toggle
 */
async function toggleWorkflow(workflowName) {
    const contentDiv = document.getElementById(`workflow-${workflowName}`);
    const header = contentDiv.previousElementSibling;
    const toggleIcon = header.querySelector('.toggle-icon');

    if (contentDiv.style.display === 'none') {
        // Show and load content
        contentDiv.style.display = 'block';
        toggleIcon.textContent = '▲';

        // Load content if not already loaded
        if (contentDiv.querySelector('.loading')) {
            await loadWorkflowContent(workflowName, contentDiv);
        }
    } else {
        // Hide
        contentDiv.style.display = 'none';
        toggleIcon.textContent = '▼';
    }
}

/**
 * Load workflow content via API
 * @param {string} workflowName - Name of the workflow
 * @param {HTMLElement} container - Container element to render into
 */
async function loadWorkflowContent(workflowName, container) {
    try {
        const response = await fetch(`/api/workflows/${workflowName}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        // Parse markdown
        container.innerHTML = marked.parse(data.content);

        // Process Mermaid diagrams
        await renderMermaidDiagrams(container);

        // Add copy buttons to code blocks
        addCopyButtons(container);

    } catch (error) {
        container.innerHTML = `
            <div class="error">
                <p>Error loading workflow: ${error.message}</p>
                <p>Please check that the workflow file exists and is valid.</p>
            </div>
        `;
    }
}

/**
 * Render Mermaid diagrams in a container
 * @param {HTMLElement} container - Container with mermaid code blocks
 */
async function renderMermaidDiagrams(container) {
    const mermaidBlocks = container.querySelectorAll('code.language-mermaid');

    for (const block of mermaidBlocks) {
        try {
            const mermaidDiv = document.createElement('div');
            mermaidDiv.className = 'mermaid';
            mermaidDiv.textContent = block.textContent;

            // Replace the pre/code block with the mermaid div
            const pre = block.closest('pre');
            if (pre) {
                pre.replaceWith(mermaidDiv);
            }
        } catch (error) {
            console.error('Error rendering Mermaid diagram:', error);
        }
    }

    // Re-run Mermaid rendering
    if (typeof mermaid !== 'undefined') {
        mermaid.init(undefined, container.querySelectorAll('.mermaid'));
    }
}

/**
 * Add copy buttons to code blocks
 * @param {HTMLElement} container - Container with code blocks
 */
function addCopyButtons(container) {
    const codeBlocks = container.querySelectorAll('pre code:not(.language-mermaid)');

    codeBlocks.forEach(codeBlock => {
        const pre = codeBlock.parentElement;
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';
        button.onclick = () => copyToClipboard(codeBlock.textContent, button);

        pre.style.position = 'relative';
        pre.appendChild(button);
    });
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @param {HTMLElement} button - Button element to show feedback
 */
async function copyToClipboard(text, button) {
    try {
        await navigator.clipboard.writeText(text);
        const originalText = button.textContent;
        button.textContent = '✓ Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    } catch (error) {
        console.error('Failed to copy:', error);
        button.textContent = '✗ Failed';
    }
}

/**
 * Save annotation for a workflow
 * @param {string} workflowName - Name of the workflow
 * @param {string} text - Annotation text
 * @param {string} author - Author name
 */
async function saveAnnotation(workflowName, text, author = 'User') {
    try {
        // Load existing annotations
        const response = await fetch(`/api/workflows/${workflowName}/annotations`);
        const data = await response.json();
        const annotations = data.annotations || [];

        // Add new annotation
        annotations.push({
            text: text,
            author: author,
            date: new Date().toISOString().split('T')[0]
        });

        // Save
        const saveResponse = await fetch(`/api/workflows/${workflowName}/annotations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ annotations })
        });

        if (!saveResponse.ok) {
            throw new Error('Failed to save annotation');
        }

        return true;
    } catch (error) {
        console.error('Error saving annotation:', error);
        throw error;
    }
}

/**
 * Search workflows by text
 * @param {string} query - Search query
 */
function searchWorkflows(query) {
    const workflowCards = document.querySelectorAll('.workflow-card');
    const lowerQuery = query.toLowerCase();

    workflowCards.forEach(card => {
        const name = card.querySelector('h3').textContent.toLowerCase();
        const matches = name.includes(lowerQuery);

        card.style.display = matches ? 'block' : 'none';
    });
}

// Export functions for use in HTML
window.toggleWorkflow = toggleWorkflow;
window.loadWorkflowContent = loadWorkflowContent;
window.saveAnnotation = saveAnnotation;
window.searchWorkflows = searchWorkflows;
