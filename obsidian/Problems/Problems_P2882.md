---
title: "P2882"
source: "luogu"
problem_id: "P2882"
language: "en"
tags: ["greedy", "simulation"]
techniques: ["difference array", "greedy flipping"]
related: ["[[P1719]]"]
---

# P2882

## Statement
Given a sequence of cows facing either forward or backward, you can flip the direction of a consecutive segment of length K in one operation. The goal is to make all cows face forward using the minimum number of operations. Additionally, determine the optimal value of K.

## Solution
For each possible K, simulate the process using a difference array to track flips efficiently. Maintain the current flip parity while scanning from left to right. If a cow is facing the wrong direction under current parity, perform a flip starting at that position. Count operations and choose the K with the minimum number of flips.

## Related
- [[P1719]]
