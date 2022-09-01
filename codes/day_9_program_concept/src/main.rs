fn main() {
    // Checking Mutability
    let mut x = "Hello World";
    println!("xの値は {} です", x);
    x = "Hello Rust";
    println!("xの値は {} です", x);

    // Checking Shadowing
    let x = 1;
    let x = x + 2;
    {
        let x = x * 3;
        println!("インナースコープの値: {}", x);
    }
    println!("アウタースコープの値: {}", x);

    // Checking Tuple
    let tup = (100, 2.3, 4);
    let (x, y, z) = tup;
    println!("yの値: {}", y);
    println!("3番目の値: {}", tup.2);

    let s1 = String::from("Hello, Rust!");
    let s2 = s1;
//    println!("s1は{}です。", s1);
    println!("s2は{}です。", s2);
}

