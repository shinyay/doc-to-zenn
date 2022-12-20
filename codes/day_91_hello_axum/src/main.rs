use std::net::SocketAddr;

use axum::Router;
use axum::routing::get;

#[tokio::main]
async fn main() {

    let app = Router::new().route("/", get(root));
    let addr = SocketAddr::from(([127, 9, 0, 1], 3000));

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn root() -> &'static str {
    "Hello, axum!"
}