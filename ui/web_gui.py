#!/usr/bin/env python3
"""
KaliGPT Web GUI - Modern Web Interface using Flask
AI-Powered Penetration Testing Assistant
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import os
import sys
import json
from pathlib import Path
from datetime import datetime
import threading

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.ai_engine import AIEngine
except ImportError:
    # Fallback for development/testing
    AIEngine = None

from payloads.generator import PayloadGenerator

try:
    from reporting.report_builder import ReportBuilder as ReportGenerator
except ImportError:
    # Fallback for development/testing
    ReportGenerator = None

from models.model_selector import ModelSelector

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.config['SECRET_KEY'] = 'kaligpt-secret-key-change-in-production'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state
state = {
    'ai_engine': None,
    'payload_generator': None,
    'report_generator': ReportGenerator(),
    'model_selector': ModelSelector(),
    'current_session': {
        'commands': [],
        'outputs': [],
        'payloads': [],
        'findings': []
    },
    'connected': False,
    'current_model': None
}


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available AI models"""
    try:
        models = state['model_selector'].list_available_models()
        return jsonify({
            'success': True,
            'models': models
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/connect', methods=['POST'])
def connect_ai():
    """Connect to AI engine"""
    try:
        data = request.json
        model = data.get('model', 'gpt-5.1')
        
        # Initialize AI engine
        state['ai_engine'] = AIEngine(model=model)
        state['payload_generator'] = PayloadGenerator(state['ai_engine'])
        state['connected'] = True
        state['current_model'] = model
        
        return jsonify({
            'success': True,
            'message': f'Connected to {model}',
            'model': model
        })
    except Exception as e:
        state['connected'] = False
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze command output"""
    if not state['connected']:
        return jsonify({
            'success': False,
            'error': 'AI engine not connected'
        }), 400
    
    try:
        data = request.json
        command_output = data.get('output', '')
        
        prompt = f"""Analyze this penetration testing command output and provide:
1. What was discovered
2. Security implications
3. Next recommended steps
4. Potential vulnerabilities

Output:
{command_output}
"""
        
        # Analyze with AI
        response = state['ai_engine'].analyze(prompt)
        
        # Store in session
        state['current_session']['commands'].append(command_output)
        state['current_session']['outputs'].append(response)
        
        return jsonify({
            'success': True,
            'analysis': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available payload templates"""
    try:
        if not state['payload_generator']:
            state['payload_generator'] = PayloadGenerator()
        
        templates = state['payload_generator'].list_templates()
        
        return jsonify({
            'success': True,
            'templates': templates
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/payload/generate', methods=['POST'])
def generate_payload():
    """Generate payload from template"""
    try:
        if not state['payload_generator']:
            state['payload_generator'] = PayloadGenerator()
        
        data = request.json
        payload_type = data.get('type')
        template = data.get('template')
        variables = data.get('variables', {})
        
        payload = state['payload_generator'].get_from_template(
            payload_type, template, variables
        )
        
        # Store in session
        state['current_session']['payloads'].append({
            'type': payload_type,
            'template': template,
            'payload': payload,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'payload': payload
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/payload/ai-generate', methods=['POST'])
def ai_generate_payload():
    """Generate payload using AI"""
    if not state['connected']:
        return jsonify({
            'success': False,
            'error': 'AI engine not connected'
        }), 400
    
    try:
        data = request.json
        target_info = data.get('target_info', {})
        
        payload = state['payload_generator'].generate_with_ai(target_info)
        
        # Store in session
        state['current_session']['payloads'].append({
            'type': 'ai_generated',
            'target_info': target_info,
            'payload': payload,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'payload': payload
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/report/preview', methods=['POST'])
def preview_report():
    """Generate report preview"""
    try:
        data = request.json
        fmt = data.get('format', 'markdown')
        
        report_data = {
            'target': data.get('target', 'Target System'),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'findings': state['current_session']['outputs'],
            'payloads': state['current_session']['payloads']
        }
        
        if fmt == 'markdown':
            report = state['report_generator'].generate_markdown(report_data)
        elif fmt == 'html':
            report = state['report_generator'].generate_html(report_data)
        else:
            report = json.dumps(report_data, indent=2)
        
        return jsonify({
            'success': True,
            'report': report,
            'format': fmt
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/session/save', methods=['POST'])
def save_session():
    """Save current session"""
    try:
        data = request.json
        filename = data.get('filename', f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        session_path = Path('sessions') / filename
        session_path.parent.mkdir(exist_ok=True)
        
        with open(session_path, 'w') as f:
            json.dump(state['current_session'], f, indent=2)
        
        return jsonify({
            'success': True,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/session/load', methods=['POST'])
def load_session():
    """Load a saved session"""
    try:
        data = request.json
        filename = data.get('filename')
        
        session_path = Path('sessions') / filename
        
        with open(session_path, 'r') as f:
            state['current_session'] = json.load(f)
        
        return jsonify({
            'success': True,
            'session': state['current_session']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/session/clear', methods=['POST'])
def clear_session():
    """Clear current session"""
    state['current_session'] = {
        'commands': [],
        'outputs': [],
        'payloads': [],
        'findings': []
    }
    
    return jsonify({
        'success': True,
        'message': 'Session cleared'
    })


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current system status"""
    return jsonify({
        'success': True,
        'connected': state['connected'],
        'model': state['current_model'],
        'session_items': len(state['current_session']['commands'])
    })


# WebSocket events for real-time updates
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status', {
        'connected': state['connected'],
        'model': state['current_model']
    })


@socketio.on('analyze_stream')
def handle_analyze_stream(data):
    """Stream analysis results"""
    if not state['connected']:
        emit('error', {'message': 'AI engine not connected'})
        return
    
    try:
        command_output = data.get('output', '')
        
        # Emit progress
        emit('progress', {'message': 'Analyzing with AI...'})
        
        prompt = f"""Analyze this penetration testing command output:
{command_output}
"""
        
        response = state['ai_engine'].analyze(prompt)
        
        # Emit result
        emit('analysis_result', {
            'analysis': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        emit('error', {'message': str(e)})


def run_web_gui(host='0.0.0.0', port=5000, debug=False):
    """Run the web GUI"""
    print(f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🔒 KaliGPT Web Interface                              ║
║                                                          ║
║   Access the GUI at: http://localhost:{port}            ║
║                                                          ║
║   Press Ctrl+C to stop                                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")
    
    socketio.run(app, host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_gui(debug=True)
