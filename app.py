"""
============================================================
  Leg Comfort and Ergonomic Sitting Survey
  Psychological State Assessment Program  —  Streamlit Edition
  Module: Fundamentals of Programming, 4BUIS008C (Level 4)
  Version: 2.0
  Run with:  streamlit run streamlit_survey.py
============================================================
"""

import json
import csv
import io
import os
from datetime import datetime
import streamlit as st

# ================================================================
# PAGE CONFIG  (must be first Streamlit call)
# ================================================================
st.set_page_config(
    page_title="Leg Comfort Survey",
    page_icon="🪑",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ================================================================
# SECTION 1 — REQUIRED VARIABLE TYPES (all 10 demonstrated here)
# ================================================================
VERSION_FLOAT: float        = 2.0                                    # float
ALLOWED_SAVE_EXT: frozenset = frozenset({".json", ".csv", ".txt"})   # frozenset
SESSION_FILES: set          = set()                                   # set
CURRENT_RECORD: dict        = {}                                      # dict

# int, str, list, tuple, range, bool used throughout (annotated at first use)

# ================================================================
# SECTION 2 — EMBEDDED QUESTIONS  (19 questions, 4 domains)
# ================================================================
QUESTIONS: list = [                                                   # list type
    # ---- Domain A: Leg Symptoms ----
    {
        "id": 1, "domain": "Leg Symptoms",
        "q": "During or after a long sitting session, how often do you notice heaviness in your legs?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 2, "domain": "Leg Symptoms",
        "q": "How frequently do you experience swelling or puffiness in your feet or ankles after sitting for an extended period?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 3, "domain": "Leg Symptoms",
        "q": "How often do you feel numbness or tingling sensations in your legs while seated?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 4, "domain": "Leg Symptoms",
        "q": "How regularly do you experience aching or pain behind your knees during prolonged sitting?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 5, "domain": "Leg Symptoms",
        "q": "How often does your foot lose sensation ('fall asleep') during a seated study or work session?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 6, "domain": "Leg Symptoms",
        "q": "How frequently do you feel muscle cramps or tightness in your calves after sitting for a long period?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    # ---- Domain B: Chair-Fit Indicators ----
    {
        "id": 7, "domain": "Chair-Fit Indicators",
        "q": "When seated, how often do you notice uncomfortable pressure at the back of your thighs from the seat edge?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 8, "domain": "Chair-Fit Indicators",
        "q": "How frequently do your feet dangle or fail to rest flat on the floor while you are seated?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 9, "domain": "Chair-Fit Indicators",
        "q": "How often does the front edge of your chair press uncomfortably into the underside of your thighs?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 10, "domain": "Chair-Fit Indicators",
        "q": "How regularly do you feel that your chair height forces you to hold your legs in an awkward or strained position?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    # ---- Domain C: Postural Behaviour ----
    {
        "id": 11, "domain": "Postural Behaviour",
        "q": "How often do you cross your legs or feet under the chair during extended sitting sessions?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 12, "domain": "Postural Behaviour",
        "q": "How frequently do you notice yourself slouching or shifting your weight to one side when seated for long periods?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 13, "domain": "Postural Behaviour",
        "q": "How often do you perch on the edge of your chair rather than sitting with your back fully supported?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    {
        "id": 14, "domain": "Postural Behaviour",
        "q": "How frequently do you excessively change your leg position due to discomfort during a single sitting session?",
        "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)],
        "reverse": False,
    },
    # ---- Domain D: Protective Habits (REVERSE scored) ----
    {
        "id": 15, "domain": "Protective Habits",
        "q": "How often do you take short standing or walking breaks during long sitting sessions?",
        "opts": [("Always", 0), ("Often", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)],
        "reverse": True,
    },
    {
        "id": 16, "domain": "Protective Habits",
        "q": "How regularly do you adjust your chair height so that your feet rest flat and comfortably on the floor?",
        "opts": [("Always", 0), ("Often", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)],
        "reverse": True,
    },
    {
        "id": 17, "domain": "Protective Habits",
        "q": "How often do you use a footrest or similar support when your feet cannot naturally reach the floor?",
        "opts": [("Always", 0), ("Often", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)],
        "reverse": True,
    },
    {
        "id": 18, "domain": "Protective Habits",
        "q": "How frequently do you perform leg stretches or light movements during or after a prolonged sitting session?",
        "opts": [("Always", 0), ("Often", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)],
        "reverse": True,
    },
    {
        "id": 19, "domain": "Protective Habits",
        "q": "How often do you consciously check and correct your sitting posture during a long study or work session?",
        "opts": [("Always", 0), ("Often", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)],
        "reverse": True,
    },
]

QUESTION_INDEX_RANGE: range = range(len(QUESTIONS))                  # range type

# ================================================================
# SECTION 3 — PSYCHOLOGICAL STATES  (6 states, score 0–76)
# ================================================================
PSYCH_STATES: dict = {
    "Minimal Risk":   {"range": (0,  12), "colour": "#27ae60", "emoji": "🟢",
                       "description": "Excellent leg comfort and sitting habits detected. Your ergonomic practices are effective — no intervention required at this time. Continue your current routine and maintain regular movement breaks."},
    "Low Risk":       {"range": (13, 25), "colour": "#2ecc71", "emoji": "🟩",
                       "description": "Minor leg discomfort or sub-optimal sitting habits detected. Self-monitoring is recommended. Aim to take a short standing break every 30–45 minutes and verify that your feet rest flat on the floor."},
    "Moderate Risk":  {"range": (26, 38), "colour": "#f39c12", "emoji": "🟡",
                       "description": "Noticeable leg discomfort and/or inconsistent ergonomic habits detected. Review your chair height, seat depth, and break frequency. Consider using a footrest if your feet do not reach the floor comfortably."},
    "High Risk":      {"range": (39, 51), "colour": "#e67e22", "emoji": "🟠",
                       "description": "Significant leg discomfort and poor ergonomic habits identified. A formal workstation ergonomic adjustment is strongly advised. Seek guidance from an occupational health professional or ergonomics advisor."},
    "Very High Risk": {"range": (52, 63), "colour": "#e74c3c", "emoji": "🔴",
                       "description": "Serious leg discomfort patterns and/or severely deficient protective habits detected. A professional ergonomic assessment is urgently recommended. Persistent symptoms such as swelling or numbness should be evaluated by a medical professional."},
    "Severe Risk":    {"range": (64, 76), "colour": "#8e44ad", "emoji": "🟣",
                       "description": "Critical ergonomic risk identified. Immediate medical and professional ergonomic evaluation is required. Do not ignore recurring pain, significant swelling, or persistent numbness — these may indicate circulation or musculoskeletal conditions requiring urgent attention."},
}

# ================================================================
# SECTION 4 — VALIDATION FUNCTIONS
# ================================================================

def validate_name(name: str) -> bool:
    """
    Validates that a name contains only letters, hyphens, apostrophes, and spaces.
    Covers names such as O'Connor, Smith-Jones, Mary Ann.
    Uses a FOR LOOP to inspect each character.
    """
    name_stripped: str = name.strip()                                # str type
    if len(name_stripped) == 0:
        return False
    allowed_extra: tuple = ("-", "'", " ")                           # tuple type
    is_valid: bool = True                                            # bool type
    for char in name_stripped:                                       # for loop — validation
        if not (char.isalpha() or char in allowed_extra):
            is_valid = False
            break
    return is_valid


def validate_dob(dob: str) -> bool:
    """Validates date of birth in YYYY-MM-DD format; must not be a future date."""
    try:
        parsed = datetime.strptime(dob.strip(), "%Y-%m-%d")
        is_valid: bool = parsed <= datetime.now()
        return is_valid
    except ValueError:
        return False


def validate_student_id(sid: str) -> bool:
    """
    Validates that the student ID consists exclusively of digits.
    Uses a FOR LOOP over each character.
    """
    sid_clean: str = sid.strip()
    if len(sid_clean) == 0:
        return False
    is_valid: bool = True                                            # bool
    for ch in sid_clean:                                             # for loop — validation
        if not ch.isdigit():
            is_valid = False
            break
    return is_valid


def validate_all_fields(field_map: dict) -> list:
    """
    Iterates over all fields using a FOR LOOP and collects names of invalid ones.
    Returns a list of error field names (empty = all valid).
    """
    errors: list = []                                                # list type
    for field_name, (value, validator) in field_map.items():        # for loop — validation
        if not validator(value):
            errors.append(field_name)
    return errors


# ================================================================
# SECTION 5 — SCORING & INTERPRETATION FUNCTIONS
# ================================================================

def interpret_score(score: int) -> tuple:                            # int parameter
    """
    Maps a numeric total score to a psychological state.
    Returns a tuple of (state_name: str, state_data: dict).
    Uses conditional if/elif/else logic.
    """
    result_state: str = "Unknown"
    result_data: dict = {"colour": "#7f8c8d", "emoji": "⚪",
                         "description": "Score could not be matched."}
    for state_name, state_data in PSYCH_STATES.items():             # for loop
        low, high = state_data["range"]
        if low <= score <= high:                                     # if — conditional
            result_state = state_name
            result_data  = state_data
            break
    return (result_state, result_data)                               # tuple returned


def build_record(given_name: str, surname: str, dob: str,
                 student_id: str, answers: list) -> dict:
    """Builds the full student result record as a dict."""
    total_score: int = 0                                             # int type
    for ans in answers:                                              # for loop
        total_score += ans["score"]
    state_name, state_data = interpret_score(total_score)
    record: dict = {
        "given_name":  given_name,
        "surname":     surname,
        "dob":         dob,
        "student_id":  student_id,
        "date_taken":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_score": total_score,
        "max_score":   len(QUESTIONS) * 4,
        "result":      state_name,
        "description": state_data["description"],
        "answers":     answers,
        "version":     VERSION_FLOAT,
    }
    return record


# ================================================================
# SECTION 6 — FILE GENERATION FUNCTIONS (in-memory for Streamlit)
# ================================================================

def generate_json_bytes(record: dict) -> bytes:
    """Serialises the result record to JSON bytes for download."""
    SESSION_FILES.add("result.json")
    return json.dumps(record, indent=2, ensure_ascii=False).encode("utf-8")


def generate_csv_bytes(record: dict) -> bytes:
    """Serialises the result record to CSV bytes for download."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Field", "Value"])
    for key, val in record.items():                                  # for loop
        if key != "answers":
            writer.writerow([key, val])
    writer.writerow([])
    writer.writerow(["#", "Question", "Domain", "Selected Option", "Score"])
    for i, ans in enumerate(record.get("answers", []), start=1):
        writer.writerow([i, ans.get("question", ""), ans.get("domain", ""),
                         ans.get("selected_option", ""), ans.get("score", "")])
    SESSION_FILES.add("result.csv")
    return output.getvalue().encode("utf-8")


def generate_txt_bytes(record: dict) -> bytes:
    """Serialises the result record to plain-text bytes for download."""
    lines: list = []
    lines.append("=" * 65)
    lines.append("  LEG COMFORT AND ERGONOMIC SITTING SURVEY — RESULT")
    lines.append("=" * 65)
    lines.append(f"  Name        : {record.get('given_name','')} {record.get('surname','')}")
    lines.append(f"  Date of Birth: {record.get('dob','')}")
    lines.append(f"  Student ID  : {record.get('student_id','')}")
    lines.append(f"  Date Taken  : {record.get('date_taken','')}")
    lines.append(f"  Total Score : {record.get('total_score','')} / {record.get('max_score','')}")
    lines.append(f"  Result      : {record.get('result','')}")
    lines.append(f"  Advice      : {record.get('description','')}")
    lines.append("-" * 65)
    lines.append("  ANSWERS:")
    for idx in QUESTION_INDEX_RANGE:                                 # range type in use
        answers = record.get("answers", [])
        if idx < len(answers):
            ans = answers[idx]
            lines.append(f"  Q{idx+1:02d}. [{ans.get('domain','')}]")
            lines.append(f"       {ans.get('question','')}")
            lines.append(f"       -> {ans.get('selected_option','')}  (Score: {ans.get('score','')})")
            lines.append("")
    lines.append("=" * 65)
    SESSION_FILES.add("result.txt")
    return "\n".join(lines).encode("utf-8")


def load_questions_from_uploaded(file_bytes: bytes) -> list:
    """
    Parses question data from uploaded JSON bytes.
    Uses a WHILE LOOP for retry on transient decode errors.
    Returns list of questions or None.
    """
    attempts: int  = 0                                               # int type
    max_attempts: int = 3
    loaded_data = None

    while attempts < max_attempts:                                   # while loop — validation
        try:
            loaded_data = json.loads(file_bytes.decode("utf-8"))
            break
        except json.JSONDecodeError:
            return None
        except Exception:
            attempts += 1
            if attempts >= max_attempts:
                return None

    if isinstance(loaded_data, list):                                # conditional if
        return loaded_data
    elif isinstance(loaded_data, dict) and "questions" in loaded_data:  # elif
        return loaded_data["questions"]
    else:                                                            # else
        return None


def generate_questions_export_bytes() -> bytes:
    """Exports embedded questions + states to JSON bytes for download."""
    export: dict = {
        "version": VERSION_FLOAT,
        "questions": [
            {**q, "opts": [list(o) for o in q["opts"]]}
            for q in QUESTIONS
        ],
        "psychological_states": {
            k: {"range": list(v["range"]), "colour": v["colour"],
                "description": v["description"]}
            for k, v in PSYCH_STATES.items()
        },
    }
    return json.dumps(export, indent=2, ensure_ascii=False).encode("utf-8")


# ================================================================
# SECTION 7 — CUSTOM CSS
# ================================================================
def inject_css() -> None:
    st.markdown("""
    <style>
      /* ---- Global ---- */
      [data-testid="stAppViewContainer"] {
        background: #1e2330;
      }
      [data-testid="stHeader"] { background: transparent; }
      .block-container { padding-top: 2rem; max-width: 760px; }

      /* ---- Typography ---- */
      h1 { color: #4a9fd4 !important; font-size: 1.9rem !important; }
      h2 { color: #4a9fd4 !important; font-size: 1.35rem !important; }
      h3 { color: #ecf0f1 !important; font-size: 1.1rem !important; }
      p, label, div { color: #ecf0f1; }

      /* ---- Cards ---- */
      .card {
        background: #2a3145;
        border-radius: 10px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1rem;
      }
      .card-accent {
        border-left: 4px solid #4a9fd4;
      }

      /* ---- Result badge ---- */
      .result-badge {
        border-radius: 10px;
        padding: 1.2rem 1.8rem;
        text-align: center;
        margin-bottom: 1rem;
      }
      .result-badge h2 { color: white !important; margin: 0; }
      .result-badge p  { color: rgba(255,255,255,0.85); font-size: 1.05rem; margin: 0.3rem 0 0; }

      /* ---- Progress text ---- */
      .progress-text {
        color: #8899aa;
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
      }

      /* ---- Domain pill ---- */
      .domain-pill {
        display: inline-block;
        background: #323a52;
        color: #4a9fd4;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }

      /* ---- Info row ---- */
      .info-row {
        background: #2a3145;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 0.82rem;
        color: #8899aa;
        margin-bottom: 1rem;
      }

      /* ---- Divider ---- */
      hr { border-color: #323a52; }

      /* ---- Streamlit widget overrides ---- */
      .stRadio > label { color: #ecf0f1 !important; font-size: 0.95rem; }
      .stRadio [data-testid="stWidgetLabel"] { color: #ecf0f1 !important; }
      div[role="radiogroup"] label { color: #ecf0f1 !important; }
      .stTextInput input {
        background: #2a3145 !important;
        color: #ecf0f1 !important;
        border: 1px solid #323a52 !important;
        border-radius: 6px;
      }
      .stTextInput input:focus {
        border-color: #4a9fd4 !important;
        box-shadow: 0 0 0 2px rgba(74,159,212,0.25) !important;
      }
      .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        transition: opacity 0.15s;
      }
      .stButton > button:hover { opacity: 0.88; }
      .stDownloadButton > button {
        border-radius: 6px;
        font-weight: 600;
      }

      /* ---- Sidebar (hide entirely) ---- */
      [data-testid="collapsedControl"] { display: none; }
      section[data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)


# ================================================================
# SECTION 8 — SESSION STATE INITIALISATION
# ================================================================
def init_state() -> None:
    """Initialises all session state keys with default values."""
    defaults: dict = {
        "page":         "menu",
        "questions":    QUESTIONS,
        "given_name":   "",
        "surname":      "",
        "dob":          "",
        "student_id":   "",
        "current_idx":  0,
        "answers":      [],
        "record":       {},
        "loaded_data":  {},
    }
    for key, val in defaults.items():                                # for loop
        if key not in st.session_state:                              # conditional if
            st.session_state[key] = val


def go(page: str, **kwargs) -> None:
    """Navigates to a new page by updating session state, then reruns."""
    st.session_state.page = page
    for k, v in kwargs.items():                                      # for loop
        st.session_state[k] = v
    st.rerun()


# ================================================================
# SECTION 9 — PAGE: MAIN MENU
# ================================================================
def page_menu() -> None:
    st.markdown("<h1 style='text-align:center'>🪑 Leg Comfort & Ergonomic Sitting Survey</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8899aa; margin-top:-0.5rem'>"
                "Psychological State Assessment &nbsp;|&nbsp; Version 2.0</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<div class='card card-accent'>"
                "<p style='color:#8899aa; font-size:0.92rem'>"
                "This survey assesses ergonomic risk and leg comfort during prolonged sitting. "
                "It covers <b>leg symptoms</b>, <b>chair-fit indicators</b>, "
                "<b>postural behaviour</b>, and <b>protective habits</b> across 19 questions.</p>"
                "</div>", unsafe_allow_html=True)

    st.markdown("### Choose an option")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📂  Load existing result file", use_container_width=True):
            go("load")
        if st.button("📋  New questionnaire  (built-in questions)", use_container_width=True):
            go("info", questions=QUESTIONS)

    with col2:
        if st.button("📁  New questionnaire  (load questions from file)", use_container_width=True):
            go("load_questions")
        if st.button("💾  Export questions to JSON file", use_container_width=True):
            go("export_questions")


# ================================================================
# SECTION 10 — PAGE: STUDENT INFORMATION
# ================================================================
def page_info() -> None:
    st.markdown("<h1>📝 Student Information</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8899aa'>Please complete all fields. "
                "Your details will be saved with your result.</p>", unsafe_allow_html=True)
    st.markdown("---")

    with st.form("info_form"):
        col1, col2 = st.columns(2)
        with col1:
            given_name = st.text_input("Given Name",
                                       value=st.session_state.given_name,
                                       placeholder="e.g. Mary Ann")
            dob = st.text_input("Date of Birth",
                                value=st.session_state.dob,
                                placeholder="YYYY-MM-DD")
        with col2:
            surname = st.text_input("Surname",
                                    value=st.session_state.surname,
                                    placeholder="e.g. O'Connor")
            student_id = st.text_input("Student ID",
                                       value=st.session_state.student_id,
                                       placeholder="digits only, e.g. 00123456")

        st.markdown("<br>", unsafe_allow_html=True)
        bc, _, sc = st.columns([2, 3, 2])
        with bc:
            back = st.form_submit_button("← Back", use_container_width=True)
        with sc:
            start = st.form_submit_button("Start Survey →", use_container_width=True,
                                          type="primary")

    if back:
        go("menu")

    if start:
        # Build field validation map and run validate_all_fields (for loop inside)
        field_map: dict = {
            "Given Name":                  (given_name,  validate_name),
            "Surname":                     (surname,     validate_name),
            "Date of Birth (YYYY-MM-DD)":  (dob,         validate_dob),
            "Student ID (digits only)":    (student_id,  validate_student_id),
        }
        errors_found: bool = True                                    # bool
        while errors_found:                                          # while loop — validation
            error_fields: list = validate_all_fields(field_map)     # for loop inside
            if not error_fields:                                     # conditional if
                errors_found = False
            else:                                                    # conditional else
                st.error("⚠  Invalid or missing:  " + ",  ".join(error_fields))
                break   # stop and let the user correct — form will re-render

        if not errors_found:
            go("survey",
               given_name=given_name.strip(),
               surname=surname.strip(),
               dob=dob.strip(),
               student_id=student_id.strip(),
               current_idx=0,
               answers=[None] * len(st.session_state.questions))


# ================================================================
# SECTION 11 — PAGE: SURVEY
# ================================================================
def page_survey() -> None:
    questions: list = st.session_state.questions
    idx: int        = st.session_state.current_idx                   # int type
    total: int      = len(questions)

    q_data: dict = questions[idx]

    # ---- Progress ----
    progress_pct: float = idx / total                                # float arithmetic
    st.markdown(f"<p class='progress-text'>Question {idx + 1} of {total}</p>",
                unsafe_allow_html=True)
    st.progress(progress_pct)

    # ---- Domain pill ----
    st.markdown(f"<span class='domain-pill'>{q_data.get('domain','')}</span>",
                unsafe_allow_html=True)

    # ---- Question card ----
    st.markdown(f"<div class='card'><h3>Q{idx+1}. {q_data['q']}</h3></div>",
                unsafe_allow_html=True)

    # Build option labels list
    opt_labels: list = [label for label, _ in q_data["opts"]]

    # Determine previously selected index (if the user navigated back)
    prev_answer = st.session_state.answers[idx]
    default_idx = None
    if prev_answer is not None:                                      # conditional if
        for i, (label, _) in enumerate(q_data["opts"]):             # for loop
            if label == prev_answer["selected_option"]:
                default_idx = i
                break

    selected_label = st.radio(
        "Choose your answer:",
        opt_labels,
        index=default_idx,
        key=f"radio_q{idx}",
    )

    # Reverse-score note
    if q_data.get("reverse"):                                        # conditional if
        st.caption("ℹ️  Protective habit — choosing 'Always' contributes 0 points (lowest risk).")

    st.markdown("---")

    # ---- Navigation ----
    nav_cols = st.columns([1, 3, 1])
    with nav_cols[0]:
        back_disabled: bool = (idx == 0)
        if st.button("← Back", disabled=back_disabled, use_container_width=True):
            # Save current answer if something is selected
            if selected_label:
                score: int = next(sc for lbl, sc in q_data["opts"]  # int type
                                  if lbl == selected_label)
                st.session_state.answers[idx] = {
                    "question":        q_data["q"],
                    "domain":          q_data.get("domain", ""),
                    "selected_option": selected_label,
                    "score":           score,
                }
            st.session_state.current_idx -= 1
            st.rerun()

    with nav_cols[2]:
        btn_label: str = "Finish ✓" if idx == total - 1 else "Next →"
        if st.button(btn_label, type="primary", use_container_width=True):
            if selected_label is None:                               # conditional if
                st.error("⚠  Please select an answer before continuing.")
            else:                                                    # conditional else
                score: int = next(sc for lbl, sc in q_data["opts"]
                                  if lbl == selected_label)
                st.session_state.answers[idx] = {
                    "question":        q_data["q"],
                    "domain":          q_data.get("domain", ""),
                    "selected_option": selected_label,
                    "score":           score,
                }
                if idx < total - 1:                                  # conditional if
                    st.session_state.current_idx += 1
                    st.rerun()
                else:                                                # conditional else — done
                    record: dict = build_record(
                        st.session_state.given_name,
                        st.session_state.surname,
                        st.session_state.dob,
                        st.session_state.student_id,
                        st.session_state.answers,
                    )
                    global CURRENT_RECORD
                    CURRENT_RECORD = record
                    go("result", record=record)


# ================================================================
# SECTION 12 — PAGE: RESULTS
# ================================================================
def page_result() -> None:
    record: dict = st.session_state.record
    if not record:                                                   # conditional if
        st.warning("No result data found. Please take the survey first.")
        if st.button("← Back to Menu"):
            go("menu")
        return

    state_name: str  = record.get("result", "Unknown")
    description: str = record.get("description", "")
    total: int       = record.get("total_score", 0)
    max_s: int       = record.get("max_score", 76)
    _, state_data    = interpret_score(total)
    colour: str      = state_data.get("colour", "#4a9fd4")
    emoji: str       = state_data.get("emoji", "⚪")

    st.markdown("<h1 style='text-align:center'>✅ Survey Complete</h1>",
                unsafe_allow_html=True)

    # Result badge
    st.markdown(
        f"<div class='result-badge' style='background:{colour}'>"
        f"<h2>{emoji} &nbsp; {state_name}</h2>"
        f"<p>Total Score: &nbsp; <strong>{total}</strong> / {max_s}</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Score bar
    st.progress(total / max_s)

    # Description
    st.markdown("<div class='card card-accent'>"
                f"<p style='color:#8899aa; font-size:0.8rem; margin-bottom:4px'>"
                f"ASSESSMENT &amp; RECOMMENDATION</p>"
                f"<p>{description}</p></div>",
                unsafe_allow_html=True)

    # Student info strip
    st.markdown(
        f"<div class='info-row'>"
        f"👤 <b>{record.get('given_name','')} {record.get('surname','')}</b>"
        f" &nbsp;|&nbsp; DOB: {record.get('dob','')}"
        f" &nbsp;|&nbsp; ID: {record.get('student_id','')}"
        f" &nbsp;|&nbsp; Taken: {record.get('date_taken','')}"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ---- Answer breakdown (expandable) ----
    with st.expander("📋 View full answer breakdown"):
        for i, ans in enumerate(record.get("answers", []), start=1):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(
                    f"<p style='margin:0; font-size:0.88rem; color:#8899aa'>"
                    f"<b>Q{i}. [{ans.get('domain','')}]</b></p>"
                    f"<p style='margin:0 0 4px; font-size:0.9rem'>{ans.get('question','')}</p>"
                    f"<p style='margin:0; color:#4a9fd4; font-size:0.88rem'>"
                    f"→ {ans.get('selected_option','')}</p>",
                    unsafe_allow_html=True,
                )
            with col_b:
                st.markdown(
                    f"<p style='text-align:right; font-size:1.1rem; font-weight:700; "
                    f"color:#ecf0f1; margin-top:18px'>{ans.get('score','')}</p>",
                    unsafe_allow_html=True,
                )
            st.markdown("<hr style='margin:6px 0'>", unsafe_allow_html=True)

    # ---- Download buttons ----
    st.markdown("### 💾 Save your result")
    sid: str = record.get("student_id", "student")
    dc1, dc2, dc3 = st.columns(3)

    with dc1:
        st.download_button(
            label="⬇  Download JSON",
            data=generate_json_bytes(record),
            file_name=f"result_{sid}.json",
            mime="application/json",
            use_container_width=True,
        )
    with dc2:
        st.download_button(
            label="⬇  Download CSV",
            data=generate_csv_bytes(record),
            file_name=f"result_{sid}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with dc3:
        st.download_button(
            label="⬇  Download TXT",
            data=generate_txt_bytes(record),
            file_name=f"result_{sid}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⌂ Return to Main Menu", use_container_width=True):
        go("menu")


# ================================================================
# SECTION 13 — PAGE: LOAD EXISTING RESULT
# ================================================================
def page_load() -> None:
    st.markdown("<h1>📂 Load Existing Result</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8899aa'>Upload a previously saved result file "
                "(JSON, CSV, or TXT) to view its contents.</p>", unsafe_allow_html=True)
    st.markdown("---")

    uploaded = st.file_uploader("Choose a result file", type=["json", "csv", "txt"],
                                 label_visibility="collapsed")

    if uploaded is not None:                                         # conditional if
        ext: str = os.path.splitext(uploaded.name)[1].lower()
        SESSION_FILES.add(uploaded.name)

        if ext == ".json":                                           # conditional if
            try:
                data: dict = json.loads(uploaded.read().decode("utf-8"))
                state_name: str = data.get("result", "Unknown")
                _, state_data   = interpret_score(data.get("total_score", 0))
                colour: str     = state_data.get("colour", "#4a9fd4")
                emoji: str      = state_data.get("emoji", "⚪")

                st.markdown(
                    f"<div class='result-badge' style='background:{colour}'>"
                    f"<h2>{emoji} &nbsp; {state_name}</h2>"
                    f"<p>Total Score: <strong>{data.get('total_score','?')}</strong> "
                    f"/ {data.get('max_score','?')}</p>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div class='info-row'>"
                    f"👤 <b>{data.get('given_name','')} {data.get('surname','')}</b>"
                    f" &nbsp;|&nbsp; DOB: {data.get('dob','')}"
                    f" &nbsp;|&nbsp; ID: {data.get('student_id','')}"
                    f" &nbsp;|&nbsp; Taken: {data.get('date_taken','')}"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"<div class='card card-accent'>"
                            f"<p style='color:#8899aa; font-size:0.8rem'>RECOMMENDATION</p>"
                            f"<p>{data.get('description','')}</p></div>",
                            unsafe_allow_html=True)

                with st.expander("📋 View full answer breakdown"):
                    answers = data.get("answers", [])
                    for i, ans in enumerate(answers, start=1):
                        st.markdown(
                            f"**Q{i}. [{ans.get('domain','')}]** — {ans.get('question','')}\n\n"
                            f"→ *{ans.get('selected_option','')}*  (Score: **{ans.get('score','')}**)\n\n---"
                        )
            except Exception as exc:
                st.error(f"Could not parse JSON file: {exc}")

        else:                                                        # conditional else — txt / csv
            try:
                content: str = uploaded.read().decode("utf-8")
                st.code(content, language=None)
            except Exception as exc:
                st.error(f"Could not read file: {exc}")

    if st.button("← Back to Menu", use_container_width=False):
        go("menu")


# ================================================================
# SECTION 14 — PAGE: LOAD QUESTIONS FROM FILE
# ================================================================
def page_load_questions() -> None:
    st.markdown("<h1>📁 Load Questions from File</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8899aa'>Upload a <code>survey_questions.json</code> file "
                "to use its questions for a new questionnaire.</p>", unsafe_allow_html=True)
    st.markdown("---")

    uploaded = st.file_uploader("Upload questions JSON file", type=["json"],
                                 label_visibility="collapsed")

    if uploaded is not None:                                         # conditional if
        loaded: list = load_questions_from_uploaded(uploaded.read())
        if loaded is None:                                           # conditional if
            st.error("❌ Could not load questions. Please ensure the file is valid JSON.")
        else:                                                        # conditional else
            st.success(f"✅ Loaded {len(loaded)} question(s) from: **{uploaded.name}**")
            if st.button("Continue to Student Info →", type="primary"):
                go("info", questions=loaded)

    if st.button("← Back to Menu"):
        go("menu")


# ================================================================
# SECTION 15 — PAGE: EXPORT QUESTIONS
# ================================================================
def page_export_questions() -> None:
    st.markdown("<h1>💾 Export Questions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8899aa'>Download the embedded questions as a JSON file. "
                "You can edit this file and reload it from the main menu.</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    export_bytes: bytes = generate_questions_export_bytes()

    st.markdown(f"<div class='card'>"
                f"<p>The export contains <b>{len(QUESTIONS)} questions</b> across "
                f"4 domains and <b>{len(PSYCH_STATES)} psychological states</b>.</p>"
                f"</div>", unsafe_allow_html=True)

    st.download_button(
        label="⬇  Download survey_questions.json",
        data=export_bytes,
        file_name="survey_questions.json",
        mime="application/json",
        use_container_width=True,
        type="primary",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Menu"):
        go("menu")


# ================================================================
# SECTION 16 — ROUTER (entry point)
# ================================================================
def main() -> None:
    inject_css()
    init_state()

    # Route to the correct page based on session state
    page: str = st.session_state.page
    if page == "menu":                    page_menu()
    elif page == "info":                  page_info()
    elif page == "survey":                page_survey()
    elif page == "result":                page_result()
    elif page == "load":                  page_load()
    elif page == "load_questions":        page_load_questions()
    elif page == "export_questions":      page_export_questions()
    else:                                 page_menu()


if __name__ == "__main__":
    main()
