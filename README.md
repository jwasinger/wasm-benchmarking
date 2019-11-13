# wasm-metering

Utilities for benchmarking and analysis of webassembly engines

## Setup

Docker and Python 3.7 should be installed as prerequisites

```
pipenv shell
pipenv install
```

Build docker images for wasm engines:
`bash build_engine_images.sh`

## Usage

### Generate Benchmarking Datasets

`python main.py benchmark -c`

### Do Regression Analysis on a Dataset

`python main.py analyse -f /path/to/dataset.json`

## Supported engines

Wasmi - https://github.com/paritytech/wasmi

## Benchmark Wasm Format

Wasm blobs used for benchmarking should conform to a standard environment interface.  Currently two host functions are exposed to the wasm runtime:
- `inputDataCopy(ptr: u32, offset: u32, length: u32)`: copy `length` bytes of input data passed from the host (starting at `offset`) into memory at `ptr`
- `inputDataSize() -> u32`: return the size of input data passed from the host
