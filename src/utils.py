
import os
import sys
import dill
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        logging.error("Error occurred while saving object")
        raise CustomException(e, sys)
    
    
def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}

        for name, model in models.items():
            param_grid = params.get(name, {})  # ✅ default empty

            # Run GridSearch only if params exist
            if param_grid:
                gs = GridSearchCV(model, param_grid, cv=3)
                gs.fit(X_train, y_train)
                model.set_params(**gs.best_params_)

            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_score = r2_score(y_train, y_train_pred)
            test_score = r2_score(y_test, y_test_pred)

            logging.info(f"{name} -> Train R2: {train_score:.4f}, Test R2: {test_score:.4f}")
            report[name] = test_score

        return report

    except Exception as e:
        logging.exception("Error occurred during model evaluation")  # ✅ includes traceback
        raise CustomException(e, sys)