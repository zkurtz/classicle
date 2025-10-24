# Python coding standard

Follow the google Python style guide except where overridden by the rules below.

## Type hinting

- Apply type hints to all function parameters and return values, including in unit test modules.
- Use modern type hinting. Example: Do not use Dict, List, Optional; use dict, list, | instead.

## Strings

- Use f-strings for string interpolation.

## Classes

Use dataclasses where applicable, in descending order of preference:
1. @attrs.frozen
2. @attrs.define (only where mutability is required)
3. @dataclass

Use kw_only=True except when there is only one argument.

## Keyword args

Use keyword-only arguments for functions with more than one argument.

## Formatting

Use trailing commas in function signatures or lists with more than two items, except where it would reduce readability.

## Tuple unpacking

Avoid tuple unpacking, except in trivial (at most two return values) or localized use cases. Prefer to define and return dataclasses with documented attributes.

## Docstrings

Follow the Google style guide for function docstrings.

## Conditionals

Reorder to avoid negation: prefer `result = foo if condition else bar` instead of `result = bar if not condition else foo`.

Do not use `==` for comparison to boolean values:
- Instead of `if is_valid == True:`, use `if is_valid:`.
- Instead of `df[df['col'] == False]`, use `df[~df['col']]`.

## Package preferences

`click` is better than `argparse`.

## Pandas best practices

Do not use `inplace=True`.

When selecting rows from a DataFrame, use `.loc` or `.iloc` methods rather than direct bracket notation.

## Zen

Simple is better than complex:
- Do not introduce try-except logic except where explicitly requested.
- Do not create any empty `__init__.py` files unless explicitly requested.


# SQL coding standard

Use CTEs instead of subqueries wherever possible.

Do not alias table names unless there is a naming conflict or if line length exceeds 120 characters.
