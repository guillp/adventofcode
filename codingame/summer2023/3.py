def merge_files(file_contents: list[str]) -> str:
    res = dict[str, set[str]]()
    for file_content in file_contents:
        for line in file_content.split("\n"):
            fields = set(line.split(";"))
            name = next(field for field in fields if field.startswith("Name="))
            res.setdefault(name, set())
            res[name] |= fields - {name}

    return "\n".join(
        f"{name};{';'.join(sorted(res[name], key=lambda field: field.split('=')[0]))}" if res[name] else name
        for name in sorted(res)
    )
