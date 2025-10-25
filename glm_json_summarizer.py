#!/usr/bin/env python3
"""
GLM API JSON Summarizer
Uses the Anthropic-compatible GLM API to summarize JSON files.
"""

import json
import os
import sys
import argparse
from anthropic import Anthropic


def load_json_file(file_path):
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file_path}': {e}")
        sys.exit(1)


def summarize_json_with_glm(json_data, api_key, base_url, model="claude-sonnet-4-5-20250929"):
    """
    Summarize JSON data using the GLM API (Anthropic-compatible).

    Args:
        json_data: The JSON data to summarize
        api_key: GLM API key
        base_url: GLM API base URL
        model: Model identifier (default: claude-sonnet-4-5-20250929)

    Returns:
        Summary text from the API
    """
    # Initialize the Anthropic client with GLM endpoint
    client = Anthropic(
        api_key=api_key,
        base_url=base_url
    )

    # Convert JSON to formatted string
    json_str = json.dumps(json_data, indent=2, ensure_ascii=False)

    # Create the prompt
    prompt = f"""Please analyze and summarize the following JSON data.
Provide:
1. A brief overview of the data structure
2. Key information and patterns
3. Notable insights or observations

JSON Data:
```json
{json_str}
```

Please provide a clear and concise summary."""

    try:
        # Make API call
        message = client.messages.create(
            model=model,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the response text
        return message.content[0].text

    except Exception as e:
        print(f"Error calling GLM API: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Summarize JSON files using GLM API (Anthropic-compatible)"
    )
    parser.add_argument(
        "json_file",
        help="Path to the JSON file to summarize"
    )
    parser.add_argument(
        "--api-key",
        help="GLM API key (or set GLM_API_KEY environment variable)",
        default=os.getenv("GLM_API_KEY")
    )
    parser.add_argument(
        "--base-url",
        help="GLM API base URL (or set GLM_BASE_URL environment variable)",
        default=os.getenv("GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
    )
    parser.add_argument(
        "--model",
        help="Model to use (default: claude-sonnet-4-5-20250929)",
        default="claude-sonnet-4-5-20250929"
    )
    parser.add_argument(
        "--output",
        help="Output file for the summary (default: print to stdout)",
        default=None
    )

    args = parser.parse_args()

    # Validate API key
    if not args.api_key:
        print("Error: GLM API key is required. Set GLM_API_KEY environment variable or use --api-key")
        sys.exit(1)

    # Load JSON file
    print(f"Loading JSON file: {args.json_file}")
    json_data = load_json_file(args.json_file)

    # Generate summary
    print("Generating summary using GLM API...")
    summary = summarize_json_with_glm(
        json_data,
        args.api_key,
        args.base_url,
        args.model
    )

    # Output results
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60 + "\n")
    print(summary)

    # Save to file if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"\nSummary saved to: {args.output}")


if __name__ == "__main__":
    main()
