# app/services/match_utils.py

def normalize(text: str) -> str:
    if not text:
        return ""
    return (
        text.lower()
        .replace(".dll", "")
        .replace("_", "")
        .replace("-", "")
        .replace(" ", "")
        .replace(".", "")
    )


def build_index(packages):
    index = {}

    for pkg in packages:
        if not pkg.name:
            continue

        norm_name = normalize(pkg.name)
        index[norm_name] = pkg

        if pkg.full_name:
            norm_full = normalize(pkg.full_name)
            index[norm_full] = pkg

    return index