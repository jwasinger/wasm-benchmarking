import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

def multi_linear_regression(ys, coeffs):
    x = pd.DataFrame(coeffs)
    y = pd.DataFrame(ys)

    lin_reg_mod = LinearRegression()

    import pdb; pdb.set_trace()
    lin_reg_mod.fit(x,y)

    # test_set_rmse = (np.sqrt(mean_squared_error(y_test, pred)))

    # test_set_r2 = r2_score(y_test, pred)

    # print(test_set_rmse)
    # print(test_set_r2)
