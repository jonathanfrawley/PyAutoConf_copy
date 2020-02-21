import pytest

import autoconf as ac


class MyClass:
    def __init__(self, one, two):
        self.one = one
        self.two = two


@pytest.fixture(name="my_class_config")
def make_my_class_config():
    return {
        "one": ac.default_prior,
        "two": ac.default_prior
    }


def test_make_config(my_class_config):
    path, value = ac.make_config_for_class(
        MyClass
    )
    assert path == ["test_autoconf", "json_prior", "test_generation", "MyClass"]
    assert value == my_class_config


@pytest.fixture(
    name="filename"
)
def make_filename():
    return "priors.json"


@pytest.fixture(
    name="config"
)
def make_config(filename):
    return ac.JSONPriorConfig(
        {
            "test_autoconf.json_prior.test_generation.AnotherClass": {
                "attribute": {}
            }
        },
        directory=filename
    )


@pytest.fixture(
    name="result",
    autouse=True
)
def make_result(config):
    return config.for_class_and_suffix_path(
        MyClass,
        ["one"]
    )


def test_generate(result):
    assert result == ac.default_prior


def test_rearrange(config, my_class_config):
    assert config.obj == {
        "test_autoconf.json_prior.test_generation": {
            "MyClass": my_class_config,
            "AnotherClass": {
                "attribute": {}
            }
        }
    }
