#!/usr/bin/env python3
"""Generate markdown + HTML for Q&A export, grouped by question type."""
import json
import sys


def generate_md(answers_path, output_md, type_mapping_path=None, title="LazyGraphRAG V5"):
    with open(answers_path, encoding='utf-8') as f:
        answers = json.load(f)

    # Build question_text -> type lookup
    q_type_map = {}
    if type_mapping_path:
        with open(type_mapping_path, encoding='utf-8') as f:
            mapping = json.load(f)
        for m in mapping:
            q_type_map[m['question_text']] = m['question_type']

    # Tag each answer with type
    for a in answers:
        a['_type'] = q_type_map.get(a['question'], 'unknown')

    # Split into global and local
    global_qs = [a for a in answers if a['_type'] == 'data_global']
    local_qs = [a for a in answers if a['_type'] == 'data_local']
    unknown_qs = [a for a in answers if a['_type'] == 'unknown']

    total_latency = sum(a.get('latency_seconds', 0) for a in answers)
    avg_latency = total_latency / len(answers) if answers else 0
    success_count = sum(1 for a in answers if a.get('status') == 'success')

    md = []
    md.append(f'# {title} — Questions & Answers\n')
    md.append('**Corpus:** Leukemia Drug Discovery — 3,071 Papers  ')
    md.append(f'**Questions:** {len(answers)} ({len(global_qs)} Global + {len(local_qs)} Local)  ')
    md.append(f'**Avg Latency:** {avg_latency:.1f}s | **Total:** {total_latency/60:.1f} min  ')
    md.append(f'**Success Rate:** {success_count}/{len(answers)} ({success_count/len(answers)*100:.0f}%)\n')
    md.append('---\n')

    def write_section(qs, section_title, prefix, label):
        md.append(f'# {section_title}\n')
        md.append('---\n')
        for i, qa in enumerate(qs, 1):
            q = qa.get('question', 'N/A')
            a = qa.get('answer', 'N/A')
            lat = qa.get('latency_seconds', 0)
            qid = qa.get('question_id', '')[:12]
            md.append(f'## {prefix}{i}. [{label}] {q}\n')
            md.append(f'*ID: {qid}... | Latency: {lat:.1f}s*\n')
            md.append('**Answer:**\n')
            md.append(f'{a}\n')
            md.append('---\n')

    if global_qs:
        write_section(global_qs, 'Global Questions (Cross-Document Synthesis)', 'G', 'GLOBAL')
    if local_qs:
        write_section(local_qs, 'Local Questions (Document-Specific Facts)', 'L', 'LOCAL')
    if unknown_qs:
        write_section(unknown_qs, 'Other Questions', 'U', 'UNKNOWN')

    with open(output_md, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    print(f'Markdown: {output_md} ({len(global_qs)}G + {len(local_qs)}L = {len(answers)} Q&As)')
    return output_md


def md_to_html(md_path, html_path):
    with open(md_path, encoding='utf-8') as f:
        md_text = f.read()

    # Simple markdown to HTML conversion
    import re

    lines = md_text.split('\n')
    html_lines = []
    in_paragraph = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('# '):
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h1>{stripped[2:]}</h1>')
        elif stripped.startswith('## '):
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append(f'<h2>{stripped[3:]}</h2>')
        elif stripped == '---':
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
            html_lines.append('<hr/>')
        elif stripped == '':
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
        else:
            # Handle inline markdown
            text = stripped
            # Bold
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            # Italic
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            # Line break for trailing double space
            if line.rstrip().endswith('  '):
                text += '<br/>'

            if not in_paragraph:
                html_lines.append('<p>')
                in_paragraph = True
            html_lines.append(text)

    if in_paragraph:
        html_lines.append('</p>')

    body = '\n'.join(html_lines)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>LazyGraphRAG V5 — Questions &amp; Answers</title>
<style>
  body {{
    font-family: 'Segoe UI', Calibri, Arial, sans-serif;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
    color: #1a1a2e;
    line-height: 1.6;
    background: #fafbfc;
  }}
  h1 {{
    color: #0066cc;
    border-bottom: 3px solid #0066cc;
    padding-bottom: 10px;
    font-size: 28px;
  }}
  h2 {{
    color: #0d47a1;
    font-size: 15px;
    margin-top: 30px;
    margin-bottom: 5px;
    line-height: 1.4;
  }}
  hr {{
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 20px 0;
  }}
  p {{
    margin: 6px 0;
    font-size: 14px;
  }}
  em {{
    color: #888;
    font-size: 12px;
  }}
  strong {{
    color: #333;
  }}
  @media print {{
    body {{ max-width: 100%; padding: 20px; }}
    h2 {{ page-break-before: auto; }}
  }}
</style>
</head>
<body>
{body}
</body>
</html>"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'HTML: {html_path}')


if __name__ == '__main__':
    answers_path = sys.argv[1] if len(sys.argv) > 1 else 'lgr_answers_v5.json'
    md_path = sys.argv[2] if len(sys.argv) > 2 else 'docs/lgr_qa_v5.md'
    html_path = sys.argv[3] if len(sys.argv) > 3 else 'docs/lgr_qa_v5.html'
    type_mapping = sys.argv[4] if len(sys.argv) > 4 else None
    title = sys.argv[5] if len(sys.argv) > 5 else 'LazyGraphRAG V5'

    generate_md(answers_path, md_path, type_mapping, title)
    md_to_html(md_path, html_path)
