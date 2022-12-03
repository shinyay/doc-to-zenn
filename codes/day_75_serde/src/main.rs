use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Point {
    x: i32,
    y: i32
}

fn main() {

    println!("Hello, world!");
}
