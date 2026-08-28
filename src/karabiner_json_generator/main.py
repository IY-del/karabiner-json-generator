from pathlib import Path
from typing import Annotated

import typer

from karabiner_json_generator.config_io import load_yaml_files, write_json_file
from karabiner_json_generator.parse import parse_layout

app = typer.Typer()


@app.command()
def generate(
    input_path: Annotated[
        Path | None,
        typer.Argument(
            help="YAML ファイル、または YAML を含むディレクトリ。省略時はカレントディレクトリ",
        ),
    ] = None,
    output_dir: Annotated[
        Path | None,
        typer.Option(
            "--output-dir",
            "-o",
            help="生成先ディレクトリ。省略時は入力側と同じ場所",
        ),
    ] = None,
    check: Annotated[
        bool,
        typer.Option(
            "--check",
            help="JSON を書き込まず検証のみ行う",
        ),
    ] = False,
) -> None:
    input_path = (input_path or Path.cwd()).resolve()
    yaml_files = load_yaml_files(input_path)

    for yaml_path, mapping in yaml_files.items():
        layout = parse_layout(yaml_path.stem, mapping)

        if check:
            typer.echo(f"valid: {yaml_path}")
            continue

        destination_dir = output_dir or yaml_path.parent
        written_path = write_json_file(
            model=layout,
            output_dir=destination_dir,
            name=yaml_path.stem,
        )
        typer.echo(f"written: {written_path}")


if __name__ == "__main__":
    app()
