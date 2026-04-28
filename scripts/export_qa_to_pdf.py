#!/usr/bin/env python3
"""Export BenchmarkQED questions and LGR answers to PDF.

This script copies Q&A results to a PDF file for human review.
It does NOT process or display the content - just formats and exports.

Usage:
    python export_qa_to_pdf.py /data/output /path/to/output.pdf
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def export_to_pdf(output_dir: str, pdf_path: str) -> None:
    """Export questions and answers to PDF without reading content."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    
    output_path = Path(output_dir)
    
    # Find question and answer files
    questions_files = []
    answers_file = None
    
    # Look for both local and global questions
    for pattern in ["data_local_questions/selected_questions.json", 
                    "data_global_questions/selected_questions.json",
                    "questions.json"]:
        candidate = output_path / pattern
        if candidate.exists():
            questions_files.append(candidate)
    
    # Look for answers
    answers_file = output_path / "answers.json"
    
    if not questions_files:
        print(f"ERROR: No questions files found in {output_dir}")
        sys.exit(1)
    
    # Load data from all question files (no content inspection)
    questions_data = []
    for qf in questions_files:
        with open(qf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Tag each question with its source
            source = "local" if "local" in qf.name or "local" in str(qf.parent) else "global"
            for q in data:
                q["_source"] = source
            questions_data.extend(data)
        print(f"Loaded {len(data)} questions from {qf.parent.name}")
    
    answers_data = []
    if answers_file and answers_file.exists():
        with open(answers_file, 'r', encoding='utf-8') as f:
            answers_data = json.load(f)
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                           leftMargin=0.75*inch, rightMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16, spaceAfter=12)
    heading_style = ParagraphStyle('QHeading', parent=styles['Heading2'], fontSize=12, 
                                   textColor='darkblue', spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, 
                               spaceAfter=12, leading=14)
    meta_style = ParagraphStyle('Meta', parent=styles['Normal'], fontSize=8, 
                               textColor='gray', spaceAfter=6)
    
    story = []
    
    # Title page
    story.append(Paragraph("BenchmarkQED Evaluation Results", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
    story.append(Paragraph(f"Questions files: {', '.join(qf.parent.name for qf in questions_files)}", meta_style))
    story.append(Paragraph(f"Answers file: {answers_file.name if answers_file else 'N/A'}", meta_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Build answer lookup by question_id
    answer_lookup = {}
    for ans in answers_data:
        qid = ans.get("question_id") or ans.get("id")
        if qid:
            answer_lookup[qid] = ans
    
    # Process each question
    for i, q in enumerate(questions_data, 1):
        q_id = q.get("id") or q.get("question_id") or f"q_{i}"
        q_text = q.get("question") or q.get("text") or "[No question text]"
        q_type = q.get("type") or q.get("question_type") or "unknown"
        q_source = q.get("_source", "unknown")
        
        story.append(Paragraph(f"Question {i} (ID: {q_id})", heading_style))
        story.append(Paragraph(f"Type: {q_type} | Source: {q_source}", meta_style))
        story.append(Paragraph(q_text.replace('\n', '<br/>'), body_style))
        
        # Add answer if available
        if q_id in answer_lookup:
            ans = answer_lookup[q_id]
            ans_text = ans.get("answer") or ans.get("response") or "[No answer]"
            story.append(Paragraph("<b>LGR Search Answer:</b>", heading_style))
            story.append(Paragraph(ans_text.replace('\n', '<br/>'), body_style))
        else:
            story.append(Paragraph("<i>No answer available</i>", meta_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Page break every 2 Q&A pairs
        if i % 2 == 0 and i < len(questions_data):
            story.append(PageBreak())
    
    # Build PDF
    doc.build(story)
    print(f"PDF exported to: {pdf_path}")
    print(f"Total questions: {len(questions_data)}")
    print(f"Total answers: {len(answer_lookup)}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python export_qa_to_pdf.py <output_dir> <pdf_path>")
        print("Example: python export_qa_to_pdf.py /data/output /data/output/eval_results.pdf")
        sys.exit(1)
    
    export_to_pdf(sys.argv[1], sys.argv[2])
