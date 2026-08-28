from config_io import load_yaml_files, write_json_file
from parse import parse_layout

def main() -> None:
    layouts = {
        name: parse_layout(name, mapping)
        for name, mapping in load_yaml_files().items()
    }

    for name, layout in layouts.items():
        written_path = write_json_file(layout, name)
        print(f"written: {written_path.name}")

if __name__ == "__main__":
    main()
