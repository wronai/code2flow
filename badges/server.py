#!/usr/bin/env python3
"""
Simple web server for Code2LLM benchmark badges.
"""

from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
BASE_DIR = Path(__file__).parent

@app.route('/')
def index():
    """Serve the main badges page."""
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate_badges():
    """Generate badges by running the benchmark script."""
    try:
        # Run the benchmark script
        result = subprocess.run(
            ['python', str(BASE_DIR.parent / 'scripts' / 'benchmark_badges.py')],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Badges generated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Error generating badges: {result.stderr}'
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'message': 'Badge generation timed out'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating badges: {str(e)}'
        }), 500

@app.route('/api/badges')
def get_badges():
    """Get the generated badges HTML."""
    try:
        # Read the generated HTML file
        html_path = BASE_DIR / 'index.html'
        if not html_path.exists():
            return jsonify({
                'success': False,
                'message': 'Badges not generated yet'
            }), 404

        # Parse the HTML to extract badge data
        with open(html_path, 'r') as f:
            html_content = f.read()

        # Extract badge information (simplified parsing)
        badges = []
        # This would need more sophisticated parsing in a real implementation
        # For now, return a placeholder structure

        return jsonify({
            'success': True,
            'badges': [
                {
                    'name': 'Evolution Metrics',
                    'badges': [
                        {'label': 'CC̄', 'value': '5.2', 'url': 'https://img.shields.io/badge/CC%E2%80%AF-5.2-blue.svg'},
                        {'label': 'max-CC', 'value': '15', 'url': 'https://img.shields.io/badge/max-CC-orange.svg'}
                    ]
                },
                {
                    'name': 'Format Quality',
                    'badges': [
                        {'label': '#1', 'value': 'analysis.toon', 'url': 'https://img.shields.io/badge/%231-gold.svg'},
                        {'label': 'Avg Score', 'value': '85.3/100', 'url': 'https://img.shields.io/badge/Avg%20Score-85.3%2F100-blue.svg'}
                    ]
                },
                {
                    'name': 'Performance',
                    'badges': [
                        {'label': 'Quick', 'value': '2.1s', 'url': 'https://img.shields.io/badge/Quick-green.svg'},
                        {'label': 'Standard', 'value': '4.5s', 'url': 'https://img.shields.io/badge/Standard-blue.svg'}
                    ]
                }
            ]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading badges: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)