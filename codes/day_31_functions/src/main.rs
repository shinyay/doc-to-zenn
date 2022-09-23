fn main() {
}

fn is_divisible_by(x: u32, y: u32) -> b {
    if y == 0 {
        return false;
    }
    x % y == 0
}

fn fizzbuzz(n: u32) -> () {
    if is_divisible_by(n, 15) {
        println!("fizzbuzz");
    } else if is_divisible_by(n, 3) {
        println!("fizz")
    } else if is_divisible_by(n, 5) {
        println!("buzz")
    } else {
        println!("()")
    }
}
