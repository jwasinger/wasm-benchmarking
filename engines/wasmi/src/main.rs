extern crate rustc_hex;
extern crate wasmi;

#[macro_use]
extern crate clap;

use std::time::{Duration, Instant};
use rustc_hex::FromHex;
use serde::{Deserialize, Serialize};
use std::env;
use std::fs::File;
use wasmi::memory_units::Pages;
use wasmi::{
    Error as InterpreterError, Externals, FuncInstance, FuncRef, ImportsBuilder, MemoryInstance,
    MemoryRef, Module, ModuleImportResolver, ModuleInstance, NopExternals, RuntimeArgs,
    RuntimeValue, Signature, Trap, TrapKind, ValueType,
};
use clap::{Arg, App, SubCommand};

struct Runtime<'a> {
    memory: Option<MemoryRef>,
    block_data: &'a [u8],
}

impl<'a> Runtime<'a> {
    fn new(
        block_data: &'a [u8],
        memory: Option<MemoryRef>,
    ) -> Runtime<'a> {
        Runtime {
            memory: if memory.is_some() {
                memory
            } else {
                // Allocate a single page if no memory was exported.
                Some(MemoryInstance::alloc(Pages(1), Some(Pages(1))).unwrap())
            },
            block_data: block_data
        }
    }
}

impl<'a> Externals for Runtime<'a> {
    fn invoke_index(
        &mut self,
        index: usize,
        args: RuntimeArgs,
    ) -> Result<Option<RuntimeValue>, Trap> {
        //println!("invoking index {}", index);
        match index {
            // TODO why are these indices reversed compared to the order of the functions in the wat
            1 => {
                let ret: i32 = self.block_data.len() as i32;
                //println!("blockdatasize {}", ret);
                Ok(Some(ret.into()))
            },
            0 => {
                let ptr: u32 = args.nth(0);
                let offset: u32 = args.nth(1);
                let length: u32 = args.nth(2);
                println!(
                    "blockdatacopy to {} from {} for {} bytes",
                    ptr, offset, length
                );

                // TODO: add overflow check
                let offset = offset as usize;
                let length = length as usize;

                // TODO: add checks for out of bounds access
                let memory = self.memory.as_ref().expect("expects memory object");
                memory
                    .set(ptr, &self.block_data[offset..length])
                    .expect("expects writing to memory to succeed");

                Ok(None)
            },
            PUSHNEWDEPOSIT_FUNC_INDEX => unimplemented!(),
            _ => panic!("unknown function index"),
        }
    }
}

struct RuntimeModuleImportResolver;

impl<'a> ModuleImportResolver for RuntimeModuleImportResolver {
    fn resolve_func(
        &self,
        field_name: &str,
        _signature: &Signature,
    ) -> Result<FuncRef, InterpreterError> {
        let func_ref = match field_name {
            "inputDataCopy" => FuncInstance::alloc_host(
                Signature::new(&[ValueType::I32, ValueType::I32, ValueType::I32][..], None),
                0,
            ),
            "getInputDataSize" => FuncInstance::alloc_host(
                Signature::new(&[][..], Some(ValueType::I32)),
                1,
            ),
            _ => {
                return Err(InterpreterError::Function(format!(
                    "host module doesn't export function with name {}",
                    field_name
                )))
            }
        };
        Ok(func_ref)
    }
}

pub fn execute_code(
    code: &[u8],
    block_data: &[u8],
) {
    let module = Module::from_buffer(&code).expect("Module loading to succeed");
    let mut imports = ImportsBuilder::new();
    // FIXME: use eth2
    imports.push_resolver("env", &RuntimeModuleImportResolver);

    let instance = ModuleInstance::new(&module, &imports)
        .expect("Module instantation expected to succeed")
        .assert_no_start();

    let internal_mem = instance
        .export_by_name("memory")
        .expect("Module expected to have 'memory' export")
        .as_memory()
        .cloned()
        .expect("'memory' export should be a memory");

    let mut runtime = Runtime::new(block_data, Some(internal_mem));

    let now = Instant::now();

    let result = instance
        .invoke_export("main", &[], &mut runtime)
        .expect("Executed 'main'");

    println!("execution time: {} microseconds", now.elapsed().as_micros());
}

fn load_file(filename: &str) -> Vec<u8> {
    use std::io::prelude::*;
    let mut file = File::open(filename).expect("loading file failed");
    let mut buf = Vec::new();
    file.read_to_end(&mut buf).expect("reading file failed");
    buf
}

fn main() {
    let matches = App::new("My Super Program")
                          .version("1.0")
                          .author("Kevin K. <kbknapp@gmail.com>")
                          .about("Does awesome things")
                          .arg(Arg::with_name("wasmfile")
                               .short("w")
                               .long("wasmfile")
                               .value_name("WASM_FILE")
                               .help("provides the location to a wasm source file")
                               .takes_value(true))
                          .arg(Arg::with_name("input")
                               .short("i")
                               .long("input")
                               .value_name("INPUT")
                               .help("input (hex) to be provided to the engine")
                               .takes_value(true))
                          .get_matches();

    let source = matches.value_of("wasmfile").expect("wasm file argument missing");
    let input = matches.value_of("input").expect("execution input argument missing");
	println!("input is {}", &input);

    let code = load_file(&source);
    let block_data = input.from_hex().expect("could decode input from hex");//[0u8; 32];
    execute_code(&code, &block_data);
}
