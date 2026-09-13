from flask import Flask, jsonify
from flask_cors import CORS
import agent

app = Flask(__name__)
CORS(app)

@app.route("/api/run")
def run():
    agent.reset_demo()
    agent.data.shipments[0]["status"] = "delayed"
    result = agent.resolve_disruption("SHIP-001")
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000)