from firstClassifier import logger
from firstClassifier.config import ConfigurationManager
from firstClassifier.components.prepare_base_model import PrepareBaseModel




try:
    
    config= ConfigurationManager()
    logger.info("Configuration loading")
    perpare_base_model_config= config.get_prepare_base_model_config()
    logger.info("preparing base model")
    prepare_base_model= PrepareBaseModel(perpare_base_model_config)
    prepare_base_model.get_base_model()
    logger.info("Model update completed")
  
except Exception as e:
    e