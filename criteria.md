# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer
For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.
**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
The pipeline's retrieval stage must surface the exact chunk containing the campus_life (corpus) credit-hour exception sentence so the LLM doesn't miss the critical nuance of the housing lottery rule. If the retrieved text chunks do not contain the answer, the LLM has 0 chance of generating an accurate response based on our data, leading directly to a hallucination or a generic fallback message. In a RAG pipeline, the retrieval stage acts as a strict bottleneck; the downstream generation layer is only as good as the context it receives. Setting a target of 4 out of 5 successful retrievals ensures the chunking strategy, embedding model, and vector database search parameters are well-optimized to surface highly relevant source material, while realistically allowing a minor margin for error on highly niche or poorly phrased edge-case queries.

---

## 2. Every answer names a source
Every answer the system produces names at least 1 source document.
**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
Every generated answer must name its specific source document to allow students to verify the precise campus_life (corpus) policies—like housing eligibility—directly against the original document. Requiring all 5 answers to name a source document is a strict, zero-tolerance baseline because sourcing is entirely controlled by programmatic metadata, not LLM reasoning. Unlike semantic accuracy—which can falter on complex text—attaching a source simply requires the code to forward the file name or URL embedded within the retrieved chunk directly to the final output. For this target to fail, the entire metadata tracking pipeline would have to break down, or the LLM would have to completely ignore its structural system prompt instructions. Setting a 100% success rate ensures the system remains auditable, giving users immediate transparency so they can easily cross-reference and verify any response against the original document.

---

## 3. The relevance gate stops out-of-corpus questions
When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.
<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->
**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
The pipeline's vector distance cutoff must filter out 4 of 5 irrelevant queries to prevent the campus life assistant from hallucinating arbitrary answers on topics completely missing from the campus_life files. A reliable RAG system must know its own limits to prevent hallucinating plausible-sounding lies when asked about topics completely outside its database. During my earlier milestone testing, the out-of-corpus queries generated a clear mathematical gap, averaging a high vector distance of 0.847, while relevant queries stayed well below our maximum allowable threshold. Setting a target of 4 out of 5 successful rejections ensures that our 0.6 distance cutoff is finely tuned enough to act as a strict guardrail against unrelated data, while allowing a minor margin of error for rare edge cases where an out-of-scope question accidentally shares misleading keyword similarities with our internal campus documents.

---

## 4. At least 80% of sampled chunks must contain full, complete sentences
<!-- YOU WRITE THIS ONE. Something about your chunks.
     How would you know if your chunks were the right size? Name something
     countable or observable.
     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->
Derived sampled chunks, at a rate no less than 80%, do not cut off mid-sentence; this ensures the system retrieves standalone, grammatically complete units of information.
**Why this target:**
 Our campus_life corpus relies heavily on precise rules, like the housing credit-hr criteria. If a chunk splits mid-sentence (e.g., separating "ordered by accumulated credit hours first," from its modifier ", and only tie-break randomly"), the embedding model loses the true conditional logic of the policy. However, there is a risk for long-sections of text to appear without sentence boundaries (. , ? , ! ) appearing. The use of "rarely" enables cutting off for the occasional split (assumption where 20% or 1 out of 5 will need the sentence-only exception so chunks don't get too large) on massive paragraphs but retain a preference for punctuations as a signifying deliminator.

---

## 5. System must pass 80% of 5 complex tests by citing sources and providing complete answers
<!-- YOU WRITE THIS ONE TOO. Your choice.
     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->
The system must achieve at least a 4/5 (80%) pass rate across a dedicated test suite of 5 specific complex-process questions (e.g., housing priority ladder eligibility).
     • A query passes only if the response correctly cites source file and returns an accurate, complete answer iexplanation to its corresponding test question (specific to a corpus).
     • A query fails if the response does not cite source file name (in its response) or omits any detail that is required to properly answer its original corresponding test question; output answer is incomplete, vague, or irrelevant.
**Why this target:**
For housing, its document (in the corpus campus_life) reveals a tricky nuance: seniority isn't just about year, it's about accumulated credit hours. A basic RAG setup might retrieve the general "Housing" document for a question like "Does taking summer classes help my housing lottery?", but if chunks are too diluted or our embedding space is too broad, the LLM might miss the exact sentence: "a senior who took summer courses reliably beats a senior who didn't." Hence, we need a high-accuracy target here because providing a student with a generic "housing is random" answer when a precise credit-hr exception exists is a critical hallucination for a campus life assistant. 

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
