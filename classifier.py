import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def classify_document(text):
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    return prediction