from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import PageBreak
import datetime

OUTPUT_PATH = "GymAI_Project_Report.pdf"

PRIMARY = colors.HexColor("#6366f1")
PRIMARY_DARK = colors.HexColor("#4f46e5")
ACCENT = colors.HexColor("#f59e0b")
BG_DARK = colors.HexColor("#1a1a24")
BG_CARD = colors.HexColor("#22222f")
TEXT_MUTED = colors.HexColor("#8b8ba0")
SUCCESS = colors.HexColor("#10b981")
WHITE = colors.white
LIGHT_GRAY = colors.HexColor("#f1f5f9")
MID_GRAY = colors.HexColor("#e2e8f0")
DARK_GRAY = colors.HexColor("#334155")
TABLE_HEADER_BG = colors.HexColor("#e0e7ff")
TABLE_ROW_ALT = colors.HexColor("#f8faff")

def build_styles():
    styles = getSampleStyleSheet()

    custom = {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontSize=36,
            fontName="Helvetica-Bold",
            textColor=PRIMARY,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            fontSize=14,
            fontName="Helvetica",
            textColor=TEXT_MUTED,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "cover_date": ParagraphStyle(
            "cover_date",
            fontSize=11,
            fontName="Helvetica",
            textColor=TEXT_MUTED,
            alignment=TA_CENTER,
        ),
        "section_heading": ParagraphStyle(
            "section_heading",
            fontSize=16,
            fontName="Helvetica-Bold",
            textColor=PRIMARY,
            spaceBefore=18,
            spaceAfter=6,
            borderPad=(0, 0, 4, 0),
        ),
        "sub_heading": ParagraphStyle(
            "sub_heading",
            fontSize=12,
            fontName="Helvetica-Bold",
            textColor=DARK_GRAY,
            spaceBefore=12,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=10,
            fontName="Helvetica",
            textColor=DARK_GRAY,
            leading=16,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontSize=10,
            fontName="Helvetica",
            textColor=DARK_GRAY,
            leading=16,
            leftIndent=14,
            spaceAfter=3,
            bulletIndent=4,
        ),
        "label": ParagraphStyle(
            "label",
            fontSize=9,
            fontName="Helvetica-Bold",
            textColor=PRIMARY,
            spaceAfter=2,
        ),
        "caption": ParagraphStyle(
            "caption",
            fontSize=8,
            fontName="Helvetica-Oblique",
            textColor=TEXT_MUTED,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "code": ParagraphStyle(
            "code",
            fontSize=9,
            fontName="Courier",
            textColor=PRIMARY_DARK,
            backColor=LIGHT_GRAY,
            leading=14,
            leftIndent=10,
            rightIndent=10,
            spaceAfter=6,
            spaceBefore=4,
            borderPad=6,
        ),
        "highlight_box_title": ParagraphStyle(
            "highlight_box_title",
            fontSize=11,
            fontName="Helvetica-Bold",
            textColor=WHITE,
        ),
        "highlight_box_body": ParagraphStyle(
            "highlight_box_body",
            fontSize=10,
            fontName="Helvetica",
            textColor=WHITE,
            leading=16,
        ),
    }
    return custom

def hr(color=MID_GRAY, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=4)

def section_title(text, s):
    return [
        Paragraph(text, s["section_heading"]),
        hr(PRIMARY, 1.5),
        Spacer(1, 4),
    ]

def sub_title(text, s):
    return [Paragraph(text, s["sub_heading"])]

def body(text, s):
    return Paragraph(text, s["body"])

def bullet_list(items, s):
    return [Paragraph(f"• {item}", s["bullet"]) for item in items]

def colored_table(data, col_widths, header_bg=TABLE_HEADER_BG):
    t = Table(data, colWidths=col_widths)
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), PRIMARY_DARK),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, TABLE_ROW_ALT]),
        ("TEXTCOLOR", (0, 1), (-1, -1), DARK_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ROWHEIGHT", (0, 0), (-1, -1), 20),
    ])
    t.setStyle(style)
    return t

def highlight_box(title, content_lines, s, bg=PRIMARY):
    box_data = [[Paragraph(title, s["highlight_box_title"])]]
    for line in content_lines:
        box_data.append([Paragraph(f"• {line}", s["highlight_box_body"])])
    t = Table(box_data, colWidths=[16.5 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [6]),
        ("BOX", (0, 0), (-1, -1), 0, bg),
    ]))
    return t

def build_cover(s, elements):
    elements.append(Spacer(1, 3 * cm))

    cover_box = Table(
        [[Paragraph("GymAI", s["cover_title"])],
         [Paragraph("AI-Powered Gym Plan Generator", s["cover_subtitle"])],
         [Spacer(1, 0.3 * cm)],
         [Paragraph("Project Report", s["cover_subtitle"])],
         [Spacer(1, 0.5 * cm)],
         [Paragraph(f"Generated: {datetime.date.today().strftime('%B %d, %Y')}", s["cover_date"])]],
        colWidths=[16.5 * cm]
    )
    cover_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
        ("BOX", (0, 0), (-1, -1), 3, PRIMARY),
        ("ROUNDEDCORNERS", [8]),
    ]))
    elements.append(cover_box)
    elements.append(Spacer(1, 2 * cm))

    tagline_data = [[Paragraph(
        "A personalized, intelligent fitness planning tool that generates detailed workout plans "
        "tailored to individual goals, fitness levels, and available equipment — "
        "no API key required.",
        ParagraphStyle("tl", fontSize=11, fontName="Helvetica-Oblique",
                       textColor=DARK_GRAY, alignment=TA_CENTER, leading=18)
    )]]
    tl = Table(tagline_data, colWidths=[16.5 * cm])
    tl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("BOX", (0, 0), (-1, -1), 1, MID_GRAY),
    ]))
    elements.append(tl)
    elements.append(PageBreak())

def build_overview(s, elements):
    elements += section_title("1. Project Overview", s)
    elements.append(body(
        "GymAI is a web-based application that generates fully personalized gym workout plans "
        "for users based on their individual fitness goals, experience level, weekly availability, "
        "session duration preferences, and available equipment. The application is built with a "
        "Python Flask backend and a modern, responsive single-page frontend.",
        s
    ))
    elements.append(body(
        "A core design principle of GymAI is <b>zero external dependency</b> for core functionality. "
        "The plan generation engine is built entirely in Python, producing detailed, scientifically "
        "structured plans without requiring any third-party API. When an OpenAI API key is optionally "
        "provided, the system transparently upgrades to GPT-4o-powered generation.",
        s
    ))
    elements.append(Spacer(1, 6))
    elements += sub_title("Key Objectives", s)
    elements += bullet_list([
        "Provide instant, personalized workout plans based on user input",
        "Support a wide range of goals, levels, and equipment configurations",
        "Present plans in a clean, readable, printable format",
        "Allow seamless upgrade to AI-powered generation (OpenAI GPT-4o)",
    ], s)
    elements.append(Spacer(1, 8))

def build_tech_stack(s, elements):
    elements += section_title("2. Technology Stack", s)

    data = [
        ["Component", "Technology", "Purpose"],
        ["Backend Framework", "Python Flask", "HTTP routing, SSE streaming, request handling"],
        ["Plan Generation", "Custom Python Engine", "Template-based, goal-aware plan generation"],
        ["AI (Optional)", "OpenAI GPT-4o", "AI-enhanced plan generation when API key is present"],
        ["Frontend", "HTML5 / CSS3 / JavaScript", "Single-page responsive UI"],
        ["Markdown Rendering", "marked.js (CDN)", "Renders plan output as formatted HTML"],
        ["Icons", "Font Awesome 6.5 (CDN)", "UI icons throughout the interface"],
        ["Fonts", "Inter (Google Fonts)", "Clean, modern typography"],
        ["PDF Generation", "ReportLab", "This project report"],
        ["Package Manager", "pip / uv", "Python dependency management"],
        ["Deployment Platform", "Replit", "Hosting and workflow management"],
    ]
    col_widths = [4 * cm, 4.5 * cm, 8 * cm]
    elements.append(colored_table(data, col_widths))
    elements.append(Spacer(1, 10))

def build_file_structure(s, elements):
    elements += section_title("3. Project File Structure", s)

    elements.append(body(
        "The project follows a clean, conventional Flask application layout:", s
    ))

    structure = (
        "GymAI/\n"
        "├── main.py                  ← Flask app + plan generation engine\n"
        "├── generate_report.py       ← PDF report generator (this document)\n"
        "├── readme.md                ← Project documentation\n"
        "├── pyproject.toml           ← Python project config & dependencies\n"
        "├── templates/\n"
        "│   └── index.html           ← Single-page UI with all form controls\n"
        "└── static/\n"
        "    ├── css/\n"
        "    │   └── style.css        ← Dark theme, responsive layout\n"
        "    └── js/\n"
        "        └── app.js           ← Form logic, SSE streaming, markdown render"
    )
    code_para = Paragraph(structure.replace("\n", "<br/>").replace(" ", "&nbsp;"), s["code"])
    elements.append(code_para)
    elements.append(Spacer(1, 8))

def build_features(s, elements):
    elements += section_title("4. Features & Capabilities", s)

    elements += sub_title("4.1 Goal Selection", s)
    elements.append(body(
        "Users can choose from 6 pre-defined fitness goals via a visual button grid, "
        "or type a custom goal in free text. The system maps user intent to one of "
        "6 internal goal categories that drive exercise selection, rep schemes, and nutritional guidance.", s
    ))

    data = [
        ["Goal", "Internal Key", "Focus"],
        ["Build Muscle", "muscle", "Progressive overload, hypertrophy rep ranges (6-15), high protein"],
        ["Lose Weight", "weight", "HIIT circuits, higher reps, calorie deficit guidance"],
        ["Get Fit", "fitness", "Balanced strength + cardio, moderate progression"],
        ["Athletic", "athletic", "Power, speed, plyometrics, sport-specific conditioning"],
        ["Recomp", "recomp", "Maintenance calories, dual strength + cardio approach"],
        ["Flexibility", "flexibility", "Mobility drills, stretching protocols, breathwork"],
    ]
    col_widths = [3.2 * cm, 3 * cm, 10.3 * cm]
    elements.append(colored_table(data, col_widths))
    elements.append(Spacer(1, 10))

    elements += sub_title("4.2 Fitness Level Adaptation", s)
    elements.append(body(
        "Three fitness levels (Beginner, Intermediate, Advanced) adjust training volume, "
        "rep targets, rest periods, and complexity of exercises. Beginners receive "
        "simpler movements with longer rest periods; advanced users receive heavier "
        "compound emphasis with shorter rest.", s
    ))
    elements.append(Spacer(1, 6))

    elements += sub_title("4.3 Scheduling & Weekly Splits", s)
    elements.append(body(
        "The app supports 2–6 training days per week. For each combination of days and goal, "
        "a pre-designed optimal split is selected. Rest days are intelligently distributed "
        "to maximize recovery between muscle groups.", s
    ))

    data = [
        ["Days/Week", "Muscle Building Split", "Fat Loss Split"],
        ["2", "Full Body A / Full Body B", "Full Body Circuit A / Full Body Circuit B"],
        ["3", "Push / Pull / Legs", "Upper Circuits / Lower Circuits / HIIT"],
        ["4", "Chest+Tris / Back+Bis / Legs / Shoulders", "Upper Strength / Lower Strength / Upper HIIT / Lower HIIT"],
        ["5", "Chest / Back / Legs / Shoulders / Arms", "Push HIIT / Pull / Legs / Cardio / Full Body"],
        ["6", "Chest+Tris / Back+Bis / Legs (Q) / Shoulders / Legs (H) / Arms", "Push / Pull / Legs / HIIT / Upper / Lower HIIT"],
    ]
    col_widths = [2.2 * cm, 7.2 * cm, 7.1 * cm]
    elements.append(colored_table(data, col_widths))
    elements.append(Spacer(1, 10))

    elements += sub_title("4.4 Equipment-Aware Exercise Selection", s)
    elements.append(body(
        "The plan generator selects exercises appropriate for the user's available equipment. "
        "Four equipment profiles are supported:", s
    ))
    elements += bullet_list([
        "<b>Full Gym</b> — barbells, cables, machines, dumbbells (default)",
        "<b>Dumbbells</b> — all exercises adapted to dumbbell variations",
        "<b>Bodyweight</b> — no equipment required, uses calisthenics",
        "<b>Resistance Bands</b> — band-specific exercise variations",
    ], s)
    elements.append(Spacer(1, 6))

    elements += sub_title("4.5 Real-Time Streaming Output", s)
    elements.append(body(
        "Plan content is delivered via Server-Sent Events (SSE), streaming the output "
        "word-by-word to the browser. This provides a dynamic, responsive experience "
        "similar to AI chat interfaces, with a blinking cursor during generation.", s
    ))
    elements.append(Spacer(1, 6))

    elements += sub_title("4.6 Export Options", s)
    elements += bullet_list([
        "<b>Copy to Clipboard</b> — copies the raw Markdown plan text",
        "<b>Print</b> — opens a clean print-optimized view of the plan",
    ], s)

def build_plan_engine(s, elements):
    elements.append(PageBreak())
    elements += section_title("5. Plan Generation Engine", s)

    elements.append(body(
        "The core of GymAI is a pure-Python plan generation engine that produces "
        "structured, varied, and medically-informed workout plans without any external AI service. "
        "The engine consists of several interconnected components:", s
    ))

    elements += sub_title("5.1 Exercise Database", s)
    elements.append(body(
        "A curated dictionary of exercises categorized by type (compound, accessory, cardio/HIIT, flexibility) "
        "and equipment availability. Each category contains equipment-specific lists ensuring "
        "all generated exercises are achievable with the user's stated tools.", s
    ))
    elements.append(Spacer(1, 6))

    elements += sub_title("5.2 Goal Detection (NLP Intent Mapping)", s)
    elements.append(body(
        "The <code>get_goal_key()</code> function performs lightweight natural language processing "
        "on the user's goal text, matching keywords to one of the six internal goal categories. "
        "This allows both preset button selections and free-text inputs to be handled consistently.", s
    ))
    elements.append(Spacer(1, 6))

    elements += sub_title("5.3 Rep / Set / Rest Schemes", s)
    elements.append(body(
        "The <code>get_reps_sets()</code> function returns evidence-based training parameters "
        "based on goal and experience level:", s
    ))

    data = [
        ["Goal", "Level", "Exercise Type", "Sets", "Reps", "Rest"],
        ["Muscle", "Intermediate+", "Compound", "3–4", "6–10", "90–120 sec"],
        ["Muscle", "Beginner", "Compound", "3", "8–12", "60–90 sec"],
        ["Fat Loss", "All", "Compound", "3", "12–15", "45–60 sec"],
        ["Athletic", "Intermediate+", "Compound", "4–5", "3–6", "2–3 min"],
        ["Recomp", "All", "Compound", "4", "8–12", "60–90 sec"],
        ["Flexibility", "All", "All", "1–2", "45–60s hold", "30 sec"],
    ]
    col_widths = [2.8 * cm, 2.8 * cm, 2.8 * cm, 2 * cm, 2.5 * cm, 3.6 * cm]
    elements.append(colored_table(data, col_widths))
    elements.append(Spacer(1, 10))

    elements += sub_title("5.4 Progressive Overload Framework", s)
    elements.append(body(
        "Every generated plan includes a built-in 4-week periodization cycle:", s
    ))
    elements += bullet_list([
        "<b>Week 1 — Foundation:</b> Learn movements, perfect form, moderate weight",
        "<b>Week 2 — Build:</b> Add 1-2 reps or increase weight by 2.5–5kg",
        "<b>Week 3 — Push:</b> Add 1 extra set on compounds, increase weight",
        "<b>Week 4 — Deload:</b> Reduce volume by 40%, maintain weight, recover",
    ], s)
    elements.append(Spacer(1, 6))

    elements += sub_title("5.5 Optional OpenAI Integration", s)
    elements.append(body(
        "When an <code>OPENAI_API_KEY</code> environment secret is present, the application "
        "automatically routes requests to the OpenAI GPT-4o API instead of the template engine. "
        "The streaming interface remains identical from the frontend's perspective — the switch is "
        "completely transparent to the user.", s
    ))

def build_ui_design(s, elements):
    elements += section_title("6. UI / UX Design", s)

    elements.append(body(
        "The interface uses a dark, modern aesthetic inspired by professional fitness and tech products. "
        "The layout is a two-column split: a sticky form panel on the left and a live results "
        "panel on the right.", s
    ))

    elements += sub_title("Design Decisions", s)
    data = [
        ["Design Element", "Decision", "Rationale"],
        ["Color Scheme", "Dark theme (#0f0f13 background)", "Reduces eye strain; professional gym aesthetic"],
        ["Primary Color", "Indigo (#6366f1)", "Modern, trustworthy, fitness-tech feel"],
        ["Accent Color", "Amber (#f59e0b)", "Warm contrast for highlights and day labels"],
        ["Goal Selection", "Visual icon buttons (not dropdown)", "Faster, more engaging UX for mobile users"],
        ["Days Per Week", "Slider with live display", "Intuitive, tactile interaction"],
        ["Duration", "4-option button group", "Discrete choices, no free-text errors"],
        ["Equipment", "Multi-select chips", "Allows combination selection easily"],
        ["Output", "Streaming with cursor", "Mimics AI interaction, feels dynamic"],
        ["Tables", "Markdown → HTML", "Rich formatting without pre-rendering cost"],
        ["Typography", "Inter (variable weight)", "Highly legible at small sizes on screen"],
    ]
    col_widths = [3.5 * cm, 5 * cm, 8 * cm]
    elements.append(colored_table(data, col_widths))
    elements.append(Spacer(1, 10))

def build_api(s, elements):
    elements += section_title("7. API Reference", s)

    elements += sub_title("GET /", s)
    elements.append(body("Serves the main application HTML page (index.html).", s))
    elements.append(Spacer(1, 6))

    elements += sub_title("POST /generate", s)
    elements.append(body(
        "Accepts JSON body with user inputs and returns a <code>text/event-stream</code> "
        "Server-Sent Event response with the generated plan.", s
    ))

    data = [
        ["Field", "Type", "Required", "Description"],
        ["goal", "string", "Yes", "User's fitness goal (selected or custom text)"],
        ["fitness_level", "string", "Yes", "Beginner / Intermediate / Advanced (with year range)"],
        ["days_per_week", "string", "No", "Number of training days (2–6). Default: 3"],
        ["duration", "string", "No", "Session duration in minutes. Default: 45"],
        ["equipment", "string", "No", "Comma-separated list of available equipment"],
        ["age", "string", "No", "User's age (used for personalization notes)"],
        ["injuries", "string", "No", "Known injuries or physical limitations"],
        ["additional", "string", "No", "Any extra notes or preferences"],
    ]
    col_widths = [3 * cm, 2.2 * cm, 2.2 * cm, 9.1 * cm]
    elements.append(colored_table(data, col_widths))
    elements.append(Spacer(1, 8))

    elements.append(body(
        "<b>SSE Response Events:</b> Each event is a JSON object on a <code>data:</code> line. "
        "The stream sends <code>{content: '...'}</code> chunks until done, then "
        "<code>{done: true}</code>. On error: <code>{error: 'message'}</code>.", s
    ))

def build_future(s, elements):
    elements.append(PageBreak())
    elements += section_title("8. Potential Enhancements", s)

    elements.append(body(
        "The following features could extend GymAI's capabilities in future iterations:", s
    ))

    data = [
        ["Feature", "Description", "Priority"],
        ["User Accounts", "Save and revisit previous plans with login/auth", "High"],
        ["Plan History", "Persistent storage of generated plans per user", "High"],
        ["Progress Tracking", "Log completed workouts, track weight/reps over time", "High"],
        ["Exercise Library", "Searchable database with video demonstrations", "Medium"],
        ["Nutrition Calculator", "TDEE + macro calculator integrated into the plan", "Medium"],
        ["Calendar Export", "Export weekly schedule to Google Calendar / iCal", "Medium"],
        ["Mobile App", "React Native or Expo mobile version", "Medium"],
        ["Community Plans", "Share and rate plans with other users", "Low"],
        ["Wearable Integration", "Sync with Apple Health / Fitbit / Garmin", "Low"],
        ["AI Form Check", "Upload video for AI-powered form feedback", "Low"],
    ]
    col_widths = [4 * cm, 10 * cm, 2.5 * cm]
    elements.append(colored_table(data, col_widths))
    elements.append(Spacer(1, 10))

def build_summary(s, elements):
    elements += section_title("9. Summary", s)

    elements.append(body(
        "GymAI successfully demonstrates that a sophisticated, user-friendly fitness planning "
        "tool can be built with minimal dependencies. The smart template engine delivers "
        "immediately useful, well-structured workout plans for any user — from beginners "
        "with only bodyweight to advanced athletes with full gym access.", s
    ))

    box = highlight_box(
        "Project Highlights",
        [
            "Zero external API dependency for core functionality",
            "6 goal types × 3 fitness levels × 4 equipment profiles = 72+ plan configurations",
            "2–6 day splits with evidence-based periodization",
            "Real-time streaming delivery via Server-Sent Events",
            "Seamless optional upgrade to OpenAI GPT-4o",
            "Responsive dark-mode UI with markdown rendering",
            "Copy to clipboard and print export options",
        ],
        s,
        bg=PRIMARY_DARK,
    )
    elements.append(box)
    elements.append(Spacer(1, 10))


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(TEXT_MUTED)
    page_num = canvas.getPageNumber()
    text = f"GymAI Project Report  ·  Page {page_num}"
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, text)
    canvas.setStrokeColor(MID_GRAY)
    canvas.setLineWidth(0.4)
    canvas.line(2 * cm, 1.6 * cm, A4[0] - 2 * cm, 1.6 * cm)
    canvas.restoreState()


def generate():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title="GymAI Project Report",
        author="GymAI",
        subject="AI-Powered Gym Plan Generator",
    )

    s = build_styles()
    elements = []

    build_overview(s, elements)
    build_tech_stack(s, elements)
    build_file_structure(s, elements)
    build_features(s, elements)
    build_plan_engine(s, elements)
    build_ui_design(s, elements)
    build_api(s, elements)
    build_future(s, elements)
    build_summary(s, elements)

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Report saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
