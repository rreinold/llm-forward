# LLM Proxy

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A lightweight, production-ready proxy for OpenAI's API built with FastAPI and Pydantic. Deploy as a Docker container to add authentication, rate limiting, and request/response processing to your LLM applications.

## Features

- **🚀 FastAPI-based**: High-performance async web server
- **🔐 Authentication**: Secure API key management
- **🐳 Docker Ready**: Production-ready containerization
- **✅ Type Safety**: Full Pydantic validation and type hints

## Quick Start with Docker

The easiest way to get started is using Docker:

```bash
# Build the image
docker build -t llm-proxy .

# Run with your OpenAI API key
docker run -p 8000:80 -e OPENAI_API_KEY=your-api-key-here llm-proxy
```

Your proxy will be available at `http://localhost:8000` and accepts the same API format as OpenAI.

## API Usage

The proxy implements OpenAI's chat completions API:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

## Installation

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/llm-proxy.git
cd llm-proxy

# Build and run
docker build -t llm-proxy .
docker run -p 80:80 -e OPENAI_API_KEY=your-key llm-proxy
```

### Local Development

```bash
# Install dependencies
uv sync

# Set your OpenAI API key
export OPENAI_API_KEY=your-api-key-here

# Run the development server
python -m llm_proxy
```

### Using uvicorn directly

```bash
# For production deployment
uvicorn llm_proxy.main:create_app --host 0.0.0.0 --port 80
```

## Configuration

Configure the proxy using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |


## Docker Deployment

### Production Deployment

```bash
# Build optimized image
docker build -t llm-proxy:latest .

# Run with environment variables
docker run -d \
  --name llm-proxy \
  -p 80:80 \
  -e OPENAI_API_KEY=your-api-key \
  llm-proxy:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  llm-proxy:
    build: .
    ports:
      - "80:80"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
```

## Development

### Setup

```bash
# Install development dependencies
uv sync --extra dev

# Run tests
pytest

# Run integration tests (requires OpenAI API key)
pytest -m integration

# Format code
black .
isort .

# Type checking
mypy .
```

### Testing

```bash
# Run all default tests
pytest

# Run only integration tests
pytest -m integration
```

## API Reference

### Request Format

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### Response Format

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for high-performance web APIs
- Uses [Pydantic](https://github.com/pydantic/pydantic) for data validation
- Inspired by the need for simple, production-ready LLM proxies

## OpenAI Assistants Proxy (Concise Usage)

1. **Set environment variables:**
   ```bash
   export OPENAI_API_KEY=sk-...  # your OpenAI API key
   export OAI_ASSISTANT_ID=asst_JF0fe2OdKnFHicJGqQ68RNbt
   ```

2. **Run the proxy:**
   ```bash
   uv run llm_proxy
   ```

3. **POST to the assistant endpoint:**
   ```bash
   curl -X POST http://localhost:8000/v1/assistants/asst_JF0fe2OdKnFHicJGqQ68RNbt/messages \
     -H "Content-Type: application/json" \
     -d '{"messages":[{"role":"user","content":"Can you suggest a recipe for dinner?"}]}'
   ```

- The proxy will forward requests to the OpenAI Assistants API and return the assistant's response.
