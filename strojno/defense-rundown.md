# Lab defense rundown: instructions

Use this when I give you this file plus a lab notebook (e.g. `@defense-rundown.md @2026/SU1-2026-LAB2.ipynb`).
Help me prepare to defend that lab. Do the first rundown, then answer my follow-up questions in the same style.

## Context
- Course: Strojno učenje 1 (SU1), FER. I'm repeating the class after failing it last year.
- I solved this lab, but I don't remember my solution.
- Lecture slides are in `predavanja/`. I know most of the theory, but not all.
- The defense is described as easy and lenient. I'll be asked:
  - **theory**, e.g. "what is a model?"
  - **lab-specific** questions, e.g. "show me a model", "what did you do in this task?"
  - **theory + lab** questions, e.g. "what happens when you change this number?"
  - **Python functions** we used, e.g. "what does `make_labels` / `StandardScaler` do?"

## Before writing
1. Dump every notebook cell **with its saved outputs**. The file is too big to read raw, so use a script, and print the full outputs because the numbers matter:
   ```
   python3 -c "import json; nb=json.load(open('<path>')); [print(f'=== [{i}] {c[\"cell_type\"]} ===\n'+''.join(c['source'])+''.join('\n--> OUT: '+''.join(o.get('text') or o.get('data',{}).get('text/plain','')) for o in c.get('outputs',[]))) for i,c in enumerate(nb['cells'])]"
   ```
2. Skim the matching lecture PDFs in `predavanja/` when you need to check a topic or a Croatian term.
3. Answer in chat, not in a doc or artifact.

## Language and style
- Simplified technical English: short sentences, no fluff.
- Use English terms. Add the Croatian term in brackets for anything less common that I might not recognize in English, e.g. basis functions (bazne funkcije), design matrix (matrica dizajna), overfitting (prenaučenost). Common terms like hypothesis or linear regression need no translation.
- Use **my actual numbers** from the saved outputs (weights, errors, std values). Don't use generic ones.
- Lead with the answer, then explain why.

## Structure of the first rundown

### Part 1: Theory
A compact rundown of the theory behind the lab, as bullet groups per topic:
- definitions
- key formulas, written inline (e.g. `w = (ΦᵀΦ + λI)⁻¹Φᵀy`)
- what each hyperparameter does when you increase or decrease it
- links to general concepts: overfitting/underfitting, bias–variance, model selection, etc.

### Part 2: The lab in general
- What the lab is about and the workflow that repeats across tasks (e.g. data → features → fit → predict → error → plot).
- The data used, and why.
- A **table of the notable Python functions**, both library ones and ones I wrote or were given: what each does and the important parameters. Include fit vs transform vs fit_transform where it applies.

### Part 3: Task by task
For each task and subtask:
- what we did, why, and the key result, with my numbers
- the answer to every **Q:** in the notebook (they're likely defense questions)
- "what happens if you change X" for the main numbers in that task

At the end of a task, add a short note on anything in **my code** that's wrong or deviates from the instructions and that an examiner could ask about: say what it is and how to fix it. Don't fix the notebook unless I ask.

## Follow-up questions
- Answer the question asked. Don't repeat the whole rundown.
- If my observation contradicts what you said (e.g. "but my plot shows X"), check it, ideally by running a quick simulation:
  - `/usr/local/bin/python3` has numpy but not sklearn, so reimplement with numpy (`np.linalg.lstsq`, `np.vander`, etc.).
  - Run several seeds to tell a real effect from chance.
- If something you said earlier turns out to be wrong or imprecise, correct it explicitly ("a correction to what I said earlier").
- Re-read the notebook outputs when relevant. I may have edited and re-run cells since the first dump.
- Show the math on my numbers when it explains something (e.g. verify a weight by hand).
- When it helps, end with a short **"For the defense"** answer: one or two sentences I could say out loud.
- Add an **"If they push"** note when there's a subtlety beyond the expected answer.
