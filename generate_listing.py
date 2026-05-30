#!/usr/bin/env python3
import os
import html
import io
import zipfile
import base64

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

    # Zip all source files to embed in HTML
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for rel_path, full_path in py_files:
            try:
                zip_file.write(full_path, rel_path)
            except Exception as e:
                print(f"Failed to add {rel_path} to zip: {e}")
    zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Source Code Listing</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-color: #e2e8f0;
            --text-muted: #94a3b8;
            --accent-color: #38bdf8;
            --accent-hover: #7dd3fc;
            --border-color: #334155;
            --code-bg: #0b0f19;
            --success-color: #34d399;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 2rem 1.5rem;
            line-height: 1.5;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}

        header {{
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            flex-wrap: wrap;
            gap: 1.5rem;
        }}

        .header-text {{
            flex: 1;
            min-width: 300px;
        }}

        h1 {{
            font-size: 2.25rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .subtitle {{
            color: var(--text-muted);
            margin: 0;
            font-size: 1rem;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.625rem 1.25rem;
            font-size: 0.875rem;
            font-weight: 600;
            border-radius: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid var(--border-color);
            background-color: var(--card-bg);
            color: var(--text-color);
            text-decoration: none;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            border: none;
            color: #0f172a;
            box-shadow: 0 4px 6px -1px rgba(56, 189, 248, 0.2);
        }}

        .btn-primary:hover {{
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(56, 189, 248, 0.3);
            filter: brightness(1.1);
        }}

        .btn-primary:active {{
            transform: translateY(0);
        }}

        .file-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            margin-bottom: 1.25rem;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .file-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -4px rgba(0, 0, 0, 0.2);
            border-color: #475569;
        }}

        details {{
            width: 100%;
        }}

        summary {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.25rem;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
            outline: none;
        }}

        summary::-webkit-details-marker {{
            display: none;
        }}

        .file-info {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .file-icon {{
            color: var(--accent-color);
            width: 20px;
            height: 20px;
        }}

        .file-name {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 1rem;
            word-break: break-all;
        }}

        .toggle-indicator {{
            display: flex;
            align-items: center;
            color: var(--text-muted);
            font-size: 0.875rem;
            gap: 0.5rem;
            transition: color 0.2s;
        }}

        summary:hover .toggle-indicator {{
            color: var(--accent-color);
        }}

        .toggle-arrow {{
            transition: transform 0.2s ease;
        }}

        details[open] summary .toggle-arrow {{
            transform: rotate(90deg);
        }}

        .code-container {{
            position: relative;
            border-top: 1px solid var(--border-color);
            background-color: var(--code-bg);
        }}

        .actions-group {{
            position: absolute;
            top: 0.75rem;
            right: 0.75rem;
            display: flex;
            gap: 0.5rem;
            z-index: 10;
        }}

        .action-btn {{
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
            text-decoration: none;
        }}

        .action-btn:hover {{
            background-color: var(--accent-color);
            color: #0f172a;
            border-color: var(--accent-color);
        }}

        .action-btn.copied {{
            background-color: var(--success-color);
            color: #0f172a;
            border-color: var(--success-color);
        }}

        pre {{
            margin: 0;
            padding: 1.25rem;
            overflow-x: auto;
        }}

        code {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.875rem;
            tab-size: 4;
            display: block;
            color: #f8fafc;
        }}

        /* Toast notification styles */
        .toast-container {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            pointer-events: none;
        }}

        .toast {{
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid #ef4444;
            color: var(--text-color);
            padding: 1rem 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 16px -6px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(12px);
            font-size: 0.875rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            transform: translateY(100%);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            pointer-events: auto;
            max-width: 380px;
        }}

        .toast.show {{
            transform: translateY(0);
            opacity: 1;
        }}

        .toast-icon {{
            color: #ef4444;
            flex-shrink: 0;
        }}

        .toast-message {{
            font-weight: 500;
        }}
        
        .toast-highlight {{
            font-family: monospace;
            color: #f87171;
            background: rgba(239, 68, 68, 0.1);
            padding: 0.125rem 0.375rem;
            border-radius: 0.25rem;
            margin-left: 0.25rem;
            word-break: break-all;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-text">
                <h1>Source Code Listing</h1>
                <p class="subtitle">Collapsible repository views for easy reference, copying, and download.</p>
            </div>
            <div>
                <button class="btn btn-primary" onclick="downloadAllZip()">
                    <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                    </svg>
                    <span>Download All Sources (.zip)</span>
                </button>
            </div>
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
                        <div class="actions-group">
                            <button class="action-btn" onclick="copyCode(this)">
                                <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
                                </svg>
                                <span>Copy</span>
                            </button>
                            <a class="action-btn" href="#{rel_path}" target="_blank">
                                <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                                </svg>
                                <span>Raw</span>
                            </a>
                            <button class="action-btn" onclick="downloadFile('{os.path.basename(rel_path)}', this)">
                                <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                                </svg>
                                <span>Download</span>
                            </button>
                        </div>
                        <pre><code>{escaped_content}</code></pre>
                    </div>
                </details>
            </div>
            """
        except Exception as e:
            print(f"Skipping {rel_path} due to error: {e}")

    html_content += f"""
        </main>
    </div>

    <script>
        const zipBase64 = "{zip_base64}";

        function getCodeText(element) {{
            const container = element.closest('.code-container');
            return container.querySelector('code').textContent;
        }}

        function copyCode(button) {{
            const code = getCodeText(button);
            navigator.clipboard.writeText(code).then(() => {{
                const label = button.querySelector('span');
                const originalText = label.textContent;
                
                button.classList.add('copied');
                label.textContent = 'Copied!';
                
                setTimeout(() => {{
                    button.classList.remove('copied');
                    label.textContent = originalText;
                }}, 2000);
            }}).catch(err => {{
                console.error('Failed to copy text: ', err);
            }});
        }}

        let originalHTML = null;
        let originalStyle = null;

        function checkHash() {{
            if (originalHTML === null) {{
                originalHTML = document.body.innerHTML;
                originalStyle = {{
                    margin: document.body.style.margin || '',
                    background: document.body.style.background || '',
                    color: document.body.style.color || '',
                    fontFamily: document.body.style.fontFamily || '',
                    padding: document.body.style.padding || '',
                    whiteSpace: document.body.style.whiteSpace || '',
                    overflow: document.body.style.overflow || ''
                }};
            }}

            const targetFile = window.location.hash ? decodeURIComponent(window.location.hash.substring(1)) : '';
            
            if (!targetFile) {{
                document.body.innerHTML = originalHTML;
                for (const key in originalStyle) {{
                    document.body.style[key] = originalStyle[key];
                }}
                return;
            }}
            
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = originalHTML;
            
            const cards = tempDiv.querySelectorAll('.file-card');
            let matchedCard = null;
            for (const card of cards) {{
                const nameSpan = card.querySelector('.file-name');
                if (nameSpan) {{
                    const name = nameSpan.textContent.trim();
                    if (name === targetFile || name.endsWith('/' + targetFile)) {{
                        matchedCard = card;
                        break;
                    }}
                }}
            }}
            
            if (matchedCard) {{
                const code = matchedCard.querySelector('code').textContent;
                document.body.innerHTML = '';
                document.body.style.margin = '0';
                document.body.style.background = '#0b0f19';
                document.body.style.color = '#f8fafc';
                document.body.style.fontFamily = '"SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace';
                document.body.style.padding = '1.5rem';
                document.body.style.whiteSpace = 'pre';
                document.body.style.overflow = 'auto';
                
                const pre = document.createElement('pre');
                pre.style.margin = '0';
                pre.textContent = code;
                document.body.appendChild(pre);
            }} else {{
                document.body.innerHTML = originalHTML;
                for (const key in originalStyle) {{
                    document.body.style[key] = originalStyle[key];
                }}
                showToast(targetFile);
            }}
        }}

        function escapeHtml(text) {{
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}

        function showToast(path) {{
            let container = document.querySelector('.toast-container');
            if (!container) {{
                container = document.createElement('div');
                container.className = 'toast-container';
                document.body.appendChild(container);
            }}
            
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerHTML = `
                <svg class="toast-icon" width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
                <div class="toast-message">The path of<span class="toast-highlight">${{escapeHtml(path)}} does not exist</span></div>
            `;
            
            container.appendChild(toast);
            
            setTimeout(() => {{
                toast.classList.add('show');
            }}, 10);
            
            setTimeout(() => {{
                toast.classList.remove('show');
                setTimeout(() => {{
                    toast.remove();
                }}, 300);
            }}, 4000);
        }}

        window.addEventListener('load', checkHash);
        window.addEventListener('hashchange', checkHash);

        function downloadFile(filename, button) {{
            const code = getCodeText(button);
            const blob = new Blob([code], {{ type: 'text/plain;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}

        function downloadAllZip() {{
            const binaryString = atob(zipBase64);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {{
                bytes[i] = binaryString.charCodeAt(i);
            }}
            const blob = new Blob([bytes], {{ type: 'application/zip' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'sources.zip';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}
    </script>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Successfully generated '{output_file}' with {len(py_files)} files!")

if __name__ == "__main__":
    generate_html()
