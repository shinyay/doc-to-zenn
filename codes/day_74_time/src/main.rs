use time::OffsetDateTime;
fn main() {
    let now = OffsetDateTime::now_utc();
    println!("Hello, world at {now}");
}
