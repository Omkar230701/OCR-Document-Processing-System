from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

texts = [
    "Invoice number total amount due GST",
    "Invoice date bill payment total amount",
    "Tax invoice total due amount",

    "Payment receipt thank you for payment",
    "Receipt total amount paid cash",
    "Payment successful receipt transaction total",

    "Monthly report analysis summary data",
    "Financial report revenue growth summary"
]

labels = [
    "invoice",
    "invoice",
    "invoice",

    "receipt",
    "receipt",
    "receipt",

    "report",
    "report"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained successfully!")