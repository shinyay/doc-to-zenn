use std::net::TcpListener;

fn main() {
    let listner = TcpListener::bind("127.0.0.1:8080").unwrap();

    for stream in listner.incoming() {
        let stream = stream.unwrap();
        println!("接続確立!");
    }
}
