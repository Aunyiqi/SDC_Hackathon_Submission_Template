from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

OUT = Path('submission')
OUT.mkdir(exist_ok=True)

BLUE = colors.HexColor('#0B4EA2')
LIGHT = colors.HexColor('#EAF3FF')
DARK = colors.HexColor('#102A43')
GREY = colors.HexColor('#5C6B7A')

styles = getSampleStyleSheet()
TITLE = ParagraphStyle('TitleX', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=BLUE, alignment=TA_CENTER, spaceAfter=14)
H1 = ParagraphStyle('H1X', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=BLUE, spaceAfter=8)
H2 = ParagraphStyle('H2X', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=DARK, spaceAfter=6)
BODY = ParagraphStyle('BodyX', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6)
SMALL = ParagraphStyle('SmallX', parent=BODY, fontSize=8, leading=11, textColor=GREY)
CENTER = ParagraphStyle('CenterX', parent=BODY, alignment=TA_CENTER)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#B8D5F5'))
    canvas.line(18*mm, 13*mm, 192*mm, 13*mm)
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(GREY)
    canvas.drawString(18*mm, 8*mm, 'Vortex OrderGuard · SDC Hackathon 2026 · Public GitHub copy')
    canvas.drawRightString(192*mm, 8*mm, f'Page {doc.page}')
    canvas.restoreState()


def doc(path, title):
    return SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=17*mm, bottomMargin=18*mm, title=title, author='Team Vortex')


def p(text, style=BODY):
    return Paragraph(text, style)


def bullets(items):
    return [Paragraph('• ' + x, BODY) for x in items]


def section_page(story, heading, paragraphs=None, bullet_items=None, table=None, note=None):
    story += [p(heading, H1), Spacer(1, 4)]
    for x in (paragraphs or []): story.append(p(x))
    story += bullets(bullet_items or [])
    if table:
        t = Table(table, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),BLUE),('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
            ('FONTSIZE',(0,0),(-1,-1),7.5),('LEADING',(0,0),(-1,-1),10),
            ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#9FC5E8')),
            ('BACKGROUND',(0,1),(-1,-1),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
            ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ]))
        story += [Spacer(1,6), t]
    if note: story += [Spacer(1,8), p('<b>Note:</b> '+note, SMALL)]
    story.append(PageBreak())


def cover(story, title, subtitle, lines):
    story += [Spacer(1, 35*mm), p(title, TITLE), p(subtitle, ParagraphStyle('Sub', parent=H1, alignment=TA_CENTER, textColor=DARK)), Spacer(1,10*mm)]
    box = Table([[Paragraph('<br/>'.join(lines), BODY)]], colWidths=[160*mm])
    box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),0.8,BLUE),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12)]))
    story += [box, Spacer(1,12*mm), p('Team Vortex · Vortex OrderGuard', CENTER), p('Prepared 24 October 2026', CENTER), PageBreak()]


def make_preliminary():
    story=[]
    cover(story, 'SDC Hackathon 2026', 'Phase 1: Preliminary Project Proposal — Vortex OrderGuard', [
        '<b>Selected Domain:</b> Domain 2 — Orbyte Smart SME Challenge: Less Busywork, Better Business',
        '<b>Selected SDG:</b> SDG 8 — Decent Work and Economic Growth; intended alignment with Targets 8.2 and 8.3',
        '<b>Live prototype:</b> https://sdc-hackathon-submission-template.replit.app',
        '<b>Repository:</b> https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template',
        '<b>Privacy note:</b> leader email/phone and signature are intentionally omitted from this public GitHub copy; complete them in the privately submitted official copy.'
    ])
    section_page(story,'1. Team & Project Details',[
        '<b>Team Name:</b> Vortex', '<b>Project / Solution Name:</b> Vortex OrderGuard', '<b>Selected Domain:</b> Domain 2', '<b>Selected SDG Track:</b> SDG 8',
        '<b>Team Leader:</b> Aun Yi Qi', '<b>University Affiliation:</b> Multimedia University (MMU)', '<b>Number of Team Members:</b> 4',
        '<b>Leader Email & Phone:</b> Omitted from public repository copy; complete in the official private submission.'
    ])
    section_page(story,'2.1. The Problem Context',[
        'Micro and small businesses often reconcile purchase orders, receiving records and supplier invoices manually across messages, spreadsheets and documents. A quantity, unit or price mismatch can be difficult to notice quickly, and the owner may spend time checking evidence before deciding whether to contact a supplier.',
        'OrderGuard focuses on this review bottleneck. The economic relevance is broad: Malaysia’s MSMEs account for a large share of national output and employment, so practical productivity tools for small firms matter. The prototype does not claim that every SME experiences the same error rate; real SME interviews and measured baseline timing remain required validation work.',
        '<b>Research context:</b> DOSM, MSMEs Performance 2025 (released 30 July 2026); World Bank, Digitalizing SMEs to Boost Competitiveness (2022).'
    ])
    section_page(story,'2.2. The Proposed AI Solution',[
        'Vortex OrderGuard is an AI-assisted supplier discrepancy review workflow. Users provide supplier text and structured purchasing evidence. Optional AI/OCR extracts suggestions from unstructured text or invoice images, while deterministic rules compare purchase order, receiving and invoice values. The system highlights quantity, unit and price exceptions, translates open discrepancies into a visible Money at Risk signal, remembers repeat supplier-item issues, and uses a transparent Trust Gate to classify cases as CLEAR, REVIEW or BLOCKED.',
        'AI never approves, rejects, converts ambiguous units or sends supplier messages. Ambiguous evidence is blocked until a human clarifies it, and consequential actions require owner approval. Workshop-aligned skills used include GenAI/API integration, database-backed workflow design, cloud deployment through Replit, and GPU serverless OCR through RunPod.'
    ])
    section_page(story,'3.1. Conceptual Tech Stack',[
        '<b>Architecture:</b> Browser UI → Flask application → optional DeepSeek extraction / RunPod OCR → human-confirmed structured fields → deterministic discrepancy engine → Trust Gate + Supplier Pattern Memory → owner approval/rejection → simulated outbox + audit history → SQLite demo database.',
        '<b>Official sponsor-provided platform/resource used:</b> RunPod sponsor credit was used for GPU serverless OCR proof-of-use. Replit is used for the required live deployment. No live Orbyte API integration is claimed.'
    ], table=[['Component','Technology'],['Frontend','HTML, CSS, JavaScript'],['Backend','Python 3, Flask'],['Data','SQLite demo database'],['AI text extraction','DeepSeek API (optional)'],['OCR','RunPod Serverless + EasyOCR'],['Hosting','Replit'],['CI / repository','GitHub + GitHub Actions']])
    section_page(story,'3.2. Design-Thinking & Deployment Strategy',[
        'The team defined a narrow operational task: reviewing supplier discrepancies without giving AI authority over business decisions. The design prioritizes explainability, visible evidence and human control. Four synthetic judge scenarios exercise discrepancy, repeat issue, ambiguous unit and clean match flows. The public demo defaults to read-only mode; owner controls require a private time-limited access code.',
        'Deployment was tested on Replit and published as a public HTTPS application. Automated regression tests cover matching, discrepancy rules, Trust Gate blocking, owner-only actions and security controls. Phase 2 validation should add SME interviews, measured task timing and usability testing before making productivity claims.'
    ])
    section_page(story,'4. Impact Baseline & Evidence',[
        'The project uses published SME economic context and a prototype test baseline rather than claiming measured field impact. DOSM reported MSMEs contributed 39.7% of Malaysia’s GDP and 48.7% of employment in 2025. This supports the importance of SME productivity but is not a measured OrderGuard customer baseline.',
        'For Phase 2, the team will establish a controlled manual-vs-prototype baseline using the same known supplier cases and record median review time, discrepancy detection rate and false alerts.'
    ])
    section_page(story,'4. Impact Metrics — Part 1', table=[['Metric Category','Response'],['Target SDG Sub-Target(s)','SDG 8.2: higher productivity through diversification, technological upgrading and innovation; SDG 8.3: support productive activities, entrepreneurship and growth of micro/small enterprises.'],['Current Problem Baseline','Pilot baseline to be measured. Initial controlled baseline assumption: current target workflow requires manual review of 100% of supplier evidence before an owner decision. This is a test assumption, not a field-measured SME statistic.']])
    section_page(story,'4. Impact Metrics — Part 2', table=[['Metric Category','Response'],['Core Measurable KPI','Median review time per supplier check (minutes), known discrepancy detection rate (%), false-alert count on clean cases, first-time-user task completion.'],['Phase 2 Impact Target','Target at least 30% reduction in median review time on the same controlled test set while maintaining 100% detection of seeded discrepancies and zero autonomous approvals. This is a future target, not a measured result.']])
    section_page(story,'5. Preliminary Checklist', bullet_items=[
        '[ ] Mandatory GenAI, Database and Cloud Deployment workshop completion — team to confirm in private submission.',
        '[ ] Verified real-world problem — public research supports the context; direct SME validation is still pending and should be completed before claiming verification.',
        '[x] Solution targets a functional deployed application, not a theoretical business case.',
        '[x] Responses in this public copy are written within the stated word limits.'
    ])
    section_page(story,'6.1. Pre-Existing / Prior-Owned Work',[
        '<b>Answer:</b> No team-owned pre-existing product code is claimed as part of Vortex OrderGuard. The repository originated from the official SDC starter/submission template and uses declared open-source dependencies. The OrderGuard workflow, rules, UI and documentation were developed for the hackathon.'
    ])
    section_page(story,'6.2. Third-Party Code, Datasets, or Models', table=[['Name','Type','License / Terms'],['Flask','Code framework','BSD-3-Clause'],['Requests','Code library','Apache-2.0'],['Gunicorn','Code server','MIT'],['RunPod Python SDK','Code / cloud SDK','MIT'],['EasyOCR 1.7.2','Pre-trained OCR library/model','Apache-2.0'],['OpenCV / Pillow / NumPy','OCR dependencies','Upstream open-source licenses'],['DeepSeek API (optional)','External AI API','Provider terms'],['Synthetic demo records','Dataset','Team-created synthetic data; no personal data']])
    section_page(story,'6.3. Employment-Related IP Conflicts',[
        'No employer-owned code, confidential information or employer systems are intentionally included in this project. The public repository contains hackathon-specific work and synthetic data. Any team member with a separate internship or employment agreement must independently confirm that agreement before final private submission.'
    ])
    story += [p('7. Team Leader Confirmation',H1), p('The team leader confirms that the information in the final privately submitted copy is accurate to the best of the team’s knowledge and that required personal contact/signature fields will be completed there.'), Spacer(1,15*mm), p('<b>Signature:</b> Omitted from public GitHub copy.'), p('<b>Date:</b> 24 October 2026')]
    doc(OUT/'SDC2026_Vortex_Preliminary.pdf','SDC2026 Vortex Preliminary').build(story,onFirstPage=footer,onLaterPages=footer)


def make_replit():
    story=[]
    cover(story,'SDC2026 Vortex Replit POU','Proof of Replit Utilisation',[
        '<b>Live URL:</b> https://sdc-hackathon-submission-template.replit.app', '<b>Repository:</b> Aunyiqi/SDC_Hackathon_Submission_Template', '<b>Branch:</b> vortex-orderguard-submission'
    ])
    section_page(story,'Evidence of Use',[
        'Replit was used to import the GitHub project, configure the Python environment and server-side secrets, preview and test the application, and publish the public Vortex OrderGuard demo.',
        'The deployment is publicly reachable at the live URL above. Public visitors are read-only by default; owner controls require a private access code and are limited to synthetic demo records.'
    ], bullet_items=['Published public HTTPS demo','Replit publication confirmed in project UI','Gunicorn production server used for deployment','Synthetic data only','Owner access protected by secret-backed session controls'])
    story += [p('Outcome',H1), p('<b>Successful public deployment used for judging and presentation.</b>'), p('Supporting repository note: docs/REPLIT_PROOF_OF_USE.md'), p('No private owner code or deployment secret is included in this PDF.')]
    doc(OUT/'SDC2026_Vortex_Replit_POU.pdf','SDC2026 Vortex Replit POU').build(story,onFirstPage=footer,onLaterPages=footer)


def make_runpod():
    story=[]
    cover(story,'SDC2026 Vortex RunPod POU','Proof of RunPod Utilisation',[
        '<b>Purpose:</b> GPU serverless OCR extraction proof-of-use', '<b>Endpoint type:</b> Queue-based RunPod Serverless', '<b>Invocation:</b> authenticated POST to https://api.runpod.ai/v2/ojf4e2o9yj00cy/run or /runsync'
    ])
    section_page(story,'Verified RunPod Evidence',[
        'A RunPod Serverless request completed successfully during the hackathon test. The recorded result showed status COMPLETED, gpu_used=true and GPU name NVIDIA GeForce RTX 5090. Recorded delay time was approximately 9.33 seconds and execution time approximately 5.57 seconds.',
        'The worker is used only for OCR/extraction. OrderGuard performs deterministic comparison and keeps approval/rejection under human control. In the captured test, OCR execution succeeded but the structured invoice fields were empty; the project therefore treats OCR as optional input and retains manual confirmation/fallback rather than claiming perfect invoice recognition.'
    ], bullet_items=['RunPod Serverless endpoint deployed','EasyOCR-based GPU inference','Sample synthetic invoice stored at docs/sample-invoice.png','No API key committed to GitHub','OCR does not approve or reject supplier cases'])
    story += [p('Sample Output Schema',H1), p('supplier_name · item · quantity · unit · unit_price · invoice_total'), p('Supporting repository note: docs/RUNPOD_PROOF_OF_USE.md')]
    doc(OUT/'SDC2026_Vortex_Runpod_POU.pdf','SDC2026 Vortex RunPod POU').build(story,onFirstPage=footer,onLaterPages=footer)


def make_tech():
    story=[]
    cover(story,'SDC Hackathon 2026','Technical Tools Declaration — Vortex OrderGuard',[
        '<b>Instruction compliance:</b> this public copy declares APIs, cloud services, AI tools, datasets, models and sponsor resources used in the project.',
        '<b>Privacy note:</b> leader email/phone and signature are omitted from the public repository copy; complete them in the privately submitted official document.'
    ])
    section_page(story,'1. Team & Project Details',[
        '<b>Team Name:</b> Vortex','<b>Project / Solution Name:</b> Vortex OrderGuard','<b>Leader:</b> Aun Yi Qi','<b>University:</b> Multimedia University (MMU)','<b>Live Prototype:</b> https://sdc-hackathon-submission-template.replit.app','<b>Code Repository:</b> https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template','<b>Email & Phone:</b> omitted from public repository copy; complete in official private submission.'
    ])
    section_page(story,'2.1. System Architecture Overview',[
        'Browser UI → Flask web application → optional DeepSeek text extraction and/or RunPod EasyOCR → human-confirmed structured fields → deterministic PO/receiving/invoice discrepancy engine → Trust Gate + Supplier Pattern Memory → owner approval/rejection → simulated outbox + audit history → SQLite demo storage.',
        'AI and OCR only extract or structure evidence. They do not calculate final business outcomes, infer unit conversions, blacklist suppliers, approve actions or send real supplier messages.'
    ])
    section_page(story,'2.2. Languages, Frameworks & Libraries', table=[['Name & Version','Purpose','License'],['Python 3.13','Backend language','PSF License'],['Flask 3.1.3','Web framework','BSD-3-Clause'],['Requests 2.34.2','HTTP client','Apache-2.0'],['Gunicorn 26.2.0','Production WSGI server','MIT'],['RunPod SDK 1.12.0','Serverless worker/API SDK','MIT'],['EasyOCR 1.7.2','OCR extraction','Apache-2.0'],['OpenCV / Pillow / NumPy','OCR/image dependencies','Upstream open-source licenses'],['HTML / CSS / JavaScript','Frontend','Team code / web standards']])
    section_page(story,'3.1. External APIs', table=[['API and Provider','Purpose','Access Tier'],['DeepSeek API (optional)','Supplier-message structured extraction; manual fallback when unavailable','Team API account / provider pricing'],['RunPod Serverless API','Authenticated invocation of GPU OCR worker','Sponsor credit / team account'],['No live Orbyte API','Orbyte integration is simulated/aligned for MVP','None']])
    section_page(story,'3.2. Cloud Platforms & Deployment', table=[['Service & Provider','Purpose','Plan / Region'],['Replit','Public HTTPS web app hosting and publication','Team Replit account; public deployment'],['RunPod Serverless','GPU compute for EasyOCR inference','Sponsor credit / serverless GPU'],['GitHub','Public repository and GitHub Actions CI','Public repository / hosted CI']])
    section_page(story,'4.1. AI Models Used in the Solution', table=[['Model & Version','Source / Provider','Usage','License / Terms'],['EasyOCR 1.7.2 pre-trained OCR models','JaidedAI / EasyOCR','Pre-trained OCR inference on RunPod GPU','Apache-2.0'],['deepseek-chat (optional API model)','DeepSeek','Pre-trained hosted model for supplier text extraction','DeepSeek provider terms']])
    section_page(story,'4.2. Datasets', table=[['Dataset Name','Source / URL','Type','License','Personal Data?'],['OrderGuard synthetic demo records','Team-created in application','Synthetic','Team-created','No'],['Synthetic invoice sample','docs/sample-invoice.png','Synthetic','Team-created','No'],['No training dataset','N/A','None — no model training/fine-tuning performed','N/A','No']])
    section_page(story,'4.3. AI-Assisted Development Tools',[
        '<b>Did the team use generative AI for development?</b> Yes.'
    ], table=[['Tool & Version','Used For','Extent'],['ChatGPT / OpenAI','Ideation, architecture review, code/document drafting, debugging assistance, pitch/submission material','Major'],['Replit Agent','Deployment and Replit configuration troubleshooting','Moderate'],['DeepSeek (where used during development/testing)','Idea generation / optional application extraction integration','Moderate']])
    section_page(story,'4.4. Review & Responsibility for AI-Generated Output',[
        'The team reviewed generated suggestions before using them, ran automated tests for core matching/security behavior, manually verified deployment and RunPod evidence, and retained human approval for consequential workflow actions. AI-generated code or text was adapted to the project rather than treated as authoritative. Known limitations are documented, including optional provider dependencies and OCR extraction failures. The team remains responsible for all submitted code and claims.'
    ])
    section_page(story,'5. Official SDC Sponsor-Provided Resources', table=[['Sponsor','Resource','How It Was Used'],['RunPod','US$25 sponsor credit/voucher issued for team use','GPU serverless OCR proof-of-use with EasyOCR; successful RTX 5090 inference recorded']])
    section_page(story,'5.1. Is the Sponsor Resource Essential?',[
        'RunPod GPU compute demonstrates the OCR acceleration path but is not essential to the core OrderGuard discrepancy engine. The application can continue with manual structured input if OCR is unavailable. The OCR layer could be replaced by another document-extraction service or CPU-based workflow, while the deterministic comparison, Trust Gate and owner approval logic remain unchanged.'
    ])
    section_page(story,'6.1. Data Handling & Privacy',[
        'The public demo is intended for synthetic records only. No real customer personal data is required. Synthetic supplier messages or invoice images may be sent to the configured DeepSeek or RunPod service only when those optional features are used. API keys and owner access codes are stored as server-side environment secrets and are not committed to the repository. Demo cases and audit events are stored in SQLite until the demo is explicitly reset. Provider-side request retention follows the provider account/service settings; therefore only synthetic data should be submitted.'
    ])
    section_page(story,'6.2. Known Limitations & Risks',[
        'OCR can misread text or return incomplete fields; a captured RunPod test completed on GPU but returned empty structured invoice fields, so OCR remains optional and requires human confirmation. Hosted AI output may be inaccurate, so deterministic rules—not the model—calculate discrepancies. The MVP uses SQLite and process-local throttling, not production multi-tenant infrastructure. There is no live Orbyte API integration. Direct SME user validation and measured productivity impact are still pending. Mitigations include manual fallback, Trust Gate blocking, owner-only actions, synthetic data, audit history and automated regression tests.'
    ])
    section_page(story,'7. Submission Checklist', bullet_items=[
        '[x] APIs, cloud services, AI tools, models and datasets used by the project are declared.',
        '[x] Third-party libraries/models are listed with license/terms information where known.',
        '[x] No API keys, passwords or credentials are included.',
        '[x] Generative-AI development assistance is disclosed.',
        '[x] RunPod sponsor credit is declared.',
        '[x] Public live prototype and repository links are provided.',
        '[ ] Public GitHub copy intentionally omits leader email/phone and handwritten signature; complete those in the official private submission.'
    ])
    story += [p('8. Team Leader Confirmation',H1), p('By submitting the final private copy, the team leader confirms that all declared resources are complete and accurate to the best of the team’s knowledge.'), Spacer(1,15*mm), p('<b>Signature:</b> Omitted from public GitHub copy.'), p('<b>Date:</b> 24 October 2026')]
    doc(OUT/'SDC2026_Vortex_TechDeclaration.pdf','SDC2026 Vortex Technical Tools Declaration').build(story,onFirstPage=footer,onLaterPages=footer)


if __name__ == '__main__':
    make_preliminary(); make_replit(); make_runpod(); make_tech()
    for f in sorted(OUT.glob('SDC2026_Vortex_*.pdf')):
        print(f, f.stat().st_size)
