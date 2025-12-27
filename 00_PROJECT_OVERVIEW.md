# TOON vs JSON Benchmark — Project Overview

## Goal
Build a reproducible benchmark to study how **representation choice (JSON vs TOON)** affects:
- token usage
- cost
- correctness
- determinism
- failure behavior

This is not a model benchmark — it is a **representation-level systems experiment**.

## Core Question
How does data representation influence LLM behavior when performing structured tasks?

## High-Level Flow
1. Generate realistic synthetic dataset  
2. Encode as JSON and TOON  
3. Run structured tasks  
4. Measure efficiency + correctness  
5. Aggregate and compare  

## Principles
- Deterministic
- Reproducible
- Schema-driven
- Representation is the only variable
- No model comparison
- No prompt tricks

## Outputs
- Dataset files
- Run artifacts
- Metrics & tables
- Plots

## Audience
Infra engineers, ML engineers, researchers, founders.

## Non-goals
- Model training
- Creativity evaluation
- Claims of superiority
- Production deployment
