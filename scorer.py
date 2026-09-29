# Imports used with OPTION METHOD 2
from http import client
import config

# Imports used with OPTION METHOD 3
from rapidfuzz import fuzz # Ensure install ("python -m pip install rapidfuzz") prior to use

# Three methods to write a scorer / judge function to test LLM Q&A output quality 
def judge(question, expects, answer, results) -> bool:
    """ 
    OPTION METHOD 1: 
        Pass if the expect is in the answer (e.g., question: 'give', expect: 'give')
    """
    # return expects.lower().strip() in answer.lower()

    """ 
    OPTION METHOD 2: 
        LLM as a Judge (expensive): Uses an LLM to evaluate if an answer satisfies the expected criteria.            
    """
    """
    # 1. Define the system instruction to force a deterministic True/False evaluation
    system = (
        "You are an objective grading assistant. Evaluate the provided answer based on "
        "the question and the expected criteria. Respond with exactly 'True' if the "
        "answer satisfies the expectation, or 'False' if it does not. Do not include "
        "any other text, explanation, or punctuation."
    )
    # 2. Construct the prompt with the input context
    prompt = (
        f"Question: {question}\n"
        f"Expected Criteria: {expects}\n"
        f"Submitted Answer: {answer}\n"
        f"Additional Context/Results: {results}\n"
        f"Does the answer satisfy the expectation? (True/False):"
    )
    # 3. Setup the API arguments following your original code snippet pattern
    kwargs = {"model": config.MODEL, "contents": prompt}
    if system:
        kwargs["config"] = {"system_instruction": system}
    try:
        # 4. Execute the call and clean up the text response
        response = client.models.generate_content(**kwargs)
        text = (response.text or "").strip()
        # 5. Parse the LLM's response into a boolean evaluation
        return text.lower() == "true"
    except Exception as exc:  # noqa: BLE001 – surfaced below
        # Handle API errors or handle fallback evaluations here
        print(f"LLM Judging failed due to: {exc}")
        return False
    """
    
    """ 
    OPTION METHOD 3 (best balance on performance vs. cost): 
        Use built-in semantic library (meaning search) w/ Python via "rapidfuzz" method import. 
        Score generated answers against the short expected phrase per question.
        Evaluates generated answer against expected facts and citations.
            Uses token_set_ratio to handle word reordering, extra context, 
            and citation placement differences.
    """
    # A modest cutoff allows harmless wording differences while keeping a short,
    # unrelated answer from passing just because it shares one common word.
    SIMILARITY_CUTOFF = 75
    # Return whether `answer` contains a close match for `expects` (e.g., "0 libs open" = "no libs open").
    #     `question` and `results` are accepted to match the evaluation runner's
    #     scorer interface; this lexical scorer only needs the expected phrase and
    #     generated answer. `partial_ratio` is useful here because answers usually
    #     contain the expected phrase among other explanatory text.
    if not isinstance(expects, str) or not isinstance(answer, str):
            return False
    expected = expects.strip()
    response = answer.strip()
    if not expected or not response:
        return False
    # token_set_ratio compares common word tokens, ignoring word order & extra text
    score = fuzz.token_set_ratio(expected.casefold(), response.casefold())
    return score >= SIMILARITY_CUTOFF
    # The Fix: Switch from fuzz.partial_ratio() to fuzz.token_set_ratio()
        # In rapidfuzz, fuzz.token_set_ratio (or fuzz.partial_token_set_ratio) splits strings into individual word tokens, finds common subset, and evaluates similarity regardless of word order, extra explanatory words, or where citation appears in sentence.
        # For example, comparing:
            # expects: "In health_center.txt, walk-in hours are from 8am to 11am."
            # answer: "The walk-in hours at the health center are 8am to 11am (from health_center.txt)."
        # fuzz.partial_ratio scores around ~65–75% (risking a fail at an 80 cutoff).
        # fuzz.token_set_ratio scores > 90% (a clean pass).
    # Why partial_ratio fails: It searches for best matching contiguous char substring between 2 texts. Because of structural differences between expects and answer, this creates a hidden bottleneck:
        # Word Order Inversion: Every expects string starts with the citation ("In health_center.txt, ..."), whereas your model generates answers with the citation appended at the end ("... (from health_center.txt)" or "Source: health_center.txt").
        # Contiguous Window Penalty: Because the filename and the fact are on opposite ends of the model's generated sentence, partial_ratio cannot capture both inside a single contiguous character window without incurring heavy edit distance penalties for the intervening text.
        # Rephrased Content: For queries like Question 1 where the LLM rephrases "you need two writing-intensive courses..." into "consists of two courses, which must be taken...", the character alignment drops further and risks dipping below the 80 cutoff.


# Use to determine if LLM output to test questions does in fact pull from embedded chunks (not AI's imagination / fabricated)
def retrieval_hits(expects: str, results: list, score_cutoff: float = 80.0) -> bool:
    """
    METHOD 1: Pure Python Check on if any part of expect in results 
        # return any(expects.strip().lower() for chunk in results)
    """
    clean_expect = expects.strip().lower()
    # Correct use of 'any' to check if the substring exists in each chunk
    return any(clean_expect in str(chunk).strip().lower() for chunk in results)

    """
    METHOD 2: Use RapidFuzz to check for semantic meaning (not just literal use of same word(s) like in METHOD 1)
        Checks if expected string partially matches any chunk in results via a fuzzy matching threshold.
    """
    """
    # Clean the expected string once
    clean_expect = expects.strip().lower()
    for chunk in results:
        clean_chunk = str(chunk).strip().lower()
        # partial_ratio is perfect for "any part of my expect in the results"
        if fuzz.partial_ratio(clean_expect, clean_chunk) >= score_cutoff:
            return True
    return False
    """


