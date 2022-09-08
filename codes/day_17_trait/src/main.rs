fn main() {
    println!("Hello, world!");
}

trait FooBarBaz {
    fn doSomething(&self);
}

struct Foo;
impl FooBarBaz for Foo {
    fn doSomething(&self) {
        println!("Foo");
    }
}

struct Bar;
impl FooBarBaz for Bar {
    fn doSomething(&self) {
        println!("Bar");
    }
}

struct Baz;
impl FooBarBaz for Baz {
    fn doSomething(&self) {
        println!("Baz");
    }
}