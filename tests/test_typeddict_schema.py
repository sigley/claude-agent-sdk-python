from __future__ import annotations

import sys
from typing import Annotated

if sys.version_info >= (3, 11):
    from typing import NotRequired, Required, TypedDict
else:
    from typing_extensions import NotRequired, Required, TypedDict

from claude_agent_sdk import _typeddict_to_json_schema


class TotalParams(TypedDict):
    query: str
    limit: NotRequired[int]
    detail: Annotated[NotRequired[str], "Optional detail"]


class PartialParams(TypedDict, total=False):
    query: Required[str]
    timeout: Annotated[Required[int], "Timeout in seconds"]
    detail: str


def test_postponed_annotations_preserve_not_required_fields() -> None:
    schema = _typeddict_to_json_schema(TotalParams)

    assert schema["required"] == ["query"]
    assert schema["properties"]["limit"] == {"type": "integer"}
    assert schema["properties"]["detail"] == {
        "type": "string",
        "description": "Optional detail",
    }


def test_postponed_annotations_preserve_required_fields() -> None:
    schema = _typeddict_to_json_schema(PartialParams)

    assert schema["required"] == ["query", "timeout"]
    assert schema["properties"]["timeout"] == {
        "type": "integer",
        "description": "Timeout in seconds",
    }
    assert "detail" not in schema["required"]
