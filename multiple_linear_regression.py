import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

# bh_data = load_boston()

# print(bh_data.keys())

# boston = pd.DataFrame(bh_data.data, columns=bh_data.feature_names)

# print(bh_data.DESCR)

# boston['MEDV'] = bh_data.target

# X = pd.DataFrame(np.c_[boston['LSTAT'], boston['RM']], columns=['LSTAT','RM'])
# y = boston['MEDV']

execution_trace_data = {
  'opcode_counts': [
  [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 11, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 1, 0, 6, 0],
[0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 11, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 1, 0, 6, 0],
[20, 0, 2648, 0, 155, 36, 0, 21, 0, 0, 0, 0, 0, 0, 42, 18551, 0, 6183, 265, 0, 6922, 0, 0, 0, 1, 269, 0, 15, 0, 69, 0, 21, 451, 0, 0, 0, 1257, 9, 74, 11, 56, 90, 0, 0, 0, 0, 0, 77, 0, 26, 397, 0, 2045, 124, 15, 0, 0, 1199, 0, 2634, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 271, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1391, 0, 0, 0, 5, 229, 0, 0, 0, 0, 4881, 189, 39, 85, 4841, 4881, 0]
  ],
  'execution_times': [5,7,2]
}

# transpose
opcode_counts = [[execution_trace_data['opcode_counts'][j][i] for j in range(0, 3)] for i in range(0, 104)]
x = pd.DataFrame(opcode_counts)
y = pd.DataFrame(execution_trace_data['execution_times'])



# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=9)

lin_reg_mod = LinearRegression()

lin_reg_mod.fit(x,y)

# pred = lin_reg_mod.predict(x)
import pdb; pdb.set_trace()

test_set_rmse = (np.sqrt(mean_squared_error(y_test, pred)))

test_set_r2 = r2_score(y_test, pred)

print(test_set_rmse)
print(test_set_r2)
