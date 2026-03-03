#!/usr/bin/env python3
"""TOON format parser - extracted from validate_toon.py"""

from pathlib import Path


def _parse_header_line(line, data):
    """Parse '# code2llm ...' header line."""
    data['meta']['project'] = 'code2llm'
    data['meta']['generated'] = line.split('|')[-1].strip() if '|' in line else ''


def _parse_stats_line(line, data):
    """Parse '# CC̄=... | critical:... | dups:... | cycles:...' header line."""
    parts = line[2:].strip().split('|')
    for part in parts:
        if 'critical' in part:
            data['stats']['critical'] = part.strip()
        elif 'dups' in part:
            data['stats']['duplicates'] = part.strip()
        elif 'cycles' in part:
            data['stats']['cycles'] = part.strip()


def _parse_health_line(line_stripped, data):
    """Parse a single HEALTH section line."""
    if line_stripped.startswith('\U0001f534') or line_stripped.startswith('\U0001f7e1'):
        data['health'].append(line_stripped)


def _parse_functions_line(line_stripped, data):
    """Parse a single FUNCTIONS section line."""
    if line_stripped.startswith('summary:'):
        return
    parts = line_stripped.split()
    if len(parts) >= 2 and parts[0].replace('.', '').isdigit():
        data['functions'].append({'name': parts[1], 'cc': float(parts[0])})


def _parse_classes_line(line_stripped, data):
    """Parse a single CLASSES section line."""
    parts = line_stripped.split()
    if parts and not parts[0].startswith('\u2588'):
        data['classes'].append({'name': parts[0]})


def _parse_hotspots_line(line_stripped, data):
    """Parse a single HOTSPOTS section line."""
    if line_stripped.startswith('#'):
        parts = line_stripped.split()
        if len(parts) >= 2:
            data['hotspots'].append({'name': parts[1]})


_SECTION_DISPATCH = {
    'health': _parse_health_line,
    'functions': _parse_functions_line,
    'classes': _parse_classes_line,
    'hotspots': _parse_hotspots_line,
}

_SECTION_HEADERS = {
    'HEALTH': 'health',
    'REFACTOR': 'refactor',
    'COUPLING:': 'coupling',
    'LAYERS:': 'layers',
    'DUPLICATES': 'duplicates',
    'FUNCTIONS': 'functions',
    'HOTSPOTS:': 'hotspots',
    'CLASSES:': 'classes',
    'D:': 'details',
}


def _detect_section(line):
    """Detect section header; return section name or None."""
    for prefix, section_name in _SECTION_HEADERS.items():
        if line.startswith(prefix):
            return section_name
    return None


def parse_toon_content(content):
    """Parse TOON v2 plain-text format."""
    data = {
        'meta': {},
        'stats': {},
        'functions': [],
        'classes': [],
        'modules': [],
        'patterns': [],
        'call_graph': {},
        'insights': {},
        'health': [],
        'refactor': [],
        'hotspots': [],
    }
    lines = content.split('\n')
    section = None
    
    for line in lines:
        line_stripped = line.strip()
        
        if line.startswith('# code2llm'):
            _parse_header_line(line, data)
            continue
        
        if line.startswith('# CC'):
            _parse_stats_line(line, data)
            continue
        
        detected = _detect_section(line)
        if detected is not None:
            section = detected
            continue
        
        if section and line_stripped:
            parser = _SECTION_DISPATCH.get(section)
            if parser:
                parser(line_stripped, data)
    
    return data


def is_toon_file(filepath):
    """Check if file is TOON format based on extension or content."""
    path = Path(filepath)
    if path.suffix == '.toon':
        return True
    # Check content for TOON header
    try:
        with open(filepath, 'r') as f:
            first_line = f.readline()
            return first_line.startswith('# code2llm') or first_line.startswith('# CC')
    except:
        return False


def load_toon(filepath):
    """Parse TOON plain-text format into structured data."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return parse_toon_content(content)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None
