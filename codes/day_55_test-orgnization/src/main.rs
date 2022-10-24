fn main() {
    println!("Hello, world!");
    println!("2 + 4 = {}", add(2, 4).to_string());
    println!("4 - 2 = {}", sub(4, 2).to_string());

}

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

pub fn sub(a: i32, b: i32) -> i32 {
    a - b
}

pub fn hello() -> &'static str {
    "test"
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn should_added_number_when_two_numbers() {
        assert_eq!(9, add(3, 6))
    }

    #[test]
    fn should_subtracted_number_when_two_numbers() {
        assert_eq!(3, sub(6, 3))
    }
}