#!/usr/bin/env python3
"""
N8N Template Extractor
Automates downloading JSON templates from n8n.io workflow pages
"""

import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Template configurations
TEMPLATES = [
    {"filename": "reddit-ai-digest.json", "url": "https://n8n.io/workflows/1895-reddit-ai-digest/"},
    {"filename": "automated-reddit-lead-generation.json", "url": "https://n8n.io/workflows/6337-automated-reddit-lead-generation-with-ai-analysis-and-google-sheets/"},
    {"filename": "monitor-reddit-job-posts.json", "url": "https://n8n.io/workflows/8120-monitor-reddit-job-posts-with-gpt-4o-analysis-and-telegram-alerts-using-google-sheets/"},
    {"filename": "generate-startup-ideas.json", "url": "https://n8n.io/workflows/6094-generate-startup-ideas-from-reddit-posts-using-gemini-ai-and-google-sheets/"},
    {"filename": "reddit-comment-sentiment.json", "url": "https://n8n.io/workflows/6620-reddit-comment-sentiment-analysis-with-bright-data-and-gemini-ai-to-google-sheets/"},
    {"filename": "analyze-reddit-content.json", "url": "https://n8n.io/workflows/6477-analyze-reddit-content-and-comments-for-sentiment-with-deepseek-ai/"},
    {"filename": "reddit-brand-engagement.json", "url": "https://n8n.io/workflows/8458-reddit-brand-engagement-with-ai-comment-generation-and-slack-notifications/"},
    {"filename": "reddit-lead-finder.json", "url": "https://n8n.io/workflows/6756-reddit-lead-finder-automated-prospecting-with-gpt-4-supabase-and-gmail-alerts/"},
    {"filename": "analyze-reddit-posts.json", "url": "https://n8n.io/workflows/2978-analyze-reddit-posts-with-ai-to-identify-business-opportunities/"},
    {"filename": "transform-reddit-to-linkedin.json", "url": "https://n8n.io/workflows/6383-transform-reddit-discussions-into-linkedin-post-ideas-with-gpt-4o-and-google-sheets/"},
    {"filename": "social-sentiment-dashboard.json", "url": "https://n8n.io/workflows/6430-social-media-sentiment-analysis-dashboard-with-custom-ai-for-twitter-reddit-and-linkedin/"},
    {"filename": "monitor-social-trends.json", "url": "https://n8n.io/workflows/8450-monitor-social-media-trends-across-reddit-instagram-and-tiktok-with-apify/"},
    {"filename": "generate-content-strategy.json", "url": "https://n8n.io/workflows/5375-generate-content-strategy-reports-analyzing-reddit-youtube-and-x-with-gemini/"},
    {"filename": "reddit-x-tech-trend.json", "url": "https://n8n.io/workflows/9730-x-and-reddit-tech-trend-analysis-with-gemini-ai-for-notion-and-telegram/"},
    {"filename": "monitor-content-trends.json", "url": "https://n8n.io/workflows/6441-monitor-content-trends-across-social-media-with-ai-slack-and-google-sheets/"},
    {"filename": "track-regional-sentiment.json", "url": "https://n8n.io/workflows/5973-track-regional-sentiment-from-social-media-with-bright-data-and-openai/"},
    {"filename": "discover-social-leads.json", "url": "https://n8n.io/workflows/6378-discover-and-generate-leads-from-social-engagement-using-trigify-google-sheets-and-slack/"},
    {"filename": "ai-social-thought-leadership.json", "url": "https://n8n.io/workflows/6375-ai-powered-social-media-thought-leadership-with-claude-sonnet-and-trigify/"},
    {"filename": "monitor-brand-x.json", "url": "https://n8n.io/workflows/8355-monitor-brand-mentions-on-x-with-gemini-ai-visual-analysis-and-telegram-alerts/"},
    {"filename": "monitor-facebook-groups.json", "url": "https://n8n.io/workflows/4235-monitor-and-track-brand-sentiment-on-facebook-groups-with-bright-data/"},
]

OUTPUT_DIR = Path("n8n_templates")


async def extract_template(page, template_info, index, total):
    """Extract JSON template from a single n8n workflow page"""
    filename = template_info["filename"]
    url = template_info["url"]

    print(f"\n[{index}/{total}] Processing: {filename}")
    print(f"    URL: {url}")

    try:
        # Navigate to the page
        await page.goto(url, wait_until="networkidle", timeout=30000)
        print(f"    ✓ Page loaded")

        # Wait a bit for dynamic content
        await asyncio.sleep(2)

        # Look for "Use for free" button - try multiple selectors
        use_free_button = None
        selectors = [
            'button:has-text("Use for free")',
            'a:has-text("Use for free")',
            '[aria-label*="Use for free"]',
            'text="Use for free"',
        ]

        for selector in selectors:
            try:
                use_free_button = await page.wait_for_selector(selector, timeout=5000)
                if use_free_button:
                    print(f"    ✓ Found 'Use for free' button")
                    break
            except:
                continue

        if not use_free_button:
            print(f"    ✗ 'Use for free' button not found")
            return {"status": "failed", "error": "Button not found", "filename": filename}

        # Click the button
        await use_free_button.click()
        print(f"    ✓ Clicked 'Use for free'")

        # Wait for modal/popup to appear
        await asyncio.sleep(2)

        # Look for "Copy template to clipboard [JSON]" button
        copy_json_button = None
        json_selectors = [
            'button:has-text("Copy template to clipboard")',
            'button:has-text("JSON")',
            '[aria-label*="Copy template"]',
            'text="Copy template to clipboard"',
        ]

        for selector in json_selectors:
            try:
                copy_json_button = await page.wait_for_selector(selector, timeout=5000)
                if copy_json_button:
                    print(f"    ✓ Found 'Copy template' button")
                    break
            except:
                continue

        if not copy_json_button:
            print(f"    ✗ 'Copy template to clipboard' button not found")
            return {"status": "failed", "error": "Copy button not found", "filename": filename}

        # Click to copy JSON to clipboard
        await copy_json_button.click()
        print(f"    ✓ Clicked 'Copy template to clipboard'")

        # Wait a moment for clipboard operation
        await asyncio.sleep(1)

        # Read from clipboard using CDP (Chrome DevTools Protocol)
        # Note: This requires proper permissions
        try:
            # Alternative: Try to get the content from a textarea or pre element if it's displayed
            json_content = None

            # Try to find JSON in the page
            json_selectors_content = [
                'textarea',
                'pre',
                'code',
                '[class*="json"]',
            ]

            for selector in json_selectors_content:
                try:
                    element = await page.wait_for_selector(selector, timeout=2000)
                    if element:
                        content = await element.text_content()
                        if content and content.strip().startswith('{'):
                            json_content = content
                            break
                except:
                    continue

            # If we found JSON content in the page, use it
            if json_content:
                # Validate it's proper JSON
                json.loads(json_content)  # This will raise if invalid

                # Save to file
                output_path = OUTPUT_DIR / filename
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(json_content)

                print(f"    ✓ Saved to: {output_path}")
                return {"status": "success", "filename": filename, "path": str(output_path)}
            else:
                print(f"    ✗ Could not extract JSON content")
                return {"status": "failed", "error": "JSON content not found", "filename": filename}

        except json.JSONDecodeError as e:
            print(f"    ✗ Invalid JSON: {e}")
            return {"status": "failed", "error": f"Invalid JSON: {e}", "filename": filename}
        except Exception as e:
            print(f"    ✗ Error reading content: {e}")
            return {"status": "failed", "error": str(e), "filename": filename}

    except PlaywrightTimeout as e:
        print(f"    ✗ Timeout: {e}")
        return {"status": "failed", "error": f"Timeout: {e}", "filename": filename}
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return {"status": "failed", "error": str(e), "filename": filename}


async def main():
    """Main extraction process"""
    print("="*70)
    print("N8N Template Extractor")
    print("="*70)

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"\n✓ Output directory: {OUTPUT_DIR.absolute()}\n")

    results = {
        "success": [],
        "failed": []
    }

    async with async_playwright() as p:
        # Launch browser (headless=False to see what's happening)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        total = len(TEMPLATES)

        # Process each template
        for index, template in enumerate(TEMPLATES, 1):
            result = await extract_template(page, template, index, total)

            if result["status"] == "success":
                results["success"].append(result)
            else:
                results["failed"].append(result)

            # Small delay between requests
            await asyncio.sleep(2)

        await browser.close()

    # Print summary report
    print("\n" + "="*70)
    print("EXTRACTION SUMMARY")
    print("="*70)
    print(f"\n✓ Successful: {len(results['success'])}/{total}")
    for r in results['success']:
        print(f"  - {r['filename']}")

    print(f"\n✗ Failed: {len(results['failed'])}/{total}")
    for r in results['failed']:
        print(f"  - {r['filename']}: {r['error']}")

    print("\n" + "="*70)

    # Save summary to JSON
    summary_path = OUTPUT_DIR / "_extraction_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    asyncio.run(main())
