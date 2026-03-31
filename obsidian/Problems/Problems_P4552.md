---
title: "P4552"
source: "luogu"
problem_id: "P4552"
language: "en"
tags: ["greedy", "math"]
techniques: ["difference array", "greedy analysis"]
related: ["[[P1314]]"]
---

# P4552

## Statement
Given a sequence a[i], you can increment or decrement all elements in any chosen subarray by 1 in one operation. The goal is to make all elements equal with the minimum number of operations and determine the number of distinct ways to achieve this.

## Solution
Define the difference array d[i] = a[i] − a[i−1]. Let the sum of positive differences be P and the absolute sum of negative differences be Q. The minimum number of operations required is max(P, Q). The number of ways to achieve this is |P − Q| + 1.

## Related
- [[P1314]]
