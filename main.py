from subprocess import Popen, PIPE
import re

# TODO: use docker python api/daemon (I think it will reduce startup time)

def generate_inputs():
    for i in range(0, 512,2):
        yield "1"*i

def invoke_keccak_docker(keccak_script, execution_input):
    process = Popen(["bash", keccak_script, '1'*512], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    return output

def get_execution_trace_opcodes(execution_input):
    output = invoke_keccak_docker("run_keccak_bench_instrumented.sh", None)
    instruction_counts = [line for line in output.split("\r\n") if "instruction counts: " in line][0][20:].split(', ')
    return [x for x in instruction_counts if x]


def main():
    # generate a number of random inputs

    for inp in inputs:
        # get execution trace opcodes

        # run the input several (hundred?) times gettng an averaged execution time

        # append the averaged execution time and execution trace opcodes to the dataset
        pass

    # transform the data

    # do MLR to solve for the opcode costs

if __name__ == "__main__":
    # invoke_keccak_docker("run_keccak_bench_instrumented.sh", None)
    print(get_execution_trace_opcodes(None))
    # main()
