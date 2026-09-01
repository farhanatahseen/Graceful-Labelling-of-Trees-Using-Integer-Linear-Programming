# Graceful-Labelling-of-Trees-Using-Integer-Linear-Programming

This repository contains a Python implementation of an Integer Linear Programming (ILP) formulation for finding graceful labellings of trees. Given a tree with *n* vertices, the model assigns distinct integer labels to vertices such that the induced edge labels (absolute differences between adjacent vertex labels) form the set {1, 2, ..., n−1}.

The ILP model is implemented using [PuLP](https://coin-or.github.io/pulp/), an open-source linear programming modelling library for Python, and solved with the CBC (Coin-or Branch and Cut) solver.

## Features
- Encodes vertex-label distinctness, edge-label distinctness, and absolute-difference linearisation as linear constraints
- Solves for a feasible graceful labelling on any input tree
- Verifies correctness by independently recomputing edge labels from the solver's output

## Requirements
- Python 3.x
- [PuLP](https://pypi.org/project/PuLP/) (`pip install pulp`)

## Usage
```bash
python graceful.py
```
Edit the `n` and `edges` variables in the script to test different trees.

## Background
This implementation accompanies the paper *"Graceful Labelling of Trees Using Integer Linear Programming."*
