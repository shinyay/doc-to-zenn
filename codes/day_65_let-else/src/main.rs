fn main() {
    let optional = Some(5);

    match optional {
        Some(i) => {
            println!("Matched {:?}!", i)
        },
        _ => {},        
    }

    if let Some(i) = optional {
        println!("Matched {:?}!", i);
    }

    let result = if let Some(i) = optional {
        println!("RESULT {:?}!", i);
    };

    // 変数のxへの束縛範囲

    // if-let文
    if let Some(x) = Some(3) { 
        // ------↓ここから束縛↓------
        assert_eq!(x, 3);
        // ------↑ここまで↑------
    } else {}

    // let-else文
    let Some(x) = Some(4) else {
        return
    };
    // ------↓ここから束縛↓------
    assert_eq!(x, 4);


}
