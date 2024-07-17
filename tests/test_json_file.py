import os
import pytest
from pathlib import Path
from ooj.json_file import JsonFile


# Base path from test JSON files
BASE_PATH = Path('tests/files/test_json_files')


class TestJsonFile:
    @pytest.mark.parametrize(
        "file_path",
        [
            BASE_PATH / "created_file.json",
            BASE_PATH / "not_created_file.json"
        ]
    )
    def test_create_if_not_exists(self, file_path):
        JsonFile(file_path)

        assert file_path.exists()

    @pytest.mark.parametrize(
        "keys_path, value",
        [
            ("key_1", "value_1"),
            (["key_2", "nested_key_2"], "value"),
            ("new_key", "value")
        ]
    )
    def test_set_and_get_value(self, keys_path, value):
        file = JsonFile(BASE_PATH / "set_and_get_value.json")
        file.set_value(keys_path, value)
        assert file.get_value(keys_path) == value

    @pytest.mark.parametrize(
        "keys_path",
        [
            "key",
            ["keys", "nested_key"]
        ]
    )
    def test_remove_key(self, keys_path):
        file = JsonFile(BASE_PATH / "remove_key.json")
        file.set_value(keys_path, "dummy_value")
        file.remove_key(keys_path)
        with pytest.raises(KeyError):
            file.get_value(keys_path)

    @pytest.mark.parametrize(
        "keys_path",
        [
            "key",
            ["keys", "nested_key"]
        ]
    )
    def test_remove_key(self, keys_path):
        file = JsonFile(BASE_PATH / "remove_key.json")
        file.set_value(keys_path, "dummy_value")
        file.remove_key(keys_path)
        with pytest.raises(KeyError):
            file.get_value(keys_path)

    @pytest.mark.parametrize(
        "file_or_dict, range_",
        [
            (JsonFile(BASE_PATH / 'select.json'), range(0, 10)),
            (
                {"key1": 0, "key2": 12, "key3": -8,
                "key4": 4, "key5": 2, "key6": -5,
                "key7": -3, "key8": 7, "key9": -84,
                "key10": 9},
                range(-10, 0)
            )
        ]
    )
    def test_select(self, file_or_dict, range_):
        data = JsonFile.select(file_or_dict, range_)

        keys = []
        if isinstance(data, JsonFile):
            for key, value in data.read().items():
                if value in range_:
                    keys.append(key)

            assert data.read()[keys[0]] in range_

        elif isinstance(data, dict):
            for key, value in data.items():
                if value in range_:
                    keys.append(key)

            assert data[keys[0]] in range_