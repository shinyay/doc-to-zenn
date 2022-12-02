use time::{OffsetDateTime, Date, Time, PrimitiveDateTime, macros::datetime};
fn main() {
    let now = OffsetDateTime::now_utc();
    println!("Hello, world at {now}");

    let now = OffsetDateTime::now_local();
    println!("Hello, world at {:?}", now);

    let date = Date::from_iso_week_date(2022, 48, time::Weekday::Friday).unwrap();
    let datetime: PrimitiveDateTime = date.with_hms(11, 22, 33).unwrap();
    let time = Time::from_hms(11, 22, 33).unwrap();
    println!("Date: {date}");
    println!("Time: {time}");
    println!("DateTime: {datetime}");

    let start = datetime!(2022-01-01 0:00:00);
    let end = datetime!(2022-12-31 23:59:59);
    let duration = end - start;
    println!("{duration}");
}