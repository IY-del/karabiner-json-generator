from schemas import (
    ComplexModifications,
    From,
    Manipulator,
    Modifier,
    Rule,
    To,
)

def parse_layout(name: str, mapping: dict[str, str]) -> ComplexModifications:
    manipulators = [
        Manipulator(
            from_=From( # type: ignore
                key_code=from_key,
                modifiers=Modifier(
                    optional=["shift", "caps_lock"],
                ),
            ),
            to=[
                To(
                    key_code=to_key,
                )
            ],
        )
        for from_key, to_key in mapping.items()
    ]

    return ComplexModifications(
        title=name,
        rules=[
            Rule(
                description=name,
                manipulators=manipulators,
            )
        ],
    )
