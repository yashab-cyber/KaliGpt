#!/usr/bin/env python3
"""
KaliGPT AI Engine
Routes commands to appropriate LLM and manages AI interactions

Created by Yashab Alam
Instagram: https://www.instagram.com/yashab.alam
LinkedIn: https://www.linkedin.com/in/yashab-alam
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime


class AIEngine:
    """
    Core AI engine that processes pentesting data and provides recommendations
    """
    
    def __init__(self, model_type: str = "gpt", config_path: Optional[str] = None):
        """
        Initialize AI Engine
        
        Args:
            model_type: Type of model to use (gpt, llama, qwen, mistral, ollama)
            config_path: Path to configuration file
        """
        self.model_type = model_type
        self.config = self._load_config(config_path)
        self.model = self._initialize_model()
        self.conversation_history = []
        
    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from file or use defaults"""
        default_config = {
            "model_type": self.model_type,
            "temperature": 0.7,
            "max_tokens": 2000,
            "system_prompt": self._get_system_prompt()
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI"""
        return """You are KaliGPT, an expert AI penetration testing assistant.

Your role is to:
1. Analyze output from pentesting tools (nmap, metasploit, sqlmap, nikto, gobuster, hydra, etc.)
2. Recommend the next logical step in the penetration testing process
3. Provide specific commands to execute
4. Explain vulnerabilities and attack vectors
5. Generate custom payloads when needed
6. Follow the pentesting methodology: Reconnaissance → Enumeration → Exploitation → Post-Exploitation → Reporting

Guidelines:
- Always provide actionable, specific commands
- Explain WHY each step is recommended
- Consider safety and legality (only on authorized targets)
- Prioritize high-impact vulnerabilities
- Think like a professional penetration tester
- Be concise but thorough

Format your responses as:
**Analysis:** [What you found]
**Recommended Action:** [What to do next]
**Command:** [Exact command to run]
**Explanation:** [Why this step is important]
**Alternative Options:** [Other approaches if applicable]
"""
    
    def _initialize_model(self):
        """Initialize the appropriate model based on type"""
        from models.model_selector import ModelSelector
        selector = ModelSelector(self.config)
        return selector.get_model(self.model_type)
    
    def analyze_output(self, command: str, output: str, tool_type: Optional[str] = None) -> Dict:
        """
        Analyze command output and provide recommendations
        
        Args:
            command: The command that was executed
            output: The output from the command
            tool_type: Type of tool (nmap, metasploit, etc.)
            
        Returns:
            Dict with analysis, recommendation, next_command, explanation
        """
        # Build the analysis prompt
        prompt = self._build_analysis_prompt(command, output, tool_type)
        
        # Get AI response
        response = self.model.generate(prompt, self.conversation_history)
        
        # Parse the response
        parsed = self._parse_response(response)
        
        # Update conversation history
        self.conversation_history.append({
            "role": "user",
            "content": f"Command: {command}\nOutput: {output[:500]}..."
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Keep history manageable (last 10 exchanges)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return parsed
    
    def _build_analysis_prompt(self, command: str, output: str, tool_type: Optional[str]) -> str:
        """Build the prompt for AI analysis"""
        
        tool_context = f"\n**Tool Type:** {tool_type}" if tool_type else ""
        
        prompt = f"""Analyze this penetration testing command output and recommend the next step:

**Command Executed:** {command}{tool_context}

**Output:**
```
{output[:3000]}
```

Provide your analysis and recommendations following the format in your system prompt.
"""
        return prompt
    
    def _parse_response(self, response: str) -> Dict:
        """Parse AI response into structured format"""
        
        result = {
            "raw_response": response,
            "analysis": "",
            "recommendation": "",
            "command": "",
            "explanation": "",
            "alternatives": [],
            "timestamp": datetime.now().isoformat()
        }
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("**Analysis:**"):
                current_section = "analysis"
                result["analysis"] = line.replace("**Analysis:**", "").strip()
            elif line.startswith("**Recommended Action:**"):
                current_section = "recommendation"
                result["recommendation"] = line.replace("**Recommended Action:**", "").strip()
            elif line.startswith("**Command:**"):
                current_section = "command"
                cmd = line.replace("**Command:**", "").strip()
                # Remove markdown code formatting if present
                cmd = cmd.replace('`', '').strip()
                result["command"] = cmd
            elif line.startswith("**Explanation:**"):
                current_section = "explanation"
                result["explanation"] = line.replace("**Explanation:**", "").strip()
            elif line.startswith("**Alternative Options:**") or line.startswith("**Alternatives:**"):
                current_section = "alternatives"
            elif current_section and line:
                # Continue adding to current section
                if current_section == "alternatives":
                    if line.startswith("-") or line.startswith("•"):
                        result["alternatives"].append(line.lstrip("-•").strip())
                elif current_section in result:
                    result[current_section] += " " + line
        
        return result
    
    def generate_payload(self, payload_type: str, target_info: Dict) -> str:
        """
        Generate custom payload
        
        Args:
            payload_type: Type of payload (sqli, xss, lfi, rce, reverse_shell, etc.)
            target_info: Information about the target
            
        Returns:
            Generated payload
        """
        prompt = f"""Generate a {payload_type} payload for the following target:

Target Information:
{json.dumps(target_info, indent=2)}

Provide the payload code directly, with explanation."""
        
        response = self.model.generate(prompt, [])
        return response
    
    def suggest_workflow_step(self, current_phase: str, findings: List[Dict]) -> Dict:
        """
        Suggest next workflow step based on current phase
        
        Args:
            current_phase: Current pentesting phase (recon, enum, exploit, post-exploit)
            findings: List of findings so far
            
        Returns:
            Dict with next phase and recommended actions
        """
        findings_summary = json.dumps(findings, indent=2)
        
        prompt = f"""Based on the current penetration testing phase and findings, recommend the next steps:

**Current Phase:** {current_phase}

**Findings So Far:**
```json
{findings_summary}
```

What should be the next focus area and specific actions to take?
"""
        
        response = self.model.generate(prompt, self.conversation_history)
        return self._parse_response(response)
    
    def explain_vulnerability(self, vuln_name: str, context: str = "") -> str:
        """
        Explain a vulnerability and how to exploit it
        
        Args:
            vuln_name: Name of the vulnerability
            context: Additional context
            
        Returns:
            Detailed explanation
        """
        prompt = f"""Explain the vulnerability: {vuln_name}

Context: {context}

Provide:
1. What the vulnerability is
2. Why it's dangerous
3. How to exploit it
4. Remediation steps
"""
        
        response = self.model.generate(prompt, [])
        return response
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def save_conversation(self, filepath: str):
        """Save conversation history to file"""
        with open(filepath, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)


class ContextManager:
    """
    Manages context across multiple commands and sessions
    """
    
    def __init__(self):
        self.target_info = {}
        self.discovered_services = []
        self.discovered_vulnerabilities = []
        self.executed_exploits = []
        self.current_phase = "reconnaissance"
        
    def update_target(self, ip: str, hostname: Optional[str] = None):
        """Update target information"""
        self.target_info['ip'] = ip
        if hostname:
            self.target_info['hostname'] = hostname
    
    def add_service(self, port: int, service: str, version: Optional[str] = None):
        """Add discovered service"""
        service_info = {
            'port': port,
            'service': service,
            'version': version,
            'timestamp': datetime.now().isoformat()
        }
        self.discovered_services.append(service_info)
    
    def add_vulnerability(self, vuln: Dict):
        """Add discovered vulnerability"""
        vuln['timestamp'] = datetime.now().isoformat()
        self.discovered_vulnerabilities.append(vuln)
    
    def add_exploit(self, exploit: Dict):
        """Log executed exploit"""
        exploit['timestamp'] = datetime.now().isoformat()
        self.executed_exploits.append(exploit)
    
    def set_phase(self, phase: str):
        """Update current pentesting phase"""
        valid_phases = [
            "reconnaissance",
            "enumeration", 
            "exploitation",
            "post-exploitation",
            "lateral-movement",
            "privilege-escalation",
            "reporting"
        ]
        if phase in valid_phases:
            self.current_phase = phase
    
    def get_context(self) -> Dict:
        """Get full context"""
        return {
            'target': self.target_info,
            'services': self.discovered_services,
            'vulnerabilities': self.discovered_vulnerabilities,
            'exploits': self.executed_exploits,
            'phase': self.current_phase
        }
    
    def save_context(self, filepath: str):
        """Save context to file"""
        with open(filepath, 'w') as f:
            json.dump(self.get_context(), f, indent=2)
    
    def load_context(self, filepath: str):
        """Load context from file"""
        with open(filepath, 'r') as f:
            context = json.load(f)
            self.target_info = context.get('target', {})
            self.discovered_services = context.get('services', [])
            self.discovered_vulnerabilities = context.get('vulnerabilities', [])
            self.executed_exploits = context.get('exploits', [])
            self.current_phase = context.get('phase', 'reconnaissance')
