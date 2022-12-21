use std::env;
use std::net::SocketAddr;
use axum::response::IntoResponse;
use axum::{Router, Json};
use axum::routing::{get, post};
use axum::http::StatusCode;
use serde::Deserialize;
use serde::Serialize;

#[tokio::main]
async fn main() {

    let log_level = env::var("RUST_LOG").unwrap_or("info".to_string());
    env::set_var("RUST_LOG", log_level);
    tracing_subscriber::fmt::init();

    let app = Router::new()
    .route("/", get(root))
    .route("/users", post(create_user));

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    tracing::debug!("listening on {}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn root() -> &'static str {
    "Hello, axum!"
}

async fn create_user (Json(payload): Json<CreateUser>) -> impl IntoResponse {
    let user = User {
        id: 1111,
        username: payload.username,
    };
    (StatusCode::CREATED, Json(user))
}

#[derive(Deserialize)]
struct CreateUser {
    username: String,
}

#[derive(Serialize)]
struct User {
    id: u64,
    username: String,
}