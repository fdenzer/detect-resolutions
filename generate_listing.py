#!/usr/bin/env python3
import os
import html

def generate_html():
    src_dir = "src"
    output_file = "listing.htm"
    
    if not os.path.exists(src_dir):
        print(f"Error: '{src_dir}' directory not found.")
        return

    # Find all Python files recursively in src
    py_files = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start=os.path.dirname(src_dir))
                py_files.append((rel_path, full_path))
    
    py_files.sort()

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Source Code Listing</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-color: #e2e8f0;
            --text-muted: #94a3b8;
            --accent-color: #38bdf8;
            --accent-hover: #7dd3fc;
            --border-color: #334155;
            --code-bg: #0b0f19;
            --success-color: #34d399;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 2rem 1.5rem;
            line-height: 1.5;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        header {
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
        }

        h1 {
            font-size: 2.25rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: var(--text-muted);
            margin: 0;
            font-size: 1rem;
        }

        .file-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            margin-bottom: 1.25rem;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .file-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -4px rgba(0, 0, 0, 0.2);
            border-color: #475569;
        }

        details {
            width: 100%;
        }

        summary {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.25rem;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
            outline: none;
        }

        summary::-webkit-details-marker {
            display: none;
        }

        .file-info {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .file-icon {
            color: var(--accent-color);
            width: 20px;
            height: 20px;
        }

        .file-name {
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 1rem;
            word-break: break-all;
        }

        .toggle-indicator {
            display: flex;
            align-items: center;
            color: var(--text-muted);
            font-size: 0.875rem;
            gap: 0.5rem;
            transition: color 0.2s;
        }

        summary:hover .toggle-indicator {
            color: var(--accent-color);
        }

        .toggle-arrow {
            transition: transform 0.2s ease;
        }

        details[open] summary .toggle-arrow {
            transform: rotate(90deg);
        }

        .code-container {
            position: relative;
            border-top: 1px solid var(--border-color);
            background-color: var(--code-bg);
        }

        .copy-btn {
            position: absolute;
            top: 0.75rem;
            right: 0.75rem;
            background-color: rgba(30, 41, 59, 0.8);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 0.375rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 500;
            border-radius: 0.375rem;
            cursor: pointer;
            backdrop-filter: blur(4px);
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .copy-btn:hover {
            background-color: var(--accent-color);
            color: #0f172a;
            border-color: var(--accent-color);
        }

        .copy-btn.copied {
            background-color: var(--success-color);
            color: #0f172a;
            border-color: var(--success-color);
        }

        pre {
            margin: 0;
            padding: 1.25rem;
            overflow-x: auto;
        }

        code {
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.875rem;
            tab-size: 4;
            display: block;
            color: #f8fafc;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Source Code Listing</h1>
            <p class="subtitle">Collapsible repository views for easy reference and copying.</p>
        </header>
        
        <main>
"""

    for rel_path, full_path in py_files:
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            escaped_content = html.escape(content)
            
            html_content += f"""
            <div class="file-card">
                <details>
                    <summary>
                        <div class="file-info">
                            <svg class="file-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            <span class="file-name">{rel_path}</span>
                        </div>
                        <div class="toggle-indicator">
                            <span>Click to view</span>
                            <svg class="toggle-arrow" width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </div>
                    </summary>
                    <div class="code-container">
                        <button class="copy-btn" onclick="copyCode(this)">
                            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
                            </svg>
                            <span>Copy</span>
                        </button>
                        <pre><code>{escaped_content}</code></pre>
                    </div>
                </details>
            </div>
            """
        except Exception as e:
            print(f"Skipping {rel_path} due to error: {e}")

    html_content += """
        </main>
    </div>

    <script>
        function copyCode(button) {
            const container = button.closest('.code-container');
            const code = container.querySelector('code').textContent;
            
            navigator.clipboard.writeText(code).then(() => {
                const label = button.querySelector('span');
                const originalText = label.textContent;
                
                button.classList.add('copied');
                label.textContent = 'Copied!';
                
                setTimeout(() => {
                    button.classList.remove('copied');
                    label.textContent = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
            });
        }
    </script>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Successfully generated '{output_file}' with {len(py_files)} files!")

if __name__ == "__main__":
    generate_html()
