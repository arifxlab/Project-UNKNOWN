# Project UNKNOWN — Memory

## Purpose

This document records durable project knowledge, major decisions, constraints, research conclusions, rejected approaches, and current milestone state.

It is not a conversation diary.

---

# Project Identity

**Name:** Project UNKNOWN

**Research Area:** Autonomous Concept Formation & Model Discovery

**Started:** 2026-09-23

**Development Mode:** Research-grade / experimental / production-quality

---

# Core Thesis

UNKNOWN investigates whether an artificial system can detect when its current representation of an unfamiliar environment is inadequate, construct a new reusable concept or representation, and experimentally validate that concept.

The project focuses on:

> Representation discovery before relationship discovery.

---

# Current Research Question

> Can an artificial system autonomously detect when its current representation of an environment is systematically inadequate, construct a reusable candidate concept that extends that representation, and experimentally determine whether the candidate provides explanatory, predictive, interventional, and transfer value beyond the original representation?

**Status:** Provisional

**Reason:** Prior-art investigation is not yet complete.

---

# Working Hypothesis

> When an environment contains reusable structure that cannot be adequately represented by the system's current vocabulary, a system equipped with explicit representation-failure detection, candidate concept formation, hypothesis generation, intervention, and falsification mechanisms can discover and validate a reusable abstraction that provides measurable explanatory, predictive, interventional, and transfer value beyond the original representation.

**Status:** Working hypothesis

---

# Null Hypothesis

> Adding autonomous concept formation and validation does not produce a reliable improvement over appropriately designed fixed-representation, feature-discovery, latent-representation, and predictive baselines.

**Status:** Working null hypothesis

---

# Core Discovery Principle

A candidate concept does not become a discovery merely because:

- an LLM generated a name;
- a cluster was found;
- a latent representation improved prediction;
- a correlation exists;
- a visualization appears meaningful;
- a model generated a plausible explanation.

A candidate must survive predefined validation.

---

# Discovery Pipeline

```text
Candidate
    ↓
Formalize
    ↓
Generate Predictions
    ↓
Intervene
    ↓
Observe
    ↓
Support / Falsify
    ↓
Transfer Test
    ↓
Validated Concept