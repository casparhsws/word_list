import glob, os
from typing import List
from itertools import compress, product, chain
from functools import partial


class SCOWLWordProcessor:
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

    def __init__(
        self,
        directory,
        categories,
        subcategories,
        sizes,
        out_directory="./filtered_words",
    ):
        self.directory = directory
        self.categories = self.valid_arg_check(categories, "categories")
        self.subcategories = self.valid_arg_check(subcategories, "subcategories")
        self.sizes = self.valid_arg_check(sizes, "sizes")

    def make_out_directory(self, directory):
        return directory

    @staticmethod
    def valid_arg_check(
        args: List,
        valid_set_name: str,
    ):
        valid_set = SCOWLWordProcessor._VALID_ARGS_.get(valid_set_name)
        missing = list(compress(args, [a not in valid_set for a in args]))
        if missing:
            raise ValueError(
                f"Arguments {missing} not found in valid set '{valid_set_name}': {valid_set}"
            )
        return args

    def file_combinations(self):
        categories = [c + "-" for c in self.categories]
        subcategories = [c + "." for c in self.subcategories]
        sizes = [str(c) for c in self.sizes]
        yield from map(
            lambda x: "".join(x), product(*[categories, subcategories, sizes])
        )

    def file_word_stream(self, file):
        filepath = os.path.join(self.directory, file)
        with open(filepath, encoding="ISO-8859-1") as fp:
            line = fp.readline()
            while line:
                yield line.strip().replace("'s", "")
                line = fp.readline()

    def files_stream_words(self):
        return chain.from_iterable(
            (self.file_word_stream(file) for file in self.file_combinations())
        )

    def process_word_files(self):
        for word in self.files_stream_words():
            print(word)

    @staticmethod
    def words_start_with(word: str, starts_with: str):
        return word[: len(starts_with)] == starts_with


if __name__ == "__main__":
    directory = r"/d/repos/sharptx/scowl-2020.12.07/final"
    categories = [
        "english",
        "american",
        "british",
        "british_z",
        "canadian",
        "australian",
    ]
    subcategories = ["upper", "words"]
    sizes = [80]
    starts_c = partial(SCOWLWordProcessor.words_start_with, starts_with="c")
    starts_a = partial(SCOWLWordProcessor.words_start_with, starts_with="a")
    function_outs = {
        starts_c: ["c_words"],
        starts_a: ["a_words"],
    }
