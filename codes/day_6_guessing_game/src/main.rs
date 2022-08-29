use std::{io, cmp::Ordering};

use rand::Rng;

fn main() {
    println!("数を予想しましょう。");

    let secret_number = rand::thread_rng().gen_range(1..101);

    println!("生成した値: {}", secret_number);

    println!("予想した値を入力してください。");
    
    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("読み込みに失敗しました。");
        
    println!("次のように予測しています: {}", guess);

    match guess.cmp(&secret_number) {
        Ordering::Less => println!("小さい"),
        Ordering::Greater => println!("大きい"),
        Ordering::Equal => println!("正解!"),        
    }
}
