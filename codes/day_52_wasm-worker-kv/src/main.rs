use anyhow::Result;
use wasm_workers_rs::{handler, http::{self, Request, Response}, cache::Cache};

fn reply(req: Request<String>, cache: &mut Cache) -> Result<Response<String>> {

    let count = cache.get("counter");
    let count_num = match count {
        Some(_) => todo!(),
        None => todo!(),
    };

    Ok(http::Response::builder()
        .status(200)
        .header("x-generated-by", "wasm-workers-server")
        .body(String::from("Hello Wasm!").into())?)
}