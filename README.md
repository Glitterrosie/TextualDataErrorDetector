# TextualDataErrorDetector

## Project Description
This project was conducted as part of a seminar. Our group was tasked with detecting textual data errors in datasets that had been deliberately polluted by another team. The objective was to identify and differentiate between four distinct types of textual errors: **typos**, **misspellings**, **OCR errors**, and **word transpositions**.

## Textual Data Errors
### Typos
Result from accidental keystroke errors. These can be classified into five categories, illustrated using the word apple:
   - Insertion: A neighboring character is added (e.g., appele).
   - Replication: A character is repeated (e.g., applle).
   - Deletion: A character is omitted (e.g., aple).
   - Transposition: Two adjacent characters are swapped (e.g., appel).
   - Substitution: A character is replaced with a neighboring character on the keyboard (e.g., aplle).
### Misspellings
Arise from a lack of knowledge of the correct spelling of a word. Examples include the word "accommodate", which is frequently written as "accomodate" or "acommodate", and "acquire", which is often written as "aquire".
### OCR errors
Occur during the digitization of printed texts using optical character recognition software. Characters with similar visual shapes may be misidentified, such as the letter "B" being recognized as "8".
### Word transpositions
Refer to values that are placed in incorrect columns. Word transpositions are typically caused by data ingestion issues, such as entering a first name in the last name column.

## Datasets
- **IMDB dataset:** Includes information on different scenes shot for a movie. One row corresponds to one scene for one person in the scene for this movie. The dataset has 200.000 rows and 24 columns and therefore is the dataset with the largest number of rows.
- **Australien Weather Dataset:** This dataset contains one weather observation per day per region, including different measurements like temperature or wind speed. We have a total of 29.092 rows with 23 columns.
- **Medical Diabetes Dataset:** Includes one row per hospital admission of patients. This dataset has 20.353 rows and 53 columns, which makes it the dataset with the most columns.

## Implementation
We implemented a three-phase approach consisting of generic labeling, specific labeling, and an additional phase dedicated to detecting word transpositions. 

### 1. Phase
The first phase involves generic labeling to identify implausible values without classifying the specific error type. The output of this phase is a generic-label-dataframe of the same dimensions as the original dataset, where each cell contains either a 0 (indicating no error) or a token representing a potential error.

Each cell is tokenized using regular expressions. Since we assume at most one error per cell, we iterate through the tokens and apply a set of column-specific checks. These checks include spellcheckers, categorical value lists, numeric range validations, pattern constraints, and other heuristics. For example, we validate whether a phonetic code is recognized, whether a numeric entry is within a valid range, or whether a hash value consists of valid hexadecimal characters. To handle categorical columns, we compare the token against a predefined categorical value list. If a word is valid but not part of the column's defined categories, it is considered a potential error. This tactic works for categorical columns, but not for free text fields, which do not have expected categories. For these, we rely on a spellchecker library to identify potential errors.

If a token is found to be erroneous, it is inserted into the corresponding position in the generic-label-dataframe, and the iteration for that cell stops. If no token is identified as erroneous, a 0 is recorded.

### 2. Phase
In the second phase, we refine the classification of errors found in the previous step. Using the generic-label-dataframe, we limit our analysis to cells marked as potentially erroneous. For each such cell, we extract the token and apply a column-specific labeling function to classify the error into one of three categories (excluding word transpositions).

The two main functions we implemented are for differentiating errors in string columns and for differentiating errors in number columns. These functions apply a cascade of rules ordered by their expected precision. For example, we first check for misspellings, then for typos, and finally fall back to OCR-related errors. High-precision checks are executed first to prioritize accuracy, as each cell is labeled only once. This conservative-first strategy ensures that error types identified with high confidence are not overridden by later, more optimistic checks. In cases where none of the high-precision methods match, the fallback ensures that an error label is still assigned, maintaining completeness at the cost of potentially lower precision.

Furthermore, we also implemented a method, which labels all detected errors in a column to as an OCR error. We used this function for columns, where we visually identified, that all unique wrong values in this column are caused by OCR recognition errors.

### 3. Phase
The third phase addresses word transpositions, which differ fundamentally from the other error types because they involve relationships between multiple cells. As such, they are not handled by the generic or specific labeling approaches.

To detect transpositions, we define rules that identify misplaced values between two or more columns. For instance, if two categorical columns each contain distinct value sets, we can infer a transposition when values appear in the inco

## Results
| Dataset | Error Type         | Precision | Recall |
| ------- | ------------------ | --------- | ------ |
| IMDB    | Word Transposition | 97.5%     | 96.3%  |
| Weather | OCR                | 88.5%     | 91.8%  |
| Medical | Misspelling        | 47.7%     | 48.0%  |

## Future Work and Challenges
Our main Challenges in included:
- Overlapping Error Categories: Distinguishing typos vs. OCR vs. misspellings is non-trivial.
- Plausible but Wrong Values: E.g., incorrect hashes or IDs that look valid.
- Context Sensitivity: Many errors are only detectable with domain knowledge or column relationships.

Future Work could include:
- Leverage LLMs to assist in generic labeling and classification.
- Use frequency-based heuristics for repeated misspellings.
- Apply functional dependencies to detect out-of-context values.
- Improve word transposition detection via association rules or anomaly detection techniques.



## Usage
### Run with Docker
1. Install [Docker](https://www.docker.com/) and make sure the Docker daemon is running.
2. Run `docker-compose build` to build the docker container from the provided image. This must only be done once or whenever
   - changing the `Dockerfile`
   - changing the `docker-compose.yml`
   - you add dependencies and change the `pyproject.toml` or `poetry.lock`
3. Run `docker-compose up` to run the docker container. You need to execute this command whenever you make changes to the code base.


## Commit Guideline
We use the [Conventional Commits Specification v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/#summary) for writing commit messages. Refer to the website for instructions.

### Commit Types

We use the recommended commit types from the specification, namely:

- `feat:` A code change that introduces a **new feature** to the codebase (this correlates with MINOR in Semantic Versioning)
- `fix:` A code change that **patches a bug** in your codebase (this correlates with PATCH in Semantic Versioning)
- `refactor:` A code change that **neither fixes a bug nor adds a feature**
- `build:` Changes that **affect the build system** or external dependencies (example scopes: pip, npm)
- `ci:` Changes to **CI configuration** files and scripts (examples: GitHub Actions)
- `docs:` **Documentation only** changes
- `perf:` A code change that **improves performance**
- `test:` Adding missing **tests** or correcting existing tests

### How should I voice the commit message?

- `feat:` commits: use the imperative, present tense – eg. `feat: add button` not `feat: added button` nor `feat: adds button`
- `fix:` commits: describe the bug that is being fixed – eg. `fix: button is broken` not `fix: repair broken button`

### What if I introduce a breaking change?

- Option 1): include an exclamation mark (`!`) after the commit type to draw attention to a breaking change
```
feat!: send an email to the customer when a product is shipped
```
- Option 2): include a breaking change footer
```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

### What do I do if the commit conforms to more than one of the commit types?

Go back and make multiple commits whenever possible. Part of the benefit of Conventional Commits is its ability to drive us to make more organized commits and PRs.
