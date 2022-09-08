fn main() {
    println!("Hello, world!");
    
    let foo = Foo;
    let bar = Bar;
    let baz = Baz { message: "Hello, Bazz".to_owned() };

    foo.do_something();
    Bar::do_something(&bar);

    FooBarBaz::do_something(&foo);
    FooBarBaz::do_something(&bar);
    FooBarBaz::do_something(&baz);

    println!("Message: {}", foo.hello());
    println!("Message: {}", bar.hello());
    println!("Message: {}", baz.hello());
}

trait FooBarBaz {
    fn do_something(&self);
    fn hello(&self) -> &str;
}

struct Foo;
impl FooBarBaz for Foo {
    fn do_something(&self) {
        println!("Foo");
    }
    fn hello(&self) -> &str {
        "Hello, Foo"
    }
}

struct Bar;
impl FooBarBaz for Bar {
    fn do_something(&self) {
        println!("Bar");
    }
    fn hello(&self) -> &str {
        "Hello, bar"
    }
}

struct Baz {
    message: String
}

impl FooBarBaz for Baz {
    fn do_something(&self) {
        println!("Baz");
    }
    fn hello(&self) -> &str {
        &self.message
    }
}