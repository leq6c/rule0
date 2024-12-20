# Server

## api

### `POST /stream`

#### request

```json
{
  "topic": "",
  "agents": [
    {
      "name": "name",
      "role": "role",
      "basis": "basis",
      "verbal": "verbal"
    }
  ],
  "prompts": {
    "base": "",
    "admin": "",
    "judge": "",
    "speaker": ""
  }
}
```
