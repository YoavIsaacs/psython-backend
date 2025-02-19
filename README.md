# Custom Programming Language Interpreter API - Psython

An API service that allows users to define custom keyword mappings for Python, creating personalized programming languages while maintaining Python's execution model.

## Overview

This project provides a FastAPI-based service that enables users to:
1. Create custom programming languages by remapping Python keywords
2. Validate custom language configurations
3. Translate code written in custom languages to Python
4. Securely execute translated code in isolated Docker containers

The API serves as a bridge between custom syntax and Python's execution environment, making programming more accessible to beginners or domain-specific users.

## Features

### Custom Keyword Mapping
- Remap any Python keyword to a custom identifier
- Support for internationalization and localization of programming syntax
- Encode/decode configuration for easy sharing and persistence

### Code Translation
- Tokenize and translate custom language code to valid Python
- Preserve code structure, indentation, and string literals during translation
- Validate syntax before execution

### Secure Execution Environment
- Isolated Docker containers for code execution
- Resource limits to prevent abuse (memory, CPU, network)
- Separate stdout/stderr capture

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check endpoint |
| `/encode` | POST | Encode keyword configuration to compressed base64 |
| `/decode` | POST | Decode configuration from compressed base64 |
| `/validate_keywords` | POST | Validate custom keyword mapping |
| `/translate` | POST | Translate custom code to Python without execution |
| `/execute` | POST | Translate and execute code, returning results |

## Architecture

The system consists of several core components:

### API Layer
- FastAPI framework
- Request/response models with Pydantic validation
- Comprehensive error handling

### Translation Engine
- Token-based syntax parsing
- Context-aware keyword replacement
- Abstract Syntax Tree (AST) validation

### Configuration Management
- Compression and encoding for efficient storage
- Validation to ensure language consistency
- Bidirectional mapping between Python and custom keywords

### Execution Environment
- Docker-based sandboxing
- Resource limitation and monitoring
- stdout/stderr capture and formatting

## Security Considerations

The service implements several security measures:
- Containerized execution environments
- CPU and memory limits
- Network isolation
- Input validation
- Error sanitization

## Installation

### Prerequisites
- Python 3.10+
- Docker
- FastAPI
- Docker Python SDK

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/custom-interpreter-api.git
cd custom-interpreter-api

# Install dependencies
pip install -r requirements.txt

# Build Docker execution environment
docker build -t runner:latest -f Dockerfile.runner .

# Run the service
uvicorn main:app --reload
```

## Usage Examples

### Creating a Custom Language Configuration
```python
import requests

response = requests.post(
    "http://localhost:8000/validate_keywords",
    json={
        "keywords": {
            "if": "si",
            "else": "sino",
            "for": "para",
            "while": "mientras",
            "def": "funcion",
            "return": "devolver",
            "True": "Verdadero",
            "False": "Falso"
        }
    }
)
print(response.json())
```

### Executing Code in Custom Language
```python
import requests

response = requests.post(
    "http://localhost:8000/execute",
    json={
        "code": """
funcion fibonacci(n):
    si n <= 1:
        devolver n
    sino:
        devolver fibonacci(n-1) + fibonacci(n-2)

para i en range(10):
    print(fibonacci(i))
        """,
        "config": {
            "if": "si",
            "else": "sino",
            "for": "para",
            "in": "en",
            "def": "funcion",
            "return": "devolver"
        }
    }
)
print(response.json())
```

## API Documentation

Once running, the API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Project Structure
```
.
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── interpreter.py  # API endpoints
│   ├── core/
│   │   ├── docker_manager.py   # Docker execution environment
│   │   ├── interpreter.py      # Config encoding/validation
│   │   └── translator_validator.py # Code translation
│   └── schemas/
│       └── config.py           # Data models
├── docker/
│   └── runner/
│       ├── Dockerfile
│       └── runner.py           # Code execution script
├── main.py                     # Application entry point
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- FastAPI for the web framework
- Docker for containerization
- Python AST and tokenize modules for parsing
