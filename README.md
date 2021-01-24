# Code for Parsing SCOWL word list
 
Details of the list can be [found here](https://github.com/en-wl/wordlist). To parse the word list, you must download the appropriate files for your operating system from this link.

### Usage
The whole module is accessed through the `SCOWLWordProcessor` class.
It requires the following arguments:
| Argument      | Description                                                                                                                       |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| directory     | The path to the 'final' folder in the SCOWL download.                                                                             |
| categories    | A list of categories you wish to include                                                                                          |
| subcategories | A list of subcategories you wish to include                                                                                       |
| sizes         | A list of sizes you wish to include                                                                                               |
| function_outs | A dictionary with functions as keys and file names as values. Functions are applied to words and, when True, output to the files. |

More details about the category, subcategory and size options can be found in the [SCOWL Readme](http://wordlist.aspell.net/scowl-readme/).

### Demonstration

```python
from parse_words import SCOWLWordProcessor

directory = r"/d/path_to_scowl/scowl-2020.12.07/final"
categories = [
    "english",
    "british",
    "british_z",
]
subcategories = ["upper", "words"]
sizes = [10, 20, 35, 40, 50, 55, 60, 70, 80]

def word_start_c(word: str) -> bool:
        return word.lower()[0] == 'c'

def word_start_a(word: str) -> bool:
        return word.lower()[0] == 'a' 

function_outs = {
    word_start_c : ["c_words"],
    word_start_a : ["a_words", "starts_vowel"],
}

SWP = SCOWLWordProcessor(
    directory=directory,
    categories=categories,
    subcategories=subcategories,
    sizes=sizes,
    function_outs=function_outs,
)
SWP.process_word_files(mode="stream")
```

The function_outs argument means you can generate the filter for another function. For example, to split by first letter you can define and `function_outs` generator:
```python
    def build_outputs_all_letters_seperate():
        return {
            partial(SCOWLWordProcessor.words_start_with, starts_with=letter): [
                letter + "_words"
            ]
            for letter in string.ascii_lowercase
        }

    function_outs = build_outs_all_letters_seperate()
```
This will create a seperate file for each letter.
