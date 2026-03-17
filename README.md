# LLM-Powered Prompt Router

An intelligent routing service that classifies user intent and delegates requests to specialized AI personas.

## Features
- **Intent Classification**: Uses `gpt-3.5-turbo` for fast and cost-effective intent detection.
- **Expert Personas**: Specialized system prompts for Coding, Data Analysis, Writing Coaching, and Career Advice.
- **Graceful Error Handling**: Defaults to 'unclear' intent for malformed inputs or low confidence.
- **Detailed Logging**: All interactions are logged to `route_log.jsonl`.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your `.env` file with your OpenAI API Key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Interactive Mode
Run the router in an interactive CLI session:
```bash
python main.py
```

### Single Message
Process a single message:
```bash
python main.py --msg "how do i sort a list in python?"
```

### Run Tests
Execute the 15 standard test cases:
```bash
python main.py --test
```

## Project Structure
- `router.py`: Core logic for classification and routing.
- `prompts.json`: Configuration file for expert system prompts.
- `main.py`: CLI and test runner.
- `route_log.jsonl`: Performance and routing log.
