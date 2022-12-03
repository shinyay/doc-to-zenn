use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Point {
    x: i32,
    y: i32
}

fn main() {

    let point = Point { x: 1, y: 2};

    let serialized = serde_json::to_string(&point).unwrap();
    println!("シリアライズ: {serialized}");
}
