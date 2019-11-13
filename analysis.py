import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

def multi_linear_regression(coeffs, ys):
    x = pd.DataFrame(coeffs)
    y = pd.DataFrame(ys)

    lin_reg_mod = LinearRegression()

    lin_reg_mod.fit(x,y)
    import pdb; pdb.set_trace()

    # TODO print opcodes, calculate their corresponding gas costs at 10 mil gas = 1 second execution time
    print("model coefficients: ")
    print(lin_reg_mod.coef_)

    print("R^2 score (0 bad, 1 perfect fit):")
    print(lin_reg_mod.score(x, y))
    # print(r2_score(x, y, multioutput='variance_weighted'))

    # test_set_rmse = (np.sqrt(mean_squared_error(y_test, pred)))

    # test_set_r2 = r2_score(y_test, pred)

    # print(test_set_rmse)
    # print(test_set_r2)
