
from firstClassifier.entity import PrepareBaseModelConfig
import tensorflow as tf
from pathlib import Path
from firstClassifier import logger

class PrepareBaseModel:
    """Get the base model and update the parameters with dataset.
    Picking up Defined architectures in Tensorflow and updating with dataset available
    """
    def __init__(self, config: PrepareBaseModelConfig):
        self.config= config
    
    def get_base_model(self):
        """Consider base model VGG16 and saves in folder path
        """
        logger.info("Creating base model frm VGG16")
        self.model= tf.keras.applications.vgg16.VGG16(
            input_shape=self.config.params_image_size,
            weights= self.config.params_weights,
            include_top= self.config.params_include_top
        )
        base_model_path= self.config.base_model_path
        self.save_model(path= base_model_path, model= self.model)
        logger.info(f"Model saved in: {base_model_path}")

    @staticmethod
    def _prepare_full_model(model: tf.keras.Model, classes: int, freeze_all: bool, freeze_till:int, learning_rate:float):
        if freeze_all:
            logger.info("Freezing all the layers")
            for layer in model.layers:
                model.trainable= False
        elif (freeze_till is not None) and (freeze_till >0):
            logger.info(f"freezing layers till {freeze_till}")
            for layer in model.layers[:-freeze_till]:
                model.trainable= False

        ##Flatten the layers to apply ANN
        flatten_in= tf.keras.layers.Flatten()(model.output)
        prediction= tf.keras.layers.Dense(
                        units= classes,
                        activation='softmax',
                        )(flatten_in)
        
        full_model= tf.keras.models.Model(
            inputs= model.input,
            outputs= prediction
        )
        full_model.compile(
            optimizer= tf.keras.optimizers.SGD(learning_rate=learning_rate),
            loss= tf.keras.losses.CategoricalCrossentropy(),
            metrics= ["accuracy"]

        )
        full_model.summary()
        return full_model

    def update_base_model(self):
        self.full_model= self._prepare_full_model(
                model= self.model, 
                classes= self.config.params_classes,
                freeze_all= True,
                freeze_till= None,
                learning_rate= self.config.params_learning_rate
        )
        self.save_model(path= self.config.updated_base_model_path, model= self.full_model)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)
    