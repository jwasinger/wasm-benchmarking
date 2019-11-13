import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

wasm_opcodes = [
    "Br",
    "BrIfEqz",
    "BrIfNez",
    "BrTable",
    "Call",
    "CallIndirect",
    "CurrentMemory",
    "Drop",
    "F32Const",
    "F32Load",
    "F32Store",
    "F64Const",
    "F64Load",
    "F64Store",
    "GetGlobal",
    "GetLocal",
    "GrowMemory",
    "I32Add",
    "I32And",
    "I32Clz",
    "I32Const",
    "I32Ctz",
    "I32DivS",
    "I32DivU",
    "I32Eq",
    "I32Eqz",
    "I32GeS",
    "I32GeU",
    "I32GtS",
    "I32GtU",
    "I32LeS",
    "I32LeU",
    "I32Load",
    "I32Load16S",
    "I32Load16U",
    "I32Load8S",
    "I32Load8U",
    "I32LtS",
    "I32LtU",
    "I32Mul",
    "I32Ne",
    "I32Or",
    "I32Popcnt",
    "I32RemS",
    "I32RemU",
    "I32Rotl",
    "I32Rotr",
    "I32Shl",
    "I32ShrS",
    "I32ShrU",
    "I32Store",
    "I32Store16",
    "I32Store8",
    "I32Sub",
    "I32WrapI64",
    "I32Xor",
    "I64Add",
    "I64And",
    "I64Clz",
    "I64Const",
    "I64Ctz",
    "I64DivS",
    "I64DivU",
    "I64Eq",
    "I64Eqz",
    "I64ExtendSI32",
    "I64ExtendUI32",
    "I64GeS",
    "I64GeU",
    "I64GtS",
    "I64GtU",
    "I64LeS",
    "I64LeU",
    "I64Load",
    "I64Load16S",
    "I64Load16U",
    "I64Load32S",
    "I64Load32U",
    "I64Load8S",
    "I64Load8U",
    "I64LtS",
    "I64LtU",
    "I64Mul",
    "I64Ne",
    "I64Or",
    "I64Popcnt",
    "I64RemS",
    "I64RemU",
    "I64Rotl",
    "I64Rotr",
    "I64Shl",
    "I64ShrS",
    "I64ShrU",
    "I64Store",
    "I64Store16",
    "I64Store32",
    "I64Store8",
    "I64Sub",
    "I64Xor",
    "Return",
    "Select",
    "SetGlobal",
    "SetLocal",
    "TeeLocal",
    "Unreachable"]

def multi_linear_regression(coeffs, ys):
    x = pd.DataFrame(coeffs)
    y = pd.DataFrame(ys)

    lin_reg_mod = LinearRegression()

    lin_reg_mod.fit(x,y)

    # TODO print opcodes, calculate their corresponding gas costs at 10 mil gas = 1 second execution time
    print("model coefficients: ")

    for i in range(0, len(lin_reg_mod.coef_)):
        print("predicted gas cost of {} is {}".format(wasm_opcodes[i], lin_reg_mod.coef_[i][0]))

    print("R^2 score (0 bad, 1 perfect fit):")
    print(lin_reg_mod.score(x, y))
    # print(r2_score(x, y, multioutput='variance_weighted'))

    # test_set_rmse = (np.sqrt(mean_squared_error(y_test, pred)))

    # test_set_r2 = r2_score(y_test, pred)

    # print(test_set_rmse)
    # print(test_set_r2)
