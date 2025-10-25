# GLM JSON Summarizer - Usage Guide

A Python script that uses the GLM API (Anthropic-compatible interface) to intelligently summarize JSON files.

## Features

- Reads and parses JSON files
- Uses GLM's Anthropic-compatible API for intelligent summarization
- Configurable via command-line arguments or environment variables
- Supports output to stdout or file
- Comprehensive error handling

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your GLM API credentials:
```bash
export GLM_API_KEY="your-api-key-here"
export GLM_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"
```

## Usage

### Basic Usage

Summarize a JSON file (prints to stdout):
```bash
python glm_json_summarizer.py sample_data.json
```

### With Command-Line Options

```bash
python glm_json_summarizer.py sample_data.json \
  --api-key "your-api-key" \
  --base-url "https://open.bigmodel.cn/api/paas/v4/" \
  --model "claude-sonnet-4-5-20250929" \
  --output summary.txt
```

### Environment Variables

Instead of passing the API key and base URL each time, set environment variables:

```bash
# Linux/Mac
export GLM_API_KEY="your-api-key-here"
export GLM_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"

# Windows (Command Prompt)
set GLM_API_KEY=your-api-key-here
set GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/

# Windows (PowerShell)
$env:GLM_API_KEY="your-api-key-here"
$env:GLM_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"
```

Then run:
```bash
python glm_json_summarizer.py sample_data.json
```

## Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `json_file` | Path to the JSON file to summarize | Required |
| `--api-key` | GLM API key | `$GLM_API_KEY` |
| `--base-url` | GLM API base URL | `$GLM_BASE_URL` or GLM default |
| `--model` | Model identifier | `claude-sonnet-4-5-20250929` |
| `--output` | Output file path | stdout |

## Example Output

```
Loading JSON file: sample_data.json
Generating summary using GLM API...

============================================================
SUMMARY
============================================================

This JSON file contains information about an "awesome-ai" project that curates AI tools and resources...

[Detailed summary from GLM API]

Summary saved to: summary.txt
```

## Testing with Sample Data

A sample JSON file (`sample_data.json`) is included for testing. Run:

```bash
python glm_json_summarizer.py sample_data.json
```

## Error Handling

The script handles common errors:
- Missing or invalid JSON files
- Missing API credentials
- API connection errors
- Invalid JSON syntax

## Notes

- The GLM API uses an Anthropic-compatible interface, so the `anthropic` Python library is used
- Adjust the `max_tokens` parameter in the script if you need longer summaries
- The default GLM base URL may vary; check GLM documentation for the latest endpoint

## License

This script is provided as-is for educational and practical use with the GLM API.
