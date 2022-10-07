use std::marker::PhantomData;

#[derive(Debug,PartialEq)]
struct PhantomStruct<X, A> {
    value: A,
    phantom: PhantomData<X>
}

fn main() {
    let _phantom1: PhantomStruct<i32, char> = PhantomStruct {
        value: 'P', 
        phantom: PhantomData
    };

    let _phantom2: PhantomStruct<i64, char> = PhantomStruct {
        value: 'P', 
        phantom: PhantomData
     };

    println!("_phantom1 == _phantom2: {}", _phantom1 == _phantom2);
}
