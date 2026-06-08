# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

--- Campus survival tips and orientation knowledge for college students — 
the practical stuff that doesn't appear in official handbooks, like what 
to actually pack, how to handle dorm life, managing money, mental health, 
and academic habits. This knowledge is hard to find officially because it 
lives in Reddit threads, student forums, and word of mouth rather than 
any official university resource.

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/college| Packing list megathread| https://www.reddit.com/r/college/comments/w0npss/college_packing_list_megathread_post_all_lists/|
| 2 | r/college| High school habits to stop| https://www.reddit.com/r/AskReddit/comments/xowbt/college_redditors_whats_the_one_high_school_habit/|
| 3 | PCWorld| Best laptops for college| https://www.pcworld.com/article/557622/the-best-laptop-for-college.html|
| 4 | r/txstate| Things I wish I knew| https://www.reddit.com/r/txstate/comments/2drouc/things_i_wish_i_knew_my_first_year_of_college_all/|
| 5 | r/txstate| Dorm tips| https://www.reddit.com/r/txstate/comments/13po30j/dorm_tips/|
| 6 | BestColleges| Budgeting guide| https://www.bestcolleges.com/resources/budgeting-in-college/|
| 7 | Mental Health Coalition| College mental health toolkit| https://www.thementalhealthcoalition.org/college-mental-health-toolkit/|
| 8 | r/college| Things I wish someone told me| https://www.reddit.com/r/college/comments/vw3u15/things_i_wish_someone_told_me_before_i_started/|
| 9 | ThoughtCo| 10 things before college| https://www.thoughtco.com/what-you-need-to-know-before-starting-college-787027|
| 10 | r/studytips| College survival guide| https://www.reddit.com/r/studytips/comments/1mx6xt3/college_survival_guide_based_on_my_experience_and/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
400
**Overlap:**
50 characters
**Why these choices fit your documents:**
Documents are a mix of short Reddit comments and long structured 
guides. 400 characters keeps chunks small enough that a single tip stays 
together without mixing unrelated topics, but large enough that short 
Reddit comments don't get cut into meaningless fragments. 50-character 
overlap ensures sentences split across boundaries still appear complete 
in at least one chunk. Preprocessing removed HTML tags and bot replies.

**Final chunk count:**
65
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
For real deployment I'd consider larger models 
like OpenAI's text-embedding-3-large for better accuracy on nuanced 
queries, but they cost money per API call. I'd also consider context 
length — all-MiniLM caps at 256 tokens which can cut longer chunks. 
Local models like all-MiniLM have no network latency, while API models 
add a round trip on every query.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
Answer the user's question using ONLY the information 
provided in the documents below. If the documents don't contain enough 
information to answer, say 'I don't have enough information on that.'
**How source attribution is surfaced in the response:**
Source attribution is surfaced two ways: the LLM is instructed to cite 
sources inline in its response, and the UI programmatically displays the 
source filenames retrieved from ChromaDB metadata in a separate Sources box.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Clothes to bring to dorm?| Minimize wardrobe, ~10 outfits| Correctly cited shoe advice and wardrobe minimalism from packing list| Relevant| Accurate|
| 2 | Habits to stop in class?| No talking, phones, loud food| Listed 5 specific classroom habits from high_school_habits.txt| Relevant| Accurate|
| 3 | Laptop on a budget?| 8GB RAM, consider Chromebook| Specific advice on RAM, Chromebook vs Windows, keyboard quality| Relevant| Accurate|
| 4 | Texas State dorm rules?| No candles, air fryers, 700w microwave| Refused to answer despite info being in txstate_dorm_tips.txt| Partially relevant| Inaccurate|
| 5 | Social tips first week?| Go to dorm events, meet people early| Refused to answer despite info being in things_i_wish_i_knew.txt| Partially relevant| Inaccurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
"What are the dorm rules freshmen at Texas State 
are surprised by?"
**What the system returned:**
 "I don't have enough information on that."
**Root cause (tied to a specific pipeline stage):**
The grounding instruction in the system prompt was too strict. 
The instruction told the LLM to only answer if documents contained enough 
information, but the LLM interpreted the query too literally — the document 
uses phrases like "do not bring candles" rather than "rules freshmen are 
surprised by." The semantic gap between the query vocabulary and document 
vocabulary caused the generation stage to refuse a question it could have 
answered.
**What you would change to fix it:**
 Soften the system prompt to say "answer as best you 
can from the documents" rather than requiring explicit coverage. Also 
adding more explicit keywords to txstate_dorm_tips.txt (like the document 
enrichment technique used for high_school_habits.txt) would help retrieval 
return a higher-confidence match.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
 Writing the chunking strategy section before 
coding forced me to think about document structure first. When I saw that 
my documents ranged from 1-sentence Reddit comments to multi-paragraph 
guides, I chose 400 characters deliberately rather than using a default. 
This saved me from having to debug bad retrieval later.

**One way your implementation diverged from the spec, and why:**
The spec didn't anticipate document 
enrichment — adding explicit keywords to source files to improve retrieval. 
I added classroom habit keywords to high_school_habits.txt after seeing 
that query 2 was returning irrelevant chunks with distance scores above 
1.0. This wasn't in the plan but improved retrieval significantly.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*My Chunking Strategy and Documents sections from 
  planning.md
- *What it produced:*ingest.py with load_documents() and chunk_text() 
  functions using 400 character chunks and 50 character overlap

- *What I changed or overrode:* kept the chunk size but added a strip() check to 
  filter empty chunks

**Instance 2**

- *What I gave the AI:* kept the chunk size but added a strip() check to 
  filter empty chunks
- *What it produced:*embed.py and retrieve.py using all-MiniLM-L6-v2 
  and ChromaDB with source metadata
- *What I changed or overrode:* I increased n_results from 5 to 7 after testing showed 
  relevant chunks were ranking outside the top 5 for some queries
