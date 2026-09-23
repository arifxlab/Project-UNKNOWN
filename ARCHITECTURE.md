# 8. `ARCHITECTURE.md`

This one intentionally stays conservative.

```markdown
# Project UNKNOWN — Architecture

## Status

**Stage:** Sprint 0

**Status:** Preliminary / Not Frozen

---

# 1. Architecture Principle

UNKNOWN architecture must follow the scientific experiment.

The architecture should not become complex merely to appear production-grade.

---

# 2. Preliminary System Boundary

```text
+---------------------------------------------------+
|                 PROJECT UNKNOWN                   |
|                                                   |
|  +-------------------+                            |
|  | Environment       |                            |
|  +---------+---------+                            |
|            | observations                         |
|            v                                      |
|  +-------------------+                            |
|  | Representation     |                           |
|  | Manager            |                           |
|  +---------+---------+                            |
|            |                                      |
|            v                                      |
|  +-------------------+                            |
|  | Predictive /       |                           |
|  | Explanatory Model  |                           |
|  +---------+---------+                            |
|            |                                      |
|            v                                      |
|  +-------------------+                            |
|  | Representation     |                           |
|  | Failure Detector   |                           |
|  +---------+---------+                            |
|            |                                      |
|            v                                      |
|  +-------------------+                            |
|  | Concept Generator  |                           |
|  +---------+---------+                            |
|            | candidates                           |
|            v                                      |
|  +-------------------+                            |
|  | Hypothesis Engine  |                           |
|  +---------+---------+                            |
|            | predictions                          |
|            v                                      |
|  +-------------------+                            |
|  | Experiment /       |                            |
|  | Intervention       |                            |
|  | Planner            |                            |
|  +---------+---------+                            |
|            |                                      |
|            v                                      |
|  +-------------------+                            |
|  | Validator /        |                            |
|  | Falsifier          |                            |
|  +---------+---------+                            |
|            |                                      |
|            v                                      |
|  +-------------------+                            |
|  | Concept Registry   |                            |
|  +-------------------+                            |
|                                                   |
+---------------------------------------------------+