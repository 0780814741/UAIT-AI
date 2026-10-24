# UAIT AI

A rule-based chatbot for people who ask about the **United African Institute of Technology (UAIT)** in Kigali:
future students (programs, applying, fees, location) and current students (homework deadlines, class times, exams).
The chatbot itself uses Python, `re` (regular expressions), dictionaries and functions only: there is no machine learning.

Built for **AITCD001 Chatbots Development**, Learning Outcome 2 (Portfolio Project).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/0780814741/UAIT-AI/blob/main/uait_ai.ipynb)

**Live demo (online now):** [https://uait-ai.onrender.com](https://uait-ai.onrender.com) (free hosting: the first load can take about a minute)

> The chatbot is an automated program, not a member of staff. It says so in its greeting, and "human" connects the user to a person at any point.
> Its facts live in the dictionaries `PROGRAMS`, `FEES` and `FACTS` in the notebook. They come from the course and from public listings and **must be checked against UAIT's official sources**.

## What it can do (9 intents, plus a name and a greeting)

| Intent | Example messages (including Kinyarwanda and SMS spelling) |
|---|---|
| `programs` | "what programs do you offer", "tell me about cyber security", "wat progs u hav", "amasomo" |
| `apply` | "how do i apply", "i want to join", "kwiyandikisha" |
| `fees` | "how much is the application fee", "what is the tuition", "minerval", "amafaranga ... angahe", "hw much 2 apply" |
| `location` | "where is uait", "wer is uait", "ishuri riri he" |
| `homework` | "when is the homework due", "assignment deadline" |
| `schedule` | "what time is class", "timetable" |
| `exams` | "when are the exams", "my results" |
| `callback` | "can i get a callback", "i want an appointment" (a short conversation with a confirmation, below) |
| `cancel` | "cancel", "never mind" |

**The callback conversation.** It asks the topic, then the part of the day, repeats both back and asks yes or no.
Only after a yes is the request saved. It never asks for a phone number, ID or surname.

**Closure.** "bye", "exit", "quit", "thanks" or "murakoze" ends the chat at any point, even in the middle of a callback request.

## How the code is organised

The notebook `uait_ai.ipynb` follows the course's steps:

- **Step 2: the rule table.** `RULES` is a list of `(intent, pattern)` pairs, tried in order. The first match wins.
- **Step 3: the router.** `normalise` removes punctuation and capitals, `split_requests` and `route` handle two requests in one message.
- **Step 4: handler functions.** One function per intent, collected in `HANDLERS`. `handle_programs` and `handle_fees` read the message and choose their answer from dictionaries.
- **Step 5: the callback flow.** `FLOW_STEPS` (the questions) and `continue_flow` (the machinery), with a confirmation.
- **Step 6: context.** A remembered name, the last intent, and follow-ups ("and drone?").
- **Step 7: the fallback.** It says what the chatbot can do, writes the message to `UNMATCHED`, and after two misses in a row offers a member of staff. Handler errors are caught and logged in `ERROR_LOG`.
- **Web version (bonus).** `app.py` and `requirements.txt` put the same chatbot online, live at [https://uait-ai.onrender.com](https://uait-ai.onrender.com) (see [Web version](#web-version-bonus)).

**Design.** My answers to *Designing Your Chatbot*, written before the code: [`designing_your_chatbot.md`](designing_your_chatbot.md).

## How to run it

1. Click the **Open in Colab** badge (or open `uait_ai.ipynb` in Jupyter).
2. Run all cells from the top (Runtime, then Restart and run all).
3. To talk to it, remove the `#` in front of `chat()` in the last cell and run that cell on its own.

A sample conversation (a scripted run of the notebook's `run_conversation`; you can also talk to it yourself with `chat()`):

```text
You: muraho
Bot: Muraho! I am UAIT AI, a computer program. I can help with programs, applying, fees, where UAIT is, homework deadlines, exams and callbacks from admissions.
You: what programs do you offer
Bot: UAIT programs include AI Technology, Cyber Security, Drone Technology, Jewelry Design and Piano Performance. Ask about one, for example 'cyber security'.
You: and drone?
Bot: Drone Technology: a certificate program.
You: how much is the application fee and where is uait
Bot: The application fee is listed as 50,000 RWF, and UAIT supports some applicants with an exemption. Please confirm the current amount with admissions. UAIT is in Kimihurura, Gasabo District, Kigali.
You: can i get a callback
Bot: What is it about? Admissions, fees, programs or exams?
You: fees
Bot: Which part of the day suits you? Morning or afternoon?
You: morning
Bot: So: fees, morning. Shall I send the request? Yes or no.
You: yes
Bot: Callback request noted for admissions: fees, morning. Thank you.
You: bye
Bot: Thank you for contacting us. Murakoze.
```

## Testing

The ten conversations and what I expected were written **before the code and before any test was run**: see [`tests_expected.md`](tests_expected.md).
Then I ran them (Step 8 of the notebook, outputs saved).

| # | Test | Result | Notes |
|---|------|--------|-------|
| 1 | Greeting, a name, a goodbye | Passed | Greeting, name and goodbye all as expected. |
| 2 | Two requests in one message | Passed | One reply answered both the location and the application fee. |
| 3 | Callback, confirmed | Passed | Confirmed with yes; the request was saved. |
| 4 | Callback, refused at the end | Passed | Refused with no; nothing was sent. |
| 5 | A side question during the callback | **Failed, then fixed** | The side question was stored as the topic (`fee`). See the bug log below. After the fix: passed. |
| 6 | Cancelling halfway | Passed | Cancelled halfway; nothing was sent. |
| 7 | A follow-up | Passed | "and drone?" was understood from the previous message. |
| 8 | Unexpected input, then a person | Passed | Empty input, fallback, second fallback, then staff. |
| 9 | Local phrasing | Passed | Kinyarwanda `amafaranga ... angahe` was understood. |
| 10 | One I think will break | **Failed, as predicted** | The bot started the callback questions for "i dont want a callback". Not fixed: listed under known limitations. |

### The ten test logs (as run, before the fix)

```text
Test 1: A greeting, a name, a goodbye
You: muraho
Bot: Muraho! I am UAIT AI, a computer program. I can help with programs, applying, fees, where UAIT is, homework deadlines, exams and callbacks from admissions.
You: my name is sam
Bot: Nice to meet you, Sam.
You: bye
Bot: Thank you, Sam. Murakoze.

Test 2: Two requests in one message
You: where is uait and how much is the application fee
Bot: UAIT is in Kimihurura, Gasabo District, Kigali. The application fee is listed as 50,000 RWF, and UAIT supports some applicants with an exemption. Please confirm the current amount with admissions.

Test 3: A callback, confirmed
You: can i get a callback
Bot: What is it about? Admissions, fees, programs or exams?
You: fees
Bot: Which part of the day suits you? Morning or afternoon?
You: morning
Bot: So: fees, morning. Shall I send the request? Yes or no.
You: yes
Bot: Callback request noted for admissions: fees, morning. Thank you.

Test 4: A callback, refused at the end
You: i want an appointment
Bot: What is it about? Admissions, fees, programs or exams?
You: programs
Bot: Which part of the day suits you? Morning or afternoon?
You: afternoon
Bot: So: programs, afternoon. Shall I send the request? Yes or no.
You: no
Bot: No problem. Nothing has been sent.

Test 5: A side question during the callback
You: call me back
Bot: What is it about? Admissions, fees, programs or exams?
You: how much is the application fee
Bot: Which part of the day suits you? Morning or afternoon?
You: fees
Bot: The application fee is listed as 50,000 RWF, and UAIT supports some applicants with an exemption. Please confirm the current amount with admissions. Tuition depends on the program. For the exact amount for your program, ask admissions: type 'callback' and I will pass on your request. Which part of the day suits you? Morning or afternoon?
You: afternoon
Bot: So: fee, afternoon. Shall I send the request? Yes or no.

Test 6: Cancelling halfway
You: request a callback
Bot: What is it about? Admissions, fees, programs or exams?
You: admissions
Bot: Which part of the day suits you? Morning or afternoon?
You: cancel
Bot: Your callback request has been cancelled. Nothing was sent.

Test 7: A follow up
You: what programs do you offer
Bot: UAIT programs include AI Technology, Cyber Security, Drone Technology, Jewelry Design and Piano Performance. Ask about one, for example 'cyber security'.
You: and drone?
Bot: Drone Technology: a certificate program.

Test 8: Unexpected input, then a person
You: 
Bot: Please type a question. I can help with programs, applying, fees, where UAIT is, homework deadlines, exams and callbacks from admissions.
You: asdfgh
Bot: Sorry, I did not understand. I can help with programs, applying, fees, where UAIT is, homework deadlines, exams and callbacks from admissions.
You: qwerty
Bot: Sorry, I still did not understand. Type 'human' for a member of staff, or ask about programs, applying, fees, where UAIT is, homework deadlines, exams and callbacks from admissions.
You: human
Bot: Connecting you to a member of staff. They can see this conversation.

Test 9: Local phrasing
You: amafaranga y'ishuri ni angahe
Bot: The application fee is listed as 50,000 RWF, and UAIT supports some applicants with an exemption. Please confirm the current amount with admissions. Tuition depends on the program. For the exact amount for your program, ask admissions: type 'callback' and I will pass on your request.
You: murakoze
Bot: Thank you for contacting us. Murakoze.

Test 10: One I think will break
You: i dont want a callback
Bot: What is it about? Admissions, fees, programs or exams?
```

## A bug found and fixed

**What happened.** In test 5, while the bot was asking *"What is it about?"*, I asked a side question: *"how much is the application fee"*.
The bot did not answer it. It took the question as the **answer** to its own question and stored the topic as `fee`.
Later, the confirmation read *"So: fee, afternoon"*, and my real answer `fees` was treated as a side question and answered with the fee text.

```text
Test 5: A side question during the callback
You: call me back
Bot: What is it about? Admissions, fees, programs or exams?
You: how much is the application fee
Bot: Which part of the day suits you? Morning or afternoon?
You: fees
Bot: The application fee is listed as 50,000 RWF, and UAIT supports some applicants with an exemption. Please confirm the current amount with admissions. Tuition depends on the program. For the exact amount for your program, ask admissions: type 'callback' and I will pass on your request. Which part of the day suits you? Morning or afternoon?
You: afternoon
Bot: So: fee, afternoon. Shall I send the request? Yes or no.
```

**Cause.** `continue_flow` uses `re.search` to look for a valid answer anywhere in the message. The topic pattern contains `fees?`,
so the word *fee* inside a question counted as an answer.

**The fix (Step 9).** A message that is a question (it starts with what, how, where, when, why, which, can, could, do, does, is or are, or contains a `?`)
is never taken as an answer to the callback questions. It goes to the router, the side question is answered, and the flow asks its question again.
The old function is kept as `_continue_flow_before_fix` so the change is visible.

**Test run again after the fix:**

```text
Test 5 again: A side question during the callback
You: call me back
Bot: What is it about? Admissions, fees, programs or exams?
You: how much is the application fee
Bot: The application fee is listed as 50,000 RWF, and UAIT supports some applicants with an exemption. Please confirm the current amount with admissions. What is it about? Admissions, fees, programs or exams?
You: fees
Bot: Which part of the day suits you? Morning or afternoon?
You: afternoon
Bot: So: fees, afternoon. Shall I send the request? Yes or no.
```

I then ran all ten tests again. Tests 1 to 9 passed, test 10 failed in the same way as before.

## Web version (bonus)

The chatbot is **uploaded and live online**: [https://uait-ai.onrender.com](https://uait-ai.onrender.com)

`app.py` runs the same chatbot as a web page, using Gradio. The chatbot code is copied unchanged from the notebook (including the fix from test 5), and each visitor gets their own conversation, so two people never mix. It is hosted on Render's free plan and deployed from this repository (`app.py` and `requirements.txt`). Because the plan is free, the service sleeps after about 15 minutes without visitors, so **the first load can take about a minute**.

To run it on your own computer: `pip install -r requirements.txt`, then `python app.py`.

The web version needs no key and no extra service. Please do not type personal details in the live chatbot.

## Known limitations

- **Negation (test 10).** "i dont want a callback" still starts the callback questions, because the rule only looks for the word *callback*. Fixing it would need a rule that checks for words such as *dont*, *not* and *no* in front of an intent.
- **Phrasings not understood.** In Step 10, 2 of 9 local-phrasing messages ended in `UNMATCHED`: "when is the next intake" (there is no intake intent yet) and "how do i get to uait" (the location rule only knows *where*, *address*, *directions* and similar words).
- **A reply phrased as a question is not an answer.** After the fix, someone who answers "what about fees?" is asked the question again.
- **Facts.** The bot does not hold tuition amounts, the timetable or exam dates. It says so and offers a callback or a person. The facts it does give must be verified before real use.
- **Logs are kept in memory only.** `UNMATCHED` and `CALLBACKS` disappear when the notebook is closed or the web service restarts.

## Privacy and ethics

- No real names, phone numbers, ID numbers or keys are in this repository. The name "Sam" in the tests is invented.
- The chatbot never asks for personal details, and its greeting says it is a computer program.
- It does not pretend to know what it does not know: unknown facts lead to admissions or a person.

## Rubric map (Learning Outcome 2)

| Indicator | Where to see it |
|---|---|
| Structured if-else response logic | Steps 2 to 4 of the notebook: `RULES`, `route`, `HANDLERS` |
| Fallback or default responses | Step 7: `fallback`, `UNMATCHED`, `STILL_LOST` (offers staff after two misses) |
| Basic input variations | `normalise`, regular expressions in `RULES`, Step 10 (`PHRASING`) |
| 5+ valid user intents | The table above: nine intents with handlers |
| Modular or organised code | One function per intent, dictionaries `PROGRAMS`, `FEES`, `FACTS`, `HANDLERS`, `FLOW_STEPS` |
| Conversation closure logic | `EXIT_WORDS`, "human", `cancel`, and the yes/no confirmation in `continue_flow` |
| Identifies and fixes bugs | "A bug found and fixed" above, and Step 9 |
| Tests with varied inputs | `tests_expected.md` and the ten test logs above |
| Refines code based on test results | Step 9: the change made because test 5 failed, and test 5 run again |
