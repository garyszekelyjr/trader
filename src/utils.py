import re


CAMEL_CASE_TO_SNAKE_CASE = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def camel_case_to_snake_case(string: str) -> str:
    return CAMEL_CASE_TO_SNAKE_CASE.sub("_", string).lower()
