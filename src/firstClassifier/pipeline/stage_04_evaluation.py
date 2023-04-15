from firstClassifier.components.evaluation import Evaluation
from firstClassifier.config.configuration import ConfigurationManager
from firstClassifier import logger

STAGE_NAME="Data Evaluation Stage"
def main():
    config= ConfigurationManager()
    validation_config= config.get_validation_config()
    evaluate= Evaluation(validation_config)
    evaluate.evaluation()
    evaluate.save_score()  


if __name__=="__main__":
    try:
        logger.info(f"<<<<<<<<<<<<<{STAGE_NAME} has started>>>>>>>>>>>>>")
        main()
        logger.info(f"<<<<<<<<<<<<<{STAGE_NAME} has Ended>>>>>>>>>>>>>")

    except Exception as e:
        logger.exception(e)
        raise e