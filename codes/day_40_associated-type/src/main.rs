struct Point(i32, i32);

trait Position<X, Y> {
    fn exist(&self, _: &X, _: &Y) -> bool;
    fn h_axis(&self) -> i32;
    fn v_axis(&self) -> i32;
}

impl Position<i32, i32> for Point{
    fn exist(&self, x: &i32, y: &i32) -> bool {
        (&self.0 == x) && (&self.1 == y)
    }

   fn h_axis(&self) -> i32 {
        self.0
    }

    fn v_axis(&self) -> i32 {
        self.1
    }
}

fn main() {
    let x = 5;
    let y = 10;

    let point = Point(x, y);

    println!("Point X:{}, Y:{}", x, y);
}
