use thiserror::Error;

#[derive(Debug, Error)]
enum RepositoryError {
    #[error("NotFound, id is {0}")]
    NotFound(i32),
}

fn main() {
    println!("Hello, world!");
}
