fn main() {
    print_message("Hello, world".to_string());
}

fn print_message(msg: String) -> String {
    println!("{}", msg);
    msg
}

#[test]
fn test_message() {
    assert_eq!("Hello", print_message("Hello".to_string()));
}