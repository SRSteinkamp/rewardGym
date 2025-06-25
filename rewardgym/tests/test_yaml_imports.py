import warnings

import pytest
import yaml

from rewardgym.tasks.yaml_tools import instantiate_from_config, load_environment_graph


def write_yaml_file(tmp_path, content: dict):
    """Helper to write a YAML file"""
    file = tmp_path / "test_graph.yaml"
    file.write_text(yaml.dump(content))
    return file


def test_list_format(tmp_path):
    yaml_data = {"0": [1, 2, 3], "1": [4, 5]}
    path = write_yaml_file(tmp_path, yaml_data)

    result = load_environment_graph(path)
    assert result == {
        0: [1, 2, 3],
        1: [4, 5],
    }


def test_dict_with_next_and_prob(tmp_path):
    yaml_data = {
        "0": {"1": {"next": [3, 4], "prob": 0.8}, "2": {"next": [5], "prob": 0.2}}
    }
    path = write_yaml_file(tmp_path, yaml_data)

    result = load_environment_graph(path)
    assert result == {0: {1: ([3, 4], 0.8), 2: ([5], 0.2)}}


def test_dict_with_mixed_keys(tmp_path):
    yaml_data = {"0": {"1": {"next": [3], "prob": 1.0}, "skip": True}}
    path = write_yaml_file(tmp_path, yaml_data)

    result = load_environment_graph(path)
    assert result == {0: {1: ([3], 1.0), "skip": True}}


def test_invalid_format_raises(tmp_path):
    yaml_data = {"0": "invalid_string"}
    path = write_yaml_file(tmp_path, yaml_data)

    with pytest.raises(ValueError, match="Unsupported value format"):
        load_environment_graph(path)


def test_empty_graph(tmp_path):
    yaml_data = {}
    path = write_yaml_file(tmp_path, yaml_data)

    result = load_environment_graph(path)
    assert result == {}


def test_key_conversion_to_int(tmp_path):
    yaml_data = {"10": [1, 2], "11": {"3": {"next": [4], "prob": 0.5}}}
    path = write_yaml_file(tmp_path, yaml_data)

    result = load_environment_graph(path)
    assert 10 in result
    assert 11 in result
    assert isinstance(result[11], dict)
    assert 3 in result[11]  # Converted from string to int


# ==== Dummy classes for testing ====
class DummyA:
    def __init__(self, x, y=0):
        self.x = x
        self.y = y


class DummyB:
    def __init__(self, name, value=1):
        self.name = name
        self.value = value


class DummyNested:
    def __init__(self, a: DummyA, b: DummyB):
        self.a = a
        self.b = b


# ==== Class map ====
CLASS_MAP = {
    "DummyA": DummyA,
    "DummyB": DummyB,
    "Nested": DummyNested,
}


# ==== Tests ====


def test_simple_instantiation():
    config = {"class": "DummyA", "x": 10, "y": 20}
    obj = instantiate_from_config(config, CLASS_MAP)
    assert isinstance(obj, DummyA)
    assert obj.x == 10
    assert obj.y == 20


def test_missing_optional_param():
    config = {"class": "DummyB", "name": "test"}
    obj = instantiate_from_config(config, CLASS_MAP)
    assert isinstance(obj, DummyB)
    assert obj.name == "test"
    assert obj.value == 1


def test_injection_of_missing_key():
    config = {"class": "DummyA", "x": 5}
    obj = instantiate_from_config(config, CLASS_MAP, inject_keys={"y": 99})
    assert isinstance(obj, DummyA)
    assert obj.y == 99


def test_injection_does_not_override():
    config = {"class": "DummyA", "x": 5, "y": 2}
    obj = instantiate_from_config(config, CLASS_MAP, inject_keys={"y": 99})
    assert obj.y == 2


def test_nested_instantiation():
    config = {
        "class": "Nested",
        "a": {"class": "DummyA", "x": 1},
        "b": {"class": "DummyB", "name": "nested"},
    }
    obj = instantiate_from_config(config, CLASS_MAP, inject_keys={"y": 7})
    assert isinstance(obj, DummyNested)
    assert isinstance(obj.a, DummyA)
    assert isinstance(obj.b, DummyB)
    assert obj.a.y == 7


def test_list_of_objects():
    config = [{"class": "DummyA", "x": 1}, {"class": "DummyB", "name": "item"}]
    result = instantiate_from_config(config, CLASS_MAP)
    assert isinstance(result, list)
    assert isinstance(result[0], DummyA)
    assert isinstance(result[1], DummyB)


def test_deeply_nested_dict():
    config = {"layer1": {"layer2": {"class": "DummyA", "x": 42}}}
    result = instantiate_from_config(config, CLASS_MAP)
    assert isinstance(result["layer1"]["layer2"], DummyA)
    assert result["layer1"]["layer2"].x == 42


def test_alternative_class_key():
    config = {"type": "DummyA", "x": 123}
    obj = instantiate_from_config(config, CLASS_MAP, class_keys=["type"])
    assert isinstance(obj, DummyA)
    assert obj.x == 123


def test_class_not_found_error():
    config = {"class": "UnknownClass", "x": 0}
    with pytest.raises(ValueError, match="Unknown class/type 'UnknownClass'"):
        instantiate_from_config(config, CLASS_MAP)


def test_non_dict_or_list_value():
    config = 42  # scalar
    result = instantiate_from_config(config, CLASS_MAP)
    assert result == 42


def test_ignores_invalid_injected_key():
    class DummyC:
        def __init__(self, foo):
            self.foo = foo

    config = {"class": "DummyC", "foo": 1}

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = instantiate_from_config(
            config, {"DummyC": DummyC}, inject_keys={"badkey": 123}
        )

        assert isinstance(result, DummyC)
        assert result.foo == 1
        assert len(w) == 1
        assert "Ignoring injected key 'badkey'" in str(w[0].message)
