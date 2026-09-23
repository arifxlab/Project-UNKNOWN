# 2. `RULES.md`

Replace the entire file:

```markdown
# Project UNKNOWN — Rules

## Purpose

This document defines the research and engineering rules governing Project UNKNOWN.

These rules exist to prevent premature conclusions, unsupported novelty claims, irreproducible experiments, and unnecessary engineering complexity.

---

# 1. Research Integrity

## Rule 1.1 — No Unsupported Novelty Claims

Never claim that UNKNOWN is novel merely because an idea appears different from familiar systems.

Novelty must be evaluated against relevant prior art.

---

## Rule 1.2 — Hypothesis Is Not Fact

Clearly distinguish:

- hypothesis;
- assumption;
- observation;
- experiment;
- result;
- interpretation;
- conclusion.

A hypothesis must never be written as an established result before experimental validation.

---

## Rule 1.3 — Discovery Requires Evidence

A generated concept is not a discovery merely because:

- an LLM named it;
- it sounds plausible;
- it forms a visually attractive cluster;
- it improves training loss;
- it correlates with an outcome;
- a model can explain it after the fact.

Discovery requires predefined validation criteria.

---

## Rule 1.4 — Falsifiability

Every serious candidate concept must have at least one condition under which it could be rejected.

If a candidate cannot fail experimentally, it is not sufficiently specified for scientific validation.

---

# 2. Experimental Integrity

## Rule 2.1 — Define Before Testing

Where practical, define:

- hypothesis;
- baseline;
- evaluation metric;
- intervention;
- expected result;
- failure condition

before running the decisive experiment.

---

## Rule 2.2 — No Cherry-Picking

Do not report only successful experiments.

Failed experiments, rejected hypotheses, and unexpected results must remain traceable.

---

## Rule 2.3 — Baselines Are Mandatory

Major claims must be compared against appropriate baselines.

A complex system must not receive credit merely because it performs better than an intentionally weak baseline.

---

## Rule 2.4 — Holdout Integrity

Data or environments used for discovery must not silently become evaluation data.

Train/discovery, validation, intervention, and transfer contexts must be clearly separated where appropriate.

---

## Rule 2.5 — Ground Truth Is Hidden From UNKNOWN

When using synthetic environments with known mechanisms, the true hidden mechanism may be known to the experiment designer but must not be directly supplied to the discovery system.

---

## Rule 2.6 — False Discoveries Must Exist

Experiments should contain situations where:

- correlations are misleading;
- predictive features are not causally/interventionally valid;
- context-specific patterns fail to transfer;
- plausible candidate concepts are incorrect.

UNKNOWN must have opportunities to reject bad hypotheses.

---

# 3. Reproducibility

## Rule 3.1 — Record Configuration

Experiments must record relevant:

- random seeds;
- environment configuration;
- model configuration;
- dataset/version;
- code version;
- dependency versions;
- experiment parameters.

---

## Rule 3.2 — Version Results

Important results must be associated with a specific repository state.

---

## Rule 3.3 — Determinism Where Practical

Experiments should be deterministic where the underlying framework permits it.

When nondeterminism is unavoidable, it must be measured or documented.

---

## Rule 3.4 — Re-run Capability

A completed experiment should be reproducible from documented configuration and repository state.

---

# 4. Concept Integrity

## Rule 4.1 — No Human Naming as Evidence

A researcher assigning a meaningful name to an extracted latent structure does not constitute concept discovery.

---

## Rule 4.2 — Representation Before Label

A concept must have operational behavior before receiving a semantic label.

---

## Rule 4.3 — Reusability Matters

A candidate that only explains one isolated observation should not automatically be treated as a reusable concept.

---

## Rule 4.4 — Transfer Matters

Where applicable, a candidate must be tested outside the exact context from which it was constructed.

---

## Rule 4.5 — Alternative Explanations

A candidate should be compared against plausible competing explanations whenever the experiment permits this.

---

# 5. Engineering Rules

## Rule 5.1 — Architecture Follows Science

Do not introduce architectural components merely because they appear sophisticated.

Architecture must support the scientific requirements.

---

## Rule 5.2 — Minimal Necessary Complexity

Do not simplify a scientifically necessary system merely because it is difficult.

Do not introduce complexity that the experiment does not require.

---

## Rule 5.3 — Complete File Contents

When a file is created or modified during project work, provide the complete final contents of that file.

Do not provide partial replacement snippets for project files.

---

## Rule 5.4 — Tests Before Progression

Relevant tests must pass before moving to the next implementation milestone.

---

## Rule 5.5 — Git Checkpoint

Every completed sprint must produce a Git commit and push.

---

# 6. Documentation Rules

## Rule 6.1 — Documents Have Distinct Roles

Do not duplicate the same information across multiple documents without a reason.

---

## Rule 6.2 — Decisions Must Be Traceable

Major decisions should record:

- decision;
- reason;
- alternatives considered;
- consequences where relevant.

---

## Rule 6.3 — Memory Is Not a Diary

MEMORY.md records durable project knowledge, not every conversation.

---

## Rule 6.4 — Tasks Remain Traceable

Completed tasks remain recorded rather than being silently deleted.

---

# 7. Research Failure

## Rule 7.1 — Negative Results Are Valid

A failed hypothesis is a legitimate research outcome.

---

## Rule 7.2 — Kill Criteria Must Be Respected

If a predefined kill criterion is reached, do not silently ignore it.

The thesis must be revised, narrowed, or abandoned as appropriate.

---

## Rule 7.3 — Do Not Move the Goalposts

Evaluation criteria must not be changed after seeing results solely to make an unsuccessful experiment appear successful.

Any justified change must be documented.

---

# 8. External Models and APIs

## Rule 8.1 — No Proprietary Dependency for Core Discovery

The core discovery experiment must be runnable without an expensive proprietary API.

---

## Rule 8.2 — Model-Assisted Reasoning Must Be Explicit

If an LLM is eventually used for candidate generation or reasoning, its exact role must be documented.

---

## Rule 8.3 — LLM Output Is Hypothesis Material

LLM-generated concepts or explanations must be treated as candidate hypotheses rather than scientific conclusions.

---

# 9. Sprint Discipline

Each sprint must contain:

1. Objective
2. Research/engineering questions
3. Tasks
4. Files affected
5. Implementation
6. Tests
7. Evaluation
8. Evidence
9. Documentation updates
10. Git commit
11. Git push
12. Definition of Done

Do not casually jump between sprints.

---

# 10. Core Principle

> Evidence outranks intuition.

> Reproducibility outranks convenience.

> Falsification outranks confirmation.

> Scientific clarity outranks implementation volume.