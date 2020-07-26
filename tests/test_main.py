import os
import pathlib

import pytest
from ruamel import yaml

import expense_viewer.main as main
import expense_viewer.exceptions as exceptions


def test_read_yaml_file_contents():
    """Test that loading of a yaml file works."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    test_yaml_file = pathlib.Path(current_dir) / "test_data/yaml_test_file.yaml"
    yaml_contents = main.read_yaml_file_contents(test_yaml_file)
    assert yaml_contents == [
        "Casablanca",
        "North by Northwest",
        "The Man Who Wasn't There",
    ]


def test_reading_yaml_error_for_nonexistent_file():
    """Test that loading yaml file gives CouldNotLoadYamlFileError error."""
    yaml_file = pathlib.Path("non_existent_file.yaml")
    with pytest.raises(exceptions.CouldNotLoadYamlFileError):
        main.read_yaml_file_contents(yaml_file)
