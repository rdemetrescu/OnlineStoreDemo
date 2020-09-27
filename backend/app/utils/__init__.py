def dict_include_prefix(d, prefix: str):
    return {f"{prefix}{k}": v for k, v in d.items()}


def dict_remove_prefix(d, prefix: str):
    index = len(prefix)
    return {k[index:]: v for k, v in d.items() if k.startswith(prefix)}
