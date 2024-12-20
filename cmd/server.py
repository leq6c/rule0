from flask import Flask, Response, request

from rule0.builder import AgentConfig, Builder

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/stream", methods=["POST"])
def stream():
    data = request.json

    note = data["note"]
    topic = data["topic"]
    prompts = data["prompts"]
    agents = [AgentConfig.decode(agent) for agent in data["agents"]]

    builder = Builder(topic, agents, prompts)

    def generate():
        for logs in builder.run(note):
            yield logs

    return Response(generate(), content_type="text/event-stream")

def spawn_server(port: int):
    app.run(port=port, debug=True)
