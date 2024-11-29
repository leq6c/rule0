# Example Flow

## Prerequisites

### Topic

"Choose pizza over sushi"

### Participants

- **Alice**: pizza is better
- **Bob**: sushi is better

## Initial state

### parameters

- **history**: []
- **participants**: [Alice, Bob]

## Flow

### Step 1: User inputs topic

user: "Choose pizza over sushi" -> admin

### Step 2: Admin declares the start of the flow

admin: "MARKER: ----- Discussion started ----- " -> judge

### Step 3: Judge validates the marker and adds it to the history

judge: "MARKER: ----- Discussion started ----- " -> (history)

### Step 4: Judge calls for admin to proceed

judge: "GRANTED" -> admin

### Step 5: Admin suggests participants to speak

admin: "CALL: Alice, Bob" -> judge

### Step 6: Judge calls for Alice to speak

judge: "GRANTED" -> Alice

### Step 7: Alice speaks

Alice: "SPEAK: I think pizza is better because it's more delicious" -> judge

### Step 8: Judge validates the message and adds it to the history

judge: "SPEAK: (Alice) I think pizza is better because it's more delicious" -> (history)

### Step 9: Judge calls for Bob to speak

judge: "GRANTED" -> Bob

### Step 10: Bob speaks

Bob: "SPEAK: I think sushi is better because it's healthier" -> judge

### Step 11: Judge validates the message and adds it to the history

judge: "SPEAK: (Bob) I think sushi is better because it's healthier" -> (history)

### Step 12: Judge calls for admin to proceed

judge: "GRANTED" -> admin

### Step 13: Admin calls for vote

admin: "MARKER: ----- Vote started ----- " -> judge

### Step 14: Judge validates the marker and adds it to the history

judge: "MARKER: ----- Vote started ----- " -> (history)

### Step 15: Judge calls for admin to proceed

judge: "GRANTED" -> admin
