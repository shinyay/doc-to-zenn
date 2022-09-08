fn main() {
    println!("Hello, world!");
    
    let foo = Foo;
    let bar = Bar;
    let baz = Baz;

    foo.do_something();
    Bar::do_something(&bar);
    FooBarBaz::do_something(&baz);
}

trait FooBarBaz {
    fn do_something(&self);
}

struct Foo;
impl FooBarBaz for Foo {
    fn do_something(&self) {
        println!("Foo");
    }
}

struct Bar;
impl FooBarBaz for Bar {
    fn do_something(&self) {
        println!("Bar");
    }
}

struct Baz;
impl FooBarBaz for Baz {
    fn do_something(&self) {
        println!("Baz");
    }
}