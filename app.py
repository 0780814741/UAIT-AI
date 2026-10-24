# UAIT AI: web version of the notebook chatbot (uait_ai.ipynb).
# ---- from notebook cell 2 ----
# AITCD001, Week 7: a rule-based chatbot for a domain of my own
import re
from datetime import datetime

print("ready")


# ---- from notebook cell 4 ----
# STEP 1. YOUR DOMAIN
BOT_NAME = "UAIT AI"
USERS = "future and current students of the United African Institute of Technology in Kigali"
TOPICS = "programs, applying, fees, where UAIT is, homework deadlines, exams and callbacks from admissions"

print(f"{BOT_NAME}: a chatbot for {USERS}.")
print(f"It can help with {TOPICS}.")


# ---- from notebook cell 6 ----
# STEP 2. YOUR DOMAIN: nine intents, in priority order.
# Step 6 adds "name" and "greeting".
RULES = [
    ("cancel",   r"\bcancel\w*\b|\bcancle\b|\bcall it off\b|\bnever ?mind\b"),
    ("callback", r"\bcall ?backs?\b|\bcall me\b|\bappointments?\b|\bcontact me\b"),
    ("fees",     r"\bfees?\b|\bcosts?\b|\bprices?\b|\bhow ?much\b|\bhw ?much\b|\bangahe\b"
                 r"|\bamafaranga\b|\bminerval\b|\btuition\b|\bpay\w*\b"),
    ("programs", r"\bprogra?m(me)?s?\b|\bprogs?\b|\bcourses?\b|\bamasomo\b|\bstudy\w*\b"
                 r"|\boffer\w*\b|\bteach\w*\b|\btell me about\b"),
    ("apply",    r"\bapply\w*\b|\bapplication\b|\badmissions?\b|\bjoin\w*\b|\benrol\w*\b"
                 r"|\bregist\w*\b|\bkwiyandikisha\b|\bgusaba\b"),
    ("location", r"\bwhere\b|\bwhr\b|\bwer\b|\blocat\w*\b|\baddress\b|\bdirections?\b"
                 r"|\bkimihurura\b|\bririhe\b|\briri he\b|\bcampus\b"),
    ("homework", r"\bhomework\b|\bassignments?\b|\bdeadlines?\b|\bdue\b|\bsubmit\w*\b|\bportfolio\b"),
    ("schedule", r"\bschedules?\b|\btimetable\b|\bclass(es)?\b|\blectures?\b|\bwhat ?time\b|\bwat ?tym\b"),
    ("exams",    r"\bexams?\b|\bresults?\b|\bmarks?\b|\bgrades?\b|\btests?\b"),
]

print(len(RULES), "intents in the rule table")


# ---- from notebook cell 8 ----
# STEP 3. PROVIDED: cleaning, matching, and several requests in one message (Weeks 3 to 5).
def normalise(text):
    """Remove punctuation (keeping the colon of 21:00), lowercase, trim."""
    return re.sub(r"[^\w\s:]", "", text).lower().strip()


def match(message):
    """The tag of the first rule that matches, or "fallback"."""
    text = normalise(message)
    for tag, pattern in RULES:
        if re.search(pattern, text):
            return tag
    return "fallback"


CONNECTORS = r"\band\b|\bbut\b|\balso\b|\bthen\b|[?]"


def split_requests(message):
    """Break one message into the separate requests it contains."""
    requests = []
    for part in re.split(CONNECTORS, message.lower()):
        part = normalise(part)
        if part != "":
            requests.append(part)
    return requests


def route(message):
    """One (intent, request) pair for each request understood."""
    found = []
    seen = []
    for request in split_requests(message):
        tag = match(request)
        if tag != "fallback" and tag not in seen:
            seen.append(tag)
            found.append((tag, request))
    return found


print(route("where is uait and how much is the application fee"))


# ---- from notebook cell 10 ----
# STEP 4. YOUR DOMAIN: the knowledge lives in dictionaries; one handler per intent.
# VERIFY these facts against UAIT's official sources before relying on them.
PROGRAMS = {
    "ai": "AI Technology: a certificate program.",
    "cyber": "Cyber Security: a certificate program.",
    "cybersecurity": "Cyber Security: a certificate program.",
    "drone": "Drone Technology: a certificate program.",
    "jewelry": "Jewelry Design: a certificate program.",
    "jewellery": "Jewelry Design: a certificate program.",
    "piano": "Piano Performance: a certificate program.",
}
PROGRAM_PATTERN = r"\b(" + "|".join(PROGRAMS) + r")\b"     # \b(ai|cyber|cybersecurity|drone|...)\b

FEES = {
    "application": "The application fee is listed as 50,000 RWF, and UAIT supports some applicants with an "
                   "exemption. Please confirm the current amount with admissions.",
    "tuition": "Tuition depends on the program. For the exact amount for your program, ask admissions: "
               "type 'callback' and I will pass on your request.",
}

FACTS = {
    "location": "UAIT is in Kimihurura, Gasabo District, Kigali.",
    "apply": "To apply, choose a program and contact UAIT admissions. There is an application fee (ask me about "
             "fees). I can request a callback from admissions: type 'callback'.",
    "homework": "For AITCD001 homework: it is released on a Thursday and due the following Thursday at 23:59. "
                "Handed in by the Sunday after the due date: full marks. By the next Thursday: minus 10 points "
                "out of 100. After that it is closed.",
    "schedule": "Class times depend on your program and are given by your instructors. Check your timetable or "
                "ask your instructor. I do not hold the timetable.",
    "exams": "Exam dates and results come from your instructors and UAIT administration. I do not hold them: "
             "type 'human' for a member of staff.",
}


def handle_programs(text):
    """Reads the message: the program named, if we offer it."""
    found = re.search(PROGRAM_PATTERN, text)
    if found:
        return PROGRAMS[found.group(1)]
    return ("UAIT programs include AI Technology, Cyber Security, Drone Technology, Jewelry Design and "
            "Piano Performance. Ask about one, for example 'cyber security'.")


def handle_fees(text):
    """Reads the message: the application fee, tuition, or both."""
    if re.search(r"\bapplication\b|\bapply\b", text):
        return FEES["application"]
    if re.search(r"\btuition\b|\bminerval\b|\bschool\b", text):
        return FEES["tuition"]
    return FEES["application"] + " " + FEES["tuition"]


def handle_apply(text):
    return FACTS["apply"]


def handle_location(text):
    return FACTS["location"]


def handle_homework(text):
    return FACTS["homework"]


def handle_schedule(text):
    return FACTS["schedule"]


def handle_exams(text):
    return FACTS["exams"]


def handle_callback(text):
    """Starts the callback conversation (Step 5)."""
    if flow["step"] is not None:
        return "Your callback request is already under way."
    return start_flow()


def handle_cancel(text):
    if flow["step"] is not None:
        reset_flow()
        return "Your callback request has been cancelled. Nothing was sent."
    return "There is no callback request in progress to cancel."


HANDLERS = {
    "cancel":   handle_cancel,
    "callback": handle_callback,
    "fees":     handle_fees,
    "programs": handle_programs,
    "apply":    handle_apply,
    "location": handle_location,
    "homework": handle_homework,
    "schedule": handle_schedule,
    "exams":    handle_exams,
}
ASKS = ["callback"]       # intents whose reply is a question: it goes last

for tag, pattern in RULES:
    if tag not in HANDLERS:
        print("No handler for:", tag)
print(len(HANDLERS), "intents routed")


# ---- from notebook cell 12 ----
# STEP 5a. YOUR DOMAIN: the questions of the callback conversation, in order.
FLOW_STEPS = [
    ("topic", "What is it about? Admissions, fees, programs or exams?",
     r"\b(admissions?|fees?|programs?|programmes?|exams?)\b"),
    ("time",  "Which part of the day suits you? Morning or afternoon?", r"\b(morning|afternoon)\b"),
]
DONE = "Callback request noted for admissions: "          # said after "yes"
NOT_DONE = "No problem. Nothing has been sent."           # said after "no"

print(len(FLOW_STEPS), "questions, then a confirmation")


# ---- from notebook cell 14 ----
# STEP 5b. PROVIDED: the flow (Weeks 4 and 5), driven by FLOW_STEPS, ending with a real confirmation.
flow = {"step": None, "collected": {}}
CALLBACKS = []                                   # requests confirmed with a yes
YES = r"\b(yes|yeah|yego|correct|ok|okay)\b"     # yego: yes
NO = r"\b(no|nope|oya|wrong)\b"                  # oya: no


def start_flow():
    flow["step"] = 0
    flow["collected"] = {}
    return FLOW_STEPS[0][1]


def reset_flow():
    flow["step"] = None
    flow["collected"] = {}


def summary():
    return ", ".join(flow["collected"].values())


def continue_flow(message):
    """One answer: store it, ask the next question, and at the end, confirm."""
    text = normalise(message)
    if flow["step"] == "confirm":
        if re.search(YES, text):
            noted = summary()
            CALLBACKS.append(dict(flow["collected"]))
            reset_flow()
            return DONE + noted + ". Thank you."
        if re.search(NO, text):
            reset_flow()
            return NOT_DONE
        return "Please answer yes or no."
    name, question, pattern = FLOW_STEPS[flow["step"]]
    found = re.search(pattern, text)
    if not found:
        return question                          # not a valid answer: ask again
    flow["collected"][name] = found.group()
    flow["step"] = flow["step"] + 1
    if flow["step"] < len(FLOW_STEPS):
        return FLOW_STEPS[flow["step"]][1]       # the next question
    flow["step"] = "confirm"
    return "So: " + summary() + ". Shall I send the request? Yes or no."


print("Bot:", start_flow())
for answer in ["fees please", "in the morning", "yes"]:
    print("You:", answer)
    print("Bot:", continue_flow(answer))
reset_flow()
CALLBACKS.clear()


# ---- from notebook cell 16 ----
# STEP 6. PROVIDED, except FOLLOW_UPS: memory, a name, a greeting, follow ups (Week 5).
# Run this cell ONCE: it adds the name and greeting rules to RULES.
context = {"name": None, "last_intent": None, "fallbacks": 0}


def reset_context():
    context["name"] = None
    context["last_intent"] = None
    context["fallbacks"] = 0


NAME = r"\bmy name is (\w+)"


def handle_name(text):
    found = re.search(NAME, text)
    if found:
        context["name"] = found.group(1).capitalize()
        return f"Nice to meet you, {context['name']}."
    return "Sorry, I did not catch your name."


def handle_greeting(text):
    if context["name"] is not None:
        return f"Muraho, {context['name']}! How can I help?"
    return (f"Muraho! I am {BOT_NAME}, a computer program. "
            f"I can help with {TOPICS}.")


RULES.insert(0, ("name", r"\bmy name is\b"))
RULES.append(("greeting", r"\bhello\b|\bhi\b|\bhey\b|\bmuraho\b|\bmwaramutse\b|\bmwiriwe\b"))
HANDLERS["name"] = handle_name
HANDLERS["greeting"] = handle_greeting

# YOUR DOMAIN: an intent, and the pattern that continues it ("and drone?" after the programs).
FOLLOW_UPS = {"programs": PROGRAM_PATTERN}


def follow_up(text):
    """A message with no intent of its own, read in the light of the last one."""
    last = context["last_intent"]
    if last in FOLLOW_UPS and re.search(FOLLOW_UPS[last], text):
        return [(last, text)]
    return []


print(len(RULES), "rules,", len(HANDLERS), "intents routed")


# ---- from notebook cell 18 ----
# STEP 7. PROVIDED: validation, errors, the fallback and a person (Week 6).
MAX_LENGTH = 300
ASK_AGAIN = f"Please type a question. I can help with {TOPICS}."
IN_WORDS = "Please type your question in words."
TOO_LONG = "That is a long message. Could you ask one thing at a time?"


def validate(message):
    """Return a reply if the message cannot be used; None if it can."""
    if message is None:
        return ASK_AGAIN
    text = message.strip()
    if text == "":
        return ASK_AGAIN
    if normalise(text) == "":
        return IN_WORDS
    if len(text) > MAX_LENGTH:
        return TOO_LONG
    return None


ERROR_LOG = []
SORRY = "Sorry, something went wrong on my side. Please try again, or type 'human'."


def log_error(message, error):
    ERROR_LOG.append({"time": datetime.now().strftime("%H:%M:%S"), "message": message,
                      "error": type(error).__name__ + ": " + str(error)})


def safe_handle(tag, request):
    """Run one handler. If it raises an error, log it and apologise instead of crashing."""
    try:
        return HANDLERS[tag](request)
    except Exception as error:
        log_error(request, error)
        return SORRY


def respond(found):
    """Answer every request found; a reply that asks a question goes last."""
    answers = []
    questions = []
    for tag, request in found:
        reply = safe_handle(tag, request)
        if tag in ASKS:
            questions.append(reply)
        else:
            answers.append(reply)
    return " ".join(answers + questions)


UNMATCHED = []
FALLBACK = f"Sorry, I did not understand. I can help with {TOPICS}."
STILL_LOST = f"Sorry, I still did not understand. Type 'human' for a member of staff, or ask about {TOPICS}."


def fallback(message):
    UNMATCHED.append(message)
    context["fallbacks"] = context["fallbacks"] + 1
    if context["fallbacks"] >= 2:
        return STILL_LOST
    return FALLBACK


EXIT_WORDS = ("bye", "goodbye", "exit", "quit", "thanks", "murakoze")
HUMAN_WORDS = ("human", "staff", "agent", "person")
HANDOVER = "Connecting you to a member of staff. They can see this conversation."

LLM_CLASSIFIER = None     # Step 12 can set this to an LLM helper; None means the rules only
LLM_RESCUED = []          # messages the rules missed and the LLM routed: (message, intent)


def llm_rescue(message):
    """Optional: ask the LLM to name an intent. Only an intent that has a handler is accepted."""
    tag = LLM_CLASSIFIER(message)
    if tag in HANDLERS:
        LLM_RESCUED.append((message, tag))
        return [(tag, normalise(message))]
    return []

print("validation, error handling and the fallback are ready")


# ---- from notebook cell 20 ----
# STEP 7, continued. PROVIDED: one complete turn, in the Week 6 order.
def reply_to(message):
    problem = validate(message)                  # 0. unusable input
    if problem is not None:
        return problem
    text = normalise(message)

    if text in EXIT_WORDS:                       # 1. the exit, at any point
        name = context["name"]
        reset_flow()
        reset_context()
        if name is not None:
            return f"Thank you, {name}. Murakoze."
        return "Thank you for contacting us. Murakoze."

    if text in HUMAN_WORDS:                      # 2. a person, at any point
        reset_flow()
        return HANDOVER

    if flow["step"] is not None:                 # 3. the flow sees it first
        step_before = flow["step"]
        flow_reply = continue_flow(message)
        if flow["step"] != step_before:
            return flow_reply
        found = route(message)
        if len(found) == 0:
            return flow_reply
        reply = respond(found)
        if flow["step"] is not None:
            reply = reply + " " + flow_reply
        return reply

    found = route(message)                       # 4. route
    if len(found) == 0:
        found = follow_up(text)                  # 5. a follow up
    if len(found) == 0 and LLM_CLASSIFIER is not None:
        found = llm_rescue(message)              # 5b. optional: an LLM names the intent
    if len(found) == 0:
        return fallback(message)                 # 6. the fallback, counted

    context["fallbacks"] = 0
    last_tag, last_request = found[-1]
    context["last_intent"] = last_tag
    return respond(found)


def run_conversation(turns):
    """Play a conversation from a clean start, printing both sides."""
    reset_flow()
    reset_context()
    for message in turns:
        print("You:", message)
        print("Bot:", reply_to(message))
    print()


# ---- from notebook cell 24 ----
# STEP 9. Refine: test 5 failed. "how much is the application fee" was stored as the topic ("fee"),
# because the flow searches the whole sentence for an answer, even when the sentence is a question.
# The change: a message that is a question is never taken as the answer to the callback questions.
# It goes to the router instead (the side question is answered), and the flow asks its question again.
QUESTION = r"^\s*(what|how|where|when|why|which|can|could|do|does|is|are)\b|\?"

if "_continue_flow_before_fix" not in globals():
    _continue_flow_before_fix = continue_flow        # kept so that the fix is visible


def continue_flow(message):
    """Refined after test 5: a question is not an answer."""
    if flow["step"] != "confirm" and re.search(QUESTION, message.lower()):
        return FLOW_STEPS[flow["step"]][1]           # not an answer: ask again
    return _continue_flow_before_fix(message)


# =====================================================================
# WEB VERSION (Gradio). The chatbot code above is the notebook's code, unchanged.
# Each visitor gets their own conversation state, so two people never mix.
# =====================================================================
import copy
import threading
import gradio as gr

_LOCK = threading.Lock()
GREETING = (f"{BOT_NAME}: an automated assistant, a computer program, not a member of staff. "
            f"It can help with {TOPICS}. Type 'human' for a person, or 'bye' to finish. "
            "Please do not type personal details such as names, phone numbers or ID numbers.")


def new_state():
    return {"context": {"name": None, "last_intent": None, "fallbacks": 0},
            "flow": {"step": None, "collected": {}}}


def answer(message, history, state):
    """One turn: load this visitor's state, run reply_to, save the state again."""
    if state is None:
        state = new_state()
    with _LOCK:
        saved_flow = copy.deepcopy(flow)
        saved_context = copy.deepcopy(context)
        flow.clear(); flow.update(copy.deepcopy(state["flow"]))
        context.clear(); context.update(copy.deepcopy(state["context"]))
        try:
            reply = reply_to(message)
        except Exception as error:                      # never show a crash to a visitor
            ERROR_LOG.append(repr(error))
            reply = "Sorry, something went wrong. Type 'human' for a member of staff."
        state = {"context": copy.deepcopy(context), "flow": copy.deepcopy(flow)}
        flow.clear(); flow.update(saved_flow)
        context.clear(); context.update(saved_context)
    history = (history or []) + [{"role": "user", "content": message},
                                 {"role": "assistant", "content": reply}]
    return "", history, state


LOGO = "data:image/png;base64,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"

# UAIT green, taken from the logo (about #449444)
UAIT_GREEN = gr.themes.Color(
    c50="#f0f8f0", c100="#dcefdc", c200="#bbdfbb", c300="#8fca8f", c400="#62ae62",
    c500="#449444", c600="#387a38", c700="#2e622e", c800="#274e27", c900="#213f21", c950="#122412")
THEME = gr.themes.Soft(primary_hue=UAIT_GREEN, secondary_hue=UAIT_GREEN, neutral_hue="slate")

CSS = """
.gradio-container {max-width: 820px !important; margin: auto;}
#header {display:flex; align-items:center; gap:16px; padding:14px 18px; background:#ffffff;
         border:1px solid #bbdfbb; border-bottom:4px solid #449444; border-radius:12px; margin-bottom:10px;}
#header img {height:46px; width:auto;}
#header .sub {color:#2e622e; font-size:0.95rem; line-height:1.3;}
#header .sub b {display:block; font-size:1.1rem; color:#213f21;}
#footer {color:#2e622e; font-size:0.85rem; text-align:center;}
#footer a {color:#387a38; font-weight:600;}
"""

HEADER = ('<div id="header"><img src="' + LOGO + '" alt="UAIT logo">'
          '<div class="sub"><b>UAIT AI</b>Rule-based assistant for the United African Institute of Technology, Kigali</div></div>')

with gr.Blocks(title="UAIT AI") as demo:
    gr.HTML(HEADER)
    chatbot = gr.Chatbot(value=[{"role": "assistant", "content": GREETING}], height=420)
    box = gr.Textbox(placeholder="Type your question and press Enter", show_label=False)
    session = gr.State(None)
    box.submit(answer, [box, chatbot, session], [box, chatbot, session])
    gr.HTML('<div id="footer">Facts must be confirmed with UAIT admissions. Portfolio Project 1, AITCD001 Chatbots Development. '
            'Source code: <a href="https://github.com/0780814741/UAIT-AI">github.com/0780814741/UAIT-AI</a></div>')

if __name__ == "__main__":
    demo.launch(theme=THEME, css=CSS)
