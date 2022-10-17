fn main() {
    call_unwrap();
    // call_panic();
}

fn call_panic() {
    println!("処理してます - 1");
    panic!("Panicしました！");
    println!("処理してます - 2");
}

fn call_unwrap() {
    // OK
    let x: Result<u32, &str> = Ok(2);
    assert_eq!(x.unwrap(), 2);

    // ERROR
    let x: Result<u32, &str> = Err("emergency failure");
    x.unwrap();
}
