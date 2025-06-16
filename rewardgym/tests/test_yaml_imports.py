import pytest
import yaml

from rewardgym.tasks.yaml_tools import load_environment_graph


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
