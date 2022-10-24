use day_55_test;
#[test]
fn integration_test() {
    assert_eq!(3,day_55_test::sub(day_55_test::add(3, 6), day_55_test::add(2, 4)));
}