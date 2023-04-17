import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
import time
from pathlib import Path
from firstClassifier.utils import save_json
from firstClassifier.entity import EvaluationConfig
import mlflow
import mlflow.tensorflow
from urllib.parse import urlparse

class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config= config

    
    def _valid_generator(self):

        ##Augmentation
        datagenerator_kwargs= dict(
            rescale= 1./255,
            validation_split= 0.005

        )

        dataflow_kwargs= dict(
            target_size= self.config.params_image_size[:-1],
            batch_size= self.config.params_batch_size,
            interpolation= "bilinear"
        )

        valid_datagenerator= tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator= valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle= False,
            **dataflow_kwargs
        )

    @staticmethod
    def load_model(path:Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)

        
    def evaluation(self):
        model= self.load_model(self.config.path_of_model)
        self._valid_generator()
        ##score returns loss and accuracy
        self.score= model.evaluate(
            self.valid_generator
        )

    def save_score(self):
        scores= {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data= scores)

    def log_into_mlflow(self):
        mlflow.set_registry_uri(self.config.mlflow_uri)
        #print("f{self.config.mlflow_uri}-----Hello")
        tracking_url_type_store= urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():

            mlflow.log_params(
                self.config.all_params
            )
            mlflow.log_metrics(
                {"loss": self.score[0], "accuracy": self.score[1]}
            )
            if tracking_url_type_store!="file":
                mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16 model")
            else:
                mlflow.keras.log_model(self.model, "model")