use rand::Rng;

fn main() {

    let mut rng = rand::thread_rng();
   
    for n in 1..10 {
        let x: i32 = rng.gen();
        println!("{}", x);
    }
    println!("{:?}", rng.gen::<(f64, bool)>());
}
