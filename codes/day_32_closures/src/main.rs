fn main() {

    fn do_function(i: u32) -> u32 {
        i + 1
    }

    println!("関数: {}", do_function(1));

    let do_closure_annotated = |i: u32| -> u32 { i + 1};

    println!("クロージャ: {}", do_closure_annotated(2));
}
