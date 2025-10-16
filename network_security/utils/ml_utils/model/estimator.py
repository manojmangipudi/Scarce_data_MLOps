from network_security.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os
import sys

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

class NetworkModel:
    def __init__(self, model, preprocessor):
        """
        TrainedModel constructor
        
        :param model: Trained model object
        :param preprocessor: Preprocessing object
        """
        try:
            self.model = model
            self.preprocessor = preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x):
        """
        Function accepts raw inputs and then transformed raw input using preprocessor
        and finally predicts for transformed features
        
        :param X: Raw input features
        :return: Predicted labels
        """
        try:
            x_transformed = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transformed)
            return y_hat
        
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e