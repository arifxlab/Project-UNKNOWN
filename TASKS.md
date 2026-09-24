# Project UNKNOWN - Tasks

## Current Sprint

# Sprint 0 - Scientific Foundation

**Status:** IN PROGRESS

**Started:** 2026-09-23

**Implementation:** Started under S0.4 environment boundary work

---

# Sprint 0 Objective

Establish the scientific foundation required to determine whether Project UNKNOWN represents a meaningful and sufficiently distinct research problem before implementing the autonomous discovery system.

Sprint 0 also establishes the controlled experimental environment, scientific information boundaries, formal evaluation protocol, reproducibility requirements, and architecture required for later experiments.

---

# S0.1 - Research Thesis

* [x] Establish provisional research question
* [x] Establish provisional hypothesis
* [x] Define initial research boundaries
* [x] Revise thesis after initial prior-art investigation
* [x] State current novelty position as provisional
* [x] Define explicit research boundary
* [ ] Finalize thesis after final targeted prior-art equivalence check

**Status:** PROVISIONAL

---

# S0.2 - Prior-Art Investigation

## Broad Literature Areas

* [x] Investigate concept discovery
* [x] Investigate unsupervised concept discovery
* [x] Investigate representation learning
* [x] Investigate disentangled representation learning
* [x] Investigate causal representation learning
* [x] Investigate causal abstraction
* [x] Investigate latent-variable discovery
* [x] Investigate active learning
* [x] Investigate active experimentation
* [x] Investigate automated experiment design
* [x] Investigate automated scientific discovery
* [x] Investigate theory formation
* [x] Investigate symbolic regression
* [x] Investigate world models
* [x] Investigate model-based diagnosis

## Synthesis

* [x] Identify closest systems
* [x] Build prior-art comparison matrix
* [x] Identify overlapping mechanisms
* [x] Identify candidate distinct mechanism
* [x] Record papers and systems
* [x] Record currently known unresolved questions
* [x] Perform adversarial comparison against overlapping research areas

## Required Final Check

* [ ] Perform final targeted search for essentially equivalent complete mechanisms
* [x] Review `research/literature/PRIOR_ART_MATRIX.md`
* [x] Cross-check thesis against prior-art findings
* [ ] Decide whether S0.2 can be formally closed

**Status:** NEAR COMPLETION - final targeted equivalence check remains

---

# S0.3 - Research Gap and Formal Problem Definition

## Research Gap

* [x] State the candidate research gap explicitly
* [x] Attempt to falsify the candidate research gap
* [x] Document overlapping prior-art mechanisms
* [x] Define the remaining candidate distinction
* [x] Document objections and alternative explanations
* [x] Define research kill conditions
* [x] Record that the candidate distinction is not yet a novelty claim

## Formal Definitions

* [x] Define environment
* [x] Define observation
* [x] Define action
* [x] Define hidden state
* [x] Define representation
* [x] Define representation failure
* [x] Define parameter failure
* [x] Define model-family failure
* [x] Define information-unavailable condition
* [x] Define candidate representation
* [x] Define concept
* [x] Define hypothesis
* [x] Define prediction
* [x] Define intervention
* [x] Define evidence
* [x] Define falsification
* [x] Define discovery
* [x] Define transfer
* [x] Define representation adequacy
* [x] Define candidate acceptance criteria
* [x] Define candidate rejection criteria

## Scientific Protocol

* [x] Define representation boundary
* [x] Define representation extension language
* [x] Define complexity/search constraints
* [x] Define prediction validation
* [x] Define intervention validation
* [x] Define falsification validation
* [x] Define unseen-context transfer validation
* [x] Define representation recovery distinctions
* [x] Define paired counterfactual diagnosis
* [x] Define decoy candidates
* [x] Define baseline requirements
* [x] Define UNKNOWN versus always-on search ablation
* [x] Define benchmark leakage controls

**Status:** COMPLETED PROVISIONALLY

**Primary artifacts:**

* `research/notes/S0.3_RESEARCH_GAP.md`
* `research/notes/S0.3_REPRESENTATION_SPEC.md`
* `research/notes/S0.3_EVALUATION_PROTOCOL.md`

**Scientific caveat:** S0.3 establishes the current formal problem definition but does not establish novelty. The final prior-art equivalence check remains part of S0.2.

---

# S0.4 - Synthetic Environment and Scientific Boundary

## Environment Specification

* [x] Define smallest useful environment boundary
* [x] Define public observation interface
* [x] Define public actions
* [x] Define public interventions
* [x] Define hidden benchmark state
* [x] Define ground-truth representation boundary
* [x] Define evaluation boundary
* [x] Define representation-failure condition
* [x] Define information-unavailable condition
* [x] Define model-family-failure condition
* [x] Define parameter-failure condition
* [x] Define paired counterfactual requirement
* [x] Define decoy candidate requirement
* [x] Define unseen transfer requirement
* [x] Define reproducibility boundary

## Environment Schema

* [x] Implement public schemas
* [x] Implement hidden benchmark schemas
* [x] Implement evaluation schemas
* [x] Define public/hidden/evaluation separation
* [x] Define schema versioning fields
* [x] Define public environment configuration
* [x] Define public environment metadata
* [x] Define observation schema
* [x] Define action schema
* [x] Define intervention schema
* [x] Define hidden condition schema
* [x] Define ground-truth representation schema
* [x] Define evaluation record schema

## Public Runtime

* [x] Create `PublicEnvironmentRuntime`
* [x] Implement `reset`
* [x] Implement `observe`
* [x] Implement `step`
* [x] Implement `intervene`
* [x] Implement `is_terminal`
* [x] Implement `episode_metadata`
* [x] Implement initialization validation
* [x] Implement terminal-state protection
* [x] Implement action validation
* [x] Implement intervention validation
* [x] Keep hidden state outside public runtime
* [x] Keep evaluation state outside public runtime
* [x] Keep hidden/evaluation schemas outside public runtime imports

## Leakage Protection

* [x] Define PUBLIC information layer
* [x] Define HIDDEN information layer
* [x] Define EVALUATION information layer
* [x] Define public schema leakage tests
* [x] Define runtime storage leakage tests
* [x] Define import-boundary tests
* [x] Define source-level boundary tests
* [x] Define type-annotation boundary tests
* [x] Define output boundary tests
* [x] Define oracle-surface protection
* [x] Define seed/reproducibility leakage requirements
* [x] Define benchmark metadata leakage requirements
* [ ] Execute final dynamic leakage audit after full synthetic dynamics exist

## Verification

* [x] Public schema tests pass
* [x] Hidden schema tests pass
* [x] Evaluation schema tests pass
* [x] Boundary contract tests pass
* [x] Public runtime tests pass
* [x] Leakage contract tests pass
* [x] Full environment test suite passes
* [x] Full repository test suite passes
* [x] Runtime compilation passes
* [x] `git diff --check` passes
* [x] Record S0.4 evidence

## S0.4 Boundary Outcome

S0.4 established the public/hidden/evaluation information boundary and the initial public runtime contract.

The remaining dynamic benchmark requirements were intentionally moved into the subsequent S0.5 implementation stages rather than treating the contract shell as a completed scientific benchmark.

**Status:** IMPLEMENTATION CHECKPOINT VERIFIED

**Primary artifacts:**

* `research/notes/S0.4_SYNTHETIC_ENVIRONMENT.md`
* `research/notes/S0.4_ENVIRONMENT_SCHEMA.md`
* `research/notes/S0.4_LEAKAGE_AUDIT.md`
* `research/notes/S0.4_EVIDENCE.md`
* `src/unknown/environment/schemas/public.py`
* `src/unknown/environment/schemas/hidden.py`
* `src/unknown/environment/schemas/evaluation.py`
* `src/unknown/environment/public/runtime.py`
* `tests/environment/`

**Scientific caveat:** The environment boundary is verified, but the final scientific benchmark requires controlled dynamics, hidden mechanisms, interventions, paired conditions, evaluator-side ground truth, and transfer scenarios.

---

# S0.5 - Environment Dynamics, Ground Truth, and Observation

## S0.5-A - Dynamics Contract

* [x] Define deterministic state-transition contract
* [x] Define entity state model
* [x] Define position and velocity semantics
* [x] Define world context
* [x] Define relations
* [x] Define reset contract
* [x] Define determinism contract
* [x] Define action contract
* [x] Define intervention contract boundary
* [x] Define transition contract
* [x] Define public observation projection boundary
* [x] Define hidden/evaluation isolation requirements
* [x] Define reproducibility requirements
* [x] Define dynamics testing requirements

**Status:** COMPLETED

**Primary artifact:**

* `research/notes/S0.5_DYNAMICS_CONTRACT.md`

---

## S0.5-B - Deterministic World Dynamics

* [x] Implement deterministic world models
* [x] Implement entity categories
* [x] Implement vectors
* [x] Implement entity state
* [x] Implement relation state
* [x] Implement world context
* [x] Implement world state
* [x] Implement deterministic seeded initialization
* [x] Implement bounded positions
* [x] Implement deterministic velocities
* [x] Implement deterministic entity categories
* [x] Implement deterministic relations
* [x] Implement `reset`
* [x] Implement `state`
* [x] Implement `seed`
* [x] Implement `is_terminal`
* [x] Implement `step`
* [x] Implement action validation
* [x] Implement NO_OP behavior
* [x] Implement MOVE behavior
* [x] Implement INTERACT validation boundary
* [x] Implement deterministic position integration
* [x] Implement position bounds
* [x] Implement terminal horizon
* [x] Test deterministic replay
* [x] Test action/configuration behavior
* [x] Record S0.5-B evidence
* [x] Commit and push S0.5-B checkpoint

**Status:** COMPLETED

**Primary artifacts:**

* `src/unknown/environment/dynamics/models.py`
* `src/unknown/environment/dynamics/world.py`
* `src/unknown/environment/dynamics/__init__.py`
* `tests/environment/test_deterministic_world.py`
* `tests/environment/test_world_action_configuration.py`
* `research/notes/S0.5_B_EVIDENCE.md`

**Engineering checkpoint:**

* Full environment suite after S0.5-B: 116 passed
* Deterministic world implementation verified
* Commit: `3fae8d8 feat: implement deterministic world dynamics`

**Scientific caveat:** S0.5-B establishes deterministic world mechanics only. It does not establish hidden benchmark mechanisms, concept discovery, representation failure diagnosis, causal validity, or scientific benchmark conclusions.

---

## S0.5-C - Public Observation Projection

* [x] Define public observation projection contract
* [x] Define public primitive observation fields
* [x] Define public entity projection
* [x] Define position exposure
* [x] Define velocity exposure
* [x] Keep internal mass private
* [x] Keep internal semantic category private
* [x] Define controlled public attributes
* [x] Prevent arbitrary internal-field copying
* [x] Define derived-quantity policy
* [x] Define temporal history boundary
* [x] Define public relation boundary
* [x] Define event boundary
* [x] Define observation-kind semantics
* [x] Define step-index semantics
* [x] Define deterministic simulation timestamp semantics
* [x] Define opaque observation identifiers
* [x] Define deterministic ordering
* [x] Define projection purity
* [x] Define projection isolation
* [x] Define hidden-state isolation
* [x] Define configuration boundary
* [x] Define information-availability boundary
* [x] Define information-unavailable distinction
* [x] Define representation-failure distinction
* [x] Define model-family-failure distinction
* [x] Define parameter-failure distinction
* [x] Define paired-counterfactual boundary
* [x] Define no-oracle-feature rule
* [x] Define leakage threat model
* [x] Define public error contract
* [x] Define external-dependency prohibition
* [x] Define serialization boundary
* [x] Implement `PublicObservationProjector`
* [x] Integrate projector with public runtime
* [x] Project reset observations
* [x] Project current observations
* [x] Project step results
* [x] Preserve public-only runtime outputs
* [x] Add observation projection tests
* [x] Add observation determinism tests
* [x] Add observation boundary tests
* [x] Update runtime integration tests
* [x] Update leakage contract test fixture
* [x] Verify public runtime compilation
* [x] Verify full repository test suite
* [x] Record S0.5-C evidence

**Status:** IMPLEMENTED - CHECKPOINT READY

**Primary artifact:**

* `research/notes/S0.5_C_OBSERVATION_CONTRACT.md`

**Implementation artifacts:**

* `src/unknown/environment/observation/__init__.py`
* `src/unknown/environment/observation/projection.py`
* `src/unknown/environment/public/runtime.py`

**Test artifacts:**

* `tests/environment/test_public_observation_projection.py`
* `tests/environment/test_observation_boundary.py`
* `tests/environment/test_observation_determinism.py`
* `tests/environment/test_public_runtime.py`
* `tests/environment/test_leakage_contract.py`

**Verification state:**

* S0.5-C focused projection tests: 25 passed
* Leakage contract tests: 19 passed
* Full repository suite: 147 passed
* Runtime compilation: passed
* `git diff --cached --check`: passed
* `git diff --check`: passed

**Scientific caveat:** S0.5-C establishes the public observation projection boundary and its executable tests. It does not establish autonomous concept discovery, representation-failure diagnosis, successful representation extension, causal discovery, predictive superiority, intervention validity, falsification validity, transfer validity, or benchmark-level scientific conclusions.

---

# S0.5-D - Dynamic Environment Completion

* [ ] Define hidden dynamic mechanisms
* [ ] Define observable variables
* [ ] Define hidden variables
* [ ] Define generating equations/functions
* [ ] Define controlled relations
* [ ] Define meaningful action semantics
* [ ] Define intervention transition semantics
* [ ] Define benchmark condition generation
* [ ] Define paired counterfactual environments
* [ ] Define information-unavailable controls
* [ ] Define model-family controls
* [ ] Define parameter-failure controls
* [ ] Define false candidate opportunities
* [ ] Define genuine reusable concept opportunities
* [ ] Define unseen transfer contexts
* [ ] Define evaluator-side ground-truth records
* [ ] Implement hidden environment state
* [ ] Implement evaluator-side ground truth
* [ ] Implement meaningful intervention dynamics
* [ ] Implement benchmark condition generation
* [ ] Implement paired benchmark scenarios
* [ ] Implement transfer scenarios
* [ ] Execute dynamic leakage audit

**Status:** NOT STARTED

S0.5-D — Dynamic Environment Completion
Status: IN PROGRESS

S0.5-D.1 — Dynamic Environment Contract
Status: COMPLETED

Completed:
- Defined authoritative dynamic transition contract.
- Defined action semantics.
- Defined intervention semantics.
- Defined deterministic temporal semantics.
- Defined information-unavailable conditions.
- Defined representation-failure conditions.
- Defined model-family controls.
- Defined parameter-failure controls.
- Defined decoy conditions.
- Defined paired-counterfactual requirements.
- Defined hidden/evaluation separation.
- Defined leakage requirements.
- Defined reproducibility requirements.
- Defined scientific and engineering acceptance criteria.
- Defined S0.5-D Definition of Done.

Artifact:
- research/notes/S0.5_D_DYNAMIC_ENVIRONMENT_CONTRACT.md

S0.5-D.2 — Dynamic Transition Hardening
Status: NOT STARTED

S0.5-D.3 — Authoritative Intervention Transition
Status: NOT STARTED

S0.5-D.4 — Controlled Benchmark Conditions
Status: NOT STARTED

S0.5-D.5 — Paired Counterfactuals
Status: NOT STARTED

S0.5-D.6 — Hidden/Evaluation Integration
Status: NOT STARTED

S0.5-D.7 — Leakage + Reproducibility Audit
Status: NOT STARTED

S0.5-D.8 — Evidence + Checkpoint
Status: NOT STARTED

---

# S0.5-E - Ground Truth

* [ ] Define true hidden mechanism
* [ ] Define hidden variables
* [ ] Define generating equations/functions
* [ ] Define intervention semantics
* [ ] Define ground-truth concept properties
* [ ] Define ground-truth transfer behavior
* [ ] Define ground-truth access restrictions
* [ ] Define paired information controls
* [ ] Define ground-truth evaluator representation
* [ ] Define equivalence criteria for recovered representations

**Status:** NOT STARTED

---

# S0.6 - Baselines

* [ ] Fixed representation baseline
* [ ] Parameter-optimization baseline
* [ ] Model-family expansion baseline
* [ ] Statistical feature discovery baseline
* [ ] Latent/clustering baseline
* [ ] Predictive-only feature expansion baseline
* [ ] Always-on representation search baseline
* [ ] Define baseline implementation constraints
* [ ] Define fair comparison protocol
* [ ] Define computational budgets
* [ ] Define search budgets
* [ ] Define information-access parity

**Status:** NOT STARTED

---

# S0.7 - Evaluation

* [ ] Define representation-failure diagnosis metrics
* [ ] Define explanatory metrics
* [ ] Define predictive metrics
* [ ] Define intervention metrics
* [ ] Define falsification metrics
* [ ] Define transfer metrics
* [ ] Define false-discovery metrics
* [ ] Define representation-recovery metrics
* [ ] Define complexity metrics
* [ ] Define reproducibility criteria
* [ ] Define statistical comparison methodology
* [ ] Define ablation methodology
* [ ] Define confidence intervals or uncertainty reporting
* [ ] Define failure-case reporting

**Status:** NOT STARTED

---

# S0.8 - Intervention Protocol

* [ ] Define intervention types
* [ ] Define intervention selection
* [ ] Define intervention budget
* [ ] Define expected predictions
* [ ] Define competing hypotheses
* [ ] Define rejection conditions
* [ ] Define intervention leakage controls
* [ ] Define intervention reproducibility
* [ ] Define intervention coverage requirements

**Status:** NOT STARTED

---

# S0.9 - Reproducibility

* [ ] Define random seed policy
* [ ] Define experiment configuration
* [ ] Define environment versioning
* [ ] Define model versioning
* [ ] Define result storage
* [ ] Define experiment identifiers
* [ ] Define repository-state tracking
* [ ] Define dependency locking
* [ ] Define hardware/software recording
* [ ] Define deterministic replay
* [ ] Define artifact manifest

**Status:** NOT STARTED

---

# S0.10 - Kill Criteria

* [ ] Validate prior-art kill criterion
* [ ] Validate baseline kill criterion
* [ ] Validate concept-definition kill criterion
* [ ] Validate representation-diagnosis kill criterion
* [ ] Validate intervention-value kill criterion
* [ ] Validate transfer kill criterion
* [ ] Validate reproducibility kill criterion
* [ ] Validate benchmark leakage kill criterion
* [ ] Validate complexity/search-budget kill criterion
* [ ] Validate negative-result preservation criterion

**Status:** NOT STARTED

---

# S0.11 - Architecture

* [ ] Establish research architecture
* [ ] Establish experiment architecture
* [ ] Establish configuration strategy
* [ ] Establish result storage strategy
* [ ] Establish test architecture
* [ ] Establish extensibility boundaries
* [ ] Confirm architecture against scientific requirements
* [ ] Confirm public/hidden/evaluation separation
* [ ] Confirm evaluator isolation
* [ ] Confirm reproducibility architecture

**Status:** PROVISIONAL

---

# S0.12 - Documentation

* [x] README.md initial version
* [x] RULES.md initial version
* [x] RESEARCH_THESIS.md initial version
* [x] PRD.md initial version
* [x] DESIGN.md initial version
* [x] ARCHITECTURE.md initial version
* [x] TASKS.md initial version
* [x] MEMORY.md initial version
* [x] Prior-art matrix
* [x] S0.3 research-gap documentation
* [x] S0.3 representation specification
* [x] S0.3 evaluation protocol
* [x] S0.4 synthetic environment specification
* [x] S0.4 environment schema
* [x] S0.4 leakage audit
* [x] S0.4 evidence
* [x] S0.4 environment schema tests
* [x] S0.4 environment runtime tests
* [x] S0.4 leakage contract tests
* [x] S0.5-A dynamics contract
* [x] S0.5-B deterministic world implementation
* [x] S0.5-B evidence
* [x] S0.5-C observation contract
* [x] S0.5-C observation implementation
* [x] S0.5-C observation tests
* [ ] S0.5-C evidence
* [ ] Final Sprint 0 evidence package

**Status:** IN PROGRESS

---

# S0.13 - Final Sprint Review

* [ ] Review scientific question
* [ ] Review prior art
* [ ] Review research boundary
* [ ] Review formal definitions
* [ ] Review environment
* [ ] Review ground truth
* [ ] Review baselines
* [ ] Review evaluation
* [ ] Review intervention protocol
* [ ] Review kill criteria
* [ ] Review architecture
* [ ] Verify reproducibility plan
* [ ] Verify benchmark leakage controls
* [ ] Review negative-result policy

**Status:** NOT STARTED

---

# S0.14 - Git Checkpoint

* [ ] Check working tree
* [ ] Review changed files
* [ ] Run required validation
* [ ] Stage files
* [ ] Review staged diff
* [ ] Commit Sprint 0
* [ ] Configure GitHub remote
* [ ] Push to GitHub
* [ ] Verify remote state
* [ ] Confirm clean working tree
* [ ] Record Sprint 0 checkpoint

**Status:** NOT STARTED

---

# Definition of Done

Sprint 0 is complete only when:

* [ ] Research question is precise
* [ ] Working hypothesis is explicit
* [ ] Prior-art boundary is documented
* [ ] No unsupported novelty claim remains
* [ ] Final targeted prior-art equivalence check is complete
* [ ] Formal terminology is established
* [ ] Representation failure is operationally defined
* [ ] First scientific environment is specified
* [ ] Ground truth is specified
* [ ] Baselines are specified
* [ ] Evaluation metrics are specified
* [ ] Intervention protocol is specified
* [ ] Reproducibility protocol is specified
* [ ] Kill criteria are specified
* [ ] Architecture direction is justified
* [ ] Public/hidden/evaluation boundary is verified
* [ ] Documentation is complete
* [ ] Evidence is recorded
* [ ] Git commit exists
* [ ] Git push succeeds
* [ ] Working tree is clean

---

# Future Sprint Placeholder

No future sprint should be started until Sprint 0 reaches its Definition of Done.
