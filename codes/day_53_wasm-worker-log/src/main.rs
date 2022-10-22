use anyhow::Result;
use wasm_workers_rs::{handler, http::{self, Request, Response}};
use serde_json;

#[handler]
fn reply(req: Request<String>) -> Result<Response<String>> {

    debug
    
    Ok(http::Response::builder()
    .status(200)
    .header("x-generated-by", "wasm-workers-server")
    .body(String::from("Hello Wasm!").into())?)
}