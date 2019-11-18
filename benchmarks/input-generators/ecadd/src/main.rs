use rand::{thread_rng, Rng};
use bn::{G1, AffineG1, G2, Fr, Group, Fq};
use bn::arith::U256;

use rustc_hex::{ToHex, FromHex};
//use rustc_serialize::hex::FromHex;
use hex::encode;

fn format_point(p: &AffineG1) -> Vec<u8> {
    let mut result = p.x().into_u256().0[1].to_be_bytes().to_vec();
    result.extend(p.x().into_u256().0[0].to_be_bytes().to_vec());
    result.extend(p.y().into_u256().0[1].to_be_bytes().to_vec());
    result.extend(p.y().into_u256().0[0].to_be_bytes().to_vec());
    result
    /*
    &format!("{:x}", &p.x().into_u256().0[1]) +
    &format!("{:x}", &p.y().into_u256().0[0]) +
    &format!("{:x}", &p.y().into_u256().0[1]) */
}

fn main() {
    let mut rng = thread_rng();
    
    for i in 0..20 {
        let p1 = AffineG1::from_jacobian(G1::one() * Fr::random(&mut rng)).expect("couldn't convert to jacobian");
        let p2 = AffineG1::from_jacobian(G1::one() * Fr::random(&mut rng)).expect("couldn't convert to jacobian");
        // let p3 = p1 + p2;

        //println!("p1/2 is: ");
        //println!("{}{}", format_point(&p1), format_point(&p2));
        let mut formatted_input = format_point(&p1);
        formatted_input.extend(&format_point(&p2));
        // let formatted_input = ().from_hex().expect("wasn't valid hex");

        println!("{}", encode(&formatted_input));
        let mut output = [0u8; 64];

		match ethereum_bn128::bn128_add(&formatted_input[..], &mut output) {
			Ok(_) => {},
			Err(e) => panic!(e),
		}
    }

    //println!("{:?}", p2);
}
