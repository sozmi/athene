from datetime import datetime
import numpy as np

from db.repos.image_repository import select_label
from db.repos.keras_repository import create_model, select_model_by_path
from defenitions import ROOT_DIR

from tensorflow.keras import layers, saving
from tensorflow.keras.preprocessing import image_dataset_from_directory, image
from tensorflow.keras.callbacks import CSVLogger
from tensorflow.keras.models import Sequential

class ModelManager:
    def __init__(self):
        self.model_path = None
        self.model = None

    def load_model(self, path):
        if self.model_path != path:
            self.model = saving.load_model(path)
            self.model_path = path

    def predict_image(self, image_path, filename):
        img = image.load_img(image_path, target_size=(512, 512))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        km = select_model_by_path(filename)
        lids = [int(n) for n in km.lids.split()]
        s1 = select_label(lids[0]).name
        s2 = select_label(lids[1]).name
        result = self.model.predict(img)
        print(result[0])
        return s1 if result >= 0.5 else s2

    def classify(self, image_path, model_path, filename):
        if self.model_path != model_path:
            self.load_model(model_path)

        result = self.predict_image(image_path, filename)
        return result

    def train_new(self, name, classes, epc):
        #classes = ['0', '1']
        self.model = Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(512, 512, 3)),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D(2, 2),

            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.1),
            layers.BatchNormalization(),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.2),
            layers.BatchNormalization(),
            layers.Dense(1, activation='sigmoid')
        ])
        self.model_path = None
        self.train(name, classes, epc)

    def train(self, name, classes, epc):
        base_dir = f'{ROOT_DIR}/data/images'

        train_datagen = image_dataset_from_directory(base_dir,
                                                     labels='inferred',
                                                     label_mode='int',
                                                     class_names=classes,
                                                     image_size=(512, 512),
                                                     subset='training',
                                                     seed=1,
                                                     validation_split=0.1,
                                                     batch_size=32)
        test_datagen = image_dataset_from_directory(base_dir,
                                                    labels='inferred',
                                                    label_mode='int',
                                                    class_names=classes,
                                                    image_size=(512, 512),
                                                    subset='validation',
                                                    seed=1,
                                                    validation_split=0.1,
                                                    batch_size=32)
        self.model.compile(
            loss='binary_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

        csv_logger = CSVLogger(f'{ROOT_DIR}/data/models/history/{name}.log', separator=',', append=False)
        self.model.fit(train_datagen,
                       epochs=epc,
                       validation_data=test_datagen,
                       callbacks=[csv_logger])

        now = datetime.now()
        sd = now.strftime('%Y-%m-%d %H-%M-%S')
        self.model_path = f'{ROOT_DIR}/data/models/{name}_{sd}.keras'
        self.model.save(self.model_path)
        create_model(f'{name}_{sd}.keras', f'{name}.log', " ".join(classes))
