use std::marker::PhantomData;

struct PhantomStruct<X, A> {
    value: A,
    phantom: PhantomData<X>
}

fn main() {
    println!("Hello, world!");
}
