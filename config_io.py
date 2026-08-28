from pathlib import Path
import yaml
from pydantic import BaseModel

current_dir = Path.cwd()
def load_yaml_files() -> dict:
    data = {}
    for yaml_path in [*current_dir.glob("*.yaml"), *current_dir.glob("*.yml")]:
        with yaml_path.open("r", encoding="utf-8") as file:
            if yaml_path.stem in data:
                raise ValueError(
                    f"Duplicate layout name: {yaml_path.stem}.yaml and {yaml_path.stem}.yml"
                )
            data[yaml_path.stem] = yaml.safe_load(file)
    return data

def write_json_file(model: BaseModel, name: str) -> Path:
    output_path = current_dir / f"{name}.json"
    output_path.write_text(
        model.model_dump_json(
            by_alias=True,
            exclude_none=True,
            indent=4,
        ),
        encoding="utf-8",
    )
    return output_path
