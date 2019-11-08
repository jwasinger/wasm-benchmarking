from subprocess import Popen, PIPE
import statistics
import re
import json
from mlr import mlr

# TODO: use docker python api/daemon (I think it will reduce startup time)

def generate_inputs(num):
    for i in range(10, num * 10 + 10,10):
        yield "1" * i

def invoke_keccak_docker(keccak_script, execution_input):
    process = Popen(["bash", keccak_script, execution_input], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    return output.decode()

def bench(execution_input):
    output = invoke_keccak_docker("run_keccak_bench.sh", execution_input)
    execution_time = [line for line in output.split("\r\n") if "execution time: " in line][0][17:].strip(' microseconds')
    execution_time = float(execution_time)
    return execution_time

def get_execution_trace_opcodes(execution_input):
    output = invoke_keccak_docker("run_keccak_bench_instrumented.sh", execution_input)
    instruction_counts = [line for line in output.split("\r\n") if "instruction counts: " in line][0][20:].split(', ')
    return [int(x) for x in instruction_counts if x]

def generate_dataset():
    # generate a number of random inputs

    inputs = generate_inputs(200)
    dataset = {
        'execution_times': [],
        'opcode_counts': []
    }

    for inp in inputs:
        # get execution trace opcodes
        opcode_counts = get_execution_trace_opcodes(inp)

        times = []
        # run the input several (hundred?) times gettng an averaged execution time
        for i in range(0, 30):
            times.append(bench(inp))

        averaged_execution_time = int(round(statistics.mean(times)))

        # append the averaged execution time and execution trace opcodes to the dataset
        dataset['execution_times'].append(averaged_execution_time)
        dataset['opcode_counts'].append(opcode_counts)

    return dataset

def main():
    dataset = generate_dataset()
    with open('dataset.json', 'w') as f:
        json.dump(dataset, f)

    # dataset = None
    # with open('dataset.json', 'r') as f:
    #    dataset = json.load(f)

    import pdb; pdb.set_trace()

    mlr(dataset['execution_times'], dataset['opcode_counts'])

if __name__ == "__main__":
    # invoke_keccak_docker("run_keccak_bench_instrumented.sh", None)
    # print(get_execution_trace_opcodes(None))
    main()
