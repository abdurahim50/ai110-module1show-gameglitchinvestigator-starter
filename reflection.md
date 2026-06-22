# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  When I first ran the game, it actually looked pretty good. The Streamlit interface was clean with a sidebar for difficulty settings, a score display, and a text box for entering guesses. There was even a debug panel that showed the secret number and game state. At first glance, it seemed like a working game.

  But as soon as I started playing, I noticed things were off. On Normal I guessed 50 and it said "Go LOWER!", then I guessed 80 and it said "Go HIGHER!" — those two hints contradict each other, so the answer would have to be below 50 and above 80 at the same time. That's impossible, which is how I realized the hints were backwards. On Hard the problems piled up: the sidebar said the range was 1 to 50, but the info box still told me to guess "between 1 and 100," and when I ran out of attempts it revealed the secret was 74 — a number that shouldn't even exist in a 1-to-50 game. Then I switched to Easy and the game said "Game over" before I had made a single guess on that difficulty, because the lost status from my Hard game carried over. I also noticed the "Attempts left" counter started at 7 instead of 8 and didn't go down after my first guess.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
- The hints were backwards. On Normal, guessing 50 said "Go LOWER!" and guessing 80 said "Go HIGHER!", which can't both be true.
- The difficulty range was inconsistent. Hard showed "Range: 1 to 50" in the sidebar but "between 1 and 100" in the info box, and the secret turned out to be 74.
- Changing the difficulty didn't reset the game — switching to Easy showed "Game over" before I had guessed at all.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| On Normal, I guessed 50 and then 80 | The hints should point me toward the answer and agree with each other | 50 told me "Go LOWER!" and 80 told me "Go HIGHER!" — that can't both be true, so the hints were clearly backwards | No crash. Code-level cause: in `check_guess`, the "Too High" outcome was paired with the message "📈 Go HIGHER!" and "Too Low" with "📉 Go LOWER!" — the hint text was swapped |
| Picked Hard and played a round | A Hard game should stay inside the 1 to 50 range it advertises | The sidebar said "Range: 1 to 50" but the info box said "between 1 and 100," and the secret turned out to be 74 — way outside Hard's range | No crash. Code-level cause: the info box string was hardcoded to "between 1 and 100", and "New Game" set the secret with `random.randint(1, 100)` instead of using the difficulty's range |
| Switched the difficulty from Hard to Easy | Changing difficulty should start me a fresh game I can actually play | It said "Game over. Start a new game to try again." before I had made a single guess on Easy | No crash. Code-level cause: `st.session_state.status` stayed "lost" across difficulty changes because nothing reset the game state when the difficulty selectbox changed |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I mostly worked with Claude as a coding teammate. I'd play the game, take screenshots of the weird behavior, and then talk through what I was seeing to figure out which part of the code was responsible.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  The AI pointed out that the backwards hints came from the "Too High" outcome being paired with a "Go HIGHER!" message, and that the secret was being turned into a string on even turns. I verified the fix by running pytest (all 3 tests passed) and by replaying the game — guessing too high now correctly tells me to go lower, and I was actually able to win.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  The first command the AI gave me to run the tests was `.venv/bin/pytest tests/`, which failed with `ModuleNotFoundError: No module named 'logic_utils'`. I caught it because the error was right there in the output, and we fixed it by running `python -m pytest tests/` instead so the project folder was on the path. It was a good reminder that AI suggestions don't always work the first time and I have to actually read the output.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I used two checks for every fix. First, I replayed the exact situation that showed the bug — for example, I guessed too high again to make sure it finally told me to go lower instead of higher. Second, I ran pytest to confirm the logic functions returned the right outcomes. A bug only counted as "fixed" once both the game and the tests agreed.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I ran `python -m pytest tests/ -v` and watched `test_guess_too_high`, `test_guess_too_low`, and `test_winning_guess` all pass. That told me my `check_guess` function was returning the correct outcome for each case, which was exactly the function the backwards-hint bug lived in.

- Did AI help you design or understand any tests? How?
  Yes. The AI explained that the tests expected `check_guess` to return a single label like "Too High" rather than a tuple, which is why I kept the outcome and the hint message separate (the message mapping lives in app.py now). That kept the tests passing while the game still showed friendly hints.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  I'd say Streamlit re-runs your whole script from top to bottom every single time you click a button or change anything. So any normal variable gets created fresh each run, which is why the secret number kept "resetting" — it was being randomly picked again on every click. Session state is like a little backpack that survives those reruns: if you put the secret number in `st.session_state`, it stays the same until you decide to change it. Once I moved the secret and the score and the attempts into session state and only reset them on purpose, the game stopped glitching.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Reproducing a bug before trying to fix it. Playing the game and screenshotting the exact wrong behavior made it way easier to know what "fixed" looked like, and running pytest after each change kept me honest. I want to keep that "reproduce, fix, re-test" loop going.

- What is one thing you would do differently next time you work with AI on a coding task?
  I'd read the AI's suggestions more critically before running them, like I did when the first pytest command failed. Next time I want to skim the code it gives me and predict what it should do, instead of just running it and hoping.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  It made me realize AI-generated code can look clean and professional and still be full of subtle bugs. I trust the output a lot less now and treat "it runs" as the start of testing, not the finish line.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
