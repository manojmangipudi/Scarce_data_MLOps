from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import sys
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import TrainingPipelineConfig

if __name__=='__main__':
    try:
        trainingPipelineConfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingPipelineConfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)