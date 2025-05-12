import os
import keras
import numpy as np

class ModelManager:
    def __init__(self):
        self.model_path = None
        self.model = None

    def load_model(self, path):
        self.model = keras.saving.load_model(path)
        self.model_path = path

    def predict_image(self, image_path):
        img = keras.preprocessing.image.load_img(image_path, target_size=(512, 512))
        img = keras.preprocessing.image.img_to_array(img)
        img = np.expand_dims(img, axis=0)

        result = self.model.predict(img)
        return "Полярный медведь" if result >= 0.5 else "Бурый медведь"

    def classify(self, image_path, model_path ):
        if self.model_path != model_path:
            self.load_model(model_path)

        result = self.predict_image(image_path)
        return result