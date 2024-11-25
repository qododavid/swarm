from swarm.util import function_to_json

from swarm.util import merge_chunk
from swarm.util import merge_fields
from swarm.util import debug_print

def test_basic_function():
    def basic_function(arg1, arg2):
        return arg1 + arg2

    result = function_to_json(basic_function)
    assert result == {
        "type": "function",
        "function": {
            "name": "basic_function",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {"type": "string"},
                    "arg2": {"type": "string"},
                },
                "required": ["arg1", "arg2"],
            },
        },
    }


def test_complex_function():
    def complex_function_with_types_and_descriptions(
        arg1: int, arg2: str, arg3: float = 3.14, arg4: bool = False
    ):
        """This is a complex function with a docstring."""
        pass

    result = function_to_json(complex_function_with_types_and_descriptions)
    assert result == {
        "type": "function",
        "function": {
            "name": "complex_function_with_types_and_descriptions",
            "description": "This is a complex function with a docstring.",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {"type": "integer"},
                    "arg2": {"type": "string"},
                    "arg3": {"type": "number"},
                    "arg4": {"type": "boolean"},
                },
                "required": ["arg1", "arg2"],
            },
        },
    }

def test_merge_fields_nested_dict():
    target = {"key1": {"subkey1": "Hello"}}
    source = {"key1": {"subkey1": " World"}}
    merge_fields(target, source)
    assert target["key1"]["subkey1"] == "Hello World"


def test_merge_chunk_with_tool_calls():
    final_response = {"tool_calls": [{}, {"key": "value"}]}
    delta = {"tool_calls": [{"index": 1, "key": " new_value"}]}
    merge_chunk(final_response, delta)
    assert final_response["tool_calls"][1]["key"] == "value new_value"


def test_merge_fields_string_concatenation():
    target = {"key1": "Hello"}
    source = {"key1": " World"}
    merge_fields(target, source)
    assert target["key1"] == "Hello World"


def test_debug_print_with_output(capsys):
    debug_print(True, "This message should appear")
    captured = capsys.readouterr()
    assert "This message should appear" in captured.out
    assert "[" in captured.out and "]" in captured.out  # Check for timestamp brackets


def test_debug_print_no_output(capsys):
    debug_print(False, "This message should not appear")
    captured = capsys.readouterr()
    assert captured.out == ""

