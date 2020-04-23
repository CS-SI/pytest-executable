def test_fixture(tolerances):
    assert tolerances["field_name"].abs == 123.0
    assert tolerances["field_name"].rel == 0.0
