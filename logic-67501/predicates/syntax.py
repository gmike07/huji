# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: predicates/syntax.py

"""Syntactic handling of first-order formulas and terms."""

from __future__ import annotations
from typing import AbstractSet, Mapping, Optional, Sequence, Set, Tuple, Union, Dict

from logic_utils import fresh_variable_name_generator, frozen

from propositions.syntax import Formula as PropositionalFormula, \
    is_variable as is_propositional_variable

MAX_OP_LENGTH = 2
BINARY_OP_DICT = {'|', '&', '->'}


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


class ForbiddenVariableError(Exception):
    """Raised by `Term.substitute` and `Formula.substitute` when a substituted
    term contains a variable name that is forbidden in that context."""

    def __init__(self, variable_name: str) -> None:
        """Initializes a `ForbiddenVariableError` from its offending variable
        name.

        Parameters:
            variable_name: variable name that is forbidden in the context in
                which a term containing it was to be substituted.
        """
        assert is_variable(variable_name)
        self.variable_name = variable_name


def is_constant(s: str) -> bool:
    """Checks if the given string is a constant name.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is a constant name, ``False`` otherwise.
    """
    return (((s[0] >= '0' and s[0] <= '9') or (s[0] >= 'a' and s[0] <= 'd'))
            and s.isalnum()) or s == '_'


def is_variable(s: str) -> bool:
    """Checks if the given string is a variable name.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is a variable name, ``False`` otherwise.
    """
    return s[0] >= 'u' and s[0] <= 'z' and s.isalnum()


def is_function(s: str) -> bool:
    """Checks if the given string is a function name.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is a function name, ``False`` otherwise.
    """
    return s[0] >= 'f' and s[0] <= 't' and s.isalnum()


@frozen
class Term:
    """An immutable first-order term in tree representation, composed from
    variable names and constant names, and function names applied to them.

    Attributes:
        root (`str`): the constant name, variable name, or function name at the
            root of the term tree.
        arguments (`~typing.Optional`\\[`~typing.Tuple`\\[`Term`, ...]]): the
            arguments to the root, if the root is a function name.
    """
    root: str
    arguments: Optional[Tuple[Term, ...]]

    def __init__(self, root: str,
                 arguments: Optional[Sequence[Term]] = None) -> None:
        """Initializes a `Term` from its root and root arguments.

        Parameters:
            root: the root for the formula tree.
            arguments: the arguments to the root, if the root is a function
                name.
        """
        if is_constant(root) or is_variable(root):
            assert arguments is None
            self.root = root
        else:
            assert is_function(root)
            assert arguments is not None
            self.root = root
            self.arguments = tuple(arguments)
            assert len(self.arguments) > 0

    def __repr__(self) -> str:
        """Computes the string representation of the current term.

        Returns:
            The standard string representation of the current term.
        """
        if not is_function(self.root):
            return self.root
        string = ','.join([str(argument) for argument in self.arguments])
        return self.root + '(' + string + ')'

    def __eq__(self, other: object) -> bool:
        """Compares the current term with the given one.

        Parameters:
            other: object to compare to.

        Returns:
            ``True`` if the given object is a `Term` object that equals the
            current term, ``False`` otherwise.
        """
        return isinstance(other, Term) and str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        """Compares the current term with the given one.

        Parameters:
            other: object to compare to.

        Returns:
            ``True`` if the given object is not a `Term` object or does not
            equal the current term, ``False`` otherwise.
        """
        return not self == other

    def __hash__(self) -> int:
        return hash(str(self))

    @staticmethod
    def find_string(string: str, function_string) -> int:
        """
        :param string: the string to parse
        :param function_string: the func to satisfy
        :return: the longest s[:i] that satisfies func
        """
        if function_string(string):
            return len(string)
        index = 0
        while index < len(string) and function_string(string[:index + 1]) \
                is True:
            index += 1
        return index

    @staticmethod
    def parse_prefix(s: str) -> Tuple[Term, str]:
        """Parses a prefix of the given string into a term.

        Parameters:
            s: string to parse, which has a prefix that is a valid
                representation of a term.

        Returns:
            A pair of the parsed term and the unparsed suffix of the string. If
            the given string has as a prefix a constant name (e.g., ``'c12'``)
            or a variable name (e.g., ``'x12'``), then the parsed prefix will
            be that entire name (and not just a part of it, such as ``'x1'``).
        """
        if is_constant(s[0]):
            index = Term.find_string(s, is_constant)
            return Term(s[: index]), s[index:]
        if is_variable(s[0]):
            index = Term.find_string(s, is_variable)
            return Term(s[: index]), s[index:]
        # this is a function
        function_name = s[:Term.find_string(s, is_function)]
        s = s[len(function_name):]
        args = []
        while s[0] != ')':
            term, s = Term.parse_prefix(s[1:])  # skip the , or the (
            args.append(term)
        return Term(function_name, args), s[1:]  # skip the )

    @staticmethod
    def parse(s: str) -> Term:
        """Parses the given valid string representation into a term.

        Parameters:
            s: string to parse.

        Returns:
            A term whose standard string representation is the given string.
        """
        term, string = Term.parse_prefix(s)
        return term

    def constants(self) -> Set[str]:
        """Finds all constant names in the current term.

        Returns:
            A set of all constant names used in the current term.
        """
        if is_constant(self.root):
            return {self.root}
        if is_variable(self.root):
            return set()
        # this is a function
        new_set = set()
        for argument in self.arguments:
            new_set |= argument.constants()
        return new_set

    def variables(self) -> Set[str]:
        """Finds all variable names in the current term.

        Returns:
            A set of all variable names used in the current term.
        """
        if is_constant(self.root):
            return set()
        if is_variable(self.root):
            return {self.root}
        # this is a function
        new_set = set()
        for argument in self.arguments:
            new_set |= argument.variables()
        return new_set

    def functions(self) -> Set[Tuple[str, int]]:
        """Finds all function names in the current term, along with their
        arities.

        Returns:
            A set of pairs of function name and arity (number of arguments) for
            all function names used in the current term.
        """
        if is_constant(self.root):
            return set()
        if is_variable(self.root):
            return set()
        # this is a function
        new_set = set()
        for argument in self.arguments:
            new_set |= argument.functions()
        return new_set | {(self.root, len(self.arguments))}

    def substitute(self, substitution_map: Mapping[str, Term],
                   forbidden_variables: AbstractSet[
                       str] = frozenset()) -> Term:
        """Substitutes in the current term, each constant name `name` or
        variable name `name` that is a key in `substitution_map` with the term
        `substitution_map[name]`.

        Parameters:
            substitution_map: mapping defining the substitutions to be
                performed.
            forbidden_variables: variables not allowed in substitution terms.

        Returns:
            The term resulting from performing all substitutions. Only
            constant names and variable names originating in the current term
            are substituted (i.e., those originating in one of the specified
            substitutions are not subjected to additional substitutions).

        Raises:
            ForbiddenVariableError: If a term that is used in the requested
                substitution contains a variable from `forbidden_variables`.

        Examples:
            >>> Term.parse('f(x,c)').substitute(
            ...    {'c': Term.parse('plus(d,x)'), 'x': Term.parse('c')}, {'y'})
            f(c,plus(d,x))
            >>> Term.parse('f(x,c)').substitute(
            ...     {'c': Term.parse('plus(d,y)')}, {'y'})
            Traceback (most recent call last):
              ...
            predicates.syntax.ForbiddenVariableError: y
        """
        for element_name in substitution_map:
            assert is_constant(element_name) or is_variable(element_name)
        for variable in forbidden_variables:
            assert is_variable(variable)
        if is_variable(self.root) or is_constant(self.root):
            if self.root in substitution_map:
                if self.root in forbidden_variables:
                    return self
                variables = substitution_map[self.root].variables()
                inter = list(variables & forbidden_variables)
                if inter:
                    raise ForbiddenVariableError(inter[0])
                return substitution_map[self.root]
            return self
        args = [argument.substitute(substitution_map, forbidden_variables)
                for argument in self.arguments]
        return Term(self.root, args)


def is_equality(s: str) -> bool:
    """Checks if the given string is the equality relation.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is the equality relation, ``False``
        otherwise.
    """
    return s == '='


def is_relation(s: str) -> bool:
    """Checks if the given string is a relation name.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is a relation name, ``False`` otherwise.
    """
    return s[0] >= 'F' and s[0] <= 'T' and s.isalnum()


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
    return s == '&' or s == '|' or s == '->'


def is_quantifier(s: str) -> bool:
    """Checks if the given string is a quantifier.

    Parameters:
        s: string to check.

    Returns:
        ``True`` if the given string is a quantifier, ``False`` otherwise.
    """
    return s == 'A' or s == 'E'


@frozen
class Formula:
    """An immutable first-order formula in tree representation, composed from
    relation names applied to first-order terms, and operators and
    quantifications applied to them.

    Attributes:
        root (`str`): the relation name, equality relation, operator, or
            quantifier at the root of the formula tree.
        arguments (`~typing.Optional`\\[`~typing.Tuple`\\[`Term`, ...]]): the
            arguments to the root, if the root is a relation name or the
            equality relation.
        first (`~typing.Optional`\\[`Formula`]): the first operand to the root,
            if the root is a unary or binary operator.
        second (`~typing.Optional`\\[`Formula`]): the second
            operand to the root, if the root is a binary operator.
        variable (`~typing.Optional`\\[`str`]): the variable name quantified by
            the root, if the root is a quantification.
        predicate (`~typing.Optional`\\[`Formula`]): the predicate quantified
        by the root, if the root is a quantification.
    """
    root: str
    arguments: Optional[Tuple[Term, ...]]
    first: Optional[Formula]
    second: Optional[Formula]
    variable: Optional[str]
    predicate: Optional[Formula]

    def __init__(self, root: str,
                 arguments_or_first_or_variable: Union[Sequence[Term],
                                                       Formula, str],
                 second_or_predicate: Optional[Formula] = None) -> None:
        """Initializes a `Formula` from its root and root arguments, root
        operands, or root quantified variable and predicate.

        Parameters:
            root: the root for the formula tree.
            arguments_or_first_or_variable: the arguments to the the root, if
                the root is a relation name or the equality relation; the first
                operand to the root, if the root is a unary or binary operator;
                the variable name quantified by the root, if the root is a
                quantification.
            second_or_predicate: the second operand to the root, if the root is
                a binary operator; the predicate quantified by the root, if the
                root is a quantification.
        """
        if is_equality(root) or is_relation(root):
            # Populate self.root and self.arguments
            assert second_or_predicate is None
            assert isinstance(arguments_or_first_or_variable, Sequence) and \
                   not isinstance(arguments_or_first_or_variable, str)
            self.root, self.arguments = \
                root, tuple(arguments_or_first_or_variable)
            if is_equality(root):
                assert len(self.arguments) == 2
        elif is_unary(root):
            # Populate self.first
            assert isinstance(arguments_or_first_or_variable, Formula) and \
                   second_or_predicate is None
            self.root, self.first = root, arguments_or_first_or_variable
        elif is_binary(root):
            # Populate self.first and self.second
            assert isinstance(arguments_or_first_or_variable, Formula) and \
                   second_or_predicate is not None
            self.root, self.first, self.second = \
                root, arguments_or_first_or_variable, second_or_predicate
        else:
            assert is_quantifier(root)
            # Populate self.variable and self.predicate
            assert isinstance(arguments_or_first_or_variable, str) and \
                   is_variable(arguments_or_first_or_variable) and \
                   second_or_predicate is not None
            self.root, self.variable, self.predicate = \
                root, arguments_or_first_or_variable, second_or_predicate

    def __repr__(self) -> str:
        """Computes the string representation of the current formula.

        Returns:
            The standard string representation of the current formula.
        """
        if is_unary(self.root):  # this is of type ~p
            return self.root + str(self.first)
        if is_equality(self.root):  # this is of type p = q
            return str(self.arguments[0]) + self.root + str(self.arguments[1])
        if is_relation(self.root):  # this is of type p(a,b,c(
            string = ','.join([str(argument) for argument in self.arguments])
            return self.root + '(' + string + ')'
        if is_binary(self.root):  # this is like p op q
            return '(' + str(self.first) + self.root + str(self.second) + ')'
        # this is a quantifier, i.e. Ax[p] or Ex[p]
        return self.root + str(self.variable) + '[' + str(self.predicate) + ']'

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
            equal the current formula, ``False`` otherwise.
        """
        return not self == other

    def __hash__(self) -> int:
        return hash(str(self))

    @staticmethod
    def parse_prefix(s: str) -> Tuple[Formula, str]:
        """Parses a prefix of the given string into a formula.

        Parameters:
            s: string to parse, which has a prefix that is a valid
                representation of a formula.

        Returns:
            A pair of the parsed formula and the unparsed suffix of the string.
            If the given string has as a prefix a term followed by an equality
            followed by a constant name (e.g., ``'c12'``) or by a variable name
            (e.g., ``'x12'``), then the parsed prefix will include that entire
            name (and not just a part of it, such as ``'x1'``).
        """
        if is_unary(s[0]):  # this is of type ~p
            formula, string = Formula.parse_prefix(s[1:])
            return Formula(s[0], formula), string
        if is_quantifier(s[0]):  # this is a quantifier, i.e. Ax[p] or Ex[p]
            return Formula.parse_prefix_quantifier(s)
        if is_relation(s[0]):  # this is of type p(a,b,c(
            return Formula.parse_prefix_relation(s)
        if s[0] == '(':  # this is like p op q
            return Formula.parse_prefix_op(s)
        # this is of type p = q
        return Formula.parse_prefix_equality(s)

    @staticmethod
    def parse_prefix_op(s: str) -> Tuple[Formula, str]:
        """
        :param s: s of type (formula1 op formula2) and then junk
        :return: the formula and the remainder
        """
        s = s[1:]  # skip the (
        formula1, s = Formula.parse_prefix(s)
        op = find_op(s)
        s = s[len(op):]  # skip the op
        formula2, s = Formula.parse_prefix(s)
        return Formula(op, formula1, formula2), s[1:]  # skip the )

    @staticmethod
    def parse_prefix_quantifier(s: str) -> Tuple[Formula, str]:
        """
        :param s: s of type Ax[formula] or Ex[formula] and then junk
        :return: the formula and the remainder
        """
        quantifier = s[0]
        s = s[1:]  # skip the quantifier
        variable = s[:Term.find_string(s, is_variable)]
        s = s[len(variable):]  # skip the variable
        s = s[1:]  # skip the [
        formula, string = Formula.parse_prefix(s)
        # skip the ]
        return Formula(quantifier, variable, formula), string[1:]

    @staticmethod
    def parse_prefix_relation(s: str) -> Tuple[Formula, str]:
        """
        :param s: s of type f(f1, f2,...) and then junk or f()
        :return: the formula and the remainder
        """
        relation = s[:Term.find_string(s, is_relation)]
        s = s[len(relation):]
        if s[:2] == '()':
            return Formula(relation, []), s[2:]
        args = []
        while s[0] != ')':
            term, s = Term.parse_prefix(s[1:])  # skip the , or the (
            args.append(term)
        return Formula(relation, args), s[1:]

    @staticmethod
    def parse_prefix_equality(s: str) -> Tuple[Formula, str]:
        """
        :param s: s of type formula1=formula2 and then junk
        :return: the formula and the remainder
        """
        term1, s = Term.parse_prefix(s)
        op = s[0]
        s = s[len(op):]  # skip the op
        term2, s = Term.parse_prefix(s)
        return Formula(op, [term1, term2]), s

    @staticmethod
    def parse(s: str) -> Formula:
        """Parses the given valid string representation into a formula.

        Parameters:
            s: string to parse.

        Returns:
            A formula whose standard string representation is the given string.
        """
        formula, string = Formula.parse_prefix(s)
        return formula

    def constants(self) -> Set[str]:
        """Finds all constant names in the current formula.

        Returns:
            A set of all constant names used in the current formula.
        """
        if is_unary(self.root):  # this is of type ~p
            return self.first.constants()
        if is_equality(self.root):  # this is of type p = q
            return self.arguments[0].constants() | \
                   self.arguments[1].constants()
        if is_relation(self.root):  # this is of type p(a,b,c(
            new_set = set()
            for argument in self.arguments:
                new_set |= argument.constants()
            return new_set
        if is_binary(self.root):  # this is like p op q
            return self.first.constants() | self.second.constants()
        # this is a quantifier, i.e. Ax[p] or Ex[p]
        return self.predicate.constants()

    def variables(self) -> Set[str]:
        """Finds all variable names in the current formula.

        Returns:
            A set of all variable names used in the current formula.
        """
        if is_unary(self.root):  # this is of type ~p
            return self.first.variables()
        if is_equality(self.root):  # this is of type p = q
            return self.arguments[0].variables() | \
                   self.arguments[1].variables()
        if is_relation(self.root):  # this is of type p(a,b,c(
            new_set = set()
            for argument in self.arguments:
                new_set |= argument.variables()
            return new_set
        if is_binary(self.root):  # this is like p op q
            return self.first.variables() | self.second.variables()
        # this is a quantifier, i.e. Ax[p] or Ex[p]
        return self.predicate.variables() | {self.variable}

    def free_variables(self) -> Set[str]:
        """Finds all variable names that are free in the current formula.

        Returns:
            A set of all variable names used in the current formula not only
            within a scope of a quantification on those variable names.
        """
        if is_unary(self.root):  # this is of type ~p
            return self.first.free_variables()
        if is_equality(self.root):  # this is of type p = q
            return self.arguments[0].variables() | \
                   self.arguments[1].variables()
        if is_relation(self.root):  # this is of type p(a,b,c(
            new_set = set()
            for argument in self.arguments:
                new_set |= argument.variables()
            return new_set
        if is_binary(self.root):  # this is like p op q
            return self.first.free_variables() | self.second.free_variables()
        # this is a quantifier, i.e. Ax[p] or Ex[p]
        return {element for element in self.predicate.free_variables()
                if element != self.variable}

    def functions(self) -> Set[Tuple[str, int]]:
        """Finds all function names in the current formula, along with their
        arities.

        Returns:
            A set of pairs of function name and arity (number of arguments) for
            all function names used in the current formula.
        """
        if is_unary(self.root):  # this is of type ~p
            return self.first.functions()
        if is_equality(self.root):  # this is of type p = q
            return self.arguments[0].functions() | \
                   self.arguments[1].functions()
        if is_relation(self.root):  # this is of type p(a,b,c(
            new_set = set()
            for argument in self.arguments:
                new_set |= argument.functions()
            return new_set
        if is_binary(self.root):  # this is like p op q
            return self.first.functions() | self.second.functions()
        # this is a quantifier, i.e. Ax[p] or Ex[p]
        return self.predicate.functions()

    def relations(self) -> Set[Tuple[str, int]]:
        """Finds all relation names in the current formula, along with their
        arities.

        Returns:
            A set of pairs of relation name and arity (number of arguments) for
            all relation names used in the current formula.
        """
        if is_unary(self.root):  # this is of type ~p
            return self.first.relations()
        if is_equality(self.root):  # this is of type p = q
            return set()
        if is_relation(self.root):  # this is of type p(a,b,c(
            return {(self.root, len(self.arguments))}
        if is_binary(self.root):  # this is like p op q
            return self.first.relations() | self.second.relations()
        # this is a quantifier, i.e. Ax[p] or Ex[p]
        return self.predicate.relations()

    def substitute(self, substitution_map: Mapping[str, Term],
                   forbidden_variables: AbstractSet[str] = frozenset()) -> \
            Formula:
        """Substitutes in the current formula, each constant name `name` or free
        occurrence of variable name `name` that is a key in `substitution_map`
        with the term `substitution_map[name]`.

        Parameters:
            substitution_map: mapping defining the substitutions to be
                performed.
            forbidden_variables: variables not allowed in substitution terms.

        Returns:
            The formula resulting from performing all substitutions. Only
            constant names and variable names originating in the current formula
            are substituted (i.e., those originating in one of the specified
            substitutions are not subjected to additional substitutions).

        Raises:
            ForbiddenVariableError: If a term that is used in the requested
                substitution contains a variable from `forbidden_variables`
                or a variable occurrence that becomes bound when that term is
                substituted into the current formula.

        Examples:
            >>> Formula.parse('Ay[x=c]').substitute(
            ...     {'c': Term.parse('plus(d,x)'), 'x': Term.parse('c')}, {'z'})
            Ay[c=plus(d,x)]
            >>> Formula.parse('Ay[x=c]').substitute(
            ...     {'c': Term.parse('plus(d,z)')}, {'z'})
            Traceback (most recent call last):
              ...
            predicates.syntax.ForbiddenVariableError: z
            >>> Formula.parse('Ay[x=c]').substitute(
            ...     {'c': Term.parse('plus(d,y)')})
            Traceback (most recent call last):
              ...
            predicates.syntax.ForbiddenVariableError: y
        """
        for element_name in substitution_map:
            assert is_constant(element_name) or is_variable(element_name)
        for variable in forbidden_variables:
            assert is_variable(variable)
        if is_relation(self.root) or is_equality(self.root):
            args = [argument.substitute(substitution_map, forbidden_variables)
                    for argument in self.arguments]
            return Formula(self.root, args)
        if is_quantifier(self.root):
            new_forbidden_variables = forbidden_variables | {self.variable}
            predicate = self.predicate.substitute(substitution_map,
                                             new_forbidden_variables)
            return Formula(self.root, self.variable, predicate)
        if is_binary(self.root):
            first = self.first.substitute(substitution_map,
                                          forbidden_variables)
            second = self.second.substitute(substitution_map,
                                          forbidden_variables)
            return Formula(self.root, first, second)
        if is_unary(self.root):
            first = self.first.substitute(substitution_map,
                                          forbidden_variables)
            return Formula(self.root, first)

    def propositional_skeleton(self) -> Tuple[PropositionalFormula,
                                              Mapping[str, Formula]]:
        """Computes a propositional skeleton of the current formula.

        Returns:
            A pair. The first element of the pair is a propositional formula
            obtained from the current formula by substituting every (outermost)
            subformula that has a relation or quantifier at its root with an
            atomic propositional formula, consistently such that multiple equal
            such (outermost) subformulas are substituted with the same atomic
            propositional formula. The atomic propositional formulas used for
            substitution are obtained, from left to right, by calling
            `next`\ ``(``\ `~logic_utils.fresh_variable_name_generator`\ ``)``.
            The second element of the pair is a map from each atomic
            propositional formula to the subformula for which it was
            substituted.
        """
        dct = {}
        formula = self.convert_to_propositional_skeleton(dct)
        mapper = {dct[key] : key for key in dct.keys()}
        return formula, mapper


    def convert_to_propositional_skeleton(self, dct: Dict[Formula, str]) \
            -> PropositionalFormula:
        """
        :param dct: the current mapping from Formula to names
        :return: the new PropositionalFormula from self formula
        """
        if is_unary(self.root):
            first = self.first.convert_to_propositional_skeleton(dct)
            return PropositionalFormula('~', first)
        if is_binary(self.root):
            first = self.first.convert_to_propositional_skeleton(dct)
            second = self.second.convert_to_propositional_skeleton(dct)
            return PropositionalFormula(self.root, first, second)
        if self not in dct:
            dct[self] = next(fresh_variable_name_generator)
        return PropositionalFormula(dct[self])

    @staticmethod
    def from_propositional_skeleton(skeleton: PropositionalFormula,
                                    substitution_map: Mapping[str, Formula]) -> \
            Formula:
        """Computes a first-order formula from a propositional skeleton and a
        substitution map.

        Arguments:
            skeleton: propositional skeleton for the formula to compute.
            substitution_map: a map from each atomic propositional subformula
                of the given skeleton to a first-order formula.

        Returns:
            A first-order formula obtained from the given propositional skeleton
            by substituting each atomic propositional subformula with the formula
            mapped to it by the given map.
        """
        for key in substitution_map:
            assert is_propositional_variable(key)
        if is_propositional_variable(skeleton.root):
            return substitution_map[skeleton.root]
        if is_unary(skeleton.root):
            first = Formula.from_propositional_skeleton(skeleton.first,
                                                        substitution_map)
            return Formula(skeleton.root, first)
        if is_binary(skeleton.root):
            first = Formula.from_propositional_skeleton(skeleton.first,
                                                        substitution_map)
            second = Formula.from_propositional_skeleton(skeleton.second,
                                                        substitution_map)
            return Formula(skeleton.root, first, second)
