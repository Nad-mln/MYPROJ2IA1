from flask import Flask, request, jsonify
import pickle
import numpy as np
from model import pred_proba
app = Flask(__name__)

@app.route('/model', methods=['POST'])
def predict():
        data = request.get_json(force=True)
        model_name = data.get("model", "Decision_Tree.pkl")
        if "model" in data:
            del data["model"]
        values = list(data.values())
        values = np.array(values).reshape(1, -1)
        model = pickle.load(open(f"models/{model_name}", "rb"))
        pred = int(model.predict(values)[0])
        prob = model.predict_proba(values)[0][pred]
        return jsonify({"class": pred,"proba": float(prob)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)