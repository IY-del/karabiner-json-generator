from collections.abc import Iterable
from pathlib import Path

import yaml
from pydantic import BaseModel


def find_yaml_paths(input_path: Path) -> Iterable[Path]:
    if input_path.is_file():
        if input_path.suffix not in {".yaml", ".yml"}:
            raise ValueError(f"YAML ファイルではありません: {input_path}")
        return (input_path,)

    return tuple(
        sorted(
            {
                *input_path.glob("*.yaml"),
                *input_path.glob("*.yml"),
            }
        )
    )


def load_yaml_files(input_path: Path) -> dict[Path, dict]:
    data = {}

    for yaml_path in find_yaml_paths(input_path):
        loaded = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

        if not isinstance(loaded, dict):
            raise TypeError(
                f"YAML の最上位要素は mapping である必要があります: {yaml_path}"
            )

        data[yaml_path] = loaded

    return data


def write_json_file(
    model: BaseModel,
    output_dir: Path,
    name: str,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{name}.json"

    output_path.write_text(
        model.model_dump_json(
            by_alias=True,
            exclude_none=True,
            indent=4,
        ),
        encoding="utf-8",
    )
    return output_path
