from pathlib import Path

def get_img_path_hyperlink(label: str, path: Path | None) -> str:
    if not path:
        return f"{label}: Not generated."
    
    abs_path = path.resolve()
    file_uri = abs_path.as_uri()

    # OSC 8 Escape sequences for clickable links
    # Format: \033]8;;URI\033\\TEXT\033]8;;\033\\
    return f"{label}: \033]8;;{file_uri}\033\\{abs_path}\033]8;;\033\\"