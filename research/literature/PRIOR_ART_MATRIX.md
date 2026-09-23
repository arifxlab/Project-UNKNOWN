# Project UNKNOWN

## Prior-Art Matrix

**Project:** Project UNKNOWN — Autonomous Concept Formation & Model Discovery
**Research Phase:** Sprint 0 — Scientific Foundation
**Stage:** S0.2 — Prior-Art Investigation
**Artifact:** Prior-Art Matrix
**Status:** Working research record
**Last Updated:** September 23, 2026

---

## 1. Purpose

This document records the prior-art investigation for Project UNKNOWN.

Its purpose is to:

1. identify existing research that overlaps with the project's proposed research question;
2. prevent unsupported novelty claims;
3. distinguish capabilities that are already established from capabilities that remain unresolved;
4. identify the closest baselines and methodological predecessors;
5. define the boundary that Project UNKNOWN must satisfy if the research direction is retained;
6. provide traceable evidence for later thesis, benchmark, architecture, and evaluation decisions.

This document is a research artifact rather than a claim that Project UNKNOWN is novel.

The absence of a discovered paper or system in this matrix must **not** be interpreted as proof that no such work exists.

---

# 2. Current Research Question

The current working research question is:

> Can an artificial system autonomously detect that its current representation of an unfamiliar environment is systematically inadequate, distinguish this representation-level inadequacy from ordinary model failure, construct a reusable candidate representation, and experimentally determine whether that representation provides explanatory, predictive, interventional, and transfer value beyond the original representation?

This wording is provisional.

It may change after the prior-art investigation and formal problem definition are complete.

---

# 3. Current Research Boundary

The investigation has shown that the following broad capabilities already have substantial precedent:

* representation learning;
* latent-variable discovery;
* concept discovery;
* concept discovery without predefined concepts;
* predicate invention;
* theory revision;
* model revision;
* causal representation learning;
* intervention-based representation learning;
* missing-variable hypothesis generation;
* automated hypothesis generation;
* autonomous experimentation;
* scientific discovery agents;
* model-misspecification detection.

Therefore Project UNKNOWN must **not** claim novelty based on any of those capabilities individually.

The current candidate research boundary is narrower:

> **Representation-level inadequacy detection as an explicit scientific decision problem, followed by autonomous representation extension and experimental validation of the resulting representation as a reusable abstraction.**

This remains a research hypothesis rather than an established novelty claim.

---

# 4. Important Terminology

## 4.1 Current Representation

The representation currently available to the system for describing observations, states, or environment variables.

Denote it by:

$$
R
$$

The representation may contain directly observed variables, engineered features, learned variables, or previously discovered concepts depending on the experimental condition.

---

## 4.2 Model Failure

A failure occurring when a model operating over an adequate representation does not adequately capture the target structure.

Conceptually:

$$
R\ \text{adequate},\quad M\ \text{inadequate}
$$

Possible responses include parameter optimization, model selection, or model-structure revision.

---

## 4.3 Representation-Level Failure

A candidate failure condition in which the available representation does not contain sufficient structure for reasonable models over that representation to capture the relevant reusable phenomenon.

Conceptually:

$$
R\ \text{inadequate}
$$

This distinction is central to Project UNKNOWN but is **not yet operationally finalized**.

---

## 4.4 Candidate Concept

A newly constructed representation that is proposed as an extension to the current representational vocabulary.

A candidate concept is not accepted merely because it improves predictive performance.

It must generate testable consequences and be subjected to validation and falsification.

---

## 4.5 Reusable Concept

A candidate representation that continues to provide meaningful explanatory, predictive, interventional, or structural value outside the exact observations from which it was discovered.

Transfer to an unseen context is therefore an important component of the proposed evaluation.

---

# 5. Prior-Art Categories

---

## 5.1 Representation Shift

### Relevance

Representation shift research predates Project UNKNOWN and establishes that changing the representational space can be necessary when the current hypothesis space is inadequate.

### Representative work

Dietterich and Michalski, work on representation shift and machine learning.

### Established capability

Prior work explicitly considers changing the representation or hypothesis space when the current representation is insufficient.

### UNKNOWN overlap

* representation inadequacy;
* representation change;
* search for a more suitable representation.

### Important distinction

Project UNKNOWN is not proposing representation change itself as a novel mechanism.

The unresolved question is whether an artificial system can explicitly diagnose the problem at the representation level and make that diagnosis the trigger for autonomous concept formation.

### Assessment

**Overlap:** High
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Historical and methodological predecessor

---

# 5.2 Predicate Invention

### Representative work

Dumancic, Meert, and Blockeel, *Theory Reconstruction: A Representation Learning View on Predicate Invention* (2016).

### Established capability

Predicate invention extends an existing vocabulary by discovering new concepts or relations.

The work connects predicate invention with representation learning and theory reconstruction.

### UNKNOWN overlap

* vocabulary extension;
* concept invention;
* reusable discovered predicates;
* representation reconstruction.

### Important distinction

Predicate invention establishes that an artificial system can construct new symbolic concepts.

Project UNKNOWN instead focuses on whether the system can first establish that its current representational vocabulary is inadequate and then use that diagnosis to motivate the representational extension.

### Assessment

**Overlap:** Very high
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Major conceptual predecessor and baseline family

---

# 5.3 Theory Revision

### Representative work

Morel and Cropper, Hempel and related theory-revision research.

### Established capability

Existing systems can:

* detect hypothesis failures;
* identify portions of hypotheses associated with failure;
* constrain or modify the hypothesis space;
* search for revised explanations.

### UNKNOWN overlap

* failure-driven revision;
* hypothesis testing;
* falsification;
* iterative improvement.

### Important distinction

Theory-revision systems generally operate inside an existing formal representation or hypothesis language.

The central UNKNOWN question is whether the system can determine that the **representation language itself** is inadequate rather than merely revising a hypothesis expressed within that language.

### Assessment

**Overlap:** High
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Critical baseline and methodological predecessor

---

# 5.4 Neural Theory Revision and Predicate Invention

### Representative work

Recent neurosymbolic theory-revision systems such as NeTheR and ThReNPI.

### Established capability

These systems combine theory revision with learned neural predicates/concepts and can revise imperfect theories using newly introduced representational components.

### UNKNOWN overlap

* imperfect initial theory;
* iterative revision;
* learned concepts;
* predicate invention;
* performance-based selection of revisions.

### Important distinction

These approaches operate within defined neurosymbolic theory structures.

The unresolved UNKNOWN question is more general:

> Can a system operating in an unfamiliar environment diagnose that its current representation itself lacks a reusable distinction and independently construct that distinction?

### Assessment

**Overlap:** Very high
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Direct technical baseline

---

# 5.5 Causal Representation Learning

### Representative work

Schölkopf et al., *Toward Causal Representation Learning* (2021).

### Established capability

Causal representation learning studies how high-level causal variables can be recovered or learned from lower-level observations.

Subsequent work investigates identifiability and interventional approaches to causal representation learning.

### UNKNOWN overlap

* low-level observations;
* higher-level variables;
* representation discovery;
* causal structure;
* interventions;
* generalization.

### Important distinction

Causal representation learning commonly specifies the objective as recovery or identification of causal latent variables.

Project UNKNOWN does not assume that the missing representation is necessarily causal.

Its proposed question is whether the system can first diagnose representation inadequacy and then determine what new representation is scientifically useful.

### Assessment

**Overlap:** Very high
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Major neighboring research field and baseline family

---

# 5.6 Concept Bottleneck Models Without Predefined Concepts

### Representative work

Schrodi et al., *Concept Bottleneck Models Without Predefined Concepts* (2024; subsequently published in TMLR).

### Established capability

Concepts can be discovered without requiring a predefined human concept vocabulary.

### UNKNOWN overlap

* concepts not supplied in advance;
* discovered representations;
* downstream predictive usefulness;
* model interpretation.

### Important distinction

The objective is primarily interpretable concept-based prediction.

Project UNKNOWN instead investigates representation adequacy, scientific hypothesis formation, intervention, falsification, and transfer.

### Assessment

**Overlap:** High
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Essential concept-discovery baseline

---

# 5.7 Missing Causal Variable Hypothesis Generation

### Representative work

Sheth, Abdelnabi, and Fritz, *Hypothesizing Missing Causal Variables with LLMs* (2024).

### Established capability

AI systems can hypothesize variables missing from a partial causal representation.

### UNKNOWN overlap

* missing-variable reasoning;
* candidate concept/variable generation;
* hypothesis formation.

### Important distinction

The task provides a partial causal graph in which missing variables are part of the problem formulation.

Project UNKNOWN proposes that the system should not be explicitly told that a representation slot is missing.

The proposed challenge is to detect the inadequacy from observations and experimental failures.

### Assessment

**Overlap:** High
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Important adversarial baseline

---

# 5.8 Automated Scientific Discovery

### Representative work

AI Scientist and AI Scientist-v2.

### Established capability

These systems automate parts of the scientific workflow including:

* idea generation;
* hypothesis generation;
* code generation;
* experiment execution;
* analysis;
* iterative scientific investigation.

### UNKNOWN overlap

* autonomous hypothesis formation;
* automated experiments;
* iterative validation;
* scientific workflow automation.

### Important distinction

Automated scientific discovery systems primarily automate the **research workflow**.

Project UNKNOWN focuses on the narrower scientific problem of representation adequacy and concept formation.

An automated scientist may generate an experiment involving a representation, but that does not by itself establish a mechanism for diagnosing representation-level failure.

### Assessment

**Overlap:** Moderate to high at the systems level
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Systems-level neighboring technology

---

# 5.9 AutoSciLab and Closed-Loop Scientific Discovery

### Representative work

AutoSciLab and related autonomous scientific discovery systems.

### Established capability

These systems combine elements such as:

* experiment generation;
* hypothesis-driven experiment selection;
* latent-variable discovery;
* interpretable equation discovery;
* active experimentation;
* scientific validation.

### UNKNOWN overlap

This is one of the closest systems-level overlaps.

Both approaches potentially contain:

$$
\text{observation}
\rightarrow
\text{hypothesis}
\rightarrow
\text{experiment}
\rightarrow
\text{discovery}
$$

### Important distinction

UNKNOWN proposes making **representation adequacy** itself an explicit decision problem.

The system should distinguish:

$$
\text{wrong parameters}
$$

from:

$$
\text{wrong model structure}
$$

from:

$$
\text{insufficient representation}
$$

### Assessment

**Overlap:** Very high at the experimental-system level
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Critical systems-level comparator

---

# 5.10 Model Misspecification Detection

### Representative work

Recent work on model misspecification and "unknown unknowns" in machine learning for physics.

### Established capability

Modern research explicitly studies:

* unexpected model failures;
* diagnostic methods;
* misspecification;
* iterative model updating;
* robustness across model classes.

### UNKNOWN overlap

* systematic failure;
* diagnostics;
* model inadequacy;
* iterative revision.

### Important distinction

Model misspecification does not automatically imply representation inadequacy.

A model can fail even when the representation is sufficient.

Therefore UNKNOWN must demonstrate that its representation-level diagnosis cannot be reduced to ordinary model-misspecification detection.

### Assessment

**Overlap:** Very high diagnostically
**Novelty claim from this category:** Not justified
**Role in UNKNOWN:** Essential methodological comparator

---

# 6. Capability Matrix

| Capability                                                                                            |                  Prior Art | UNKNOWN Status                 |
| ----------------------------------------------------------------------------------------------------- | -------------------------: | ------------------------------ |
| Representation learning                                                                               |                Established | Not novel                      |
| Representation shift                                                                                  |                Established | Not novel                      |
| Latent-variable discovery                                                                             |                Established | Not novel                      |
| Concept discovery                                                                                     |                Established | Not novel                      |
| Concept discovery without predefined concepts                                                         |                Established | Not novel                      |
| Predicate invention                                                                                   |                Established | Not novel                      |
| Theory revision                                                                                       |                Established | Not novel                      |
| Failure-driven hypothesis revision                                                                    |                Established | Not novel                      |
| Causal representation learning                                                                        |                Established | Not novel                      |
| Interventional representation learning                                                                |                Established | Not novel                      |
| Missing-variable hypothesis generation                                                                |                Established | Not novel                      |
| Autonomous hypothesis generation                                                                      |                Established | Not novel                      |
| Autonomous experiment selection                                                                       |                Established | Not novel                      |
| Closed-loop scientific discovery                                                                      |                Established | Not novel                      |
| Model misspecification detection                                                                      |                Established | Not novel                      |
| Representation-level adequacy diagnosis                                                               | Requires deeper comparison | **Open research question**     |
| Explicit distinction between model failure and representation failure                                 |     Requires formalization | **Open research question**     |
| Failure-triggered autonomous representation extension                                                 | Requires deeper comparison | **Open research question**     |
| Reusable concept validation across unseen contexts                                                    |      Existing related work | **Must be compared carefully** |
| Integrated prediction + intervention + falsification + transfer protocol for representation extension | Requires deeper comparison | **Open research question**     |

---

# 7. Proposed Representation-Failure Distinction

A central hypothesis emerging from the prior-art review is that three failure levels should be experimentally separated.

## Level 1 — Parameter Failure

The representation and model family are adequate, but the model parameters are poorly estimated.

$$
R\text{ adequate}
$$

$$
M\text{ family adequate}
$$

$$
\theta\text{ inadequate}
$$

Possible response:

$$
\text{parameter optimization}
$$

---

## Level 2 — Model-Structure Failure

The representation is adequate, but the selected model family cannot express the required relationship.

$$
R\text{ adequate}
$$

$$
M\text{ family inadequate}
$$

Possible response:

$$
\text{model revision}
$$

---

## Level 3 — Representation Failure

The current representation lacks a distinction required to express the relevant reusable structure.

$$
R\text{ inadequate}
$$

Possible response:

$$
R\rightarrow R'
$$

followed by construction or selection of an appropriate model over \(R'\).

---

# 8. Candidate Operational Criterion

The following is a **candidate**, not a finalized definition.

For current representation \(R\), let:

$$
\mathcal{M}_R
$$

be a predefined family of reasonable models operating over \(R\).

Define representation-level adequacy as something related to:

$$
A(R,D)=
\max_{M\in\mathcal{M}_R}
Score(M,D)
$$

Persistent failure of one model is therefore insufficient evidence.

A stronger representation-failure signal would require evidence that:

1. multiple reasonable models over \(R\) fail;
2. failure has reproducible structure;
3. failure persists across relevant contexts;
4. increased model capacity alone does not resolve the structure;
5. a candidate representation \(R'\) removes or substantially reduces the structured failure;
6. \(R'\) produces independently testable consequences;
7. the candidate survives intervention and falsification tests;
8. the candidate retains useful structure in an unseen context.

This criterion is intentionally conservative.

---

# 9. Candidate UNKNOWN Research Loop

The current candidate loop is:

```text
Environment
    ↓
Observations
    ↓
Current Representation R
    ↓
Model Family M(R)
    ↓
Prediction / Explanation
    ↓
Systematic Residual Structure
    ↓
Representation Adequacy Analysis
    │
    ├── parameter failure
    │
    ├── model-structure failure
    │
    └── candidate representation failure
            ↓
       Concept Generation
            ↓
       Candidate R'
            ↓
       Hypothesis Formation
            ↓
       Intervention / Experiment
            ↓
       Falsification
            ↓
       Unseen-Context Transfer
            ↓
       Accept / Reject / Revise
```

This loop is provisional.

It must be validated against the literature and experimentally operationalized.

---

# 10. What Project UNKNOWN Must Not Claim

Project UNKNOWN must not claim that it is the first system to:

* discover concepts;
* discover latent variables;
* change representations;
* invent predicates;
* revise theories;
* detect model failure;
* perform scientific experiments autonomously;
* generate hypotheses;
* use interventions;
* validate causal representations;
* perform transfer learning;
* conduct automated scientific discovery.

These capabilities have substantial prior art.

---

# 11. Current Candidate Research Contribution

The current candidate contribution is narrower:

> Develop and experimentally test a framework in which representation-level inadequacy is treated as an explicit decision problem, distinguishable from parameter and model-structure failure, and use that diagnosis to trigger autonomous candidate representation formation followed by controlled prediction, intervention, falsification, and unseen-context evaluation.

This statement is **not a novelty claim**.

It is the current research hypothesis that must survive:

1. additional literature review;
2. formalization;
3. baseline construction;
4. synthetic benchmark design;
5. controlled experiments.

---

# 12. Required Baselines

The prior-art review implies that UNKNOWN must eventually compare against at least:

### Baseline A — Fixed Representation

No representation expansion.

Tests whether the original representation is already sufficient.

### Baseline B — Model-Class Search

Allows stronger model families without changing the representation.

Tests whether apparent representation failure is actually model failure.

### Baseline C — Feature Discovery

Allows statistical/learned feature discovery without explicit representation-failure diagnosis.

### Baseline D — Latent Representation Learning

Allows latent representation discovery without UNKNOWN's explicit adequacy diagnosis.

### Baseline E — Concept Discovery

Allows concept discovery without the complete validation protocol.

### Baseline F — Active Experimentation

Allows intervention/experiment selection but does not explicitly diagnose representation inadequacy.

### Baseline G — UNKNOWN

Includes:

* representation adequacy diagnosis;
* candidate concept formation;
* hypothesis generation;
* intervention;
* falsification;
* transfer validation.

Exact implementations are not yet finalized.

---

# 13. Evidence Required Before Claiming a Research Gap

Before Project UNKNOWN describes its contribution as novel, the project must establish:

* sufficiently broad literature coverage;
* comparison against the closest systems;
* explicit differences in problem formulation;
* explicit differences in autonomy;
* explicit differences in representation assumptions;
* explicit differences in validation protocol;
* benchmark-level differentiation;
* reproducible experimental evidence.

A gap should never be inferred solely because no identical title or architecture was found.

---

# 14. Open Questions

The following questions remain unresolved:

1. Has prior work explicitly formalized representation inadequacy as a separate decision problem from model misspecification?
2. Has a system autonomously diagnosed representation failure without being told that a missing variable/concept exists?
3. Has such a diagnosis directly triggered concept/representation formation?
4. Has the resulting representation been evaluated through a combined prediction/intervention/falsification/transfer protocol?
5. Are there existing systems that already implement substantially the same complete loop under another terminology?
6. Can representation failure be operationalized without defining the desired hidden representation in advance?
7. Can false candidate concepts be reliably rejected?
8. Can the resulting concept transfer to an unseen environment rather than merely improving performance on the discovery environment?

These questions must be investigated before the research gap is frozen.

---

# 15. Current Conclusion

The first two prior-art investigation passes substantially narrow the research space.

The broad Project UNKNOWN idea is **not sufficient as a novel research claim**.

The following components are individually established:

$$
\text{representation learning}
$$

$$
\text{concept discovery}
$$

$$
\text{predicate invention}
$$

$$
\text{theory revision}
$$

$$
\text{causal representation learning}
$$

$$
\text{interventional discovery}
$$

$$
\text{hypothesis generation}
$$

$$
\text{autonomous experimentation}
$$

$$
\text{model misspecification detection}
$$

The remaining candidate research boundary is:

$$
\boxed{
\text{representation-level inadequacy detection}
\rightarrow
\text{autonomous representation extension}
\rightarrow
\text{experimental validation}
}
$$

with explicit distinction from ordinary model failure.

This boundary is **not yet established as novel**.

The next research stage must test it against the closest literature and formalize the distinction sufficiently to make it experimentally falsifiable.

---

# 16. Primary References

The following references form the initial evidence base for this matrix.

1. Schölkopf et al. — *Toward Causal Representation Learning* (2021).
   https://arxiv.org/abs/2102.11107

2. Ahuja et al. — *Interventional Causal Representation Learning* (2023).
   https://proceedings.mlr.press/v202/ahuja23a.html

3. Dumancic, Meert, Blockeel — *Theory Reconstruction: A Representation Learning View on Predicate Invention* (2016).
   https://arxiv.org/abs/1606.08660

4. Schrodi et al. — *Concept Bottleneck Models Without Predefined Concepts* (2024).
   https://arxiv.org/abs/2407.03921

5. Sheth, Abdelnabi, Fritz — *Hypothesizing Missing Causal Variables with LLMs* (2024).
   https://arxiv.org/abs/2409.02604

6. Morel and Cropper — work on failure-aware theory revision and Hempel (2023).

7. AI Scientist — *Towards Fully Automated Open-Ended Scientific Discovery* (2024).
   https://arxiv.org/abs/2408.06292

8. AI Scientist-v2 — iterative agentic scientific discovery (2025).
   https://arxiv.org/abs/2504.08066

9. AutoSciLab — autonomous scientific discovery through active experimentation and latent-variable/equation discovery.
   https://ojs.aaai.org/index.php/AAAI/article/view/31990

10. *Unknown Unknowns: Model Misspecification in Machine Learning for Physics* (2026).
    https://arxiv.org/abs/2608.13633

---

## 17. Research Integrity Note

This matrix intentionally distinguishes:

* **established prior art**;
* **observed overlap**;
* **candidate distinctions**;
* **unresolved research questions**.

No novelty conclusion is drawn from the current matrix.

A future claim of novelty must be based on a substantially broader and more systematic literature review together with an experimentally precise problem definition.
