from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys
if __name__=='__main__':
    try:
        trainingpipeline_confg=TrainingPipelineConfig()
        data_ingestionconfig=DataIngestionConfig(trainingpipeline_confg)
        DataIngestions=DataIngestion(data_ingestionconfig)
        logging.info("initiate the data ingestion")
        data_ing_artifacts=DataIngestions.initiate_data_ingestion()
        logging.info("data initiation completed")
        print(data_ing_artifacts)
        data_validation_config=DataValidationConfig(trainingpipeline_confg)
        data_validation=DataValidation(data_ing_artifacts,data_validation_config)
        logging.info("initiate daata validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data validation compeleted")
        print(data_validation_artifact)

        data_transformation_config=DataTransformationConfig(trainingpipeline_confg)
        logging.info("data transformation started")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("dat transmission srtarted")


        
    except Exception as e:
           raise NetworkSecurityException(e,sys)
    