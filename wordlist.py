#!/bin/python3
"""
wordlist.py
Module for generating password wordlists based on user input and learned patterns.
"""


from gc import get_count
import os
import re
import argparse
import json
from typing import List

class WordlistGenerator:
    """
    Generates a wordlist based on user-provided password samples and learned patterns.
    """

    def __init__(self, samples: List[str], template: str = None):
        self.samples = samples
        self.template = template
        self.patterns = self._extract_patterns(samples)

    def _extract_patterns(self, samples: List[str]) -> List[str]:
        """
        Extracts regex patterns and common structures from the sample passwords.
        """
        # Example: Find common digit/letter/symbol positions
        patterns = []
        for pw in samples:
            # Replace digits with '\d', letters with 'a', symbols with '!' for pattern learning
            pattern = re.sub(r"\d", "d", pw)
            pattern = re.sub(r"[A-Za-z]", "a", pattern)
            pattern = re.sub(r"[^A-Za-z\d]", "!", pattern)
            patterns.append(pattern)
        return patterns

    def generate(self, max_count: int = 10000) -> List[str]:
        """
        Generates a wordlist using either a user-supplied template or learned patterns and mutations.
        """
        if self.template:
            return self.generate_from_template(self.template, max_count)
        wordlist = set(self.samples)
        for pw in self.samples:
            wordlist.add(pw.lower())
            wordlist.add(pw.upper())
            wordlist.add(pw.capitalize())
            wordlist.add(pw + "1")
            wordlist.add("!" + pw)
            wordlist.add(pw + "!")
        # TODO: Use patterns for more advanced generation
        return list(wordlist)[:max_count]

    def generate_from_template(
        self, template: str, max_count: int = 10000
    ) -> List[str]:
        """
        Expands a template string with bracketed ranges/sets and alternations into all possible combinations.
        Supports [1-5], [%/], [a|b|c], and repetition [1-5]{3}.
        """
        import itertools

        # Find all bracketed expressions, including repetition
        # e.g. [1-5]{3} or [a|b]{2}
        pattern = r"(\[[^\]]+\](?:\{\d+(?:,\d+)?\})?)"
        parts = re.split(pattern, template)
        options = []
        for part in parts:
            if not part:
                continue
            # Check for bracketed with repetition
            m = re.match(r"\[([^\]]+)\](\{(\d+)(?:,(\d+))?\})?", part)
            if m:
                inner = m.group(1)
                rep_min = int(m.group(3)) if m.group(3) else 1
                rep_max = int(m.group(4)) if m.group(4) else rep_min
                # Range [1-5]
                range_match = re.match(r"(\d)-(\d)", inner)
                if range_match:
                    base = [
                        str(i)
                        for i in range(
                            int(range_match.group(1)), int(range_match.group(2)) + 1
                        )
                    ]
                # Alternation [a|b|c]
                elif "|" in inner:
                    base = inner.split("|")
                # Set [%/]
                else:
                    base = list(inner)
                # Apply repetition
                rep_options = []
                for r in range(rep_min, rep_max + 1):
                    rep_options.extend(
                        ["".join(p) for p in itertools.product(base, repeat=r)]
                    )
                options.append(rep_options)
            elif part.startswith("[") and part.endswith("]"):
                inner = part[1:-1]
                range_match = re.match(r"(\d)-(\d)", inner)
                if range_match:
                    options.append(
                        [
                            str(i)
                            for i in range(
                                int(range_match.group(1)), int(range_match.group(2)) + 1
                            )
                        ]
                    )
                elif "|" in inner:
                    options.append(inner.split("|"))
                else:
                    options.append(list(inner))
            else:
                options.append([part])
        combos = itertools.product(*options)
        wordlist = ["".join(combo) for combo in combos]
        
        with open("wordlist.txt", "w") as f:
            for word in wordlist:
                f.write(word + "\n")
        
        return wordlist[:max_count]


def load_config(config_path: str):
    with open(config_path, "r") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Exodus wallet password wordlist generator"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="wordlist_config.json",
        help="Path to config file (JSON)",
    )
    parser.add_argument(
        "--input", type=str, help="Input file with password samples or templates"
    )
    parser.add_argument(
        "--template", type=str, help="Template string for password generation"
    )
    parser.add_argument(
        "--max-count",
        type=int,
        default=10000,
        help="Maximum number of passwords to generate",
    )
    parser.add_argument(
        "--input-type",
        type=str,
        choices=["samples", "templates"],
        default="samples",
        help="Specify if input file contains password samples or templates",
    )
    args = parser.parse_args()

    config = {}
    if os.path.exists(args.config):
        config = load_config(args.config)

    # Load samples or templates
    samples = []
    templates = []
    if args.input:
        with open(args.input, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        if args.input_type == "samples":
            samples = lines
        else:
            templates = lines
    elif "samples" in config:
        samples = config["samples"]
    elif "templates" in config:
        templates = config["templates"]

    # Use template from argument, config, or None
    template = args.template or config.get("template")

    if templates:
        all_words = set()
        for tpl in templates:
            if tpl:  # Only process non-empty templates
                wordgen = WordlistGenerator([], template=tpl).generate(max_count=args.max_count)
                all_words.update(wordgen)
        for word in list(all_words)[:args.max_count]:
            print(word)
    elif template:
        wordgen = WordlistGenerator([], template=template).generate(max_count=args.max_count)
        for word in wordgen:
            print(word)
    else:
        wordgen = WordlistGenerator(samples).generate(max_count=args.max_count)
        for word in wordgen:
            print(word)
            """
            Expands a template string with bracketed ranges/sets and alternations into all possible combinations.
            Supports [1-5], [%/], [a|b|c], repetition [1-5]{3}, and quantifiers [;]?, [;]*, [;]+.
            """
            import itertools

            # Find all bracketed expressions, including repetition and quantifiers
            # e.g. [1-5]{3}, [a|b]{2}, [;]?, [;]*, [;]+
            pattern = r"(\[[^\]]+\](?:\{\d+(?:,\d+)?\}|\?|\*|\+)?)"
            parts = re.split(pattern, template)
            options = []
            for part in parts:
                if not part:
                    continue
                # Check for bracketed with quantifier or repetition
                m = re.match(r"\[([^\]]+)\](\{(\d+)(?:,(\d+))?\}|\?|\*|\+)?", part)
                if m:
                    inner = m.group(1)
                    quant = m.group(2)
                    # Range [1-5]
                    range_match = re.match(r"(\d)-(\d)", inner)
                    if range_match:
                        base = [
                            str(i)
                            for i in range(
                                int(range_match.group(1)), int(range_match.group(2)) + 1
                            )
                        ]
                    elif "|" in inner:
                        base = inner.split("|")
                    else:
                        base = list(inner)
                    # Handle quantifiers
                    rep_options = []
                    if quant:
                        if quant.startswith("{"):
                            # {n} or {n,m}
                            rep_min = int(m.group(3)) if m.group(3) else 1
                            rep_max = int(m.group(4)) if m.group(4) else rep_min
                            for r in range(rep_min, rep_max + 1):
                                rep_options.extend(
                                    [
                                        "".join(p)
                                        for p in itertools.product(base, repeat=r)
                                    ]
                                )
                        
                        elif quant == "?":
                            # TODO() Error, is not correctly detecting [&]? inside of a word. Example:
                            # "pass[&]?word" should equal:
                            # "pass&word" or "password", gets interpretaded as:
                            # "pass&?word instead
                            # zero or one
                            rep_options.extend([""] + base)
                        elif quant == "*":
                            # zero to 4 (arbitrary upper limit for practicality)
                            for r in range(0, 5):
                                rep_options.extend(
                                    [
                                        "".join(p)
                                        for p in itertools.product(base, repeat=r)
                                    ]
                                )
                        elif quant == "+":
                            # one to 4 (arbitrary upper limit for practicality)
                            for r in range(1, 5):
                                rep_options.extend(
                                    [
                                        "".join(p)
                                        for p in itertools.product(base, repeat=r)
                                    ]
                                )
                        else:
                            rep_options = base
                        options.append(rep_options)
                    else:
                        options.append(base)
                elif part.startswith("[") and part.endswith("]"):
                    inner = part[1:-1]
                    range_match = re.match(r"(\d)-(\d)", inner)
                    if range_match:
                        options.append(
                            [
                                str(i)
                                for i in range(
                                    int(range_match.group(1)),
                                    int(range_match.group(2)) + 1,
                                )
                            ]
                        )
                    elif "|" in inner:
                        options.append(inner.split("|"))
                    else:
                        options.append(list(inner))
                else:
                    options.append([part])
            combos = itertools.product(*options)
            wordlist = ["".join(combo) for combo in combos]
            return wordlist[:get_count]

if __name__ == "__main__":
    main()