# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Campus survival tips and orientation knowledge for college students — the practical stuff that doesn't appear in official handbooks, like what to actually pack, how to handle dorm life, managing money, mental health, and academic habits. Hard to find officially because it lives in Reddit threads, student forums, and word of mouth.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
400
**Overlap:**
50
**Reasoning:**
My documents are a mix of short Reddit comments (1-3 sentences) and long structured guides with headers and paragraphs. 400 characters keeps chunks small enough that a single tip or idea stays together without mixing unrelated topics, but large enough that short Reddit comments don't get cut into meaningless fragments. The 50-character overlap makes sure that sentences split across chunk boundaries still appear complete in at least one chunk.---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2 via sentence-transformers
**Top-k:**
5
**Production tradeoff reflection:**
For a real system I'd think about accuracy vs cost — bigger models are better but expensive. I'd also consider context length since all-MiniLM caps at 256 tokens, and latency since local models are faster than API calls

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about how many clothes to bring to a dorm?| Bring minimally — most recommend 2 weeks of outfits, don't bring your whole wardrobe|
| 2 | What habits should freshmen stop doing in class?| Talking, being late, asking "will this be on the test?", using phones|
| 3 | What should students look for when choosing a laptop on a budget?| At least 8GB RAM, good battery life, consider Chromebook for basic tasks|
| 4 | What are dorm rules freshmen at Texas State are surprised by?| No candles, air fryers banned, 700w microwave limit, fire alarms, room checks|
| 5 | What do upperclassmen say is the most important thing to do socially in the first week?| Make friends immediately, go to dorm events, don't wait for friend groups to form|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.Reddit threads have upvote counts, deleted users, bot replies, and off-topic comments mixed in with real tips. A chunk might contain "[deleted]" or "Good bot :)" instead of useful advice, and the retriever won't know the difference.
2.some Reddit tips are so short that even at 400 characters, a chunk might just be one sentence with no surrounding context. The embedding carries weak signal and retrieval might return it for unrelated queries.
---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
```
flowchart LR
    A[Document Ingestion\nraw .txt files] --> B[Chunking\n400 chars / 50 overlap]
    B --> C[Embedding\nall-MiniLM-L6-v2]
    C --> D[Vector Store\nChromaDB]
    D --> E[Retrieval\ntop-k=5]
    E --> F[Generation\nGroq llama-3.3-70b]
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I'll give Claude my Documents section (list of 10 sources, all .txt files) and my Chunking Strategy section (400 chars, 50 overlap) and ask it to implement an ingestion script that loads the files, cleans out noise like HTML tags and deleted Reddit comments, and produces chunks matching my spec.
**Milestone 4 — Embedding and retrieval:**
I'll give Gemini my Retrieval Approach section and Architecture diagram and ask it to implement the embedding step using all-MiniLM-L6-v2 and store chunks in ChromaDB with source metadata. Then ask it to implement a retrieve() function that returns top-5 chunks with text, source, and distance score.
**Milestone 5 — Generation and interface:**
I'll give Claude my full planning.md and ask it to implement a generate_response() function using Groq's llama-3.3-70b that answers only from retrieved chunks and cites sources. Then ask it to build a Gradio interface that shows the answer and sources.