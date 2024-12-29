import json
import threading
import time

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

    topic = data["topic"]
    prompts = data["prompts"]
    agents = [AgentConfig.decode(agent) for agent in data["agents"]]

    builder = Builder(topic, agents, prompts)

    def generate():
        queue = []
        done = threading.Event()

        def send_ping():
            while not done.is_set():
                queue.append("event: ping\n\ndata: ping\n\n")
                time.sleep(3)

        def run_builder():
            try:
                for logs in builder.run():
                    if done.is_set():
                        break
                    message = "event: message\n"
                    message += "data: "
                    message += json.dumps([log.to_dict() for log in logs])
                    message += "\n\n"
                    queue.append(message)
                    # send tokens
                    message = "event: tokens\n"
                    message += "data: "
                    message += json.dumps(
                        {
                            "input": builder.total_input_tokens,
                            "output": builder.total_output_tokens,
                        }
                    )
                    message += "\n\n"
                    queue.append(message)
            finally:
                done.set()

        ping_th = threading.Thread(target=send_ping)
        builder_th = threading.Thread(target=run_builder)
        ping_th.start()
        builder_th.start()

        try:
            while not done.is_set():
                if queue:
                    yield queue.pop(0)
                else:
                    time.sleep(1)
        finally:
            done.set()
            ping_th.join()
            builder_th.join()

    return Response(generate(), mimetype="text/event-stream")


def spawn_server(port: int):
    app.run(port=port, debug=True)
