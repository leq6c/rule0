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

    topic = data["topic"]
    prompts = data["prompts"]
    agents = [AgentConfig.decode(agent) for agent in data["agents"]]

    builder = Builder(topic, agents, prompts)

    def generate():
        for logs in builder.run():
            message = "event: message\n"
            message += "data: "
            message += json.dumps([log.to_dict() for log in logs])
            message += "\n\n"
            yield message

    return Response(generate(), mimetype="text/event-stream")

def spawn_server(port: int):
    app.run(port=port, debug=True)
