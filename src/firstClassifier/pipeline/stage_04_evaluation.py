from firstClassifier.components.evaluation import Evaluation
from firstClassifier.config.configuration import ConfigurationManager
from firstClassifier import logger
import os
##Setting up environment variables for mlflow
os.environ["MLFLOW_TRACKING_URI"]="https://dagshub.com/Vikaslakkacs/First_classifier.mlflow "
os.environ["MLFLOW_TRACKING_USERNAME"]="Vikaslakkacs"
os.environ["MLFLOW_TRACKING_PASSWORD"]="7af2883531f922b7f10037acc2db95ccdd02bfa5"

STAGE_NAME="Data Evaluation Stage"
def main():
    config= ConfigurationManager()
    validation_config= config.get_validation_config()
    evaluate= Evaluation(validation_config)
    evaluate.evaluation()
    evaluate.save_score()
    evaluate.log_into_mlflow()  


if __name__=="__main__":
    try:
        logger.info(f"<<<<<<<<<<<<<{STAGE_NAME} has started>>>>>>>>>>>>>")
        main()
        logger.info(f"<<<<<<<<<<<<<{STAGE_NAME} has Ended>>>>>>>>>>>>>")

    except Exception as e:
        logger.exception(e)
        raise e