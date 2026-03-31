---
title: "P8218"
source: "luogu"
problem_id: "P8218"
language: "en"
tags: ["prefix sums"]
techniques: ["prefix sums"]
related: ["[[P1314]]"]
---

# P8218

## Statement
Given an array of n integers, answer multiple queries asking for the sum of elements in a subarray [l, r].

## Solution
Precompute prefix sums where pre[i] is the sum of the first i elements. Each query is answered as pre[r] − pre[l − 1].

## Related
- [[P1314]]
