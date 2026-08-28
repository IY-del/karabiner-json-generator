from collections.abc import Iterable
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Identifier = Literal[
    "caps_lock",
    "command",
    "control",
    "fn",
    "left_command",
    "left_control",
    "left_option",
    "left_shift",
    "option",
    "right_command",
    "right_control",
    "right_option",
    "right_shift",
    "shift",
]


class Modifier(BaseModel):
    optional: Iterable[Identifier] | None = None


class From(BaseModel):
    key_code: str
    modifiers: Modifier | None = None


class To(BaseModel):
    key_code: str


class Manipulator(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["basic"] = "basic"
    from_: From = Field(alias="from")
    to: Iterable[To]


class Rule(BaseModel):
    description: str
    manipulators: Iterable[Manipulator]


class ComplexModifications(BaseModel):
    title: str
    rules: Iterable[Rule]
