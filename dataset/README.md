# UAIT AI — Intent Dataset

## Intent dataset

**Chatbot name:** UAIT AI  
**Purpose:** A rule-based information assistant for United African Institute of Technology (UAIT), helping users ask about programs, applications, fees, campus location, academic work, schedules, exams and callback requests.

## Labels

| Label | Meaning | Messages |
|---|---|---:|
| `cancel` | Cancel or withdraw a callback/appointment request | 30 |
| `callback` | Request a call or appointment with UAIT staff | 30 |
| `fees` | Ask about tuition, application fees, costs or payment | 30 |
| `programs` | Ask about courses or what a program covers | 30 |
| `apply` | Ask how to apply, register or enroll | 30 |
| `location` | Ask for the campus address or directions | 30 |
| `homework` | Ask about homework, assignments, portfolios or deadlines | 30 |
| `schedule` | Ask about class times, lectures or timetables | 30 |
| `exams` | Ask about tests, examination dates, marks or results | 30 |
| `name` | Introduce the user's own name | 30 |
| `greeting` | Greet the chatbot | 30 |
| `out_of_scope` | Ask for something outside the UAIT information assistant's scope | 30 |

## Labelling guideline

1. One message, one label; split a message if it contains two separate requests.
2. Label the user's main goal, not just a keyword. Questions about tuition, prices or payment amounts are fees.
3. Questions about available courses or what a course teaches are programs; asking to enroll or register is apply.
4. Requests for a phone call or appointment with staff are callback; withdrawing that request is cancel.
5. Questions about campus address or directions are location.
6. Homework, assignment, portfolio and submission deadlines are homework; class times and timetables are schedule; tests, grades and exam results are exams.
7. Use name only when the user introduces their own name; use greeting for a greeting without a more specific request.
8. Use out_of_scope when the request is unrelated to UAIT admissions, programs, fees, campus, academic work or contacting the institute.
9. Preserve the message as written, including spelling, SMS forms and Kinyarwanda/mixed-language phrasing.
10. All examples in this version are constructed practice examples, not verified messages collected from real people.

## Dataset source counts

| Source | Count |
|---|---:|
| `rules` | 36 |
| `unmatched` | 0 |
| `local` | 77 |
| `people` | 0 |
| `written` | 247 |
| **Total** | **360** |

**Provenance:** All 360 rows in this version are constructed practice examples. `rules` means examples based on existing chatbot rule patterns; `local` means constructed Kinyarwanda, mixed-language or SMS-style examples; `written` means other constructed examples. No invented row is labelled `people` or `unmatched`. The assignment's requirement to collect at least 20 messages from real people is not met by this version.

## Quality check

- Total rows: **360**
- Labels: **12**
- Messages per label: **30 each**
- Unknown labels: **0**
- Duplicate messages after normalization: **0**
- Conflicting labels: **0**
- Balance (largest / smallest): **1.00**
- Real-person messages (`people`): **0 of at least 20**

The per-label count, duplicate and balance checks pass. The real-person collection requirement remains incomplete.

## Split and baseline

The notebook uses a fixed-seed, stratified 80/20 split: **288 training rows** and **72 test rows** (24 train and 6 test per label).

**Rule baseline:** 46 of 72 test messages correct (**63.9%**).

### Example baseline errors
- `when is the next intake` — labelled **apply**, but the simple rules predict **out_of_scope**.
- `ni ryari kwakira abanyeshuri bitangira` — labelled **apply**, but the simple rules predict **out_of_scope**.
- `mwambwira igihe mwampamagarira?` — labelled **callback**, but the simple rules predict **out_of_scope**.

The baseline is a simple first-match regular-expression system. It can miss paraphrases, spelling variations and messages expressed in Kinyarwanda or mixed language. A classifier trained on a larger, genuinely collected dataset may generalize better.

## Entities

| Entity label | Closed list | Count of matching messages |
|---|---|---:|
| `PROGRAM` | AI Technology; Cyber Security; Drone Technology; Jewelry Design; Piano Performance | 15 |
| `PLACE` | Kimihurura; Kigali; Gasabo | 9 |
| `COURSE` | AITCD001 | 3 |

## What is still weak

- The examples are constructed, not collected from actual UAIT users.
- There are no real unmatched-log examples in this dataset.
- Some local-language phrases should be checked by fluent Kinyarwanda speakers.
- The baseline is a simple rule system and may not understand context or follow-up messages.
- Fees, admissions requirements, schedules and exam information should be confirmed with UAIT before the chatbot gives official answers.

