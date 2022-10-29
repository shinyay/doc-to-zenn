use anyhow::Result;
use spin_sdk::{
    http::{Request, Response},
    http_component,
};

/// A simple Spin HTTP component.
#[http_component]
fn hello_spin(req: Request) -> Result<Response> {
    println!("{:?}", req.headers());

    let query_string = req.uri().query();
    let reply_body = match query_string {
        Some(s) => format!("Hello {s}!"),
        None => "誰ですか？".to_string(),
    };

    Ok(http::Response::builder()
        .status(200)
        .header("foo", "bar")
        .body(Some(reply_body.into()))?)
}
