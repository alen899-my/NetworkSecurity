from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys
if __name__=='__main__':
    try:
        trainingpipeline_confg=TrainingPipelineConfig()
        data_ingestionconfig=DataIngestionConfig(trainingpipeline_confg)
        DataIngestions=DataIngestion(data_ingestionconfig)
        logging.info("initiate the data ingestion")
        data_ing_artifacts=DataIngestions.initiate_data_ingestion()
        print(data_ing_artifacts)
    except Exception as e:
           raise NetworkSecurityException(e,sys)
    