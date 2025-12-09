#!/usr/bin/env python3
"""
Google Gemini Model Interface
Supports Gemini 2.0 Pro, Gemini 3 Pro, and other Gemini models
"""

import os
import json
from typing import List, Dict, Optional


class GeminiModel:
    """Interface for Google Gemini models"""
    
    def __init__(self, config: Dict):
        """
        Initialize Gemini model
        
        Args:
            config: Configuration dict
        """
        self.config = config
        self.api_key = config.get('api_key') or os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        self.model = config.get('model', 'gemini-3-pro')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
        
        if not self.api_key:
            raise ValueError("Google API key not found. Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable.")
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Gemini client"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            # Map model names
            model_mapping = {
                'gemini-3-pro': 'gemini-3-pro',
                'gemini-2-pro': 'gemini-2.0-pro',
                'gemini-pro': 'gemini-pro',
                'gemini-3': 'gemini-3-pro',
                'gemini-2': 'gemini-2.0-pro'
            }
            
            model_name = model_mapping.get(self.model.lower(), self.model)
            
            generation_config = {
                'temperature': self.temperature,
                'max_output_tokens': self.max_tokens,
            }
            
            self.client = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )
            
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
    
    def generate(self, prompt: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate response from Gemini
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Returns:
            Generated response
        """
        try:
            # Build conversation context
            full_prompt = ""
            
            # Add system prompt
            if 'system_prompt' in self.config:
                full_prompt += f"{self.config['system_prompt']}\n\n"
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    full_prompt += f"{role.upper()}: {content}\n"
            
            # Add current prompt
            full_prompt += f"\nUSER: {prompt}\nASSISTANT:"
            
            # Generate response
            response = self.client.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            print(f"[Error] Gemini generation failed: {e}")
            return f"Error generating response: {str(e)}"
    
    def generate_stream(self, prompt: str, conversation_history: List[Dict] = None):
        """
        Generate streaming response from Gemini
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Yields:
            Response chunks
        """
        try:
            # Build conversation context
            full_prompt = ""
            
            if 'system_prompt' in self.config:
                full_prompt += f"{self.config['system_prompt']}\n\n"
            
            if conversation_history:
                for msg in conversation_history[-5:]:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    full_prompt += f"{role.upper()}: {content}\n"
            
            full_prompt += f"\nUSER: {prompt}\nASSISTANT:"
            
            # Stream response
            response = self.client.generate_content(full_prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            yield f"Error generating response: {str(e)}"
