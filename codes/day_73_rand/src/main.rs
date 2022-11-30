use rand::{Rng, seq::SliceRandom, distributions::{Alphanumeric, Uniform}, prelude::Distribution};

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

    for n in 1..10 {
        let chars: String = (0..7).map(|_| rng.sample(Alphanumeric) as char).collect();
        println!("ランダムキャラクター{}: {}", n, chars);
    }

    let between = Uniform::from(10..10000);
    for _ in 0..10 {
        println!("{}", between.sample(&mut rng));
    }


}
