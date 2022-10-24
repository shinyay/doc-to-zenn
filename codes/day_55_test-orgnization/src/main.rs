fn main() {
    println!("Hello, world!");
    println!("2 + 4 = {}", add(2, 4).to_string());
    println!("4 - 2 = {}", sub(4, 2).to_string());

}

fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn sub(a: i32, b: i32) -> i32 {
    a - b
}