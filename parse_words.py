import glob, os
from typing import List
from itertools import compress, product

_DIRECTORY_ = r"/d/repos/sharptx/scowl-2020.12.07/final"

_VALID_ARGS_ = {
    "categories": set(
        [
            "english",
            "american",
            "british",
            "british_z",
            "canadian",
            "australian",
            "variant_1",
            "variant_2",
            "variant_3",
            "british_variant_1",
            "british_variant_2",
            "canadian_variant_1",
            "canadian_variant_2",
            "australian_variant_1",
            "australian_variant_2",
        ]
    ),
    "subcategories": set(
        ["abbreviations", "contractions", "proper-names", "upper", "words"]
    ),
    "sizes": set([10, 20, 35, 40, 50, 55, 60, 70, 80, 95]),
}


def valid_arg_check(
    args: List,
    valid_set: str,
):
    missing = list(compress(args, [a not in _VALID_ARGS_.get(valid_set) for a in args]))
    if missing:
        raise ValueError(
            f"Arguments {missing} not found in valid set '{valid_set}': {_VALID_ARGS_.get(valid_set)}"
        )


def file_combinations(categories, subcategories, sizes):
    categories = [c + "-" for c in categories]
    subcategories = [c + "." for c in subcategories]
    sizes = [str(c) for c in sizes]
    yield from map(lambda x: "".join(x), product(*[categories, subcategories, sizes]))

def parse_word_file():
    


def read_word_files(categories: List[str], subcategories: List[str], sizes: List[int]):
    valid_arg_check(categories, "categories")
    valid_arg_check(subcategories, "subcategories")
    valid_arg_check(sizes, "sizes")
    for file in file_combinations(categories, subcategories, sizes):
        filepath = os.path.join(_DIRECTORY_, file)


if __name__ == "__main__":
    read_word_files(
        ["english", "american", "british", "british_z", "canadian", "australian"],
        ["upper", "words"],
        [80],
    )