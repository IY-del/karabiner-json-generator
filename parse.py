from typing import TypeIs
from schemas import (
    ComplexModifications,
    From,
    Manipulator,
    Modifier,
    Rule,
    To,
)

type Mappings = dict[str, dict[str, str]]
type SingleMapping = dict[str, str]
type RawMappings = Mappings | SingleMapping

def is_single_mapping(mappings: RawMappings) -> TypeIs[SingleMapping]:
    return all(isinstance(value, str) for value in mappings.values())

def normalize_mappings(name, mappings: RawMappings) -> Mappings:
    if is_single_mapping(mappings):
        return {name: mappings}
    if all(isinstance(value, dict) for value in mappings.values()):
        return mappings
    raise TypeError(f"Invalid mappings for {name}: {mappings}")

def parse_layout(name: str, mappings: RawMappings) -> ComplexModifications:
    return ComplexModifications(
        title=name,
        rules=tuple(
            Rule(
                description=rule_name,
                manipulators=tuple(
                    Manipulator(
                        from_=From( # type: ignore
                            key_code=from_key,
                            modifiers=Modifier(
                                optional=["shift", "caps_lock"],
                            ),
                        ),
                        to=tuple(
                            To(
                                key_code=to_key,
                            )
                        )
                    )
                    for from_key, to_key in mapping.items()
                )
            )
            for rule_name, mapping in normalize_mappings(name, mappings).items()
        )
    )
