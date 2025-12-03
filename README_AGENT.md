# Coding Agent Implementation

## Structure

```
app/
├── agents/
│   ├── coding_agent/
│   │   └── agent.py              # Main agent with dynamic model selection
│   └── tools/
│       ├── execute_code.py       # Code execution tool
│       └── read_write_file.py    # File I/O tools
├── api/
│   └── agent_routes.py           # FastAPI routes for agent
├── core/
│   └── config.py                 # Configuration settings
└── main.py                       # FastAPI application
```

## Features

- **Dynamic Model Selection**: Automatically switches between basic and advanced models based on conversation complexity
- **Middleware Architecture**: Custom middleware intercepts LLM calls to determine optimal model
- **Tool Integration**: Execute code, read files, write files
- **Streaming Support**: Real-time agent responses via SSE

## Configuration

Update your `.env` file:

```env
GEMINI_API_KEY=your_api_key
CODING_AGENT_BASIC_MODEL=gemini-2.0-flash-exp
CODING_AGENT_ADVANCED_MODEL=gemini-2.5-flash
WORK_DIR=agent_output
```

## Usage

### Direct Usage

```python
from app.agents.coding_agent.agent import CodingAgent

agent = CodingAgent()

# Simple invoke
result = agent.invoke("Write a fibonacci function")

# Streaming
for message in agent.stream("Write a fibonacci function"):
    print(message.content)
```

### API Usage

Start the server:

```bash
uvicorn app.main:app --reload
```

Endpoints:

- `POST /agent/invoke` - Single response
- `POST /agent/stream` - Streaming response (SSE)

Example request:

```bash
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "Write a fibonacci function"}'
```

### Example Script

```bash
python example_usage.py
```

## How It Works

1. **Model Selection**: Middleware counts messages and selects appropriate model
   - ≤6 messages: Basic model (faster, cheaper)
   - >6 messages: Advanced model (smarter, for complex tasks)

2. **Tool Execution**: Agent automatically decides which tools to use based on the task

3. **Streaming**: Agent streams responses in real-time, showing tool calls and results
