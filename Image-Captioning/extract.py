import os
import numpy as np
import pickle
directory = "Images" 
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
model = ResNet50(weights='imagenet')
model = Model(inputs=model.input, outputs=model.layers[-2].output)

features = {}
directory = "Images"

for img_name in os.listdir(directory):
    print("Processing:", img_name)
    img_path = directory + "/" + img_name

    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    feature = model.predict(img, verbose=0)
    image_id = img_name.split('.')[0]

    features[image_id] = feature

pickle.dump(features, open("features.pkl", "wb"))

print("✅ Features extracted!")