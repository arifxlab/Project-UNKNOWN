# Project UNKNOWN — Research Thesis

## Status

**Research Stage:** Sprint 0 — Scientific Foundation

**Thesis Status:** Provisional

**Last Updated:** 2026-09-23

---

# 1. Research Motivation

Artificial systems commonly begin with a predefined vocabulary of variables, features, objects, states, latent dimensions, predicates, or other representational units.

They may then learn:

* relationships between variables;
* predictive models;
* causal structures;
* latent representations;
* policies;
* abstractions;
* explanations.

A deeper problem occurs when the system's current representation is itself inadequate for expressing structure that matters.

A poor prediction can have several fundamentally different causes:

1. the representation is adequate but the parameters are poorly estimated;
2. the representation is adequate but the chosen model family is inappropriate;
3. the representation itself does not contain a distinction required to express the relevant structure.

Project UNKNOWN focuses on the third case.

The project therefore investigates **representation-level inadequacy as an explicit scientific diagnosis problem**, rather than treating every model failure as an ordinary optimization or model-selection problem.

---

# 2. Primary Research Question

> Can an artificial system autonomously detect when its current representation of an environment is systematically inadequate, distinguish representation-level inadequacy from parameter and model-family failure, construct a reusable candidate representation extension, and experimentally determine whether that extension provides explanatory, predictive, interventional, falsification, and transfer value beyond the original representation?

This question is provisional.

It is intentionally narrower than the general questions of:

* concept discovery;
* representation learning;
* latent-variable discovery;
* causal representation learning;
* theory revision;
* automated scientific discovery.

Those areas already contain substantial prior work.

---

# 3. Research Boundary

The current candidate research boundary is:

> **Explicit representation-level inadequacy detection followed by failure-triggered representation extension and experimental validation of the resulting representation as a reusable abstraction.**

The project is specifically interested in the decision:

```text
Observed failure
       ↓
Parameter failure?
       ↓ no
Model-family failure?
       ↓ no
Representation-level failure?
       ↓ yes
Construct candidate representation
```

The distinction itself must be operationalized experimentally.

The project must demonstrate that the system is not simply:

* searching a larger model space;
* performing ordinary feature engineering;
* performing generic dimensionality reduction;
* clustering observations;
* discovering latent variables without a failure diagnosis;
* adding arbitrary features until prediction improves.

---

# 4. Current Prior-Art Position

The current literature review indicates substantial prior work in:

* concept discovery;
* representation learning;
* causal representation learning;
* interventional representation learning;
* causal abstraction;
* predicate invention;
* theory revision;
* neural concept invention;
* latent-variable discovery;
* automated experiment generation;
* automated scientific discovery;
* model misspecification detection.

For example, interventional causal representation learning explicitly studies recovery of high-level latent factors using intervention data.

Causal abstraction provides formal mechanisms for relating representations at different levels and evaluating them through interventions.

Neurosymbolic theory-revision work already combines theory revision with neural concept/predicate invention.

Recent model-misspecification research also explicitly treats model failure detection and iterative model updating as a scientific problem.

Therefore:

> Project UNKNOWN does **not** currently claim novelty for concept discovery, representation learning, latent-variable discovery, theory revision, intervention-based validation, or automated scientific discovery individually.

The potential research distinction remains the **integration and explicit operationalization of representation-level failure diagnosis as the trigger for representation formation**, together with a validation protocol designed to distinguish genuine reusable representations from ordinary predictive improvements.

This distinction remains unresolved.

---

# 5. Working Hypothesis

> When an environment contains reusable structure that cannot be adequately expressed by the system's current representation, a system equipped with explicit representation-failure diagnosis, candidate representation formation, hypothesis generation, intervention, falsification, and transfer evaluation can construct a reusable abstraction that provides measurable value beyond the original representation.

This is a hypothesis, not an established fact.

---

# 6. Null Hypothesis

> A system with autonomous representation formation and validation does not produce reliable additional scientific value over appropriately designed simpler baselines.

The null hypothesis will be tested against baselines capable of:

* parameter optimization;
* model-family changes;
* statistical feature discovery;
* latent representation discovery;
* predictive feature expansion.

---

# 7. Failure Taxonomy

Project UNKNOWN currently distinguishes three levels of failure.

## 7.1 Parameter Failure

The current representation and model family are adequate, but the model parameters are inadequate.

Example:

```text
Correct representation
        ↓
Correct model family
        ↓
Poor parameter estimates
```

Expected remedy:

* optimization;
* additional data;
* regularization;
* parameter estimation.

---

## 7.2 Model-Family Failure

The current representation contains the relevant information, but the chosen model family cannot express the required relationship.

Example:

```text
Adequate representation
        ↓
Inadequate model family
        ↓
Systematic prediction failure
```

Expected remedy:

* change model family;
* increase model capacity;
* change structural assumptions.

---

## 7.3 Representation Failure

The relevant distinction is not available in the current representation.

Example:

```text
Raw observations
      ↓
Current representation R
      ↓
Important distinction collapsed
      ↓
No model in the permitted family can recover it
```

Expected remedy:

* construct a representation extension;
* introduce a new candidate concept;
* revise the representational vocabulary.

The experimental challenge is to distinguish this case from the first two.

---

# 8. Working Definition of a Candidate Concept

A **candidate concept** is a newly constructed representational variable, predicate, feature, abstraction, or structured representation whose definition is generated from observations and existing representations.

A candidate is not automatically a discovery.

A candidate must have:

1. an explicit operational definition;
2. a reproducible construction procedure;
3. testable predictions;
4. identifiable conditions under which it should matter;
5. intervention semantics where applicable;
6. falsification conditions;
7. transfer tests.

---

# 9. Proposed Core Loop

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
Residual Structure
    ↓
Failure Diagnosis
    ↓
Parameter Failure?
    ├── yes → revise parameters
    ↓ no
Model-Family Failure?
    ├── yes → revise model family
    ↓ no
Representation-Level Failure?
    ├── no → continue investigation
    ↓ yes
Candidate Representation R'
    ↓
Formalize Candidate
    ↓
Generate Hypothesis
    ↓
Design Intervention / Experiment
    ↓
Observe Outcome
    ↓
Falsify / Support
    ↓
Unseen-Context Transfer
    ↓
Accept / Reject / Revise Candidate
```

---

# 10. What Would Count as Evidence?

Evidence for representation-level discovery would require more than predictive improvement.

At minimum, evidence should address:

### A. Diagnosis

The system identifies a failure pattern that cannot be adequately resolved by the permitted parameter and model-family alternatives.

### B. Construction

The system constructs a candidate representation from available evidence.

### C. Prediction

The candidate generates predictions that can be evaluated before the corresponding outcomes are observed.

### D. Intervention

The candidate makes predictions under interventions or controlled changes.

### E. Falsification

The candidate has predefined failure conditions and can be rejected.

### F. Transfer

The candidate retains useful behavior in an unseen context rather than only explaining the environment from which it was discovered.

### G. Reproducibility

Independent runs under the same protocol should produce measurable and statistically interpretable results.

---

# 11. What Does Not Count as Discovery?

The following alone do not constitute discovery:

* an LLM assigning a name to a pattern;
* a cluster appearing visually meaningful;
* a latent representation improving reconstruction;
* a feature improving prediction;
* a correlation;
* an explanation generated after observing the answer;
* post-hoc interpretation;
* memorization of the discovery environment;
* an arbitrary increase in model capacity;
* a representation that works only in one environment;
* a candidate selected only because it improves the evaluation metric.

---

# 12. Current Experimental Philosophy

The first experiments should use controlled synthetic environments.

The hidden data-generating mechanism will be known to the experiment designer but inaccessible to UNKNOWN during discovery.

The environment should contain:

* observable variables;
* hidden structure;
* multiple contexts;
* misleading correlations;
* controlled interventions;
* reusable structure;
* false candidate opportunities;
* an unseen evaluation context.

This allows the system's discovered representation to be compared against ground truth without giving the system access to that ground truth.

---

# 13. Candidate Research Contribution

The current candidate contribution is not:

> "An AI that discovers concepts."

That problem is too broad and already has extensive prior art.

The current candidate contribution is instead:

> A research framework for explicitly testing whether an artificial system can recognize representation-level inadequacy as a distinct failure mode, trigger representation extension because of that diagnosis, and validate the resulting representation through prediction, intervention, falsification, and transfer.

Whether this constitutes a genuinely novel contribution remains to be established.

---

# 14. Kill Conditions

The research direction should be reconsidered if:

1. prior art demonstrates essentially the same complete mechanism;
2. representation failure cannot be operationally distinguished from model-family failure;
3. the candidate concept cannot be formally defined;
4. improvements disappear under strong baselines;
5. candidates fail intervention tests;
6. candidates fail unseen-context transfer;
7. results cannot be reproduced;
8. the benchmark unintentionally exposes hidden ground truth;
9. the system only performs generic feature search under different terminology.

---

# 15. Current Status

**Status:** Provisional

**Research Gap:** Candidate only

**Novelty Claim:** None

**Implementation:** Not started

**Next Scientific Stage:** S0.3 — Formal Research Gap & Problem Definition

The next stage will attempt to falsify the proposed research boundary before implementation begins.
