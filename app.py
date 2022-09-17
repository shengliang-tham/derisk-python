import os
import flask
from slither.slither import Slither
from slither.detectors import all_detectors
import inspect
from slither.detectors.abstract_detector import AbstractDetector
from flask import request
from flask import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET"])
def home():
    return "hello"

@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    contractAddress = data["contractAddress"]
    print(contractAddress)
    # print(request)
    try:
        slither = Slither(contractAddress)
        detectors = [getattr(all_detectors, name) for name in dir(all_detectors)]
        detectors = [
            d
            for d in detectors
            if inspect.isclass(d) and issubclass(d, AbstractDetector)
        ]

        for detector_cls in detectors:
            slither.register_detector(detector_cls)

        results = slither.run_detectors()

        tscores = [x for x in results if x != []]
        return jsonify(tscores)
    except:
        return {}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4300))
    app.run(host="0.0.0.0", port=port)
