# The Unofficial Guide
<!-- NAME: Angelica Magnussen,  CORPUS: campus_life -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does
<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->
This repository contains an AI-powered Retrieval-Augmented Generation (RAG) application built around a custom campus_life corpus designed to help students navigate university policies, services, and daily logistics. The system accurately answers practical student questions—such as graduation requirements, health center walk-in hours, on-campus job limits, course expectations, and dining hall costs—by combining purpose-driven document chunking, vector search, and strict source grounding. Complete with an intelligent relevance gate to filter out-of-corpus queries, it ensures that every response is derived directly from the underlying documents and explicitly cites its source file.

## Chunking Strategy
**Chunk size:** Variable (split by natural sentence, paragraph, and reply boundaries)
**Overlap:** 0 (eliminated as specific punctuation and structural delimiters were used)
<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->
The corpus relies heavily on discrete student discussion threads and precise contextual rules. Instead of using an arbitrary fixed-character window, I implemented a boundary-aware chunking strategy that splits text along sentence, paragraph, and reply markers. This ensures chunks rarely cut off mid-sentence, providing standalone, grammatically complete units of information that preserve the true logical context without requiring overlapping windows.

## Sample Chunks
<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`
```
THREAD: Is a bike worth it for a 20 minute walk commute?
```

**Chunk 2** — source: `thread_first_gen.txt#1` — produced by: `chunker.py::split_documents`
```
--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.
```

**Chunk 3** — source: `thread_laptop_specs.txt#1` — produced by: `chunker.py::split_documents`
```
--- reply 1 (31 votes) ---
Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.
```

**Chunk 4** — source: `thread_office_hours_etiquette.txt#3` — produced by: `chunker.py::split_documents`
```
--- reply 3 (18 votes) ---
If it helps, treat it as a standing appointment. Go every week for a month and it stops feeling like a thing.
```

**Chunk 5** — source: `thread_roommate_conflict.txt#3` — produced by: `chunker.py::split_documents`
```
--- reply 3 (33 votes) ---
Write down specifics before the meeting. 'It's not working' is hard to act on; 'guests four nights a week past 2am' is not.
```

## Sample Answer
<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->
For assessing the GROUNDING_INSTRUCTIONS in generate.py, we can see in the below experiment 
that the current rules outline are sufficient (at least for the question chosen). 
**Question:**
     QUESTION CHOSEN & CORRECT EXPECTED ANSWER:
          What are the walk-in hours at the health center?
          In health_center.txt, walk-in hours are from 8am to 11am.
**Answer:**
python app.py ask "What are the walk-in hours at the health center?" --show-prompt 
OUTPUT: 
```
     (best distance 0.327, cutoff 0.6)

     ======================================================================
     System instruction sent with the prompt
     ======================================================================
     You answer questions using only the documents provided to you.

     Rules:
     - Use only the information in the documents below. Do not use anything you know from elsewhere.
     - If the documents don't cover the question, say you don't have enough information. Do not guess.
     - Name the document your answer came from, using the filename given in each excerpt.
     - Be brief. Two or three sentences is usually enough.

     ======================================================================
     The assembled prompt, exactly as sent
     ======================================================================
     Documents:

     [from health_center.txt]
     Walk-in hours are 8am to 11am; everything after that is by appointment and appointments run about a week out. If something is urgent, go at 8am and wait rather than booking.

     [from dining_kestrel_commons.txt]
     Hours are 7:00am to 9:00pm weekdays, 9:00am to 8:00pm weekends. Costs one meal swipe, or $12.50 cash.

     [from dining_pellew_dining_hall.txt]
     Hours are 7:00am to 8:00pm daily. Costs one meal swipe, or $11.75 cash.

     [from dining_north_kitchen.txt]
     Hours are 11:00am to 7:00pm weekdays. Costs one meal swipe, or $13.00 cash.

     [from course_phys_130.txt]
     Expect 7 hours a week, plus 3 on lab weeks.

     ---

     Question: What are the walk-in hours at the health centre?

     Answer using only the documents above, and name the file you used.
     ======================================================================

     The walk-in hours at the health center are 8:00 am to 11:00 am (health_center.txt).

     Sources retrieved: course_phys_130.txt, dining_kestrel_commons.txt, dining_north_kitchen.txt, dining_pellew_dining_hall.txt, health_center.txt

     1 model calls this session, 389 tokens (358 in, 31 out)
```

**My relevance cutoff:**
<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->
Here is the data from your terminal output organized into the requested table format.

| Question | In corpus? | Best distance | Cuttoff |
|---|---|---|---|
| What is the capital of Mongolia? | no | 0.821 | 0.6 |
| How do I change the oil in a diesel engine? | no | 0.885 | 0.6 |
| Who won the 1994 World Cup? | no | 0.874 | 0.6 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.824 | 0.6 |
| How do I write a for loop in Rust? | no | 0.831 | 0.6 |

OBSERVATIONS: 
The gap ("inbetween value") between the average 0.847 and the cutoff 0.6 is 0.247.
In vector search, Distance means how far apart two pieces of data are.
• Small Distance (0.0 to 0.2) = Very close together / high semantic match.
• Large Distance (0.8 to 1.0) = Very far apart / completely unrelated.
The cutoff is set to 0.6 (RAG system will only accept chunks that have a distance of 0.6 or lower (closer)).
Because our best queries are at 0.821 to 0.885, they are too far away. The cutoff is not "too strict"—it is actually quite loose, but the queries are completely missing from the database (which makes sense, as "In corpus?" is marked as no).

CONCLUSION: 
To summarize, the RAG app is correctly returning a fallback message for these queries. Because the questions are not in the corpus, the closest chunks the database can find are mathematically far away (averaging a high distance of 0.847). Since our strict maximum allowable distance cutoff is 0.6, these irrelevant chunks are successfully blocked. The system is performing exactly as it should by refusing to serve unrelated data to out-of-bounds questions.


## How I Used AI
<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->
**1.**
     For How I Used AI, I asked an LLM to find the average of the 5 "best distance" values and calculate the midpoint between that average and our 0.6 cutoff. The AI correctly calculated this value as 0.7235. However, my initial framing mistakenly labeled this midpoint as a "gap" and concluded that our threshold was "too strict." After realizing that a distance of 0.847 indicates completely unrelated data (since the queries were not in our corpus), I corrected the write-up. The final version accurately explains that a 0.6 distance cutoff is actually performing correctly by blocking these out-of-bounds queries from triggering a hallucinated response.
**2.**
     In the 2nd instance, I provided the AI with my project requirements and the code for chunker.py, asking it to show me exactly where and how to replace the starter's chunking function with two methods: the 	AI-Produced RecursiveCharacterTextSplitter Pipeline approach and the Hand-Rolled Splitter approach. For both methods, the AI returned the required Python code snippet along with notes explaining its logic. For the AI-Produced Pipeline method, notes explain it prevents random middle cuts using a hierarchical fallback strategy and allows filtering out trailing noise by cleaning the final pipeline output. For the Hand-Rolled Splitter method, notes explain how it prevents random middle cuts and eliminates a trailing 2-character chunk bug using a minimum size filter. However, since the AI-output notes didn't perfectly match my project's context, I edited the AI's notes (code comments) myself to align them with my own observations before putting them in my documentation.


<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1. Retrieved chunk contains the answer | 4 of 5 | 0/5 | 0/5 | 0/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->
Real system output for Criterion 1 (Retrieved chunk contains the answer): 
     What are the writing-intensive course requirements for graduation and when should they be checked?
          run 1: fail  (best distance 0.315)
          run 2: fail  (best distance 0.315)
          run 3: fail  (best distance 0.315)
     What are the walk-in hours at the health centre?
          run 1: fail  (best distance 0.327)
          run 2: fail  (best distance 0.327)
          run 3: fail  (best distance 0.327)
     What is the maximum number of hours you can work on campus per week?
          run 1: fail  (best distance 0.271)
          run 2: fail  (best distance 0.271)
          run 3: fail  (best distance 0.271)
     How many weekly hours outside of class should you expect for CS 210?
          run 1: fail  (best distance 0.243)
          run 2: fail  (best distance 0.243)
          run 3: fail  (best distance 0.243)
     How much does a meal cost at North Kitchen?
          run 1: fail  (best distance 0.434)
          run 2: fail  (best distance 0.434)
          run 3: fail  (best distance 0.434)

Real system output for Criterion 2 (Every answer names a source): 
     ### What are the writing-intensive course requirements for graduation and when should they be checked? — run 1

     - Best distance: 0.3152 (passed the gate)
     - Sources retrieved: admin_graduation_requirements.txt, admin_pass_fail_option.txt, course_engl_205_exams.txt, course_engl_205_workload.txt, money_textbooks.txt

     ```
     The writing-intensive requirement consists of two courses, which must be taken in different departments. You should check this requirement in your third year rather than your fourth. 

     Source: admin_graduation_requirements.txt
     ```

     ### What are the writing-intensive course requirements for graduation and when should they be checked? — run 2

     - Best distance: 0.3152 (passed the gate)
     - Sources retrieved: admin_graduation_requirements.txt, admin_pass_fail_option.txt, course_engl_205_exams.txt, course_engl_205_workload.txt, money_textbooks.txt

     ```
     The writing-intensive requirement consists of two courses, and they must be taken in different departments. This should be checked in your third year rather than your fourth. 

     Source: `admin_graduation_requirements.txt`
     ```

     ### What are the writing-intensive course requirements for graduation and when should they be checked? — run 3

     - Best distance: 0.3152 (passed the gate)
     - Sources retrieved: admin_graduation_requirements.txt, admin_pass_fail_option.txt, course_engl_205_exams.txt, course_engl_205_workload.txt, money_textbooks.txt

     ```
     The writing-intensive requirement consists of two courses, and they must be taken in different departments. You should check this requirement in your third year rather than your fourth. 

     Source: admin_graduation_requirements.txt
     ```

     ### What are the walk-in hours at the health centre? — run 1

     - Best distance: 0.3272 (passed the gate)
     - Sources retrieved: course_phys_130.txt, dining_kestrel_commons.txt, dining_north_kitchen.txt, dining_pellew_dining_hall.txt, health_center.txt

     ```
     The walk-in hours at the health center are 8am to 11am (from health_center.txt).
     ```

     ### What are the walk-in hours at the health centre? — run 2

     - Best distance: 0.3272 (passed the gate)
     - Sources retrieved: course_phys_130.txt, dining_kestrel_commons.txt, dining_north_kitchen.txt, dining_pellew_dining_hall.txt, health_center.txt

     ```
     Walk-in hours at the health center are from 8am to 11am (health_center.txt).
     ```

     ### What are the walk-in hours at the health centre? — run 3

     - Best distance: 0.3272 (passed the gate)
     - Sources retrieved: course_phys_130.txt, dining_kestrel_commons.txt, dining_north_kitchen.txt, dining_pellew_dining_hall.txt, health_center.txt

     ```
     Walk-in hours at the health center are from 8:00 am to 11:00 am (health_center.txt).
     ```

     ### What is the maximum number of hours you can work on campus per week? — run 1

     - Best distance: 0.2715 (passed the gate)
     - Sources retrieved: course_cs_210.txt, course_cs_210_workload.txt, course_phys_130.txt, course_stat_150.txt, money_jobs.txt

     ```
     The maximum number of hours you can work is 20 hours a week during term (money_jobs.txt).
     ```

     ### What is the maximum number of hours you can work on campus per week? — run 2

     - Best distance: 0.2715 (passed the gate)
     - Sources retrieved: course_cs_210.txt, course_cs_210_workload.txt, course_phys_130.txt, course_stat_150.txt, money_jobs.txt

     ```
     The maximum number of hours you can work is 20 hours a week during term (money_jobs.txt).
     ```

     ### What is the maximum number of hours you can work on campus per week? — run 3

     - Best distance: 0.2715 (passed the gate)
     - Sources retrieved: course_cs_210.txt, course_cs_210_workload.txt, course_phys_130.txt, course_stat_150.txt, money_jobs.txt

     ```
     The maximum number of hours you can work is 20 hours a week during term (money_jobs.txt).
     ```

     ### How many weekly hours outside of class should you expect for CS 210? — run 1

     - Best distance: 0.2427 (passed the gate)
     - Sources retrieved: course_cs_210.txt, course_cs_210_workload.txt, course_econ_101_workload.txt, course_stat_150.txt, course_stat_150_workload.txt

     ```
     You should expect 8 to 10 hours a week outside class for CS 210. 

     Source: course_cs_210.txt (and course_cs_210_workload.txt)
     ```

     ### How many weekly hours outside of class should you expect for CS 210? — run 2

     - Best distance: 0.2427 (passed the gate)
     - Sources retrieved: course_cs_210.txt, course_cs_210_workload.txt, course_econ_101_workload.txt, course_stat_150.txt, course_stat_150_workload.txt

     ```
     For CS 210, you should expect 8 to 10 hours a week outside of class. This comes from the documents `course_cs_210.txt` and `course_cs_210_workload.txt`.
     ```

     ### How many weekly hours outside of class should you expect for CS 210? — run 3

     - Best distance: 0.2427 (passed the gate)
     - Sources retrieved: course_cs_210.txt, course_cs_210_workload.txt, course_econ_101_workload.txt, course_stat_150.txt, course_stat_150_workload.txt

     ```
     For CS 210, you should expect 8 to 10 hours a week outside of class. This comes from the documents `course_cs_210.txt` and `course_cs_210_workload.txt`.
     ```

     ### How much does a meal cost at North Kitchen? — run 1

     - Best distance: 0.4342 (passed the gate)
     - Sources retrieved: dining_halden_hall.txt, dining_kestrel_commons.txt, dining_north_kitchen.txt, dining_north_kitchen_followup.txt, dining_pellew_dining_hall.txt

     ```
     A meal at North Kitchen costs one meal swipe, or $13.00 cash (from dining_north_kitchen.txt).
     ```

     ### How much does a meal cost at North Kitchen? — run 2

     - Best distance: 0.4342 (passed the gate)
     - Sources retrieved: dining_halden_hall.txt, dining_kestrel_commons.txt, dining_north_kitchen.txt, dining_north_kitchen_followup.txt, dining_pellew_dining_hall.txt

     ```
     A meal at North Kitchen costs one meal swipe or $13.00 cash (dining_north_kitchen.txt).
     ```

     ### How much does a meal cost at North Kitchen? — run 3

     - Best distance: 0.4342 (passed the gate)
     - Sources retrieved: dining_halden_hall.txt, dining_kestrel_commons.txt, dining_north_kitchen.txt, dining_north_kitchen_followup.txt, dining_pellew_dining_hall.txt

     ```
     A meal at North Kitchen costs one meal swipe or $13.00 cash (dining_north_kitchen.txt).
     ```
Real system output for Criterion 3 (Gate stops out-of-corpus questions): 
     Out-of-scope questions (the gate should refuse these):
     refused  (best distance 0.821)  What is the capital of Mongolia?
     refused  (best distance 0.885)  How do I change the oil in a diesel engine?
     refused  (best distance 0.874)  Who won the 1994 World Cup?
     refused  (best distance 0.824)  What is the recommended dosage of ibuprofen for a headache?
     refused  (best distance 0.831)  How do I write a for loop in Rust?
     -> gate refused 5 of 5


## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
