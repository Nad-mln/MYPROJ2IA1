import pickle
import numpy as np

def pred_proba(data, model_name):
    values = list(data.values())
    values = np.array(values).reshape(1, -1)
    model = pickle.load(open(f"models/{model_name}", "rb"))#rb: pour lire un modèle déjà sauvegardé
    pred = int(model.predict(values)[0])
    prob = model.predict_proba(values)[0][pred]
    return pred, prob