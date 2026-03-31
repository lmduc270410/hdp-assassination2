---
title: "P1719"
source: "luogu"
problem_id: "P1719"
language: "en"
tags: ["maximum subarray", "prefix sums"]
techniques: ["2D compression", "Kadane algorithm"]
related: ["[[P2882]]"]
---

# P1719

## Statement
Given an n × n matrix of integers, find a sub-rectangle with the maximum possible sum.

## Solution
Fix a pair of rows as top and bottom boundaries. Compress the matrix between these rows into a one-dimensional array where each element is the column sum. Then apply Kadane’s algorithm to find the maximum subarray sum. Iterate over all pairs of rows.

## Related
- [[P2882]]
