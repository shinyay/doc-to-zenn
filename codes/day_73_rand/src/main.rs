use rand::{Rng, seq::SliceRandom};

fn main() {

    let mut rng = rand::thread_rng();
   
    for n in 1..10 {
        let x: i32 = rng.gen();
        println!("{}: {}", n, x);
    }
    println!("{:?}", rng.gen::<(f64, bool)>());


    let choices = [1, 2, 4, 8, 16, 32, 64, 256];
    for n in 1..10 {
            println!("{}, {:?}",n, choices.choose(&mut rng));
    }

    let mut y = [1, 2, 3, 4, 5];
    println!("シャッフル前: {:?}", y);
    y.shuffle(&mut rng);
    println!("シャッフル後: {:?}", y);
}
