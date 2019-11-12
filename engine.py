from subprocess import Popen, PIPE
import os

# TODO: pass engine input via pipes instead of the shell (they might become too long)
# def make_temp():
#    path = "./pipe"
#    mode = 0o600
#    os.mkfifo(path, mode)

# TODO: use docker python api/daemon (I think it will reduce startup time between test cases)

class InvokeEngine:
    @staticmethod
    def invoke_engine(engine_container, wasm_file, execution_input):
        cmd_str = ["docker", "run", "-v", "{}/wasm/{}:/{}".format(os.getcwd(), wasm_file, wasm_file), "-t", engine_container, "--wasmfile", "/{}".format(wasm_file), "--input", execution_input]
        process = Popen(cmd_str, stdout = PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        return output.decode()

    @staticmethod
    def wasmi(wasm_file, execution_input):
        return InvokeEngine.invoke_engine('localhost/wasmi', wasm_file, execution_input)

    def wasmi_instrumented(wasm_file, execution_input):
        return InvokeEngine.invoke_engine('localhost/wasmi-instrumented', wasm_file, execution_input)

# consume raw output and translate into an engine-agnostic form
class EngineOutput:
    @staticmethod
    def wasmi(engine_output):
        execution_time = [line for line in engine_output.split("\r\n") if "execution time: " in line][0][17:].strip(' microseconds')
        execution_time = float(execution_time)
        return execution_time

    @staticmethod
    def wasmi_instruction_counter(engine_output):
        instruction_counts = [line for line in engine_output.split("\r\n") if "instruction counts: " in line][0][20:].split(', ')
        return [int(x) for x in instruction_counts if x]
