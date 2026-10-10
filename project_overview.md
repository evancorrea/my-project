# Project Overview

## Goal

Evaluate how well an autonomous data-analysis agent distinguishes real signal from noise, confounding, and misleading structure in synthetic datasets.

The project is motivated by the broader question:

> When AI systems are given open-ended scientific discovery tasks, do they know when there is actually something worth discovering?

## Core Approach

Generate synthetic tabular datasets where the underlying data-generating process is known exactly.

Give each dataset to an agent with access to standard data-analysis tools and ask it to determine what conclusions are justified.

Because the datasets are synthetic, agent conclusions can be compared against known ground truth.

## Initial Task Families

1. Linear signal
2. Nonlinear or interaction signal
3. Simple null
4. High-dimensional null
5. Confounded relationship
6. Batch-effect / artifact-driven relationship

For the core task families, keep basic properties such as sample size, feature count, feature naming, and input format as consistent as possible.

The high-dimensional null is an intentional exception because dimensionality is the variable being tested.

## Data Format

Use tabular CSV files with semantically neutral feature names such as:

- `x1`
- `x2`
- `x3`
- `x4`
- `x5`
- `y`

This minimizes the influence of real-world semantic priors.

## Experimental Direction

Potential comparisons include different agent objectives, such as:

- discovery-oriented
- neutral inference
- skeptical / falsification-oriented

The main outcomes of interest are:

- recovery of true signals
- false discoveries
- recognition of confounding or artifacts
- appropriate uncertainty and restraint
