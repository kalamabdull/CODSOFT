import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


model = load_model("model.keras")


tokenizer = pickle.load(open("tokenizer.pkl", "rb"))

max_length = 5

def generate_caption(photo):
    in_text = "startseq"

    for i in range(max_length):
        seq = tokenizer.texts_to_sequences([in_text])[0]
        seq = pad_sequences([seq], maxlen=max_length)

        yhat = model.predict([photo, seq], verbose=0)
        yhat = np.argmax(yhat)

        word = tokenizer.index_word.get(yhat)
        if word is None:
            break

        in_text += " " + word

    return in_text


features = pickle.load(open("features.pkl", "rb"))


key = list(features.keys())[0]


print("Caption:", generate_caption(features[key]))