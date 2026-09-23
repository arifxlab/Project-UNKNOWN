# Project UNKNOWN - Memory

## Purpose

This document records durable project knowledge, major decisions, constraints,
research conclusions, rejected approaches, and current milestone state.

It is not a conversation diary.

---

# Project Identity

**Name:** Project UNKNOWN

**Research Area:** Autonomous Concept Formation and Model Discovery

**Started:** 2026-09-23

**Development Mode:** Research-grade / experimental / production-quality

---

# Core Research Direction

UNKNOWN investigates whether an artificial system can explicitly detect when
its current representation is inadequate, distinguish that condition from
ordinary parameter or model-family failure, construct a candidate
representation extension, and experimentally validate the resulting
abstraction.

The current direction is:

> Representation-level inadequacy detection -> representation extension ->
> experimental validation.

---

# Current Research Question

> Can an artificial system autonomously detect when its current representation
> of an environment is systematically inadequate, distinguish
> representation-level inadequacy from parameter and model-family failure,
> construct a reusable candidate representation extension, and experimentally
> determine whether that extension provides explanatory, predictive,
> interventional, falsification, and transfer value beyond the original
> representation?

**Status:** Provisional

**Novelty status:** Not established

---

# Working Hypothesis

> When an environment contains reusable structure that cannot be adequately
> expressed by the system's current representation, a system equipped with
> explicit representation-failure diagnosis, candidate representation
> formation, hypothesis generation, intervention, falsification, and transfer
> evaluation can construct a reusable abstraction that provides measurable
> value beyond the original representation.

**Status:** Working hypothesis

---

# Null Hypothesis

> A system with autonomous representation formation and validation does not
> produce reliable additional scientific value over appropriately designed
> simpler baselines.

**Status:** Working null hypothesis

---

# Research Boundary

The current research boundary is:

> Explicit representation-level inadequacy detection followed by
> failure-triggered representation extension and experimental validation of
> the resulting representation as a reusable abstraction.

This boundary is deliberately narrower than broad questions such as:

* Can AI discover concepts?
* Can AI discover representations?
* Can AI invent latent variables?
* Can AI revise an incorrect model?
* Can AI perform automated scientific discovery?

Those broader mechanisms already have substantial prior-art coverage.

---

# Prior-Art Conclusions

The literature review established that the following are already active
research areas:

* concept discovery;
* representation learning;
* causal representation learning;
* interventional representation learning;
* causal abstraction;
* latent-variable discovery;
* predicate invention;
* theory revision;
* neural concept invention;
* automated scientific discovery;
* automated experiment generation;
* model misspecification detection.

Therefore UNKNOWN must not claim novelty for any of these mechanisms in
isolation.

The current candidate distinction is narrower:

> Treating representation-level inadequacy as an explicit failure-diagnosis
> problem, distinguishing it from parameter and model-family failure, and
> using that diagnosis to trigger representation extension followed by
> intervention, falsification, and transfer validation.

This remains a candidate research boundary rather than an established
contribution.

The final targeted equivalence search remains open.

---

# Failure Taxonomy

## Information Unavailable

The required distinction is absent from the permitted observation interface.

No representation learner operating within that interface should be expected
to recover the missing information.

---

## Representation Failure

The required information is available through the permitted observation
interface but is absent from the current representation.

The extension language must be capable of expressing the required distinction.

This is the central failure condition under investigation.

---

## Model-Family Failure

The relevant information is present in the current representation, but the
chosen model family cannot adequately exploit it.

A stronger permitted model family should be able to recover the required
behavior without changing the representation.

---

## Parameter Failure

The representation and model family are adequate, but the current parameter
values are inadequate.

Parameter optimization should be sufficient without representation
extension.

---

# Candidate Concept Principle

A candidate concept is not a discovery merely because it:

* improves prediction;
* forms a cluster;
* appears interpretable;
* receives a human-readable name;
* is generated by an LLM;
* correlates with an outcome;
* improves reconstruction.

A candidate requires predefined validation.

Minimum intended validation:

```text
Formal Definition
      |
      v
Prediction
      |
      v
Intervention
      |
      v
Falsification
      |
      v
Unseen-Context Transfer
```

Representation recovery and complexity are additional evaluation dimensions.

---

# Core Discovery Pipeline

```text
Environment
    |
    v
Observation
    |
    v
Representation R
    |
    v
Model M(R)
    |
    v
Failure / Residual Analysis
    |
    v
Failure Classification
    |
    v
Candidate Representation R'
    |
    v
Hypothesis
    |
    v
Experiment / Intervention
    |
    v
Evidence
    |
    v
Falsification or Support
    |
    v
Transfer
    |
    v
Accept / Reject / Revise
```

---

# Representation Formalization

The working environment abstraction is:

```text
E = (S, A, O, T)
```

where:

* `S` is the environment state space;
* `A` is the action space;
* `O` is the observation interface;
* `T` is the environment transition process.

A representation is treated as a transformation of available observations:

```text
r_t = R(o_<=t)
```

A representation is considered provisionally adequate when at least one model
within the predefined permitted model family can meet the evaluation
criterion.

A representation is considered provisionally inadequate when all permitted
models fail the predefined criterion while an allowed representation
extension can express information that resolves the failure.

This is a necessary operationalization, not by itself proof of scientific
discovery.

---

# Candidate Representation Principle

A representation extension is treated conceptually as:

```text
R' = R + C
```

where `C` is a candidate representation component.

A candidate must carry enough provenance to determine:

* what expression was introduced;
* which existing observations it depends upon;
* why the candidate was proposed;
* which failure triggered the proposal;
* what hypothesis it implies;
* what predictions it makes;
* what interventions should distinguish it;
* what observations would falsify it.

Arbitrary feature addition without this evidence is not sufficient for
scientific discovery.

---

# Experimental Principles

The project must:

* use controlled synthetic environments initially;
* separate hidden ground truth from the discovery system;
* include strong baselines;
* include misleading patterns;
* include false candidate opportunities;
* use interventions where scientifically appropriate;
* evaluate unseen contexts;
* preserve negative results;
* avoid post-hoc goalpost changes;
* record seeds and configurations;
* maintain reproducible experiments;
* distinguish discovery-time information from evaluator-only information.

---

# Scientific Information Boundary

The environment is divided into three conceptual layers.

## PUBLIC

Information legitimately available to UNKNOWN.

## HIDDEN

Benchmark-side truth unavailable to UNKNOWN during discovery.

## EVALUATION

Measurements and comparisons performed outside the discovery process.

UNKNOWN must not receive:

* hidden latent state;
* ground-truth representations;
* benchmark condition labels;
* evaluation labels;
* evaluation scores;
* oracle outcomes;
* future-state information;
* benchmark construction information.

---

# S0.4 Environment Foundation

S0.4 established the first executable public/hidden/evaluation boundary.

Implemented schema layers:

```text
src/unknown/environment/schemas/
    public.py
    hidden.py
    evaluation.py
```

Implemented public runtime:

```text
src/unknown/environment/public/runtime.py
```

Public runtime operations:

```text
reset(config, seed)
observe()
step(action)
intervene(intervention)
is_terminal()
episode_metadata()
```

The runtime provides the public contract boundary and delegates simulation
state to the deterministic dynamics layer.

The final scientific benchmark mechanisms remain outside the S0.4 boundary
and are being implemented incrementally through S0.5.

---

# S0.4 Runtime Boundary

The public runtime must not:

* import hidden schemas;
* import evaluation schemas;
* store hidden benchmark truth;
* store evaluation records;
* expose ground-truth accessors;
* expose oracle results;
* expose evaluation scores;
* return hidden or evaluation schema types.

Automated tests verify these constraints.

---

# S0.4 Schema Layers

## Public Schemas

Represent information legitimately available to UNKNOWN.

Examples include:

* public entities;
* public vectors;
* public relations;
* public observations;
* public actions;
* public interventions;
* public environment configuration;
* public environment metadata.

## Hidden Schemas

Represent benchmark-side truth.

Examples include:

* hidden variables;
* hidden relations;
* hidden state;
* ground-truth representation;
* benchmark condition;
* hidden episode records.

## Evaluation Schemas

Represent evaluator-side measurements.

Examples include:

* prediction evaluations;
* intervention records;
* falsification records;
* transfer records;
* representation recovery records;
* complexity records;
* complete discovery evaluations.

---

# S0.5-A Dynamics Contract

S0.5-A established the formal deterministic-world dynamics contract.

The contract defines:

* state transition semantics;
* entity state;
* position and velocity;
* physical and behavioral properties;
* relations;
* world context;
* episode state;
* reset semantics;
* determinism;
* actions;
* intervention boundary;
* transitions;
* terminal conditions;
* public observation projection boundary;
* hidden/evaluation separation;
* reproducibility;
* testing requirements.

Primary artifact:

```text
research/notes/S0.5_DYNAMICS_CONTRACT.md
```

Status:

**Completed**

---

# S0.5-B Deterministic World

S0.5-B implemented the first executable deterministic synthetic world.

Implementation:

```text
src/unknown/environment/dynamics/
    __init__.py
    models.py
    world.py
```

The current world supports:

* deterministic seeded initialization;
* deterministic entity identifiers;
* entity categories;
* bounded positions;
* deterministic velocities;
* entity masses;
* deterministic relations;
* world context;
* world state;
* NO_OP;
* MOVE validation and behavior;
* INTERACT validation boundary;
* deterministic position integration;
* position clamping;
* configured terminal horizon.

The dynamics layer remains the internal simulation source of truth.

Primary tests:

```text
tests/environment/test_deterministic_world.py
tests/environment/test_world_action_configuration.py
```

S0.5-B verification state:

```text
Full environment suite: 116 passed
Static compilation: passed
git diff --check: passed
```

Checkpoint:

```text
3fae8d8 feat: implement deterministic world dynamics
```

Scientific limitation:

S0.5-B establishes deterministic mechanics only. It does not establish
concept discovery, representation failure diagnosis, causal correctness,
intervention validity, transfer validity, or scientific benchmark results.

---

# S0.5-C Public Observation Projection

S0.5-C defines and implements the boundary through which internal world state
becomes information legitimately available to UNKNOWN.

Primary contract:

```text
research/notes/S0.5_C_OBSERVATION_CONTRACT.md
```

Implementation:

```text
src/unknown/environment/observation/
    __init__.py
    projection.py
```

Runtime integration:

```text
src/unknown/environment/public/runtime.py
```

The resulting architecture is:

```text
UNKNOWN
   |
   v
PublicEnvironmentRuntime
   |
   v
DeterministicWorld
   |
   v
WorldState
   |
   v
PublicObservationProjector
   |
   v
PublicObservation
```

## Public Observation Decisions

The public observation exposes:

* position;
* velocity;
* explicitly permitted relations;
* events;
* opaque entity identifiers;
* deterministic step index;
* deterministic simulation timestamp;
* controlled public attributes.

The projection does not automatically expose arbitrary internal state.

Internal mass remains private.

Internal semantic entity category remains private unless a future scientific
contract explicitly promotes it into the public observation interface.

Derived quantities such as:

* distance;
* relative position;
* relative velocity;
* acceleration;
* speed;
* nearest entity;
* collision probability;

are not automatically injected as primitive observations.

The observation projector is intended to be:

* deterministic;
* pure;
* isolated from hidden state;
* isolated from evaluation state;
* free of external dependencies;
* free of oracle features;
* deterministic in ordering and identifiers.

## S0.5-C Boundary Principle

> The simulator may know more than UNKNOWN. The evaluator may know more than
> UNKNOWN. Neither may silently communicate that additional knowledge through
> the public observation channel.

## S0.5-C Verification

Focused observation projection tests:

```text
25 passed
```

Leakage contract:

```text
19 passed
```

Full repository suite:

```text
147 passed
```

Runtime compilation:

```text
passed
```

Diff validation:

```text
git diff --cached --check  -> passed
git diff --check           -> passed
```

## S0.5-C Scientific Limitation

S0.5-C establishes an executable public observation boundary.

It does not establish:

* autonomous concept discovery;
* representation-failure diagnosis;
* successful representation extension;
* causal discovery;
* causal correctness;
* predictive superiority;
* intervention validity;
* falsification validity;
* transfer validity;
* benchmark-level scientific conclusions;
* novelty;
* superiority over existing methods.

---

# Required Future Environment Conditions

The eventual benchmark must distinguish:

```text
Information Unavailable
        |
        v
Representation Failure
        |
        v
Model-Family Failure
        |
        v
Parameter Failure
```

These conditions must be constructed so that evaluator-side ground truth can
determine whether the relevant information is:

1. absent from the observation interface;
2. present but absent from the current representation;
3. present in the representation but inaccessible to a restricted model
   family;
4. representable and model-accessible but poorly parameterized.

Paired counterfactual conditions are required.

---

# Baseline Principle

Later experiments must include at minimum:

* fixed representation;
* parameter optimization;
* stronger model-family search;
* conventional/statistical feature discovery;
* latent representation search;
* predictive-only feature expansion;
* always-on representation search.

The key scientific ablation is expected to compare failure-triggered
representation search against always-on representation search under matched
budgets.

---

# Leakage Principle

Ground truth may be used by the evaluator but must remain unavailable to
UNKNOWN during discovery.

Benchmark information must not leak through:

* public schema fields;
* runtime attributes;
* imports;
* type annotations;
* object serialization;
* filenames;
* directory names;
* logs;
* exception messages;
* metadata;
* random seeds;
* timing;
* episode lengths;
* observation counts;
* process arguments;
* environment variables;
* external tools;
* hidden benchmark labels.

Dynamic leakage auditing remains necessary once the final benchmark dynamics
exist.

---

# Research Integrity Decisions

The project will not:

* claim novelty before sufficient prior-art investigation;
* equate predictive improvement with concept discovery;
* equate interpretability with scientific validity;
* use hidden ground truth as an input to UNKNOWN;
* cherry-pick successful candidates;
* change evaluation criteria after seeing results;
* conceal negative experiments;
* replace scientific validation with LLM confidence;
* treat a larger model as evidence of representation discovery;
* treat arbitrary feature engineering as concept discovery.

---

# Current Milestone

**Sprint:** 0 - Scientific Foundation

**Current Stage:** S0.5-C Public Observation Projection

**S0.5-A:** Completed

**S0.5-B:** Completed

**S0.5-C:** Implemented - checkpoint ready

**Implementation:** Active

**Scientific benchmark:** Not yet complete

**Novelty claim:** None

**Research gap:** Candidate and provisional

**Current verified test suite:** 147 passed

**Next milestone:** S0.5-C evidence closure, followed by dynamic environment completion and ground-truth construction.

---

# Current Artifacts

Core documentation:

* `README.md`
* `RULES.md`
* `PRD.md`
* `DESIGN.md`
* `ARCHITECTURE.md`
* `RESEARCH_THESIS.md`
* `TASKS.md`
* `MEMORY.md`

Research artifacts:

* `research/literature/PRIOR_ART_MATRIX.md`
* `research/notes/S0.3_RESEARCH_GAP.md`
* `research/notes/S0.3_REPRESENTATION_SPEC.md`
* `research/notes/S0.3_EVALUATION_PROTOCOL.md`
* `research/notes/S0.4_SYNTHETIC_ENVIRONMENT.md`
* `research/notes/S0.4_ENVIRONMENT_SCHEMA.md`
* `research/notes/S0.4_LEAKAGE_AUDIT.md`
* `research/notes/S0.4_EVIDENCE.md`
* `research/notes/S0.5_DYNAMICS_CONTRACT.md`
* `research/notes/S0.5_B_EVIDENCE.md`
* `research/notes/S0.5_C_OBSERVATION_CONTRACT.md`

Implementation artifacts:

* `src/unknown/environment/schemas/public.py`
* `src/unknown/environment/schemas/hidden.py`
* `src/unknown/environment/schemas/evaluation.py`
* `src/unknown/environment/public/runtime.py`
* `src/unknown/environment/dynamics/models.py`
* `src/unknown/environment/dynamics/world.py`
* `src/unknown/environment/observation/projection.py`

Test artifacts:

* `tests/environment/test_public_schemas.py`
* `tests/environment/test_hidden_schemas.py`
* `tests/environment/test_evaluation_schemas.py`
* `tests/environment/test_boundary_contract.py`
* `tests/environment/test_public_runtime.py`
* `tests/environment/test_leakage_contract.py`
* `tests/environment/test_deterministic_world.py`
* `tests/environment/test_world_action_configuration.py`
* `tests/environment/test_public_observation_projection.py`
* `tests/environment/test_observation_boundary.py`
* `tests/environment/test_observation_determinism.py`

---

# Immediate Next Questions

Before the final synthetic benchmark is implemented, the project must
determine:

1. What is the smallest dynamic environment that exposes representation
   failure without making the hidden structure trivial?
2. How should hidden mechanisms generate observable behavior?
3. Which observable variables should be available?
4. Which relations should be observable versus latent?
5. How should information-unavailable conditions be paired with
   representation-failure conditions?
6. How should model-family and parameter controls be constructed fairly?
7. How should genuine reusable concepts be distinguished from decoys?
8. What intervention budget is scientifically sufficient?
9. What transfer contexts prevent memorization?
10. What benchmark construction choices could create leakage?
11. What baseline budgets are fair?
12. What result would falsify the central hypothesis?
13. Which intervention transition semantics should be implemented without
    creating a second source of truth?
14. Which hidden mechanisms should be implemented before benchmark conditions
    are introduced?

---

# Durable Decisions

1. No unsupported novelty claim is permitted.
2. Representation failure must be distinguished from information unavailable,
   model-family failure, and parameter failure.
3. Hidden ground truth must remain evaluator-only during discovery.
4. Representation extensions must carry provenance and testable hypotheses.
5. Prediction alone cannot establish concept discovery.
6. Intervention, falsification, and unseen-context transfer are required parts
   of the intended validation protocol.
7. False candidates and negative results are scientifically necessary.
8. The environment must support paired counterfactual controls.
9. The public runtime must remain isolated from hidden and evaluation schemas.
10. The deterministic world is the internal simulation source of truth.
11. Public observations must be produced through an explicit projection
    boundary.
12. Public observation projection must not automatically expose arbitrary
    internal fields.
13. Internal mass and semantic category are private under the current
    observation contract.
14. Derived quantities are not primitive observations unless explicitly
    promoted by a future contract.
15. Observation identifiers, ordering, and timestamps must be deterministic
    and independent of hidden benchmark semantics.
16. The current observation projector is not a scientific discovery mechanism.
17. Dynamic leakage auditing must occur after benchmark dynamics exist.
18. Sprint 0 cannot close until its full Definition of Done is satisfied.
19. No later sprint should bypass unresolved scientific kill criteria.
20. No intervention transition mechanism should be duplicated outside the
    dynamics source of truth.

---

# Previous Durable Decision

No implementation should begin until the research problem survives the S0.3
adversarial gap and formalization process.

That condition has now been satisfied sufficiently to begin controlled
environment implementation, but it does not constitute proof of novelty or
proof of the research hypothesis.

---

# Current Status

**Research question:** Provisional

**Research gap:** Candidate

**Novelty claim:** None

**S0.2 prior-art status:** Near completion

**S0.3 formalization:** Completed provisionally

**S0.4 environment boundary:** Implemented and verified

**S0.5-A dynamics contract:** Completed

**S0.5-B deterministic world:** Implemented and verified

**S0.5-C observation projection:** Implemented and verified

**Synthetic benchmark dynamics:** Partially implemented; scientific benchmark
mechanisms remain incomplete

**Autonomous discovery system:** Not yet implemented

**Current checkpoint:** S0.5-C documentation/evidence closure

**Next implementation stage:** S0.5-D dynamic environment completion and
ground-truth construction
