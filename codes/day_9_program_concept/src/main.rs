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
}
