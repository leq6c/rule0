Returns `$ACCEPT` or `$REJECT` in the first line, and the reason if `$REJECT`. And returns the new state if you need to update the state.
To update the state, you should return the new state with `$UPDATE-STATE` in this format after returning the accept or reject.
At the end of the discussion, you should return `$END` to terminate the discussion. Usually admin will use marker to declare the end of the discussion.

$UPDATE-STATE

```
{here is the new state. you should include all the information}
```

**if you don't need to update the state, you should not return the state.**
**you shouldn't add new section or anything. keep things short.**
**barely reject the action.**
admin will provide options when admin call for a vote.

Now let's start.

"{{SENDER}}" provided the following request:
{{MESSAGE}}
