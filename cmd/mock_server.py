import json

from flask import Flask, Response, request
from flask_cors import CORS

from rule0.builder import AgentConfig, Builder

app = Flask(__name__)
CORS(app)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/stream", methods=["POST"])
def stream():
    data = request.json
    print(data)

    def generate():
        # mock
        logs = [
            {"sender": "admin", "message": "Start Discussion", "action": "MARKER", "id": "0"},
            {"sender": "admin", "message": "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of \"de Finibus Bonorum et Malorum\" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, \"Lorem ipsum dolor sit amet..\", comes from a line in section 1.10.32.", "action": "SPEAK", "id": "3"},
        ]

        for i in range(4, 20, 1):
            logs.append({"sender": "admin", "message": "Hello, I am admin", "action": "SPEAK", "id": str(i)})

        for i in range(len(logs)):
            message = "event: message\n"
            message += "data: "
            message += json.dumps(logs[:i+1])
            message += "\n\n"
            yield message
            import time
            time.sleep(1)

    return Response(generate(), mimetype="text/event-stream")

def spawn_server(port: int):
    app.run(port=port, debug=True)
