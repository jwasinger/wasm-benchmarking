docker run -v $(pwd)/main.wasm:/main.wasm -t localhost/wasmi-instrumented --wasmfile /main.wasm --input $1
