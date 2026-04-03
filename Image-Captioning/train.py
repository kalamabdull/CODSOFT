import pickle
import numpy as np
features = pickle.load(open("features.pkl", "rb"))
print("Number of features:", len(features))
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, add
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

# Load features
features = pickle.load(open("features.pkl", "rb"))

# Simple captions
captions = {
    key: ["startseq a photo of something endseq"] for key in features.keys()
}

all_captions = []
for key in captions:
    all_captions.extend(captions[key])

tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_captions)

vocab_size = len(tokenizer.word_index) + 1
max_length = 5

def create_sequences():
    X1, X2, y = [], [], []

    for key in captions:
        for caption in captions[key]:
            seq = tokenizer.texts_to_sequences([caption])[0]

            for i in range(1, len(seq)):
                in_seq, out_seq = seq[:i], seq[i]

                in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
                out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]

                X1.append(features[key][0])
                X2.append(in_seq)
                y.append(out_seq)

    return np.array(X1), np.array(X2), np.array(y)

X1, X2, y = create_sequences()

# Model
inputs1 = Input(shape=(2048,))
fe = Dense(256, activation='relu')(inputs1)

inputs2 = Input(shape=(max_length,))
se = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
se = LSTM(256)(se)

decoder = add([fe, se])
outputs = Dense(vocab_size, activation='softmax')(decoder)

model = Model(inputs=[inputs1, inputs2], outputs=outputs)
model.compile(loss='categorical_crossentropy', optimizer='adam')

model.fit([X1, X2], y, epochs=2)

model.save("model.keras")
pickle.dump(tokenizer, open("tokenizer.pkl", "wb"))

print("✅ Model trained!")