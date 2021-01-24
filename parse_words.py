import os
from typing import List
from itertools import compress, product, chain
from functools import partial
from contextlib import ExitStack

# TODO: Refactor generic code


class SCOWLWordProcessor:
    _VALID_ARGS_: dict = {
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
        directory: str,
        categories: List[str],
        subcategories: List[str],
        sizes: List[int],
        function_outs: dict,
        out_directory: str = "./filtered_words/",
    ):
        self.directory = directory
        self.categories = self.valid_arg_check(categories, "categories")
        self.subcategories = self.valid_arg_check(subcategories, "subcategories")
        self.sizes = self.valid_arg_check(sizes, "sizes")
        self.function_outs = function_outs
        self.out_directory = self.make_out_directory(out_directory)
        self.output_files = list(set(chain.from_iterable(function_outs.values())))

    def make_out_directory(self, directory: str) -> str:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    @staticmethod
    def valid_arg_check(
        args: List,
        valid_set_name: str,
    ) -> List:
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
        if os.path.exists(filepath):
            with open(filepath, encoding="ISO-8859-1") as fp:
                line = fp.readline()
                while line:
                    if not line.strip().endswith("'s"):
                        yield line.strip()
                    line = fp.readline()

    def files_stream_words(self):
        return chain.from_iterable(
            (self.file_word_stream(file) for file in self.file_combinations())
        )

    def full_filename(self, file: str):
        return os.path.join(self.out_directory, file + ".txt")

    def process_word_files(self, mode: str = "batch"):
        file_paths = {fname: self.full_filename(fname) for fname in self.output_files}

        if mode == "stream":
            with ExitStack() as stack:
                files = {
                    fname: stack.enter_context(open(path, "a+"))
                    for fname, path in file_paths.items()
                }
                for word in self.files_stream_words():
                    for func, outputs in self.function_outs.items():
                        if func(word):
                            for output_file in outputs:
                                files.get(output_file).write(word + "\n")
        elif mode == "batch":
            word_outs = {fname: set() for fname in self.output_files}
            for word in self.files_stream_words():
                for func, outputs in self.function_outs.items():
                    if func(word):
                        for output_file in outputs:
                            word_outs.get(output_file).add(word)

            for fname, words in word_outs.items():
                with open(file_paths.get(fname), "w") as file:
                    for word in sorted(list(words)):
                        file.write("%s\n" % word)

    @staticmethod
    def words_start_with(word: str, starts_with: str) -> bool:
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
    sizes = [10, 20, 35, 40, 50, 55, 60, 70, 80]
    starts_c = partial(SCOWLWordProcessor.words_start_with, starts_with="c")
    starts_a = partial(SCOWLWordProcessor.words_start_with, starts_with="a")
    function_outs = {
        starts_c: ["c_words"],
        starts_a: ["a_words"],
    }
    SWP = SCOWLWordProcessor(
        directory=directory,
        categories=categories,
        subcategories=subcategories,
        sizes=sizes,
        function_outs=function_outs,
    )
    SWP.process_word_files(mode="stream")
