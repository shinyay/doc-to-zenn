fn main() {
    // call_panic();
    // call_unwrap();
    // call_expect();
    call_expect_err();
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

fn call_expect() {
    // OK
    let x: Result<u32, &str> = Err("emergency failure");
    x.expect("Testing expect");

    // ERROR
    let path = std::env::var("IMPORTANT_PATH")
.expect("env variable `IMPORTANT_PATH` should be set by `wrapper_script.sh`");
}

fn call_expect_err() {
    let x: Result<u32, &str> = Ok(10);
    x.expect_err("Testing expect_err");
}