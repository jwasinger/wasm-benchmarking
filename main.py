from subprocess import Popen, PIPE
import statistics
import re
import json
import glob
import sys
from mlr import mlr
from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from engine import InvokeEngine, EngineOutput

# TODO: use docker python api/daemon (I think it will reduce startup time between test cases)

NUM_SMOOTHING_RUNS = 1 # 10

engines = [
    'wasmi'
]

def run_benchmark(engine, benchmark, wasm_input):
    if engine == 'wasmi':
        return EngineOutput.wasmi(InvokeEngine.wasmi(benchmark['wasm'], wasm_input))

def run_benchmarks():
    engines = ['wasmi']
    datasets = {}

    for test_file in glob.iglob("./benchmarks/*.yml"):
        t = None
        with open(test_file, 'r') as f:
           t =  load(f, Loader=Loader)

        datasets[list(t.keys())[0]] = {
            'opcode_counts': [],
            'times': []
        }

        test_dataset = datasets[list(t.keys())[0]]
        test_case = t[list(t.keys())[0]]

        for inp in test_case['inputs']:
            opcode_counts = EngineOutput.wasmi_instruction_counter(InvokeEngine.wasmi_instrumented(test_case['wasm'], inp))
            test_dataset['opcode_counts'].append(opcode_counts)

            # invoke all engines (?) do we want this
            for engine in engines:
                execution_times = []

                test_dataset[engine] = [] 

                for i in range(0, NUM_SMOOTHING_RUNS):
                    execution_times.append(run_benchmark(engine, test_case, inp))

                test_dataset[engine].append(statistics.mean(execution_times))
    return datasets

def main():

    # TODO either generate or compute regression (on a pre-existing dataset) specified by cmd line flag
    dataset = run_benchmarks()
    with open('output/dataset.json', 'w') as f:
        json.dump(dataset, f)

    # mlr(dataset['execution_times'], dataset['opcode_counts'])

if __name__ == "__main__":
    # invoke_keccak_docker("run_keccak_bench_instrumented.sh", None)
    # print(get_execution_trace_opcodes(None))
    main()
