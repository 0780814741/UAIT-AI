# Designing Your Chatbot: UAIT AI

*Written before the code. Answers are for AITCD001, Portfolio Project 1.*

## 1. Who will use it?

Two groups of people who ask about the United African Institute of Technology (UAIT) in Kigali:

- **Future students and their families:** someone finishing secondary school, or a parent, who wants to know what UAIT teaches, how to apply and what it costs.
- **Current students:** someone who wants to check a homework deadline, class times or exam information.

They write on a phone, in English, in Kinyarwanda, or mixed, and often in short SMS spelling ("hw much 2 apply", "wer is uait").

## 2. What problem does it solve?

The same few questions are asked again and again, and the people who can answer them (admissions staff, instructors) are not always available. The chatbot answers the common questions at any hour, and passes everything else to a person.

## 3. What can it do, and what can it not do?

| It can | It cannot |
|---|---|
| Name UAIT's programs and describe each in one line | Give exact tuition amounts, the timetable or exam dates (it says so and offers a person) |
| Say where UAIT is | Process an application or a payment |
| Explain the homework deadline rule for AITCD001 | Reply to questions outside UAIT |
| Request a callback from admissions, after a confirmation | Remember anything after the chat is closed |

## 4. The intents

Nine intents plus a name and a greeting, in priority order (the first rule that matches wins):

| Intent | Example messages |
|---|---|
| cancel | "cancel", "never mind" |
| callback | "can i get a callback", "i want an appointment" |
| fees | "how much is the application fee", "minerval", "amafaranga ... angahe" |
| programs | "what programs do you offer", "tell me about cyber security", "wat progs u hav" |
| apply | "how do i apply", "i want to join", "kwiyandikisha" |
| location | "where is uait", "wer is uait", "ishuri riri he" |
| homework | "when is the homework due", "assignment deadline" |
| schedule | "what time is class", "timetable" |
| exams | "when are the exams", "my results" |

## 5. The conversation flow

1. The bot greets the user, says it is a computer program, and lists what it can help with.
2. The user asks a question. The bot normalises the text (lowercase, no punctuation), finds the first rule that matches and answers from its dictionaries. Two requests in one message get two answers.
3. **The callback conversation:** it asks the topic (admissions, fees, programs or exams), then the part of the day (morning or afternoon), repeats both back, and asks yes or no. Only after **yes** is the request saved. It never asks for a phone number, ID or surname.
4. **A side question** during the callback is answered, and then the bot asks its question again.
5. **Closure:** "bye", "exit", "quit", "thanks" or "murakoze" ends the chat at any point, even in the middle of the callback. "human" connects to a person at any point. "cancel" stops the callback with nothing sent.

## 6. What happens when it does not understand?

The fallback says what the chatbot can help with, and writes the message to a log (`UNMATCHED`) so I can later add a rule for it. After **two misses in a row** it offers to connect the user to a member of staff.

## 7. How will it handle different ways of writing?

- Capitals and punctuation are removed before matching.
- Patterns catch word endings (`fees?`, `apply\w*`) and several phrasings for each intent.
- Local words are included: `angahe`, `amafaranga`, `minerval`, `amasomo`, `ririhe`, `muraho`, `murakoze`, `yego`, `oya`.
- SMS spelling is included: `hw much`, `wer`, `wat tym`, `progs`, `cancle`.

## 8. What could go wrong, and what is the plan?

| Risk | Plan |
|---|---|
| Wrong information about UAIT | Facts live in dictionaries, are checked against UAIT's official sources, and the bot sends the user to admissions when it does not know. |
| The user types personal details | The bot never asks for them, and the README tells users not to type them. |
| The user thinks they are talking to a person | The greeting says it is a computer program. |
| A rule matches the wrong intent | The order of the rules is planned, and I test with ten conversations, including one I expect to break. |
| An optional LLM layer invents facts | It can only choose an existing read-only intent; the reply always comes from the rules' dictionaries. It is off by default. |

## 9. How will I know it works?

I write **ten test conversations and what I expect before the code** (see `tests_expected.md`), run them, and record what failed. Each failure goes into the README with its cause and fix. I change the code for at least one failing test, then run that test again.
