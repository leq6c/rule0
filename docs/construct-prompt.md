# Construct prompt

## _System -> Admin_: Starting the discussion

- input

```system
{system_prompt}
{admin_prompt}
{state}
```

```user
Information is all set. Please start your move.
```

- expected output

```admin
MARKER: ----- Discussion started -----
```

## _Admin -> Judge_: Sending output to judge

- input

```system
{system_prompt}
{judge_prompt}

Returns `ACCEPT` or `REJECT` in the first line, and the reason if `REJECT`. And returns the new state if you need to update the state.
```

```user
{state}

"admin" provided the following request.:
MARKER: ----- Discussion started -----
```

- expected output

```judge
ACCEPT
```

- behavior

Add the marker to the history.

## _Judge -> Admin_: Sending output to admin

- input

```system
{system_prompt}
{admin_prompt}
```

```user
{state}

# Conversation History
----- Discussion started -----
```

- expected output

```admin
CALL: {target_participant}
```

## _Admin -> Judge_: Sending output to judge

- input

```system
{system_prompt}
{judge_prompt}
```

```user
{state}

"admin" provided the following request.:
CALL: {target_participant}
```

- expected output

```judge
ACCEPT
```

## _Judge -> Participant_: Sending output to target participant

- input

```system
{system_prompt}
{participant_prompt}
```

```user
{state}

# Conversation History
----- Discussion started -----
```

- expected output

```participant
{response}
```

## _Participant -> Judge_: Sending output to judge

- input

```system
{system_prompt}
{judge_prompt}
```

```user
{state}

# Conversation History
----- Discussion started -----

Participant requested to say:
{response}
```

- expected output

```judge
ACCEPT
```

- behavior

Add the conversation to the history.

## _Judge -> Admin_: Sending output to admin

- input

```system
{system_prompt}
{admin_prompt}
```

```user
{state}

----- Discussion started -----

Participant said:
{response}
```

- expected output

```admin
CALL: {next_participant}
```

## _Admin -> Judge_: Sending output to judge

- input

```system
{system_prompt}
{judge_prompt}
```

```user
{state}

# Conversation History
----- Discussion started -----

Participant said:
{response}
```
