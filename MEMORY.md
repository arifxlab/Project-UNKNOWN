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

```
E = (S, A, O, T)
```

where:

* S is the environment state space;
* A is the action space;
* O is the observation interface;
* T is the environment transition process.

A representation is treated as a transformation of available observations:

```
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

```
R' = R + C
```

where C is a candidate representation component.

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

```
src/unknown/environment/schemas/
    public.py
    hidden.py
    evaluation.py
```

Implemented public runtime:

```
src/unknown/environment/public/runtime.py
```

Public runtime operations:

```
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

## S0.4 Runtime Boundary

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

## S0.4 Schema Layers

### Public Schemas

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

### Hidden Schemas

Represent benchmark-side truth.

Examples include:

* hidden variables;
* hidden relations;
* hidden state;
* ground-truth representation;
* benchmark condition;
* hidden episode records.

### Evaluation Schemas

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

```
research/notes/S0.5_DYNAMICS_CONTRACT.md
```

Status: **Completed**

---

# S0.5-B Deterministic World

S0.5-B implemented the first executable deterministic synthetic world.

Implementation:

```
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

```
tests/environment/test_deterministic_world.py
tests/environment/test_world_action_configuration.py
```

S0.5-B verification state:

```
Full environment suite: 116 passed
Static compilation: passed
git diff --check: passed
```

Checkpoint:

```
3fae8d8 feat: implement deterministic world dynamics
```

**Scientific limitation:**

S0.5-B establishes deterministic mechanics only. It does not establish
concept discovery, representation failure diagnosis, causal correctness,
intervention validity, transfer validity, or scientific benchmark results.

---

# S0.5-C Public Observation Projection

S0.5-C defines and implements the boundary through which internal world state
becomes information legitimately available to UNKNOWN.

Primary contract:

```
research/notes/S0.5_C_OBSERVATION_CONTRACT.md
```

Implementation:

```
src/unknown/environment/observation/
    __init__.py
    projection.py
```

Runtime integration:

```
src/unknown/environment/public/runtime.py
```

The resulting architecture is:

```
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

The simulator may know more than UNKNOWN. The evaluator may know more than
UNKNOWN. Neither may silently communicate that additional knowledge through
the public observation channel.

## S0.5-C Verification

Focused observation projection tests:

```
25 passed
```

Leakage contract:

```
19 passed
```

Full repository suite:

```
147 passed
```

Runtime compilation:

```
passed
```

Diff validation:

```
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

# S0.5-D Dynamic Environment Completion

S0.5-D treats the dynamic environment as experimental infrastructure rather
than as a demonstration environment.

## Scientific purpose

The environment must support controlled experimental distinction among:

* Information Unavailable;
* Representation Failure;
* Model-Family Failure;
* Parameter Failure;
* unnecessary or decoy candidate explanations.

The environment must not assume that a prediction failure implies
representation failure.

---

## S0.5-D.1 Dynamic Environment Contract

S0.5-D.1 established the formal contract for dynamic environment completion.

The contract defines:

* authoritative dynamic transition semantics;
* action semantics;
* intervention semantics;
* deterministic temporal semantics;
* information-unavailable conditions;
* representation-failure conditions;
* model-family controls;
* parameter-failure controls;
* decoy conditions;
* paired-counterfactual requirements;
* hidden/evaluation separation;
* leakage requirements;
* reproducibility requirements;
* scientific and engineering acceptance criteria.

Primary artifact:

```
research/notes/S0.5_D_DYNAMIC_ENVIRONMENT_CONTRACT.md
```

Status: **Completed**

---

## S0.5-D.2 Dynamic Transition Hardening

S0.5-D.2 hardened the deterministic world before intervention and benchmark
logic were introduced.

### Scientific role

The purpose was to establish that the existing transition system is suitable
as controlled experimental infrastructure.

The authoritative ordinary transition remains:

```
S_{t+1} = T(S_t, A_t)
```

No new physical mechanism was introduced during hardening.

### Durable implementation decisions

The transition path follows:

```
validate input
    |
    v
compute next state
    |
    v
commit state
    |
    v
evaluate terminal status
```

Validation occurs before state mutation.

Invalid actions therefore cannot partially mutate the world.

MOVE vectors must contain finite numeric values.

Configuration fields requiring integer semantics explicitly reject booleans
rather than relying on Python's bool subclass relationship with int.

The deterministic world continues to use the established kinematic baseline:

```
p_{t+1} = p_t + v_t * Δt
```

D.2 deliberately does not introduce:

* intervention dynamics;
* collision physics;
* friction;
* acceleration mechanisms;
* hidden benchmark variables;
* benchmark condition labels;
* evaluator logic;
* concept discovery.

### Verified invariants

D.2 tests verify:

* deterministic multi-step replay;
* invalid-action non-mutation;
* finite action-vector requirements;
* entity identity preservation;
* mass preservation;
* position-bound preservation;
* immutable world state;
* immutable entity state;
* immutable entity collections;
* immutable relation collections;
* NO_OP velocity preservation;
* MOVE target-velocity semantics;
* relation stability during ordinary actions;
* terminal-state/reset behavior.

### Verification checkpoint

Full repository test suite:

```
163 passed
```

Python compilation:

```
passed
```

Git whitespace/error validation:

```
git diff --check -> passed
```

### D.2 artifacts

```
src/unknown/environment/dynamics/world.py
tests/environment/test_world_trajectory_hardening.py
tests/environment/test_world_invariants.py
research/notes/S0.5_D2_EVIDENCE.md
```

### Scientific limitation

D.2 establishes engineering and reproducibility properties of the current
transition substrate.

It does not establish:

* intervention validity;
* causal validity;
* representation-failure diagnosis;
* concept discovery;
* transfer success;
* scientific superiority;
* benchmark validity;
* novelty.

---

## S0.5-D.3 Authoritative Intervention Transition

S0.5-D.3 established interventions as an authoritative deterministic
transition mechanism in the dynamics source of truth.

### Scientific role

The objective was to provide controlled world-state modification for later
experiments without creating a second transition engine inside the public
runtime.

The resulting architecture is:

```
Public Intervention
        |
        v
Public Runtime Validation
        |
        v
DeterministicWorld.intervene(...)
        |
        v
Authoritative World Transition
        |
        v
Public Observation Projection
```

The dynamics layer remains the single source of truth.

### Intervention semantics

#### SET_POSITION

SET_POSITION directly replaces the selected entity position.

Properties:

* target entity must exist;
* vector is required;
* vector components must be finite;
* requested position must be within world bounds;
* velocity is preserved;
* no ordinary kinematic timestep is applied;
* step index advances by one.

Out-of-bounds positions are rejected rather than silently clamped.

#### SET_VELOCITY

SET_VELOCITY directly replaces the selected entity velocity.

Properties:

* target entity must exist;
* vector is required;
* vector components must be finite;
* position is preserved;
* no ordinary kinematic timestep is applied;
* step index advances by one.

#### REMOVE_ENTITY

REMOVE_ENTITY removes the selected entity.

Properties:

* target entity must exist;
* selected entity is removed;
* all incident relations are removed;
* surviving entities are not reconnected automatically;
* step index advances by one.

### Reproducibility

Intervention history is represented internally as part of the world state so
that controlled intervention sequences form part of reproducible simulation
state.

Intervention history is not exposed through the public observation.

### Validation

Interventions follow validation-before-mutation semantics.

Invalid intervention inputs do not partially mutate world state.

### Terminal behavior

Interventions use the normal world lifecycle.

Each intervention advances the step index by one. If the configured horizon is
reached, the world becomes terminal according to the existing terminal rule.

No separate intervention-specific terminal mechanism was introduced.

### Determinism

Identical configuration, seed, initial state, action sequence, and
intervention sequence must produce identical trajectories.

No evaluator state, hidden benchmark labels, or expected outcomes are used
by the intervention transition mechanism.

### Invariants

The implementation verifies preservation of relevant state invariants:

* entity identity;
* entity mass;
* entity category;
* position bounds;
* velocity/position preservation according to intervention type;
* relation preservation for non-removal interventions;
* incident-relation removal for REMOVE_ENTITY;
* immutability of state structures.

### Verification

Final implementation verification:

```
Full repository suite: 178 passed
Python compilation: passed
git diff --check: passed
```

Git implementation checkpoint:

```
af21961 feat: implement authoritative intervention transitions
```

Remote:

```
origin/main
```

The implementation checkpoint was pushed successfully.

### Evidence

Primary evidence artifact:

```
research/notes/S0.5_D3_EVIDENCE.md
```

### Scientific limitation

D.3 establishes intervention infrastructure.

It does not establish:

* autonomous concept discovery;
* representation-failure diagnosis;
* causal discovery;
* causal validity;
* predictive superiority;
* falsification success;
* transfer success;
* benchmark validity;
* novelty;
* scientific superiority.

The intervention mechanism is infrastructure for those later experiments.

---

## S0.5-D.4 Controlled Benchmark Contract

S0.5-D.4 defines the controlled scientific benchmark required to distinguish
representation-level inadequacy from parameter failure, model-family failure,
stochastic variation, and insufficient evidence.

### Scientific condition taxonomy

The benchmark distinguishes:

* R0 - Representation-Sufficient Control;
* P1 - Parameter Failure;
* M1 - Model-Family Failure;
* R1 - Representation-Level Inadequacy;
* N1 - Non-Identifiable / Insufficient-Evidence;
* X1 - Noise / Stochastic Variation;
* T1 - Unseen-Context Transfer.

R1 is structurally defined. Performance improvement is evidence for an R1
diagnosis, not the definition of R1 itself.

### Required controls

The benchmark contract establishes:

* public/private information separation;
* intervention semantics;
* reproducibility and seed hierarchy;
* train/development/evaluation separation;
* anti-leakage controls;
* evaluator isolation;
* model-recovery ladder;
* candidate provenance;
* structural novelty requirements;
* extension complexity and parsimony controls;
* falsification;
* uncertainty;
* explicit experimental stopping budgets;
* benchmark freezing/versioning.

### Scientific evidence dimensions

Candidate extensions are evaluated separately for:

* predictive evidence;
* interventional evidence;
* falsification evidence;
* transfer evidence;
* representation-recovery evidence;
* complexity.

No single aggregate score is treated as sufficient evidence.

### Scientific boundary

D.4 establishes a research specification.

It does not establish that an executable benchmark has already demonstrated
representation discovery or scientific validity.

### Status

Completed — research specification only.

Primary conceptual artifacts include the D.4 controlled benchmark contract,
evidence record, scientific review, and supporting benchmark design notes.

---

## S0.5-D.5.1 Baseline Representation Contract

D.5.1 establishes the baseline representation R₀ as a finite, typed,
explicitly declared representation language rather than unrestricted
computation over raw observations.

The formal structure is:

```
R₀ = (V₀, T₀, O₀, C₀)
```

where:

* V₀ is the primitive vocabulary;
* T₀ is the type system;
* O₀ is the permitted operator set;
* C₀ is the composition constraint set.

Representation sufficiency is defined through expressibility under the
declared representation language rather than through the performance of a
single model.

R1 requires:

* a relevant structure outside Expressible(R₀);
* a valid representation extension capable of expressing it;
* failure of permitted parameter changes to repair the limitation;
* failure of permitted model-family expansion downstream of R₀ to repair the
  limitation.

The public/private information boundary remains mandatory.

Representation novelty is structural rather than lexical.

Exact primitive definitions, operator signatures, executable expressibility
checking, equivalence checking, and representation-specific complexity remain
later implementation/design questions.

### Status

Completed — research specification only.

Primary artifact:

```
research/notes/S0.5_D5_1_BASELINE_REPRESENTATION.md
```

Evidence artifact:

```
research/notes/S0.5_D5_1_EVIDENCE.md
```

---

## S0.5-D.5.2 World-Family Design

D.5.2 defines the world-family machinery required to construct controlled
benchmark conditions without implementing each failure class as a separate
environment.

### Core decision

UNKNOWN uses a typed relational dynamical world as the core benchmark family.

Shared world-generation machinery produces controlled instances for:

* R0;
* P1;
* M1;
* R1;
* N1;
* X1.

Benchmark conditions are configurations or structural instantiations of shared
world-family machinery rather than unrelated condition-specific environments.

### Core world ontology

The conceptual world contains:

```
World
├── Entities
├── Observable state
├── Hidden state
├── Relations
├── Dynamics
├── Action transition rules
├── Intervention transition rules
├── Observation function
├── Noise process
└── Ground-truth mechanism
```

The conceptual world state is:

```
W = (E, X, R, F, G, I, ξ)
```

where the components represent entities, state, relations, dynamics,
observation, intervention, and stochastic processes.

### Public/private boundary

UNKNOWN receives public observations and observable action/intervention
outcomes.

The evaluator may retain private information such as:

* hidden state;
* mechanism configuration;
* condition class;
* ground-truth representation;
* canonical extension;
* benchmark seed;
* expected failure class.

Those evaluator-side values must not cross the public interaction boundary.

### R1 constructive definition

A clean R1 witness is based on a representation collision.

For public histories H₁ and H₂:

```
R₀(H₁) = R₀(H₂)
```

while a scientifically relevant required outcome differs:

```
Y(H₁) != Y(H₂)
```

and an allowed extension separates the histories:

```
R₁(H₁) != R₁(H₂)
```

The model family operates downstream of R₀ and therefore cannot recover a
distinction that R₀ has already collapsed.

This establishes representation failure as an information/representation
collision rather than simply a model-performance failure.

### Higher-order relation decision

A higher-order relation remains a useful candidate construction, but relation
arity alone is not considered evidence of representation novelty.

A candidate is scientifically relevant only when its required distinction
lies outside the declared R₀ grammar and composition limits.

### Model-family boundary

Model-family expansion must remain downstream of the fixed R₀ representation
boundary.

A model that bypasses R₀ and directly consumes raw public observations would
invalidate the intended distinction between representation failure and
model-family failure.

### N1

N1 represents genuine non-identifiability or insufficient evidence.

Multiple materially different explanations may remain compatible with the
permitted public evidence.

N1 must not be converted into R1 merely because a hidden variable exists.

### X1

X1 isolates stochastic variation from systematic representation inadequacy.

The representation and model family remain sufficient while stochastic
variation produces observation or prediction variability.

### T1

T1 evaluates whether a discovered extension transfers to structurally unseen
contexts.

T1 is an evaluation dimension rather than a separate representation-failure
class.

### Transfer family

One core world family is sufficient for controlled failure construction.

A structurally distinct held-out family is required for strong transfer and
reusability evaluation.

### Anti-shortcut controls

The benchmark must control for:

* entity identity;
* entity ordering;
* entity count;
* timing;
* intervention availability;
* superficial distributions;
* initialization;
* metadata;
* condition labels;
* evaluation leakage;
* implementation artifacts.

Matched-world construction and overlapping superficial distributions are
required where scientifically appropriate.

### Intervention compatibility

Interventions remain evidence-generating mechanisms rather than automatic proof
of representation discovery.

The benchmark must distinguish independent matched trials from sequential
intervention trials where effects accumulate.

### Reproducibility

World-family generation must support deterministic reconstruction through
explicit experiment identity, configuration, and seed hierarchy.

UNKNOWN must not receive benchmark truth through seed or configuration
channels.

### Status

Completed — research specification only.

Primary artifact:

```
research/notes/S0.5_D5_2_WORLD_FAMILY_DESIGN.md
```

Evidence artifact:

```
research/notes/S0.5_D5_2_EVIDENCE.md
```

### Implementation gate

Concrete world schemas, hidden mechanisms, condition generators, executable
R1 witnesses, intervention scenarios, representation-language execution,
candidate extension machinery, and benchmark instance counts remain deferred
to D.5.3 and later executable stages.

---

## S0.5-D.5.3.1 Model-Family / Representation Boundary

D.5.3.1 sharpens the boundary between model-family expansion and
representation extension in preparation for controlled failure construction.

### Core decisions

* Model family is defined as a class of admissible mappings over a fixed
  representation closure.
* Model-family expansion may change mapping capability but may not introduce
  new representational information.
* The baseline representation closure is generated from frozen V₀/T₀/O₀/C₀
  under explicit semantic-equivalence rules.
* Unrestricted computation over raw observations is outside R₀.
* Expressibility is distinct from UNKNOWN discoverability — a distinction
  being expressible under R₀ does not imply UNKNOWN will find it.
* R1 remains constructively established through an R₀ collision:
  R₀(H₁) = R₀(H₂) while required outcomes differ.
* Representation extension changes the admissible representation closure;
  internal model computation does not automatically constitute an extension.
* The R₀ closure must be frozen before final UNKNOWN evaluation and cannot
  be adapted based on UNKNOWN performance.

### Scientific role

This subsection exists to prevent a specific confound: a sufficiently
expressive model family silently reintroducing representational information
that R₀ was defined to exclude. Freezing the R₀ closure prior to evaluation,
and defining model-family expansion strictly downstream of that closure,
keeps the R1 vs. M1 distinction well-posed.

### Status

Completed — research specification only. Executable expressibility checking,
closure generation, and semantic-equivalence rule implementation remain
deferred to later D.5.3 sub-stages.

---

## S0.5-D.5.3.2 P1 Parameter-Failure Construction

D.5.3.2 defines the controlled P1 (Parameter Failure) condition required to
cleanly separate parameter inadequacy from representation-level inadequacy
and model-family inadequacy.

### Core decisions

* P1 is structurally defined as a condition where R₀ and M₀ are sufficient,
  θ₀ is intentionally incorrect, θ* exists within M₀, and θ* is identifiable
  under the permitted public experimental protocol.
* Parameter estimates are not representation extensions.
* The canonical P1 control is the deterministic system
  `s[t+1] = α*s[t] + β*u[t]`.
* P1/N1 is separated by parameter identifiability; if materially different
  parameterizations remain indistinguishable under the permitted protocol,
  the condition is N1.
* P1/M1 is separated by whether the true mapping exists within the frozen
  model family.
* P1/R1 is separated by absence/presence of R₀ representation collisions.
* Canonical P1 is deterministic and noise-free; stochastic/noisy/mixed
  variants are deferred until X1 is independently controlled.
* P1 recovery must generalize to held-out observations/interventions and
  cannot rely on parameter memorization.
* Evaluator-private parameter truth and identifiability information must
  never enter UNKNOWN's public boundary.

### Scientific role

P1 exists to give the benchmark a clean negative control: a condition where
the correct answer is "optimize parameters, do not extend the representation
or expand the model family." Without a rigorously separated P1, any
performance gain from parameter re-fitting could be mistakenly attributed to
representation or model-family effects. Defining P1 via a deterministic,
noise-free linear-recurrence system with a known, identifiable θ* keeps the
P1/M1/R1/N1 boundaries well-posed and testable independently of stochastic
variation (X1).

### Status

Completed — research specification only. Executable P1 world-instance
generation, θ₀/θ* construction, identifiability verification, and held-out
generalization testing remain deferred to later D.5.3 sub-stages.

---

# Required Future Environment Conditions

The eventual benchmark must distinguish:

```
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

* absent from the observation interface;
* present but absent from the current representation;
* present in the representation but inaccessible to a restricted model
  family;
* representable and model-accessible but poorly parameterized.

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

**Current Stage:** S0.5-D.5.3.2 P1 Parameter-Failure Construction

| Stage | Status |
|---|---|
| S0.5-A | Completed |
| S0.5-B | Completed |
| S0.5-C | Completed |
| S0.5-D.1 | Completed |
| S0.5-D.2 | Completed |
| S0.5-D.3 | Completed |
| S0.5-D.4 | Completed — research specification only |
| S0.5-D.5.1 | Completed — research specification only |
| S0.5-D.5.2 | Completed — research specification only |
| S0.5-D.5.3.1 | Completed — research specification only |
| S0.5-D.5.3.2 | Completed — research specification only |
| S0.5-D.5.3.3 | Next |

Implementation: Active

Scientific benchmark: Not yet complete

Novelty claim: None

Research gap: Candidate and provisional

Current verified implementation test suite: **178 passed**

Next milestone: **S0.5-D.5.3.3 (or later) Controlled Failure Construction**

---

# Current Artifacts

## Core documentation

```
README.md
RULES.md
PRD.md
DESIGN.md
ARCHITECTURE.md
RESEARCH_THESIS.md
TASKS.md
MEMORY.md
```

## Research artifacts

```
research/literature/PRIOR_ART_MATRIX.md
research/notes/S0.3_RESEARCH_GAP.md
research/notes/S0.3_REPRESENTATION_SPEC.md
research/notes/S0.3_EVALUATION_PROTOCOL.md
research/notes/S0.4_SYNTHETIC_ENVIRONMENT.md
research/notes/S0.4_ENVIRONMENT_SCHEMA.md
research/notes/S0.4_LEAKAGE_AUDIT.md
research/notes/S0.4_EVIDENCE.md
research/notes/S0.5_DYNAMICS_CONTRACT.md
research/notes/S0.5_B_EVIDENCE.md
research/notes/S0.5_C_OBSERVATION_CONTRACT.md
research/notes/S0.5_C_EVIDENCE.md
research/notes/S0.5_D_DYNAMIC_ENVIRONMENT_CONTRACT.md
research/notes/S0.5_D2_EVIDENCE.md
research/notes/S0.5_D3_EVIDENCE.md
research/notes/S0.5_D4_CONTROLLED_BENCHMARK_CONTRACT.md
research/notes/S0.5_D4_EVIDENCE.md
research/notes/S0.5_D5_1_BASELINE_REPRESENTATION.md
research/notes/S0.5_D5_1_EVIDENCE.md
research/notes/S0.5_D5_2_WORLD_FAMILY_DESIGN.md
research/notes/S0.5_D5_2_EVIDENCE.md
```

## Implementation artifacts

```
src/unknown/environment/schemas/public.py
src/unknown/environment/schemas/hidden.py
src/unknown/environment/schemas/evaluation.py
src/unknown/environment/public/runtime.py
src/unknown/environment/dynamics/models.py
src/unknown/environment/dynamics/world.py
src/unknown/environment/observation/projection.py
```

## Test artifacts

```
tests/environment/test_public_schemas.py
tests/environment/test_hidden_schemas.py
tests/environment/test_evaluation_schemas.py
tests/environment/test_boundary_contract.py
tests/environment/test_public_runtime.py
tests/environment/test_leakage_contract.py
tests/environment/test_deterministic_world.py
tests/environment/test_world_action_configuration.py
tests/environment/test_public_observation_projection.py
tests/environment/test_observation_boundary.py
tests/environment/test_observation_determinism.py
tests/environment/test_world_trajectory_hardening.py
tests/environment/test_world_invariants.py
tests/environment/test_world_interventions.py
```

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
13. Which hidden mechanisms should be implemented before benchmark conditions
    are introduced?

---

# Durable Decisions

* No unsupported novelty claim is permitted.
* Representation failure must be distinguished from information unavailable,
  model-family failure, and parameter failure.
* Hidden ground truth must remain evaluator-only during discovery.
* Representation extensions must carry provenance and testable hypotheses.
* Prediction alone cannot establish concept discovery.
* Intervention, falsification, and unseen-context transfer are required parts
  of the intended validation protocol.
* False candidates and negative results are scientifically necessary.
* The environment must support paired counterfactual controls.
* The public runtime must remain isolated from hidden and evaluation schemas.
* The deterministic world is the internal simulation source of truth.
* Public observations must be produced through an explicit projection
  boundary.
* Public observation projection must not automatically expose arbitrary
  internal fields.
* Internal mass and semantic category are private under the current
  observation contract.
* Derived quantities are not primitive observations unless explicitly
  promoted by a future contract.
* Observation identifiers, ordering, and timestamps must be deterministic
  and independent of hidden benchmark semantics.
* The current observation projector is not a scientific discovery mechanism.
* Dynamic leakage auditing must occur after benchmark dynamics exist.
* Sprint 0 cannot close until its full Definition of Done is satisfied.
* No later sprint should bypass unresolved scientific kill criteria.
* No intervention transition mechanism should be duplicated outside the
  dynamics source of truth.
* Deterministic transition validation must occur before world-state mutation.
* Non-finite action vectors must be rejected at the dynamics boundary.
* Boolean values must not be accepted where integer configuration semantics
  are required.
* Ordinary D.2 hardening must not introduce new physical mechanisms that
  could confound later benchmark conditions.
* Multi-step deterministic replay and state-invariant tests are required
  before intervention and benchmark-condition work proceeds.
* Interventions are authoritative dynamics transitions, not ordinary policy
  actions.
* SET_POSITION directly replaces position and does not apply an ordinary
  kinematic timestep.
* SET_VELOCITY directly replaces velocity and does not apply an ordinary
  kinematic timestep.
* REMOVE_ENTITY removes all incident relations without automatic
  reconnection.
* Intervention transitions increment the world step index by one.
* Intervention history belongs to internal reproducibility state and is not
  part of the public observation.
* Out-of-bounds SET_POSITION interventions are rejected rather than
  silently clamped.
* Public intervention execution delegates to the authoritative dynamics
  layer.
* D.3 does not constitute evidence of concept discovery, causal validity,
  transfer success, benchmark validity, or novelty.
* The next implementation stage is controlled benchmark-condition design,
  not autonomous discovery implementation.
* D.4 defines the controlled benchmark scientifically but does not by itself
  constitute executable benchmark evidence.
* R0 is a finite, typed, explicitly declared representation language rather
  than unrestricted computation over raw observations.
* R1 is defined constructively through representation collisions under R0.
* Model-family expansion must remain downstream of the fixed R0 boundary.
* A higher-order relation is a candidate construction, not a definition of
  representation novelty.
* Shared world-family machinery must generate benchmark conditions rather
  than separate condition-specific environments.
* Structural transfer requires a held-out structurally distinct world
  family.
* N1 must remain distinct from R1 and must represent genuine
  non-identifiability or insufficient evidence.
* X1 isolates stochastic variation from systematic representation
  inadequacy.
* D.5.2 is a research specification only; executable failure construction
  remains deferred to D.5.3 and later stages.
* Model family is defined as a class of admissible mappings over a fixed
  representation closure.
* Model-family expansion may change mapping capability but may not
  introduce new representational information.
* The baseline representation closure is generated from frozen
  V₀/T₀/O₀/C₀ under explicit semantic-equivalence rules.
* Unrestricted computation over raw observations is outside R₀.
* Expressibility under R₀ is distinct from UNKNOWN discoverability.
* Representation extension changes the admissible representation closure;
  internal model computation does not automatically constitute an
  extension.
* The R₀ closure must be frozen before final UNKNOWN evaluation and cannot
  be adapted from UNKNOWN performance.
* P1 is structurally defined as a condition where R₀ and M₀ are sufficient,
  θ₀ is intentionally incorrect, θ* exists within M₀, and θ* is identifiable
  under the permitted public experimental protocol.
* Parameter estimates are not representation extensions.
* The canonical P1 control is the deterministic system
  `s[t+1] = α*s[t] + β*u[t]`.
* P1/N1 is separated by parameter identifiability; if materially different
  parameterizations remain indistinguishable under the permitted protocol,
  the condition is N1.
* P1/M1 is separated by whether the true mapping exists within the frozen
  model family.
* P1/R1 is separated by absence/presence of R₀ representation collisions.
* Canonical P1 is deterministic and noise-free; stochastic/noisy/mixed
  variants are deferred until X1 is independently controlled.
* P1 recovery must generalize to held-out observations/interventions and
  cannot rely on parameter memorization.
* Evaluator-private parameter truth and identifiability information must
  never enter UNKNOWN's public boundary.

---

# Previous Durable Decision

No implementation should begin until the research problem survives the S0.3
adversarial gap and formalization process.

That condition has now been satisfied sufficiently to begin controlled
environment implementation, but it does not constitute proof of novelty or
proof of the research hypothesis.

---

# Current Status

| Item | Status |
|---|---|
| Research question | Provisional |
| Research gap | Candidate |
| Novelty claim | None |
| S0.2 prior-art status | Near completion |
| S0.3 formalization | Completed provisionally |
| S0.4 environment boundary | Implemented and verified |
| S0.5-A dynamics contract | Completed |
| S0.5-B deterministic world | Implemented and verified |
| S0.5-C observation projection | Implemented and verified |
| S0.5-D.1 dynamic environment contract | Completed |
| S0.5-D.2 dynamic transition hardening | Implemented and verified |
| S0.5-D.3 authoritative intervention transition | Implemented and verified |
| S0.5-D.4 controlled benchmark contract | Completed — research specification |
| S0.5-D.5.1 baseline representation contract | Completed — research specification |
| S0.5-D.5.2 world-family design | Completed — research specification |
| S0.5-D.5.3.1 model-family / representation boundary | Completed — research specification |
| S0.5-D.5.3.2 P1 parameter-failure construction | Completed — research specification |
| Synthetic benchmark dynamics | Partially implemented; scientific benchmark mechanisms remain incomplete |
| Autonomous discovery system | Not yet implemented |

**Current checkpoint:** S0.5-D.5.3.2 P1 Parameter-Failure Construction

**Next research stage:** S0.5-D.5.3.3 (or later) Controlled Failure Construction

**Next implementation stage:** Deferred until D.5.3 research/design decisions
are sufficiently specified

**Working tree requirement:** Clean after the D.5.3.2 checkpoint commit

---

# Final Scientific Position

Project UNKNOWN currently has a provisional research question and candidate
research boundary.

The project does not currently claim:

* novelty;
* successful concept discovery;
* successful representation discovery;
* causal discovery;
* transfer success;
* benchmark superiority;
* scientific superiority.

The next scientific objective is to construct controlled failure cases that
can rigorously separate parameter failure, model-family failure, and
representation-level inadequacy under the R0 representation contract.