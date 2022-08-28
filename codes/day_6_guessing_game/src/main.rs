use std::io;

fn main() {
    println!("数を予想しましょう。");
    println!("予想した値を入力してください。");
    
    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("読み込みに失敗しました。");
        
    println!("次のように予測しています: {}", guess);
}
