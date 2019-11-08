docker run -v $(pwd)/main.wasm:/main.wasm -t localhost/wasmi --wasmfile /main.wasm --input $1
