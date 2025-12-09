# KaliGPT Test Suite

This directory contains tests for KaliGPT components.

## Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_parsers.py

# Run with coverage
python3 -m pytest --cov=. tests/
```

## Test Structure

- `test_parsers.py` - Parser tests
- `test_payloads.py` - Payload generator tests
- `test_ai_engine.py` - AI engine tests
- `test_executor.py` - Command executor tests
- `test_reporting.py` - Report builder tests

## Writing Tests

Add new tests following the existing patterns:

```python
import pytest
from parsers.nmap_parser import NmapParser

def test_nmap_parser():
    parser = NmapParser()
    result = parser.parse(sample_output)
    assert result['tool'] == 'nmap'
    assert len(result['open_ports']) > 0
```
