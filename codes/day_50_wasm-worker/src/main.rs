use anyhow::Result;
use wasm_workers_rs::{handler, http::{self, Request, Response}};

#[handler]
fn reply(req: Request<String>) -> Result<Response<String>> {
    Ok(http::Response::builder()
    .status(200)
    .header("x-generated-by", "wasm-workers-server")
    .body(String::from("Hello Wasm!").into())?)
}