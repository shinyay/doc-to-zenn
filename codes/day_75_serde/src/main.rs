use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Point {
    x: i32,
    y: i32
}

fn main() {

    let point = Point { x: 1, y: 2};

    println!("Hello, world!");
}
