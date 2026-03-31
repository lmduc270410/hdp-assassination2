---
title: "P1314"
source: "luogu"
problem_id: "P1314"
language: "en"
tags: ["prefix sums", "binary search"]
techniques: ["binary search on answer", "prefix sums"]
related: ["[[P4552]]", "[[P8218]]"]
---

# P1314

## Statement
You are given two arrays w[i] and v[i] of length n, and m queries each consisting of an interval [l, r]. For a chosen threshold x, only elements with w[i] ≥ x are considered valid. For each query, compute the product of the number of valid elements in [l, r] and the sum of their v[i]. Sum this value over all queries to obtain a total. Given a target S, find the value of x such that the absolute difference between the computed total and S is minimized.

## Solution
Perform binary search on x. For each candidate x, build prefix arrays counting valid elements and summing their values. For each query, compute the contribution using prefix sums. Compare the total with S and adjust the search range accordingly.

## Related
- [[P4552]]
- [[P8218]]
