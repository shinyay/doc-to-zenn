struct Rectangle {
    hight: u32,
    widthe: u32,
}

impl Rectangle {
    fn new(h: u32, w: u32) -> Rectangle {
        Rectangle { hight: h, widthe: w }
    }

    fn area(&self) ->u32 {
        self.hight * self.widthe
    }
}

pub fn rectangle_main() {
    let rec = Rectangle::new(3, 5);

    print!("Height={}, Width={}, Area={}", rec.hight, rec.widthe, rec.area());
}