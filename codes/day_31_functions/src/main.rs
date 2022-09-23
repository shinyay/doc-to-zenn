pub mod rectangle;

fn main() {
    fizzbyzz_to(30);
    rectangle::rectangle_main();
}

fn is_divisible_by(x: u32, y: u32) -> bool {
    if y == 0 {
        return false;
    }
    x % y == 0
}

fn fizzbuzz(n: u32) -> () {
    if is_divisible_by(n, 15) {
        println!("{}: fizzbuzz", n);
    } else if is_divisible_by(n, 3) {
        println!("{}: fizz", n)
    } else if is_divisible_by(n, 5) {
        println!("{}: buzz", n)
    } else {
        println!("{}: ()", n)
    }
}

fn fizzbyzz_to(upper_limit: u32) {
    for e in 1..=upper_limit {
        fizzbuzz(e)
    }
}