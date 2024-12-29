# rule0

Multi-agent deliberation framework.

## Overview

### Nodes

- **admin**: Full of power.

Manages the whole flow. Calls participants to speak, calls for vote, removing participants that violate the rules, etc.

- **participant**: Civil.

Participate in the discussion based on their assigned position or law.

- **judge**: Rule enforcer.

Validates actions that are taken by admin or participants to prevent abuse of power. All the actions are validated by the judge even if they are just want to speak or skip.

## Concept

### World

Global state.

### Clock

Global clock.

### Estoppel

Enforcing consistency in agent behavior.

### Self rewritable rules

Rules that can be rewritten by the agents themselves based on the discussion.

### Conditional actions

Represents quirks of the agents.
