from firstClassifier import logger
from firstClassifier.config import PrepareCallbacksConfig, TrainingConfig
from firstClassifier.components.training import Training
from firstClassifier.components.prepare_callback import PrepareCallback
from firstClassifier.config import ConfigurationManager

try:
    config= ConfigurationManager()
    prepare_callbacks_config= config.get_prepare_callback_config()
    prepare_callbacks= PrepareCallback(config= prepare_callbacks_config)
    callback_list= prepare_callbacks.get_tb_ckpt_callbacks()

    training_config= config.get_training_config()
    training= Training(config= training_config)
    training.get_base_model()
    training.train_valid_generator()
    training.train(
        callback_list=callback_list
    )

except Exception as e:
    raise e