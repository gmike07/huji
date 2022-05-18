# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: propositions/syntax.py

"""Syntactic handling of propositional formulae."""

from __future__ import annotations
from typing import Mapping, Optional, Set, Tuple, Union
import re
from logic_utils import frozen

BINARY_OP_DICT = {'&', '|', '->', '+', '<->', '-&', '-|'}  # {'|', '&', '->'}
BINARY_REGEX = r'[&|+]|->|<->|-&|-\|'  # r'[&|+]|->|'
OPERATOR_REGEX = r'[TF~]' + '|' + BINARY_REGEX
VARIABLE_REGEX = r'[p-z]\d*'
MAX_OP_LENGTH = 3
OPERATOR_BOOLEAN_DICT = {'~': lambda x: not x,
                         '|': lambda x, y: x or y,
                         '&': lambda x, y: x and y,
                         '->': lambda x, y: not x or y,
                         '+': lambda x, y: (x and not y) or (not x and y),
                         '<->': lambda x, y: x == y,
                         '-&': lambda x, y: not (x and y),
                         '-|': lambda x, y: not (x or y),
                         }


def is_variable(s: str) -> bool:
    """Checks if the given string is an atomic proposition.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is an atomic proposition, ``False``
        otherwise.
    """
    return 'p' <= s[0] <= 'z' and (len(s) == 1 or s[1:].isdigit())


def is_constant(s: str) -> bool:
    """Checks if the given string is a constant.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is a constant, ``False`` otherwise.
    """
    return s == 'T' or s == 'F'


def is_unary(s: str) -> bool:
    """Checks if the given string is a unary operator.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is a unary operator, ``False`` otherwise.
    """
    return s == '~'


def is_binary(s: str) -> bool:
    """Checks if the given string is a binary operator.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is a binary operator, ``False`` otherwise.
    """
    return s in BINARY_OP_DICT
    # For Chapter 3:
    # return s in {'&', '|',  '->', '+', '<->', '-&', '-|'}


def find_variable_name(s):
    """find the variable name from index 0

    Parameters:
        s: string to find variable name in

    Returns:
        a string when the string is the variable name from index 0
    """
    i = 1
    while i < len(s) and s[i].isdigit():
        i += 1
    return s[:i]


def find_op(s):
    """find the next operator from index 0

    Parameters:
         s: string to search in.

    Returns:
        returns the operator from index zero if it is an op, else return
        None
    """
    for i in range(1, MAX_OP_LENGTH + 1):
        if len(s) >= i and s[0:i] in BINARY_OP_DICT:
            return s[0:i]


@frozen
class Formula:
    """An immutable propositional formula in tree representation.

    Attributes:
        root (`str`): the constant, atomic proposition, or operator at the root
            of the formula tree.
        first (`~typing.Optional`\\[`Formula`]): the first operand to the root,
            if the root is a unary or binary operator.
        second (`~typing.Optional`\\[`Formula`]): the second operand to the
            root, if the root is a binary operator.
    """
    root: str
    first: Optional[Formula]
    second: Optional[Formula]

    def __init__(self, root: str, first: Optional[Formula] = None,
                 second: Optional[Formula] = None) -> None:
        """Initializes a `Formula` from its root and root operands.

        Parameters:
            root: the root for the formula tree.
            first: the first operand to the root, if the root is a unary or
                binary operator.
            second: the second operand to the root, if the root is a binary
                operator.
        """
        if is_variable(root) or is_constant(root):
            assert first is None and second is None
            self.root = root
        elif is_unary(root):
            assert type(first) is Formula and second is None
            self.root, self.first = root, first
        else:
            assert is_binary(root) and type(first) is Formula and \
                   type(second) is Formula
            self.root, self.first, self.second = root, first, second

    def __eq__(self, other: object) -> bool:
        """Compares the current formula with the given one.

        Parameters:
            other: object to compare to.

        Returns:
            ``True`` if the given object is a `Formula` object that equals the
            current formula, ``False`` otherwise.
        """
        return isinstance(other, Formula) and str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        """Compares the current formula with the given one.

        Parameters:
            other: object to compare to.

        Returns:
            ``True`` if the given object is not a `Formula` object or does not
            does not equal the current formula, ``False`` otherwise.
        """
        return not self == other

    def __hash__(self) -> int:
        return hash(str(self))

    def __repr__(self) -> str:
        """Computes the string representation of the current formula.

        Returns:
            The standard string representation of the current formula.
        """
        if is_unary(self.root):
            return self.root + str(self.first)
        elif is_binary(self.root):
            return '(' + str(self.first) + self.root + str(self.second) + ')'
        return self.root

    def variables(self) -> Set[str]:
        """Finds all atomic propositions (variables) in the current formula.

        Returns:
            A set of all atomic propositions used in the current formula.
        """
        return {s for s in re.findall(VARIABLE_REGEX, str(self))}

    def operators(self) -> Set[str]:
        """Finds all operators in the current formula.

        Returns:
            A set of all operators (including ``'T'`` and ``'F'``) used in the
            current formula.
        """
        return {s for s in re.findall(OPERATOR_REGEX, str(self))}

    @staticmethod
    def parse_prefix(s: str) -> Tuple[Union[Formula, None], str]:
        """Parses a prefix of the given string into a formula.

        Parameters:
            s: string to parse.

        Returns:
            A pair of the parsed formula and the unparsed suffix of the string.
            If the first token of the string is a variable name (e.g.,
            ``'x12'``), then the parsed prefix will be that entire variable
            name (and not just a part of it, such as ``'x1'``). If no prefix of
            the given string is a valid standard string representation of a
            formula then returned pair should be of ``None`` and an error
            message, where the error message is a string with some
            human-readable content.
        """
        if len(s) == 0:
            return None, "No string to parse!"
        if is_unary(s[0]):  # ~term
            formula, error = Formula.parse_prefix(s[1:])
            if formula is None:
                return None, "No term after unary op"
            return Formula(s[0], formula), s[len(s[0] + str(formula)):]

        if is_constant(s[0]):  # T or F
            return Formula(s[0]), s[1:]

        if 'p' <= s[0] <= 'z':  # variable name
            name = find_variable_name(s)
            return Formula(name), s[len(name):]

        if s[0] == '(':  # (term op term)
            formula, error = Formula.binary_term(s)
            if formula is None:
                return formula, error
            return formula, s[len(str(formula)):]
        return None, 'No option was found'

    @staticmethod
    def binary_term(s) -> Tuple[Union[Formula, None], str]:
        """Parses a prefix of the given string of type (term op term)
        into a formula.

        Parameters:
            s: string to parse.

        Returns:
            a tuple of (formula, string) when the formula is the converted
            string into object. if it fails, where will be None instead of
            formula and the string will be the error of the parsing.
        """
        # find first Term
        s = s[1:]
        first_term, error = Formula.parse_prefix(s)
        if first_term is None:
            return None, "No first term in binary op"
        s = s[len(str(first_term)):]

        # find op
        op = find_op(s)
        if op is None:
            return None, 'No op after term'
        s = s[len(op):]

        # find second term
        second_term, error = Formula.parse_prefix(s)
        if second_term is None:
            return None, 'No second binary op'
        if len(str(second_term)) >= len(s) or s[len(str(second_term))] != ')':
            return None, "no closing )"
        return Formula(op, first_term, second_term), ''

    @staticmethod
    def is_formula(s: str) -> bool:
        """Checks if the given string is a valid representation of a formula.

        Parameters:
            s: string to check.

        Returns:
            ``True`` if the given string is a valid standard string
            representation of a formula, ``False`` otherwise.
        """
        formula, error = Formula.parse_prefix(s)
        if formula is None or error != '':
            return False
        return True

    @staticmethod
    def parse(s: str) -> Formula:
        """Parses the given valid string representation into a formula.

        Parameters:
            s: string to parse.

        Returns:
            A formula whose standard string representation is the given string.
        """
        assert Formula.is_formula(s)
        formula, error = Formula.parse_prefix(s)
        return formula

    # Optional tasks for Chapter 1

    def polish(self) -> str:
        """Computes the polish notation representation of the current formula.

        Returns:
            The polish notation representation of the current formula.
        """
        if is_unary(self.root):
            return self.root + self.first.polish()
        elif is_binary(self.root):
            return self.root + self.first.polish() + self.second.polish()
        return self.root

    @staticmethod
    def parse_polish(s: str) -> Formula:
        """Parses the given polish notation representation into a formula.

        Parameters:
            s: string to parse.

        Returns:
            A formula whose polish notation representation is the given string.
        """
        if is_constant(s[0]):
            return Formula(s[0])
        if is_unary(s[0]):
            return Formula(s[0], Formula.parse_polish(s[1:]))
        op = find_op(s)
        if op:
            first = Formula.parse_polish(s[len(op):])
            second = Formula.parse_polish(s[len(op + str(first.polish())):])
            return Formula(op, first, second)
        name = find_variable_name(s)
        return Formula(name)

    # Tasks for Chapter 3

    def substitute_variables(
            self, substitution_map: Mapping[str, Formula]) -> Formula:
        """Substitutes in the current formula, each variable `v` that is a key
        in `substitution_map` with the formula `substitution_map[v]`.

        Parameters:
            substitution_map: the mapping defining the substitutions to be
                performed.

        Returns:
            The resulting formula.

        Examples:
            >>> Formula.parse('((p->p)|z)').substitute_variables(
            ...     {'p': Formula.parse('(q&r)')})
            (((q&r)->(q&r))|z)
        """
        for variable in substitution_map:
            assert is_variable(variable)
        if is_variable(self.root):
            if self.root in substitution_map.keys():
                return substitution_map[self.root]
            return Formula(self.root)
        if is_constant(self.root):
            return Formula(self.root)
        if is_unary(self.root):
            return Formula(self.root,
                           self.first.substitute_variables(substitution_map))
        if is_binary(self.root):
            return Formula(self.root,
                           self.first.substitute_variables(substitution_map),
                           self.second.substitute_variables(substitution_map))

    def substitute_operators(
            self, substitution_map: Mapping[str, Formula]) -> Formula:
        """Substitutes in the current formula, each constant or operator `op`
        that is a key in `substitution_map` with the formula
        `substitution_map[op]` applied to its (zero or one or two) operands,
        where the first operand is used for every occurrence of ``'p'`` in the
        formula and the second for every occurrence of ``'q'``.

        Parameters:
            substitution_map: the mapping defining the substitutions to be
                performed.

        Returns:
            The resulting formula.

        Examples:
            >>> Formula.parse('((x&y)&~z)').substitute_operators(
            ...     {'&': Formula.parse('~(~p|~q)')})
            ~(~~(~x|~y)|~~z)
        """
        for operator in substitution_map:
            assert is_binary(operator) or is_unary(operator) or \
                   is_constant(operator)
            assert substitution_map[operator].variables().issubset({'p', 'q'})
        if is_variable(self.root):  # if it is a variable, return itself
            return Formula(self.root)
        # if it is a T\F, return the replacement if such exists, else itself
        if is_constant(self.root):
            if self.root in substitution_map:
                return substitution_map[self.root]
            return Formula(self.root)
        # if it is a ~, return the replacement if such exists, else itself
        if is_unary(self.root):
            # replace the next one in command
            first = self.first.substitute_operators(substitution_map)
            if self.root in substitution_map:
                return substitution_map[self.root]. \
                    substitute_variables({'p': first})
            return Formula(self.root, first)
        # if it is a binary, return the replacement if such exists, else itself
        if is_binary(self.root):
            # replace the next one in command
            first = self.first.substitute_operators(substitution_map)
            second = self.second.substitute_operators(substitution_map)
            if self.root in substitution_map:
                return substitution_map[self.root]. \
                    substitute_variables({'p': first, 'q': second})
            return Formula(self.root, first, second)
