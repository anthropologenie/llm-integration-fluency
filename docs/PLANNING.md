# Planning — LLM Integration Fluency Project (`incident-investigation-agent`)

**Repo:** `llm-integration-fluency`
**Status:** Planning — not yet started
**Owner:** Karthik S R
**Evidence classification (on completion):** VERIFIED PORTFOLIO IMPLEMENTATION — kept explicitly separate from, and never merged into, the main AI Evaluation & RAG Reliability portfolio. This project exists to demonstrate framework fluency; the main portfolio remains the demonstration of native architecture judgment (NA-07). Neither should be described as superseding the other.

---

## 1. Why this project exists

A live AI-driven mock interview (Vericlick) exposed a specific, narrow gap: conceptual reasoning about RAG, retrieval, evaluation, and agentic architecture was consistently strong, but hands-on fluency with the standard framework layer — LangChain, LCEL, LangGraph, and Ragas specifically — was not. The clearest evidence was a live-coding exercise: asked to write a Ragas `evaluate()` call cold, the dictionary syntax, the `contexts`-as-a-list requirement, and the `ground_truth` key name were all fumbled, requiring the interviewer to walk through each fix.

The diagnosis that matters: **this is API muscle memory, not a knowledge gap.** The underlying concepts (Faithfulness, Answer Relevancy, Context Precision/Recall, retriever abstractions, stateful orchestration) are already understood and already implemented natively in the main portfolio. What's missing is hands-on repetition with the specific framework APIs an interviewer is likely to ask about directly.

This project is designed to close exactly that gap — not to rebuild a more impressive RAG system, and not to replace or reconsider the native-architecture decisions already made and documented (RO-17, RO-18) in the main portfolio.

**Explicitly out of scope for this project:** Graph RAG, five-agent architectures, production deployment, Docker/Kubernetes orchestration, fine-tuning, multimodal, elaborate frontends, elaborate observability. The main portfolio already carries that complexity; duplicating it here dilutes the point.

**Project operating principle:** Optimize for framework fluency and interview recall, not production completeness. A smaller implementation that I can explain, modify, debug, and reproduce from memory is more valuable than a larger implementation assembled from documentation.

**Second explicit objective — framework abstraction literacy.** Alongside fluency and recall, for every major framework component (LangChain, LCEL, Chroma, Ragas, LangGraph, checkpointing, tools) this project should be able to answer: (1) what does this abstraction do, (2) what does it abstract away, (3) what does it hide, (4) what remains application responsibility, (5) where can the abstraction leak, (6) what would I need to implement/control myself without it. This is a lens applied to the existing stages and stage notes — not a new standalone subsystem, and not additional stages.

---

## 2. The two-layer story this project is building toward

**Layer A — Framework implementation (this repo):** FastAPI → LangGraph → LangChain → Chroma → LLM → Ragas.

**Layer B — Native comparison (main portfolio, already built):** BM25 + BGE + FAISS + RRF + native LLM-as-a-judge engines + pytest + evidence traceability.

The target interview answer, once this is built:

> "I'd previously built a native RAG and evaluation system because I wanted explicit control over retrieval, evaluation, and evidence traceability. After hitting framework-specific questions in interviews, I built a separate fluency project using LangChain, LangGraph, and Chroma — using LangChain for the retriever and LCEL abstractions, LangGraph for stateful orchestration and conditional routing, and Ragas for standardized evaluation. Then I swapped the vector store and compared the framework's abstractions against my native implementation directly."

That's a maturity claim — "I understand both the abstraction layer and what's underneath it" — not a reversal of the native-architecture decision.

**The conceptual translation this project is really teaching** (not a strict one-to-one claim, but the mapping to be able to draw and defend):

| Native responsibility | Framework abstraction |
|---|---|
| BM25 | Retriever (lexical side) |
| BGE embeddings | Embeddings |
| FAISS | Vector store |
| RRF | Retrieval composition |
| Prompt builder | PromptTemplate |
| LLM call | ChatModel |
| Pipeline composition | LCEL |
| Orchestration | LangGraph |
| Native evaluation engines | Ragas |

And the reverse question, which matters as much as the forward mapping: **if the framework were removed, which of these responsibilities return to the application, and which were never really the framework's to begin with?** This reverse question is what separates "I used LangChain" from "I understand what LangChain is doing for me" — it's a central learning outcome of this project, not a side exercise, and it's what coding drill #11 (§7) and the final comparison (§8) are built around.

---

## 3. Repository structure

```text
llm-integration-fluency/
├── README.md
├── application/
│   └── incident-investigation-agent/
│       ├── api/                  # FastAPI app (Stage 0)
│       ├── chains/               # LCEL chains (Stage 3)
│       ├── graph/                # LangGraph StateGraph, nodes, state schema (Stages 5-8)
│       ├── tools/                # deterministic tools for tool-calling (Stage 7)
│       ├── retrieval/             # Chroma ingestion, retriever config (Stages 2, 10)
│       └── eval/                  # Ragas evaluation pipeline (Stage 4)
├── docs/
│   ├── PLANNING.md                    # this document
│   ├── stage-notes/                   # one short note per stage, written as completed
│   ├── framework-abstraction-leaks.md # per-component abstraction notes, written as encountered (§5a below)
│   └── native-vs-framework.md         # comparison doc (final deliverable, §8 below)
├── experiments/
│   └── chroma-vs-weaviate/         # optional backend-swap exercise (Stage 10)
└── tests/
    └── coding-drills/              # cold-recall drill scripts (§9 below), re-typed from memory repeatedly
```

---

## 4. Data and dataset reuse

Reuse the existing 22-question golden dataset and 259-chunk corpus used by the main portfolio. This is deliberate: the point of this project is comparing toolchains on a *known* problem, not producing a new dataset. Any retrieval-quality numbers from this pipeline should be read as a framework comparison against the already-measured native baseline (Hit Rate 0.500, Precision@5 0.109, Recall@5 0.324), not as a new standalone claim.

---

## 5. Staged build plan

Five focused days. Stage notes are written immediately after completing each stage, in `docs/stage-notes/`, before starting the next stage — not retrospectively. Every stage note follows the same structure:

1. What I built
2. What abstraction the framework introduced
3. What surprised me or differed from my native implementation
4. What I can now explain or reproduce that I could not before
5. What remained application responsibility
6. What abstraction leak or failure mode I observed

Examples of the kind of thing #3–6 should capture: what Chroma abstracts compared with the native FAISS layer, what LCEL actually provides, what LangGraph state means operationally, what checkpointing changes, what Ragas expects as input, what remains application responsibility regardless of framework. The point of writing these as-you-go, in this structure, is to turn the project from "I followed a tutorial" into evidence of actual framework understanding — these notes are the raw material for the Story Bank entry once this project is complete.

### 5a. `docs/framework-abstraction-leaks.md` — running log

A lightweight companion to the stage notes, updated as each major component is worked with (LangChain, LCEL, Chroma, Ragas, LangGraph, checkpointing, tools) — not a lengthy essay per component, just enough to capture the judgment call. Per component:

```
Framework:
Component:
What it abstracts:
What it hides:
What it does NOT solve:
Where the abstraction leaked:
What remained application responsibility:
What I learned:
```

This is the same "framework abstraction literacy" objective from §1, written down as it's actually discovered rather than reconstructed afterward — and it feeds directly into the final `native-vs-framework.md` deliverable (§8).

### 5b. Minimal execution tracing (cross-cutting, not a new stage)

Elaborate observability remains explicitly out of scope (§1) — no LangSmith, Phoenix, OpenTelemetry, Prometheus, Grafana, or tracing infrastructure. What's added instead is a small, application-level JSON/JSONL trace per investigation run, written once the graph (Stage 5 onward) exists: `run_id`, `question`, `nodes_executed`, retrieval info (retrieved document identifiers), `tools_called`, basic latency, `final_answer`, `confidence`. The purpose is narrow — making the graph's execution and state transitions inspectable while working through Stages 5–9 — not building an observability system. This is minimal execution evidence, nothing more.

### 5c. Failure/recovery experiments (mandatory, within Stage 5's routing)

Stage 5's conditional-routing example (`Retrieve → Assess Retrieval → good: Generate | poor: Rewrite Query → Retrieve`) is built as an actual failure/recovery experiment, not only a graph-mechanics demonstration. At minimum, work through: (1) no relevant evidence / low retrieval score, (2) query rewrite and retry, (3) still-insufficient evidence after retry, (4) malformed LLM output, (5) tool failure, (6) timeout/error path, (7) conflicting evidence, (8) checkpoint interruption/resume (ties to Stage 8). For each: `Failure → Detection → Routing/handling → Result → Trace/evidence` (the trace from §5b is what makes the last step concrete). Keep this small and deterministic where possible — the goal is connecting framework fluency to the existing reliability/evaluation background, not building a resilience framework.

### Stage 0 — Direct LLM integration (no framework)
```
FastAPI → Python function → LLM API → response
FastAPI → Pydantic request → LLM → Pydantic response
```
Understand directly: `messages`, `model`, `temperature`, `max_tokens`, structured output, error/timeout handling. This is the literal answer to "what does LLM integration mean" — API → LLM → validated response, built by hand before any framework abstracts it.

### Stage 1 — LangChain without agents
```
Document → Text Splitter → Embedding → Vector Store → Retriever → Prompt → Chat Model
```
Learn the core abstraction: **LangChain isn't the LLM — it's standardized components around it** (ChatModel, Retriever, Document, Prompt, Tool, OutputParser). Be able to explain each one individually.

### Stage 2 — ChromaDB
```
LangChain → Chroma → Retriever
```
Learn: Collection, Document, ID, Embedding, Metadata, Similarity Search, Filtering, Persistence. Deliberately compare against the native FAISS setup: Chroma provides higher-level collection, persistence, ID, metadata, and retrieval abstractions, whereas the native implementation deliberately exposes and controls content identity, staleness detection, persistence, and index lifecycle. Chroma does not automatically solve application-level staleness detection — the application still has to define what counts as stale data and when re-indexing or rebuilding is required; Chroma just gives you the storage/retrieval primitives to build that on top of. Naming precisely what the framework abstracts versus what responsibility still sits with the application is the actual learning objective here, not just getting Chroma to run.

### Stage 3 — LCEL
```
Retriever → Prompt → LLM → Parser   (composed as a single runnable chain)
```
Mandatory — this is a named, explicit gap from the transcript. Understand LCEL as **composition of runnable components**, and the `invoke()` / `batch()` / `stream()` interface. Not a syntax-memorization exercise — understand why composability matters (swap any stage without rewriting the others).

### Stage 4 — Ragas (highest-priority gap)
```
{question, answer, contexts, ground_truth} → Dataset → evaluate() → {faithfulness, answer_relevancy, context_precision, context_recall} → results
```
This directly addresses the exact API-recall failure observed during the Vericlick live-coding exercise, so it's built in two explicit steps rather than once at full scale:

**Step 1 — minimal dataset (2–3 examples), by hand.** Get the schema right before anything else: `question`, `answer`, `contexts` as a **list**, `ground_truth` (underscore). Construct the `Dataset`, call `evaluate()`, inspect the result. Then **delete the implementation and reproduce it from memory, several times**, before moving on. The learning progression: 2–3 examples → schema correctness → `evaluate()` → inspect result → delete → reproduce from memory → (only then) full-scale run.

**Step 2 — full 22-question dataset.** Only attempted once Step 1's schema and call pattern are automatic. At this point the dataset can come from the LangGraph pipeline's own outputs once Stage 5 exists, or from the existing golden dataset directly — either is fine, since the point of this stage is API fluency, not a new measured result.

Also touch DeepEval's `LLMTestCase` shape for comparison, briefly — enough to not conflate the two APIs live.

### Stage 5 — LangGraph, minimal
```
START → Retrieve → Generate → END
```
then
```
START → Retrieve → Assess Retrieval → (good → Generate) | (poor → Rewrite Query → Retrieve) 
```
Learn: State, Node, Edge, Conditional Edge, Loop. This stage maps almost directly onto the existing ALTM lifecycle model (Knowledge → Index → Retrieve → Assemble → Infer → Post-Process → Evaluate) — worth noting explicitly in the stage note, since that connection is a strong interview line. The conditional routing above is where the mandatory failure/recovery experiments (§5c) are worked through — this stage isn't complete until those are demonstrated, not just the graph mechanics.

### Stage 6 — Make the graph stateful
Define an explicit state schema, e.g.:
```python
class InvestigationState(TypedDict):
    question: str
    messages: list
    query: str
    retrieved_documents: list
    retrieval_score: float
    tool_results: list
    hypothesis: str
    answer: str
    confidence: float
```
Every node reads and writes this state. This is where "stateful agent" stops being a term and becomes something built.

### Stage 7 — Tool calling
2–3 deterministic tools, e.g. `search_documentation()`, `get_release_notes()`, `get_incident_logs()`. Flow: `User → LLM → decides tool → Tool → result → LLM → answer`. This maps directly onto the real HP experience (custom Python/FastAPI tools against GitHub Enterprise APIs) — the interview bridge here should be explicit and easy, since it's genuinely the same pattern in a different framework.

### Stage 8 — Persistent state (checkpointing)
Run an investigation partway, stop, restart, resume from the checkpoint. This is the concrete, first-hand version of "persistent agent state" — the exact phrase from the target JD's "multi-agent orchestration, tool use, persistent state, memory management, agent evaluation" line. This is also failure/recovery experiment #8 from §5c (checkpoint interruption/resume) — the same build satisfies both.

### Stage 9 — State vs. memory, explicitly distinguished
- **State** = current investigation only (current question, current evidence, current hypothesis).
- **Memory** = across investigations (incident history, previous findings, known patterns).

These two get conflated constantly in interviews — being able to draw the line cleanly, with a concrete example of each from this build, is a specific, rehearsable answer.

### Stage 10 — Chroma → Weaviate swap
**Stretch goal — not required for project completion.** Swap only the vector store; keep LangGraph/LangChain/Retriever unchanged. If Stages 0–9 are not solid, do not spend remaining time on Stage 10 — interview fluency on the core stages is the priority, not completing every numbered stage. The practical priority order across the whole project is: Ragas → LangChain/LCEL → LangGraph → tools/state → Chroma → Weaviate. The payoff line, if reached: *"I implemented the same retrieval application against two vector stores through the LangChain retriever abstraction, which showed me exactly what the framework abstracts versus what stays vendor-specific."*

---

## 6. Day-by-day schedule

The staged progression in §5 keeps its original numbering (0–10) and is not changed — but Ragas is deliberately pulled earlier in the *schedule*, into Day 3, ahead of LangGraph. It was the clearest live-coding/API-muscle-memory failure in the Vericlick interview, so it gets fixed early rather than waiting until Day 4. This is a scheduling choice, not a dependency: Ragas (Stage 4) does not conceptually depend on LangGraph (Stage 5) — the minimal 2–3-example Ragas exercise in Stage 4 can run against a hand-built `{question, answer, contexts, ground_truth}` dict before any graph exists at all.

| Day | Stages | Focus |
|---|---|---|
| 1 | 0, 1 | Direct LLM integration + LangChain fundamentals |
| 2 | 2, 3 | Chroma + LCEL |
| 3 | 4, 5 | Ragas (minimal-dataset step first) + LangGraph fundamentals |
| 4 | 6, 7 | Stateful graph + tool calling |
| 5 | 8, 9, (10*) | Checkpointing + state/memory distinction + native-vs-framework comparison; Weaviate only if time allows |

\* Stretch goal — see Stage 10.

---

## 7. Coding drill set (`tests/coding-drills/`)

Separate from the application code — the point is typing these cold, repeatedly, not building them once and moving on.

1. Ragas `Dataset` construction + `evaluate()` call
2. LangChain retriever setup (from a Chroma collection)
3. LCEL RAG chain (`retriever | prompt | llm | parser`)
4. LangGraph `StateGraph` definition with a `TypedDict` state
5. A conditional edge (routing function + `add_conditional_edges`)
6. A tool definition (`@tool` decorator or equivalent)
7. Pydantic structured output from an LLM call
8. FastAPI endpoint wrapping an LLM call
9. Chroma ingestion (`add_documents` / `add_texts` with metadata)
10. Ragas result extraction and summary printing
11. **Native ↔ framework translation drill** — given the native portfolio architecture (BM25 → BGE → FAISS → RRF → native LLM-as-a-judge), explain how the equivalent responsibilities would be expressed using LangChain → Chroma → LCEL → Ragas. Then run the exercise in reverse: identify which framework abstractions correspond to which native responsibilities, and which responsibilities remain application-specific regardless of framework. This one isn't about syntax — it tests whether the abstraction itself is understood, not just its API.

Re-run this set from memory, no reference, until automatic. This directly targets the exact failure mode from the transcript (semicolons instead of colons, `contexts` as a string instead of a list, `ground truth` instead of `ground_truth`, `dict` shadowing the builtin).

---

## 8. Final deliverable: `docs/native-vs-framework.md`

A short, honest comparison, written after Stage 9, drawing directly on the running `framework-abstraction-leaks.md` log (§5a) and the failure-experiment results (§5c). Covers:
1. Native architecture (what was built and why)
2. Framework architecture (what was built and why)
3. Native ↔ framework responsibility mapping (the table in §2, filled in with what was actually learned, not the a-priori guess)
4. What the framework abstracts
5. What the framework hides
6. Where abstractions leaked (pulled from §5a)
7. What remained application responsibility
8. Failure/recovery implications (pulled from §5c)
9. Control and traceability (native: explicit content-fingerprint identity/staleness design, explicit evidence-provenance JSONL layer; framework: what's handled automatically vs. what's hidden, informed by the minimal execution trace in §5b)
10. Dependency/complexity trade-offs (native: `math` only, enforced via AST allowlist tests; framework: LangChain + LangGraph + Chroma + Ragas dependency trees)
11. When the framework earns its complexity (stateful conditional routing, checkpointing) vs. when native gives better control
12. When I would choose native vs. framework, stated as a real judgment call, not a universal winner

This document becomes the primary source for the eventual Story Bank entry — it should be written in the same evidence-disciplined style as the rest of the interview-prep documents (state what was built, what was measured, what wasn't done, and don't oversell either side). The intended conclusion stays "I now understand both," never "framework beat native" or the reverse.

---

## 9. Success criteria — mapped to the original interview gaps

| Gap from the interview | Closed by |
|---|---|
| Ragas `evaluate()` / dataset schema, cold | Stage 4 + coding drills #1, #10 |
| LangChain retriever, chat model, prompt, parser | Stages 1–3 |
| LCEL | Stage 3 + coding drill #3 |
| ChromaDB | Stage 2 + coding drill #9 |
| LangGraph state / nodes / conditional edges | Stages 5–6 + coding drills #4–5 |
| Persistent state | Stage 8 |
| Memory (vs. state) | Stage 9 |
| Tool calling in a framework context | Stage 7 + coding drill #6 |
| Weaviate / vector-store abstraction | Stage 10 (optional) |
| "What does LLM integration mean" | Stage 0 |
| Native-vs-framework trade-off reasoning | `docs/native-vs-framework.md` |

**Completion also means more than "the code runs"** — the following are equally part of done:
- **Framework abstraction literacy:** can explain what each framework component abstracts, what remains application responsibility, and where it can leak (§5a).
- **Failure/recovery:** can demonstrate and explain the controlled failure paths through the LangGraph workflow (§5c).
- **Execution evidence:** can inspect a minimal run trace showing what happened during an investigation (§5b).
- **Native/framework translation:** can map native responsibilities to framework abstractions and explain what returns to the application if the framework is removed (§2).
- **Interview recall:** can reproduce the key APIs and patterns from memory rather than relying on documentation (§7).

**Not addressed by this project, and not intended to be:** Graph RAG (already covered, bounded as POC, in the Neo4j entry), AWS Bedrock AgentCore, MCP, self-healing test automation, Model-Based Testing. These remain separate, minimally-bounded gaps per the Interview Syllabus's anti-thrash rule — one project shouldn't try to close every open item at once.

---

## 10. Governance note

Once complete, this project's evidence should be added to the Story Bank as its own entry (working title: "Framework Fluency Project — LangChain/LangGraph/Ragas"), classified as VERIFIED PORTFOLIO IMPLEMENTATION, with the same discipline applied elsewhere: state what was measured, name what wasn't attempted, and never let this project's existence imply the native-architecture decisions (RO-17, RO-18) were reconsidered. The correct framing is additive — "I now have both" — never corrective.
