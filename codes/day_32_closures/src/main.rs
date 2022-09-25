fn main() {

    fn do_function(i: u32) -> u32 {
        i + 1
    }
    println!("関数: {}", do_function(1));

    let do_closure_annotated = |i: u32| -> u32 { i + 1};
    println!("クロージャ: {}", do_closure_annotated(2));

    // 型アノテーションの省略
    let do_clusre_inferred = |i| i + 1;
    println!("クロージャ(短縮): {}", do_clusre_inferred(3));

    let outer_scope = String::from("スコープ");
    let print = ||println!("スコープ: {}", outer_scope);
    print();

    let second_scope = &outer_scope;
    print();
    let second_print = ||println!("借用したスコープ: {}", second_scope);
    second_print();

    // 参照
    let greeting = "Hello";
    // 値
    let mut bye_greeting = "Bye".to_owned();

    let greeting_fn = || {
        // 参照に対する処理のため、Fn が必要
        println!("挨拶(fn): {}", greeting);
    };

    let greeting_mut = || {
        // 値の変更をするため、FnMut が必要
        bye_greeting.push_str("!!");
        println!("挨拶(mut): {}", bye_greeting);
    };

    apply(greeting_fn);
    apply_mut(greeting_mut);
}

fn apply_once<F>(f: F) where F: FnOnce() {
    f();
}

fn apply_mut<F>(mut f: F) where F: FnMut() {
    f();
}

fn apply<F>(f: F) where F: Fn() {
    f();
}

fn create_fn() -> impl Fn() {
    let text = "Fn".to_owned();

    move || println!("This is a: {}", text)
}

fn create_fnmut() -> impl FnMut() {
    let text = "FnMut".to_owned();

    move || println!("This is a: {}", text)
}

fn create_fnonce() -> impl FnOnce() {
    let text = "FnOnce".to_owned();

    move || println!("This is a: {}", text)
}