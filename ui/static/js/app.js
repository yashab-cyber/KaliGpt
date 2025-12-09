// KaliGPT Web GUI JavaScript

let socket;
let sessionData = {
    commands: 0,
    payloads: 0,
    findings: 0
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Socket.IO
    socket = io();
    
    socket.on('connect', function() {
        console.log('Connected to server');
        updateStatus('Connected to server');
    });
    
    socket.on('status', function(data) {
        updateAIStatus(data.connected, data.model);
    });
    
    socket.on('analysis_result', function(data) {
        hideLoading();
        displayAnalysis(data.analysis);
        sessionData.commands++;
        sessionData.findings++;
        updateSessionStats();
        updateStatus('Analysis complete');
    });
    
    socket.on('error', function(data) {
        hideLoading();
        alert('Error: ' + data.message);
        updateStatus('Error occurred');
    });
    
    socket.on('progress', function(data) {
        updateStatus(data.message);
    });
    
    // Load available models
    loadModels();
    
    // Load templates
    loadTemplates();
    
    // Check status
    checkStatus();
});

// AI Connection
async function connectAI() {
    const model = document.getElementById('modelSelect').value;
    
    showLoading('Connecting to AI engine...');
    updateStatus('Connecting to ' + model + '...');
    
    try {
        const response = await fetch('/api/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ model: model })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            updateAIStatus(true, model);
            updateStatus('Connected to ' + model);
            alert('Successfully connected to ' + model);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        hideLoading();
        updateAIStatus(false, null);
        updateStatus('Connection failed');
        alert('Failed to connect: ' + error.message);
    }
}

// Load available models
async function loadModels() {
    try {
        const response = await fetch('/api/models');
        const data = await response.json();
        
        if (data.success) {
            const select = document.getElementById('modelSelect');
            select.innerHTML = '';
            
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Failed to load models:', error);
    }
}

// Analyze Command
async function analyzeCommand() {
    const commandOutput = document.getElementById('commandInput').value.trim();
    
    if (!commandOutput) {
        alert('Please enter command output to analyze');
        return;
    }
    
    showLoading('Analyzing with AI...');
    updateStatus('Analyzing command output...');
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ output: commandOutput })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            displayAnalysis(data.analysis);
            sessionData.commands++;
            sessionData.findings++;
            updateSessionStats();
            updateStatus('Analysis complete');
            addToHistory(commandOutput, data.analysis);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        hideLoading();
        updateStatus('Analysis failed');
        alert('Analysis failed: ' + error.message);
    }
}

// Display analysis
function displayAnalysis(analysis) {
    const output = document.getElementById('aiOutput');
    const timestamp = new Date().toLocaleTimeString();
    
    const entry = document.createElement('div');
    entry.className = 'analysis-entry';
    entry.innerHTML = `
        <div style="color: var(--text-secondary); margin-bottom: 0.5rem;">
            [${timestamp}] AI Analysis:
        </div>
        <div style="color: var(--success);">
            ${analysis.replace(/\n/g, '<br>')}
        </div>
        <hr style="border: 1px solid var(--border); margin: 1rem 0;">
    `;
    
    output.appendChild(entry);
    output.scrollTop = output.scrollHeight;
}

// Load templates
async function loadTemplates() {
    try {
        const response = await fetch('/api/templates');
        const data = await response.json();
        
        if (data.success) {
            window.templatesData = data.templates;
            updateTemplates();
        }
    } catch (error) {
        console.error('Failed to load templates:', error);
    }
}

// Update template list
function updateTemplates() {
    if (!window.templatesData) return;
    
    const payloadType = document.getElementById('payloadType').value;
    const templateSelect = document.getElementById('templateSelect');
    
    templateSelect.innerHTML = '<option value="">Select template...</option>';
    
    if (window.templatesData[payloadType]) {
        window.templatesData[payloadType].forEach(template => {
            const option = document.createElement('option');
            option.value = template;
            option.textContent = template;
            templateSelect.appendChild(option);
        });
    }
}

// Generate payload
async function generatePayload() {
    const payloadType = document.getElementById('payloadType').value;
    const template = document.getElementById('templateSelect').value;
    const varsText = document.getElementById('payloadVars').value;
    
    if (!template) {
        alert('Please select a template');
        return;
    }
    
    let variables;
    try {
        variables = JSON.parse(varsText);
    } catch (error) {
        alert('Invalid JSON in variables field');
        return;
    }
    
    showLoading('Generating payload...');
    updateStatus('Generating payload...');
    
    try {
        const response = await fetch('/api/payload/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: payloadType,
                template: template,
                variables: variables
            })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            displayPayload(data.payload);
            sessionData.payloads++;
            updateSessionStats();
            updateStatus('Payload generated successfully');
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        hideLoading();
        updateStatus('Payload generation failed');
        alert('Failed to generate payload: ' + error.message);
    }
}

// Generate AI payload
async function generateAIPayload() {
    const targetInfoText = document.getElementById('targetInfo').value;
    
    let targetInfo;
    try {
        targetInfo = JSON.parse(targetInfoText);
    } catch (error) {
        alert('Invalid JSON in target information field');
        return;
    }
    
    showLoading('Generating AI payload...');
    updateStatus('Generating AI-powered payload...');
    
    try {
        const response = await fetch('/api/payload/ai-generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ target_info: targetInfo })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            displayPayload(data.payload);
            sessionData.payloads++;
            updateSessionStats();
            updateStatus('AI payload generated successfully');
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        hideLoading();
        updateStatus('AI payload generation failed');
        alert('Failed to generate AI payload: ' + error.message);
    }
}

// Display payload
function displayPayload(payload) {
    const output = document.getElementById('payloadOutput');
    output.textContent = payload;
}

// Copy payload
function copyPayload() {
    const payload = document.getElementById('payloadOutput').textContent;
    
    if (!payload) {
        alert('No payload to copy');
        return;
    }
    
    navigator.clipboard.writeText(payload).then(() => {
        updateStatus('Payload copied to clipboard');
    }).catch(error => {
        alert('Failed to copy: ' + error.message);
    });
}

// Preview report
async function previewReport() {
    const format = document.querySelector('input[name="reportFormat"]:checked').value;
    const target = document.getElementById('targetName').value;
    
    showLoading('Generating report...');
    updateStatus('Generating report preview...');
    
    try {
        const response = await fetch('/api/report/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                format: format,
                target: target
            })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            const preview = document.getElementById('reportPreview');
            preview.textContent = data.report;
            updateStatus('Report preview generated');
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        hideLoading();
        updateStatus('Report generation failed');
        alert('Failed to generate report: ' + error.message);
    }
}

// Export report
function exportReport() {
    const report = document.getElementById('reportPreview').textContent;
    const format = document.querySelector('input[name="reportFormat"]:checked').value;
    
    if (!report) {
        alert('Please generate a report preview first');
        return;
    }
    
    const extensions = {
        markdown: '.md',
        html: '.html',
        json: '.json'
    };
    
    const filename = `kaligpt_report_${Date.now()}${extensions[format]}`;
    
    const blob = new Blob([report], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
    
    updateStatus('Report exported as ' + filename);
}

// Clear session
async function clearSession() {
    if (!confirm('Clear current session? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/session/clear', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('commandInput').value = '';
            document.getElementById('aiOutput').innerHTML = '';
            document.getElementById('payloadOutput').textContent = '';
            document.getElementById('reportPreview').textContent = '';
            document.getElementById('historyList').innerHTML = '';
            
            sessionData = { commands: 0, payloads: 0, findings: 0 };
            updateSessionStats();
            updateStatus('Session cleared');
        }
    } catch (error) {
        alert('Failed to clear session: ' + error.message);
    }
}

// Clear input
function clearInput() {
    document.getElementById('commandInput').value = '';
}

// Add to history
function addToHistory(command, analysis) {
    const historyList = document.getElementById('historyList');
    const timestamp = new Date().toLocaleTimeString();
    
    const item = document.createElement('div');
    item.className = 'history-item';
    item.innerHTML = `
        <div class="history-item-header">
            <span>Entry ${sessionData.commands}</span>
            <span>${timestamp}</span>
        </div>
        <div class="history-item-content">
            <strong>Input:</strong><br>
            ${command.substring(0, 200)}${command.length > 200 ? '...' : ''}<br><br>
            <strong>Analysis:</strong><br>
            ${analysis.substring(0, 300)}${analysis.length > 300 ? '...' : ''}
        </div>
    `;
    
    historyList.insertBefore(item, historyList.firstChild);
}

// Tab switching
function switchTab(tabName) {
    // Remove active class from all tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Add active class to selected tab
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

// Update AI status
function updateAIStatus(connected, model) {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = document.querySelector('.status-text');
    
    if (connected) {
        statusIndicator.classList.remove('offline');
        statusIndicator.classList.add('online');
        statusText.textContent = 'Connected: ' + model;
    } else {
        statusIndicator.classList.remove('online');
        statusIndicator.classList.add('offline');
        statusText.textContent = 'Disconnected';
    }
}

// Update status message
function updateStatus(message) {
    document.getElementById('statusMessage').textContent = message;
}

// Update session stats
function updateSessionStats() {
    document.getElementById('commandCount').textContent = sessionData.commands;
    document.getElementById('payloadCount').textContent = sessionData.payloads;
    document.getElementById('findingCount').textContent = sessionData.findings;
}

// Show loading overlay
function showLoading(message) {
    const overlay = document.getElementById('loadingOverlay');
    const messageEl = document.getElementById('loadingMessage');
    messageEl.textContent = message;
    overlay.style.display = 'flex';
}

// Hide loading overlay
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Check status
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.success) {
            updateAIStatus(data.connected, data.model);
            sessionData.commands = data.session_items;
            updateSessionStats();
        }
    } catch (error) {
        console.error('Failed to check status:', error);
    }
}
