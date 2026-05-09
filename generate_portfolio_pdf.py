"""
Portfolio PDF Generator
Generates a professional PDF documenting the entire project.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import KeepTogether
import datetime

# Colors
NAVY = HexColor('#1e3a5f')
BLUE = HexColor('#2d6a9f')
GREEN = HexColor('#27ae60')
LIGHT_GRAY = HexColor('#f8f9fa')
DARK_GRAY = HexColor('#343a40')
MEDIUM_GRAY = HexColor('#6c757d')

def build_pdf():
    doc = SimpleDocTemplate(
        "Legal_Chatbot_Portfolio.pdf",
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle('Title', fontSize=28, textColor=white,
        alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=6)
    subtitle_style = ParagraphStyle('Subtitle', fontSize=14, textColor=white,
        alignment=TA_CENTER, fontName='Helvetica', spaceAfter=4)
    h1_style = ParagraphStyle('H1', fontSize=18, textColor=NAVY,
        fontName='Helvetica-Bold', spaceBefore=16, spaceAfter=8,
        borderPad=4)
    h2_style = ParagraphStyle('H2', fontSize=13, textColor=BLUE,
        fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', fontSize=10, textColor=DARK_GRAY,
        fontName='Helvetica', spaceAfter=6, leading=16,
        alignment=TA_JUSTIFY)
    code_style = ParagraphStyle('Code', fontSize=8, textColor=DARK_GRAY,
        fontName='Courier', spaceAfter=4, backColor=LIGHT_GRAY,
        borderPad=6, leading=12)
    bullet_style = ParagraphStyle('Bullet', fontSize=10, textColor=DARK_GRAY,
        fontName='Helvetica', spaceAfter=4, leading=14,
        leftIndent=16, bulletIndent=0)

    # ============================================================
    # COVER PAGE
    # ============================================================
    cover_data = [[Paragraph(
        '<font color="white"><b>⚖️ Legal AI Chatbot</b></font><br/>'
        '<font color="white" size="14">Complete MLOps Portfolio Project</font><br/><br/>'
        '<font color="white" size="10">Fine-tuned GPT-4o-mini • FastAPI • LangSmith • MLflow • Docker • Render</font>',
        ParagraphStyle('Cover', fontSize=28, textColor=white,
            alignment=TA_CENTER, fontName='Helvetica-Bold',
            leading=36))]]

    cover_table = Table(cover_data, colWidths=[6.5*inch])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 60),
        ('BOTTOMPADDING', (0,0), (-1,-1), 60),
        ('LEFTPADDING', (0,0), (-1,-1), 30),
        ('RIGHTPADDING', (0,0), (-1,-1), 30),
        ('ROUNDEDCORNERS', (0,0), (-1,-1), 10),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 0.3*inch))

    # Info boxes
    info_data = [
        ['Developer', 'Krishna'],
        ['Live API', 'https://legal-chatbot-a1fb.onrender.com'],
        ['GitHub', 'https://github.com/Krishna598-DS/legal-chatbot'],
        ['Date', datetime.datetime.now().strftime('%B %Y')],
        ['Model', 'ft:gpt-4o-mini-2024-07-18:personal:legal-chatbot:Dd52Ybnu'],
    ]
    info_table = Table(info_data, colWidths=[1.5*inch, 5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), BLUE),
        ('TEXTCOLOR', (0,0), (0,-1), white),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (1,0), (1,-1), 12),
        ('ROWBACKGROUNDS', (1,0), (1,-1), [LIGHT_GRAY, white]),
        ('GRID', (0,0), (-1,-1), 0.5, MEDIUM_GRAY),
        ('ROUNDEDCORNERS', (0,0), (-1,-1), 4),
    ]))
    story.append(info_table)
    story.append(PageBreak())

    # ============================================================
    # SECTION 1: PROJECT OVERVIEW
    # ============================================================
    story.append(Paragraph("1. Project Overview", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph(
        "This project demonstrates a complete, production-grade MLOps pipeline for a legal domain "
        "AI chatbot. Starting from raw data creation through fine-tuning, serving, tracing, "
        "containerization, and cloud deployment — every component reflects real-world engineering "
        "practices used at top technology companies.",
        body_style))

    story.append(Paragraph("Business Problem", h2_style))
    story.append(Paragraph(
        "General-purpose LLMs provide inconsistent legal information in varying formats. "
        "A fine-tuned domain-specific model provides consistent, professionally formatted "
        "legal information with appropriate disclaimers — at lower cost and higher reliability "
        "than prompt-engineered general models.",
        body_style))

    story.append(Paragraph("Solution Architecture", h2_style))
    arch_items = [
        "Dataset: 60 legal Q&A pairs across 6 domains, formatted as OpenAI JSONL",
        "Fine-tuning: GPT-4o-mini fine-tuned via OpenAI API — loss reduced 84.95%",
        "Experiment Tracking: MLflow logs parameters, metrics, artifacts per run",
        "API Server: FastAPI with Pydantic validation, retry logic, streaming support",
        "Observability: LangSmith traces every LLM call with full input/output/latency",
        "Frontend: Streamlit chat UI with real-time token and cost tracking",
        "Containerization: Docker Compose orchestrates API and UI as separate services",
        "Deployment: Render cloud hosting with health checks and auto-deploy from GitHub",
    ]
    for item in arch_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # ============================================================
    # SECTION 2: TECH STACK
    # ============================================================
    story.append(Paragraph("2. Technology Stack", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
    story.append(Spacer(1, 0.1*inch))

    tech_data = [
        ['Layer', 'Technology', 'Version', 'Purpose'],
        ['LLM', 'OpenAI GPT-4o-mini', 'Fine-tuned', 'Legal domain inference'],
        ['API Framework', 'FastAPI', '0.111.0', 'REST API server'],
        ['ASGI Server', 'Uvicorn', '0.29.0', 'Async request handling'],
        ['Validation', 'Pydantic', '2.7.1', 'Request/response validation'],
        ['Experiment Tracking', 'MLflow', '2.13.0', 'Training run logging'],
        ['LLM Tracing', 'LangSmith', '0.1.63', 'Inference observability'],
        ['Frontend', 'Streamlit', '1.35.0', 'Chat user interface'],
        ['Resilience', 'Tenacity', '8.3.0', 'Retry with backoff'],
        ['Tokenization', 'Tiktoken', '0.7.0', 'Token counting'],
        ['Logging', 'Loguru', '0.7.2', 'Structured logging'],
        ['Containerization', 'Docker + Compose', '29.4.3', 'Environment isolation'],
        ['Cloud Deployment', 'Render', 'Free tier', 'Public cloud hosting'],
        ['Language', 'Python', '3.11.15', 'Runtime'],
    ]

    tech_table = Table(tech_data, colWidths=[1.4*inch, 1.5*inch, 1.1*inch, 2.5*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, white]),
        ('GRID', (0,0), (-1,-1), 0.5, MEDIUM_GRAY),
    ]))
    story.append(tech_table)
    story.append(PageBreak())

    # ============================================================
    # SECTION 3: DATASET AND FINE-TUNING
    # ============================================================
    story.append(Paragraph("3. Dataset Preparation & Fine-tuning", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("Dataset Statistics", h2_style))
    ds_data = [
        ['Metric', 'Value'],
        ['Total Examples', '60'],
        ['Training Examples', '54 (90%)'],
        ['Validation Examples', '6 (10%)'],
        ['Avg Tokens per Example', '293'],
        ['Max Tokens', '358'],
        ['Min Tokens', '225'],
        ['Token Limit (OpenAI)', '4096'],
        ['Format', 'JSONL (JSON Lines)'],
        ['Random Seed', '42 (reproducible)'],
    ]
    ds_table = Table(ds_data, colWidths=[3*inch, 3.5*inch])
    ds_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, white]),
        ('GRID', (0,0), (-1,-1), 0.5, MEDIUM_GRAY),
    ]))
    story.append(ds_table)
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("Legal Domain Coverage", h2_style))
    domain_data = [
        ['Domain', 'Examples', 'Topics Covered'],
        ['Contract Law', '10', 'Breach, formation, void/voidable, force majeure, warranties'],
        ['NDA & Confidentiality', '10', 'Mutual NDA, exclusions, duration, enforcement'],
        ['Employment Law', '10', 'At-will, wrongful termination, FMLA, WARN Act'],
        ['Intellectual Property', '10', 'Copyright, patent, trademark, fair use, DMCA'],
        ['Liability & Indemnity', '10', 'Negligence, product liability, arbitration, class action'],
        ['General Legal Literacy', '10', 'Civil vs criminal, mediation, power of attorney, due diligence'],
    ]
    domain_table = Table(domain_data, colWidths=[1.5*inch, 0.8*inch, 4.2*inch])
    domain_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, white]),
        ('GRID', (0,0), (-1,-1), 0.5, MEDIUM_GRAY),
    ]))
    story.append(domain_table)
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("Training Results", h2_style))
    training_data = [
        ['Metric', 'Value'],
        ['Base Model', 'gpt-4o-mini-2024-07-18'],
        ['Fine-tuned Model ID', 'ft:gpt-4o-mini-2024-07-18:personal:legal-chatbot:Dd52Ybnu'],
        ['Fine-tuning Job ID', 'ftjob-hLTXTU5SlIoZTmmD81YWlNhC'],
        ['Epochs', '3'],
        ['Total Training Steps', '162'],
        ['Initial Training Loss', '1.86'],
        ['Final Training Loss', '0.28'],
        ['Final Validation Loss', '0.87'],
        ['Loss Reduction', '84.95%'],
        ['Estimated Cost', '$0.38'],
        ['Training Duration', '~24 minutes'],
    ]
    training_table = Table(training_data, colWidths=[2.5*inch, 4*inch])
    training_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, white]),
        ('GRID', (0,0), (-1,-1), 0.5, MEDIUM_GRAY),
    ]))
    story.append(training_table)
    story.append(PageBreak())

    # ============================================================
    # SECTION 4: API DOCUMENTATION
    # ============================================================
    story.append(Paragraph("4. API Documentation", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph(
        "The FastAPI backend exposes a RESTful API with automatic Swagger documentation. "
        "All endpoints include Pydantic validation, structured error responses, and request logging.",
        body_style))

    endpoints_data = [
        ['Method', 'Endpoint', 'Description', 'Auth'],
        ['GET', '/health', 'Liveness probe — returns server status and model ID', 'None'],
        ['GET', '/model/info', 'Returns fine-tuned model details and capabilities', 'None'],
        ['POST', '/chat', 'Send a legal question, receive a structured answer', 'None'],
        ['POST', '/chat/stream', 'Streaming response — tokens returned as generated', 'None'],
        ['GET', '/docs', 'Auto-generated Swagger UI for API exploration', 'None'],
        ['GET', '/redoc', 'ReDoc API documentation alternative', 'None'],
    ]
    ep_table = Table(endpoints_data, colWidths=[0.7*inch, 1.3*inch, 3.5*inch, 0.8*inch])
    ep_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, white]),
        ('GRID', (0,0), (-1,-1), 0.5, MEDIUM_GRAY),
    ]))
    story.append(ep_table)

    story.append(Paragraph("Sample API Request & Response", h2_style))
    story.append(Paragraph(
        'POST https://legal-chatbot-a1fb.onrender.com/chat<br/>'
        'Content-Type: application/json<br/><br/>'
        '{"question": "What is an NDA?", "temperature": 0.3, "max_tokens": 500}',
        code_style))

    story.append(Paragraph(
        '{"answer": "A Non-Disclosure Agreement (NDA) is a legally binding contract...",<br/>'
        ' "model_used": "ft:gpt-4o-mini-2024-07-18:personal:legal-chatbot:Dd52Ybnu",<br/>'
        ' "tokens_used": 317,<br/>'
        ' "response_time_ms": 9151.97,<br/>'
        ' "timestamp": "2026-05-08T07:40:56.687426"}',
        code_style))

    story.append(PageBreak())

    # ============================================================
    # SECTION 5: MLOPS PIPELINE
    # ============================================================
    story.append(Paragraph("5. MLOps Pipeline", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("MLflow Experiment Tracking", h2_style))
    mlflow_items = [
        "Tracking URI: file:///home/krishna/legal-chatbot/mlflow_runs",
        "Experiment: legal-chatbot-finetuning",
        "Run ID: dab63b95fb6c48cb835e4680bf9c9dd7",
        "Parameters logged: 10 (base model, epochs, dataset stats, inference settings)",
        "Metrics logged: 7 (training loss at 4 checkpoints, validation loss, cost, steps)",
        "Artifacts logged: 4 (model config, training JSONL, validation JSONL, run summary)",
        "Queried programmatically with mlflow.search_runs() to select best model by loss",
    ]
    for item in mlflow_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Paragraph("LangSmith Tracing", h2_style))
    langsmith_items = [
        "Project: legal-chatbot",
        "Every /chat API call traced with full prompt, response, latency, token usage",
        "@traceable decorator wraps inference functions for automatic trace capture",
        "Enables debugging bad responses by inspecting exact inputs and outputs",
        "Latency and token trends visible across all production calls",
        "Integrated with FastAPI service layer — zero changes to business logic",
    ]
    for item in langsmith_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Paragraph("Docker & Deployment", h2_style))
    docker_items = [
        "FastAPI container: python:3.11-slim base, layer-cached pip install, health check",
        "Streamlit container: separate Dockerfile, depends_on API health check",
        "Docker Compose: bridge network, service discovery by name (api:8000)",
        "Render deployment: auto-deploy on GitHub push, environment variables injected",
        "Health check endpoint pinged every 30 seconds in both Docker and Render",
    ]
    for item in docker_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # ============================================================
    # SECTION 6: INTERVIEW Q&A
    # ============================================================
    story.append(Paragraph("6. Key Interview Questions & Answers", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
    story.append(Spacer(1, 0.1*inch))

    qa_pairs = [
        ("What is fine-tuning and how does it differ from training from scratch?",
         "Fine-tuning continues training a pre-trained model on domain-specific data. "
         "Training from scratch requires billions of tokens and millions in compute. "
         "Fine-tuning requires hundreds of examples and costs dollars, leveraging the "
         "base model's existing language understanding while shifting its behavior toward the domain."),

        ("What is overfitting and did your model overfit?",
         "Overfitting is when a model memorizes training data instead of generalizing — "
         "training loss drops but validation loss rises. My training loss went from 1.86 to 0.28 "
         "while validation loss stayed at 0.87. The gap is expected; the model generalizes well "
         "as proven by correct responses to unseen legal questions."),

        ("Why FastAPI over Flask?",
         "FastAPI provides async support for concurrent LLM calls, automatic Pydantic request "
         "validation (wrong types return 422 automatically), and auto-generated Swagger UI with "
         "zero extra code. Flask requires manual validation and documentation. FastAPI is the "
         "preferred choice for ML serving APIs at modern tech companies."),

        ("What is LangSmith and why does it matter?",
         "LangSmith is an LLM observability platform that traces every inference call — the exact "
         "prompt sent, response received, latency, and token usage. In production, when a user "
         "gets a bad answer, LangSmith lets you inspect the exact input/output to determine "
         "whether the issue is the prompt, model, or data. Without it you debug blind."),

        ("How would you scale this to 10,000 concurrent users?",
         "Multiple Uvicorn workers behind nginx load balancer. Redis caching for repeated "
         "questions. AWS ECS with auto-scaling on CPU and queue depth. CDN for the Streamlit "
         "frontend. Async request queuing with Celery for expensive inference calls. "
         "Horizontal scaling of the API service with stateless design."),

        ("What is Docker and why did you use it?",
         "Docker packages code, dependencies, and runtime into portable containers that run "
         "identically everywhere. Docker Compose orchestrated two services — FastAPI and Streamlit "
         "— connected via a bridge network. Streamlit calls FastAPI by service name 'api:8000' "
         "not localhost, enabling true container-to-container communication."),

        ("How do you handle OpenAI API rate limits?",
         "Tenacity library with exponential backoff — retry up to 3 times on RateLimitError or "
         "APITimeoutError, waiting 4s then 8s then 10s between attempts. Exponential backoff "
         "prevents thundering herd where all services retry simultaneously and hit the limit again."),

        ("What would you do differently if rebuilding?",
         "Implement RAG alongside fine-tuning — fine-tuning for style and format, RAG for "
         "factual grounding from real legal documents. Add automated evaluation pipeline with "
         "semantic similarity scoring before promoting models to production. Use async OpenAI "
         "client throughout for better concurrency under load."),
    ]

    for i, (question, answer) in enumerate(qa_pairs):
        q_table = Table(
            [[Paragraph(f"Q{i+1}: {question}",
                ParagraphStyle('Q', fontSize=9, fontName='Helvetica-Bold',
                    textColor=white))]],
            colWidths=[6.5*inch]
        )
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BLUE),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
        ]))
        a_table = Table(
            [[Paragraph(answer,
                ParagraphStyle('A', fontSize=9, fontName='Helvetica',
                    textColor=DARK_GRAY, leading=14))]],
            colWidths=[6.5*inch]
        )
        a_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(KeepTogether([q_table, a_table, Spacer(1, 0.1*inch)]))

    story.append(PageBreak())

    # ============================================================
    # SECTION 7: PROJECT SUMMARY
    # ============================================================
    story.append(Paragraph("7. Project Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
    story.append(Spacer(1, 0.1*inch))

    summary_data = [
        ['Component', 'Status', 'Details'],
        ['Dataset Creation', '✅ Complete', '60 legal Q&A pairs, JSONL format, validated'],
        ['Fine-tuning', '✅ Complete', 'Loss 1.86→0.28, 84.95% reduction, $0.38 cost'],
        ['MLflow Tracking', '✅ Complete', 'Run logged, metrics queryable, artifacts saved'],
        ['FastAPI Server', '✅ Complete', '4 endpoints, Pydantic validation, Swagger docs'],
        ['LangSmith Tracing', '✅ Complete', 'Every call traced, project: legal-chatbot'],
        ['Streamlit UI', '✅ Complete', 'Chat interface, session state, cost tracking'],
        ['Docker', '✅ Complete', '2 containers, health checks, bridge network'],
        ['Cloud Deployment', '✅ Live', 'https://legal-chatbot-a1fb.onrender.com'],
        ['GitHub', '✅ Public', 'https://github.com/Krishna598-DS/legal-chatbot'],
    ]
    summary_table = Table(summary_data, colWidths=[1.8*inch, 1.2*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, white]),
        ('GRID', (0,0), (-1,-1), 0.5, MEDIUM_GRAY),
        ('TEXTCOLOR', (1,1), (1,-1), GREEN),
        ('FONTNAME', (1,1), (1,-1), 'Helvetica-Bold'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))

    # Final message
    final_data = [[Paragraph(
        '<font color="white"><b>🎯 This project demonstrates production-grade ML engineering:</b></font><br/>'
        '<font color="white">Data pipeline • Fine-tuning • Experiment tracking • REST API • '
        'LLM observability • Containerization • Cloud deployment</font><br/><br/>'
        '<font color="white">Built in 9 days from scratch with zero prior AI knowledge.</font>',
        ParagraphStyle('Final', fontSize=11, textColor=white,
            alignment=TA_CENTER, fontName='Helvetica', leading=20))]]

    final_table = Table(final_data, colWidths=[6.5*inch])
    final_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 30),
        ('BOTTOMPADDING', (0,0), (-1,-1), 30),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ('ROUNDEDCORNERS', (0,0), (-1,-1), 8),
    ]))
    story.append(final_table)

    doc.build(story)
    print("PDF generated: Legal_Chatbot_Portfolio.pdf")

if __name__ == "__main__":
    build_pdf()
