use time::{OffsetDateTime, Date, Time};
fn main() {
    let now = OffsetDateTime::now_utc();
    println!("Hello, world at {now}");

    let now = OffsetDateTime::now_local();
    println!("Hello, world at {:?}", now);

    let date = Date::from_iso_week_date(2022, 48, time::Weekday::Friday).unwrap();
    let datetime = date.with_hms(11, 22, 33).unwrap();
    let time = Time::from_hms(11, 22, 33).unwrap();
    println!("Date: {date}");
    println!("Time: {time}");
    println!("DateTime: {datetime}");
}