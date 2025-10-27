#!/usr/bin/env python3
"""
N8N Template Extractor - V3 最终版
根据实际页面结构优化：Use for free -> Copy template to clipboard (JSON)
"""

import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import pyperclip  # For clipboard access

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
SCREENSHOT_DIR = Path("debug_screenshots")


async def extract_template(page, context, template_info, index, total):
    """Extract JSON template from a single n8n workflow page"""
    filename = template_info["filename"]
    url = template_info["url"]

    print(f"\n[{index}/{total}] Processing: {filename}")
    print(f"    URL: {url}")

    try:
        # Navigate to the page
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        print(f"    ✓ Page loaded")

        # Wait for page to be fully loaded
        await asyncio.sleep(3)

        # Take initial screenshot
        screenshot_path = SCREENSHOT_DIR / f"{index:02d}_initial.png"
        await page.screenshot(path=str(screenshot_path))
        print(f"    📸 Initial screenshot: {screenshot_path.name}")

        # Step 1: Click "Use for free" button
        print(f"    🔍 Looking for 'Use for free' button...")

        use_free_button = None
        selectors_to_try = [
            'button:has-text("Use for free")',
            'a:has-text("Use for free")',
            '[aria-label*="Use for free"]',
            'text=Use for free',
        ]

        for selector in selectors_to_try:
            try:
                use_free_button = await page.wait_for_selector(selector, timeout=5000)
                if use_free_button:
                    print(f"    ✓ Found 'Use for free' button (selector: {selector})")
                    break
            except:
                continue

        if not use_free_button:
            print(f"    ✗ 'Use for free' button not found")
            screenshot_path = SCREENSHOT_DIR / f"{index:02d}_no_button.png"
            await page.screenshot(path=str(screenshot_path))
            return {"status": "failed", "error": "Use for free button not found", "filename": filename}

        # Click the button
        await use_free_button.click()
        print(f"    ✓ Clicked 'Use for free'")

        # Wait for menu to appear
        await asyncio.sleep(2)

        # Take screenshot after clicking
        screenshot_path = SCREENSHOT_DIR / f"{index:02d}_after_click.png"
        await page.screenshot(path=str(screenshot_path))
        print(f"    📸 After click screenshot: {screenshot_path.name}")

        # Step 2: Click "Copy template to clipboard (JSON)" in the menu
        print(f"    🔍 Looking for 'Copy template to clipboard' option...")

        copy_button = None
        copy_selectors = [
            'text=Copy template to clipboard (JSON)',
            'text=Copy template to clipboard',
            ':has-text("Copy template to clipboard")',
            'button:has-text("Copy template")',
            'a:has-text("Copy template")',
            '[aria-label*="Copy template"]',
        ]

        for selector in copy_selectors:
            try:
                copy_button = await page.wait_for_selector(selector, timeout=5000)
                if copy_button:
                    print(f"    ✓ Found 'Copy template' option (selector: {selector})")
                    break
            except:
                continue

        if not copy_button:
            print(f"    ✗ 'Copy template to clipboard' option not found")
            screenshot_path = SCREENSHOT_DIR / f"{index:02d}_no_copy_option.png"
            await page.screenshot(path=str(screenshot_path))
            return {"status": "failed", "error": "Copy template option not found", "filename": filename}

        # Click to copy to clipboard
        await copy_button.click()
        print(f"    ✓ Clicked 'Copy template to clipboard'")

        # Wait for clipboard operation
        await asyncio.sleep(2)

        # Take screenshot after copy
        screenshot_path = SCREENSHOT_DIR / f"{index:02d}_after_copy.png"
        await page.screenshot(path=str(screenshot_path))

        # Step 3: Read from clipboard
        print(f"    📋 Reading from clipboard...")

        # Use Playwright's CDP to read clipboard
        try:
            # Grant clipboard permissions
            await context.grant_permissions(['clipboard-read', 'clipboard-write'])

            # Read clipboard using page evaluation
            clipboard_content = await page.evaluate("""
                async () => {
                    try {
                        return await navigator.clipboard.readText();
                    } catch (e) {
                        return null;
                    }
                }
            """)

            if clipboard_content and clipboard_content.strip():
                print(f"    ✓ Got clipboard content ({len(clipboard_content)} chars)")

                # Validate it's JSON
                try:
                    parsed_json = json.loads(clipboard_content)

                    # Save to file
                    output_path = OUTPUT_DIR / filename
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(parsed_json, f, indent=2, ensure_ascii=False)

                    print(f"    ✅ Saved to: {output_path}")
                    return {"status": "success", "filename": filename, "path": str(output_path)}

                except json.JSONDecodeError as e:
                    print(f"    ✗ Invalid JSON: {e}")
                    # Save raw content for debugging
                    debug_path = OUTPUT_DIR / f"{filename}.txt"
                    with open(debug_path, 'w', encoding='utf-8') as f:
                        f.write(clipboard_content)
                    return {"status": "failed", "error": f"Invalid JSON (saved to {debug_path})", "filename": filename}
            else:
                print(f"    ✗ Clipboard is empty or inaccessible")
                return {"status": "failed", "error": "Clipboard empty", "filename": filename}

        except Exception as e:
            print(f"    ✗ Error reading clipboard: {e}")
            return {"status": "failed", "error": f"Clipboard error: {e}", "filename": filename}

    except PlaywrightTimeout as e:
        print(f"    ✗ Timeout: {e}")
        return {"status": "failed", "error": "Timeout", "filename": filename}
    except Exception as e:
        print(f"    ✗ Error: {e}")
        try:
            screenshot_path = SCREENSHOT_DIR / f"{index:02d}_error.png"
            await page.screenshot(path=str(screenshot_path))
        except:
            pass
        return {"status": "failed", "error": str(e), "filename": filename}


async def main():
    """Main extraction process"""
    print("="*70)
    print("N8N Template Extractor - V3 最终版")
    print("="*70)

    # Create output directories
    OUTPUT_DIR.mkdir(exist_ok=True)
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    print(f"\n✓ Output directory: {OUTPUT_DIR.absolute()}")
    print(f"✓ Screenshot directory: {SCREENSHOT_DIR.absolute()}\n")

    results = {
        "success": [],
        "failed": []
    }

    async with async_playwright() as p:
        # Launch browser
        print("🌐 Launching browser...")
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=300  # Slow down for visibility
        )

        # Create context with clipboard permissions
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            permissions=['clipboard-read', 'clipboard-write']
        )

        page = await context.new_page()

        total = len(TEMPLATES)

        # Process each template
        for index, template in enumerate(TEMPLATES, 1):
            try:
                result = await extract_template(page, context, template, index, total)

                if result["status"] == "success":
                    results["success"].append(result)
                else:
                    results["failed"].append(result)

                # Delay between requests
                await asyncio.sleep(3)

            except Exception as e:
                print(f"\n❌ Critical error processing {template['filename']}: {e}")
                results["failed"].append({
                    "status": "failed",
                    "error": str(e),
                    "filename": template["filename"]
                })

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
    print(f"\n📊 Summary saved to: {summary_path}")

    if len(results['failed']) > 0:
        print(f"\n📸 Check screenshots in: {SCREENSHOT_DIR.absolute()}")
        print("    Screenshots can help diagnose failures!")


if __name__ == "__main__":
    asyncio.run(main())
