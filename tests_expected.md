# Test conversations: expected results

Written **before** the chatbot code was written and before any test was run.
The "Result" column is filled in afterwards, in the README.

| # | Test | What I type | What I expect |
|---|------|-------------|---------------|
| 1 | Greeting, a name, a goodbye | `muraho` / `my name is sam` / `bye` | A greeting that names the bot and lists its topics; "Nice to meet you, Sam."; "Thank you, Sam. Murakoze." |
| 2 | Two requests in one message | `where is uait and how much is the application fee` | One reply with the location (Kimihurura, Kigali) **and** the application fee. |
| 3 | Callback, confirmed | `can i get a callback` / `fees` / `morning` / `yes` | Asks the topic, asks the time of day, repeats "fees, morning" and asks yes or no, then says the request is noted. |
| 4 | Callback, refused at the end | `i want an appointment` / `programs` / `afternoon` / `no` | Same questions, then "Nothing has been sent." |
| 5 | A side question during the callback | `call me back` / `how much is the application fee` / `fees` / `afternoon` | The fee is answered, the topic question is asked again, and the topic is **not** set to the side question. Then `fees` is accepted as the topic and `afternoon` leads to the confirmation. |
| 6 | Cancelling halfway | `request a callback` / `admissions` / `cancel` | "Your callback request has been cancelled. Nothing was sent." |
| 7 | A follow-up | `what programs do you offer` / `and drone?` | The list of programs, then the description of Drone Technology only. |
| 8 | Unexpected input, then a person | (empty) / `asdfgh` / `qwerty` / `human` | A request to type a question; the fallback; the second fallback offering a person; the handover to staff. |
| 9 | Local phrasing | `amafaranga y'ishuri ni angahe` / `murakoze` | The fees reply, then the goodbye. |
| 10 | One I think will break | `i dont want a callback` | The bot should **not** start the callback questions. I expect it to start them anyway, because it only looks for the word "callback". |
