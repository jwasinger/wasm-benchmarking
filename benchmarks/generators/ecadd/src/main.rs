#[cfg(not(test))]
#[no_mangle]
pub extern "C" fn main() {
    let input = ewasm_api::calldata_acquire();

    let mut output = [0u8; 64];
    match ethereum_bn128::bn128_add(&input[..], &mut output) {
        Ok(_) => {},
        Err(_) => panic!(),
    }
}
