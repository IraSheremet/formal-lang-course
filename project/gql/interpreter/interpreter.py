import sys

from project.gql.interpreter.Visitor import Visitor
from project.gql.interpreter.exceptions import *
from project.gql.task14 import get_parser, accept


def interpreter(*args):
    """Interpret the specified file in the Graph Query Language.

    Parameters
    ----------
    args:
        filepath - path or name of script.

    Returns
    ----------
    code: int
        Exit code. Success - 0, error - 1.
    """
    program = read_script(args[1])
    if not accept(program):
        raise IncorrectSyntaxError()
    try:
        tree = get_parser(program).prog()
        visitor = Visitor()
        visitor.visit(tree)
    except SomethingException as e:
        sys.stdout.write(f"Exception: {e.msg}\n")
        exit(1)
    exit(0)


def read_script(filepath):
    """Read script from file with .gql extension."""
    if not filepath.name.endswith(".gql"):
        raise IncorrectExtensionException()
    try:
        file = filepath.open()
    except FileNotFoundError as e:
        raise IncorrectPathException(filepath.name) from e
    return "".join(file.readlines())
