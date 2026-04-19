import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import pandas as pd
import requests
import pickle
import matplotlib.pyplot as plt
from user import user_input
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

url = "http://127.0.0.1:5000/model"

def main():

    st.title("Prédiction du niveau de qualité de l’air")
    menu = st.sidebar.selectbox("Navigation",["Accueil", "Apprentissage et comparaison", "Prédiction"])

    if menu == "Accueil":
        st.write("Cette application utilise les algorithmes de classification et l'évaluation comparative pour prédire la qualité de l'air. Son interface utilisateur comporte trois pages qui jouent des rôles distincts: récupérer les entrées de l'utilisateur, les envoyer au serveur et d'afficher la réponse du serveur. Cette première comporte un bouton permettant de charger et donc afficher le dataset, la seconde entraines plusieurs modèle puis les compare en claculant les métriques (accuracy, recall, précision, F1-score) pour en choisir la plus performante. La page 3 récupère d,abord les entrées de l'utilisateur notamment la temperature, l'humidité, les quantités de PM2.5, PM10, NO2, SO2, CO, la proximite des zones industrielles, la densite de la population, et la quualité d'air . Ensuite, elle affiche ces sélections, permet de de choisir un modèle, envois les données au serveur qui les traduit puis affiche  le résultat qui est le calcul de probabilité. En ce qui concerne le backend qui est le serveur, il reçoit les requêtes envoyées par le client, choisis le modèle adéquat puis le charge avant d'en faire la prédiction pour finalement renvoyer la reponse au client(frontend) ")
        file = st.file_uploader("Charger un fichier CSV", type=["csv"])
        if file is not None:
            data = pd.read_csv(file)  
            st.write("Aperçu du dataset :")
            st.dataframe(data)

    elif menu == "Apprentissage et comparaison":
        st.subheader("Apprentissage des modèles")
        data = pd.read_csv("../pollution.csv")
        data = data.dropna()

        DataML = data.values
        X = DataML[:, :-1]
        Y = DataML[:, -1]

        Test = 0.3
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=Test)

        choix = st.multiselect("Choisir les modèles",["Decision Tree", "Random Forest", "KNN","Logistic Regression", "Naive Bayes", "SVM"])
        if st.button("Lancer l'apprentissage"):
            results = []
            for algo in choix:
                if algo == "Decision Tree":
                    model = DecisionTreeClassifier()
                    model_name = "Decision_Tree.pkl"
                elif algo == "Random Forest":
                    model = RandomForestClassifier()
                    model_name = "Random_Forest.pkl"
                elif algo == "KNN":
                    model = KNeighborsClassifier()
                    model_name = "KNN.pkl"
                elif algo == "Logistic Regression":
                    model = LogisticRegression(max_iter=1000)
                    model_name = "Logistic_Regression.pkl"
                elif algo == "Naive Bayes":
                    model = GaussianNB()
                    model_name = "Naive_Bayes.pkl"
                elif algo == "SVM":
                    model = SVC(probability=True)
                    model_name = "SVM.pkl"
                model.fit(x_train, y_train)
                y_pred = model.predict(x_test)

   
                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred, average='weighted')
                rec = recall_score(y_test, y_pred, average='weighted')
                f1 = f1_score(y_test, y_pred, average='weighted')

                results.append({
                    "Modèle": algo,
                    "Accuracy": round(acc, 3),
                    "Precision": round(prec, 3),
                    "Recall": round(rec, 3),
                    "F1-score": round(f1, 3)
                })

              
                cm = confusion_matrix(y_test, y_pred)

                fig, ax = plt.subplots()
                disp = ConfusionMatrixDisplay(confusion_matrix=cm)
                disp.plot(ax=ax)

                st.subheader(f"Matrice de confusion - {algo}")
                st.pyplot(fig)

                pickle.dump(model, open(f"../serveur/models/{model_name}", "wb"))#wb=Write Binary. C'est pour enregistrer le modèle dans un fichier

            df = pd.DataFrame(results)

            st.write("Résultats")
            st.dataframe(df)

           
            st.subheader("Histogramme des accuracies")

            plt.figure()
            plt.bar(df["Modèle"], df["Accuracy"])
            plt.xlabel("Modèles")
            plt.ylabel("Accuracy")
            plt.title("Comparaison des modèles")

            st.pyplot(plt)

            st.success("Modèles sauvegardés")

  
    elif menu == "Prédiction":
 
        analyse = user_input()
        st.write(analyse)

        models = ["Decision_Tree.pkl", "Random_Forest.pkl", "KNN.pkl"]
        model_choice = st.selectbox("Choisir le modèle", models)

        if st.button("Prédire"):

            data_to_send = analyse.copy()
            data_to_send["model"] = model_choice

            rep = requests.post(url, json=data_to_send)
            dict_reponse = rep.json()

            pred = dict_reponse['class']
            prob = dict_reponse['proba']

            labels = ["Bonne", "Modérée", "Mauvaise", "Dangereuse"]

            if pred >= 2:
                st.error(f"Qualité : {labels[pred]}")
            else:
                st.success(f"Qualité : {labels[pred]}")

            st.metric("Probabilité", f"{round(prob*100,2)} %")


if __name__ == '__main__':
    main()