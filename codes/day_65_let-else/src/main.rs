fn main() {
    let optional = Some(5);
    match optional {
        Some(i) => {
            println!("Matched {:?}!", i)
        },
        _ => {},        
    }
}
