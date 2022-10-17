fn main() {
    let s_str: &str = "This is str";
    let s_string: String = String::from("This is String");

    println!("str: {}", s_str);
    println!("String: {}", s_string);

    let mut s_mut_str: &str = "This is mutable str";
    s_mut_str = "This is not immutable str";
    println!("str: {}", s_mut_str);

    let mut s_mut_string1: String = String::from("Hello");
    let mut s_mut_string2: String = String::from(", Rust");
    s_mut_string1 += s_mut_string2;

    println!("String: {}", s_mut_string1);
}
