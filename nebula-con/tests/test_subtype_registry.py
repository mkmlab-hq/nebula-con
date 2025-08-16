from persona.subtype_registry import REQUIRED_AXES, get_registry


def test_registry_load():
    reg = get_registry()
    codes = reg.list_subtypes()
    assert len(codes) == 12
    for code in codes:
        data = reg.get_subtype(code)
        for ax in REQUIRED_AXES:
            assert ax in data["centroid"]


def test_centroid_matrix_shape():
    reg = get_registry()
    codes, mat = reg.get_centroid_matrix()
    assert mat.shape == (12, len(REQUIRED_AXES))
    assert all(0.0 <= float(x) <= 1.0 for x in mat.flatten())
