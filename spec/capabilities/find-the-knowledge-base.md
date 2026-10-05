---
id: capability/find-the-knowledge-base
title: Find the knowledge base
narrator: the user, running any shop-knol command other than init
rests_on:
  - decision/store-found-like-git
  - decision/shop-knol-reaches-kb-wherever-kb-finds-it
  - decision/kb-only-through-its-published-contract
formulated_as: features/find-the-knowledge-base.feature
---

# Find the knowledge base

## Purpose

Every command but `init` works on exactly one knowledge base, and this capability covers how it gets there. The knowledge base is found by looking upward from the working directory, or because `KB_ROOT` names it. Where no single knowledge base can be found, the command is refused. A knowledge base found as a connection to a server serves exactly as a store found in place does.

`init` uses the same finding when no directory is named. It furnishes an empty knowledge base that kb finds, or starts one where nothing is found; that behaviour belongs to start-a-knowledge-base, not here.

## Behaviour

- When the user runs a command from a directory inside the directory holding the shop's knowledge, the command answers from the knowledge base found upward from where the user is working.
- When the user runs a command from outside any knowledge base, with `KB_ROOT` naming the shop's knowledge base, the command answers from the knowledge base `KB_ROOT` names.
- While the working directory has been removed, when the user runs a command with `KB_ROOT` naming the shop's knowledge base, the command answers from the knowledge base `KB_ROOT` names.
- If no knowledge base is found upward from the working directory and nothing names one, the command is refused because no knowledge base was found, neither above where the user is working nor named outright.
- If `KB_ROOT` names a directory that holds no knowledge base, the command is refused because `KB_ROOT` names a directory that holds no knowledge base.
- If the working directory is inside one knowledge base while `KB_ROOT` names another, the command is refused because `KB_ROOT` names a knowledge base other than the one the user is working in, and neither of the two is used.
- If the working directory has been removed and nothing names a knowledge base, the command is refused because the working directory is gone.
- Where the knowledge base found is a connection to a server hosting the store, every command behaves as it does when the store itself is found.

## Implementation, may change

- kb's client finds the store: shop-knol connects with no root, and kb searches upward from the working directory or reads `KB_ROOT`.
- A knowledge base is held as kb defines it: the store itself, or the connection to the server hosting it. kb's search looks for both in the same place.
- The words of these refusals are kb's.

## Not yet

Nothing deferred.
