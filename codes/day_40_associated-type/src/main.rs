struct Point(i32, i32);

// trait Position<X, Y> {
//     fn exist(&self, _: &X, _: &Y) -> bool;
//     fn h_axis(&self) -> i32;
//     fn v_axis(&self) -> i32;
// }

trait Position {

    type X;
    type Y;

    fn exist(&self, _: &Self::X, _: &Self::Y) -> bool;
    fn h_axis(&self) -> i32;
    fn v_axis(&self) -> i32;
}

// impl Position<i32, i32> for Point{
//     fn exist(&self, x: &i32, y: &i32) -> bool {
//         (&self.0 == x) && (&self.1 == y)
//     }

//    fn h_axis(&self) -> i32 {
//         self.0
//     }

//     fn v_axis(&self) -> i32 {
//         self.1
//     }
// }

impl Position for Point{

    type X = i32;
    type Y = i32;

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

// fn new_point<X, Y, Z>(point: &Z) where Z: Position<X, Y> {
//     println!("POINT:({},{})", point.v_axis(), point.h_axis())
// }

fn new_point<Z: Position>(point: &Z) {
    println!("POINT:({},{})", point.v_axis(), point.h_axis())
}

fn main() {
    let x = 5;
    let y = 10;

    let point = Point(x, y);

    println!("Point X:{}, Y:{}", &x, &y);
    println!("Exist?:{}", point.exist(&x, &y));

    println!("Point-X:{}", point.v_axis());
    println!("Point-Y:{}", point.h_axis());

    new_point(&point);
}
