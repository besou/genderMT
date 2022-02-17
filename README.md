# Rule-based Gender and Politeness Tagger

This repository contains scripts to tag corpora with
gender and politeness information. Currently, Russian
and French are supported.

For each line in the corpus, the script returns a string
of up to three tags from the following tag sets:
- gender of the speaker: `<1m>` (male), `<1f>` (female)
- gender of the addressee: `<2m>` (male), `<2f>` (female)
- form of address: `<T>` (informal), `<V>` (formal)

## Installation

Please install [spaCy](https://spacy.io/usage).
Then, install the following model for Russian and French,
respectively:

- `python -m spacy download ru_core_news_sm`
- `python -m spacy download fr_core_news_sm`

## Usage

Each language-specific script takes a path to a corpus
as the first argument and the file to which the output
should be written as the second argument:

- `python scripts/tag_russian_corpus.py <INFILE> <OUTFILE>`
- `python scripts/tag_french_corpus.py <INFILE> <OUTFILE>`

The output consists of four columns. The first three columns
contain either a tag from one of the respective tag set or it is
empty of no match has been found. The fourth column contains the
original sentence.

There are two test files, `corpus.ru` and `corpus.fr` for
testing purposes. These may be used as follows:

- `python scripts/tag_russian_corpus.py data/corpus.ru tags.ru`
- `python scripts/tag_french_corpus.py data/corpus.fr tags.fr`
