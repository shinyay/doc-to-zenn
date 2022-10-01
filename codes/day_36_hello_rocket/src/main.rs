#[macro_use] extern crate rocket;

#[get("/hello")]
fn index() -> &'static str {
    "Hello, Rocket"
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index])
        .mount("/test", routes![index])
}