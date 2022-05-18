# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: propositions/proofs.py

"""Proofs by deduction in propositional logic."""

from __future__ import annotations
from typing import AbstractSet, Iterable, FrozenSet, List, Mapping, Optional, \
    Set, Tuple, Union

from logic_utils import frozen

from propositions.syntax import *

SpecializationMap = Mapping[str, Formula]


@frozen
class InferenceRule:
    """An immutable inference rule in propositional logic, comprised by zero
    or more assumed propositional formulae, and a conclusion propositional
    formula.

    Attributes:
        assumptions (`~typing.Tuple`\\[`~propositions.syntax.Formula`, ...]):
            the assumptions of the rule.
        conclusion (`~propositions.syntax.Formula`): the conclusion of the
        rule.
    """
    assumptions: Tuple[Formula, ...]
    conclusion: Formula

    def __init__(self, assumptions: Iterable[Formula], conclusion: Formula)\
            -> None:
        """Initialized an `InferenceRule` from its assumptions and conclusion.

        Parameters:
            assumptions: the assumptions for the rule.
            conclusion: the conclusion for the rule.
        """
        self.assumptions = tuple(assumptions)
        self.conclusion = conclusion

    def __eq__(self, other: object) -> bool:
        """Compares the current inference rule with the given one.

        Parameters:
            other: object to compare to.

        Returns:
            ``True`` if the given object is an `InferenceRule` object that
            equals the current inference rule, ``False`` otherwise.
        """
        return (isinstance(other, InferenceRule) and
                self.assumptions == other.assumptions and
                self.conclusion == other.conclusion)

    def __ne__(self, other: object) -> bool:
        """Compares the current inference rule with the given one.

        Parameters:
            other: object to compare to.

        Returns:
            ``True`` if the given object is not an `InferenceRule` object or
            does not does not equal the current inference rule, ``False``
            otherwise.
        """
        return not self == other

    def __hash__(self) -> int:
        return hash(str(self))

    def __repr__(self) -> str:
        """Computes a string representation of the current inference rule.

        Returns:
            A string representation of the current inference rule.
        """
        return str([str(assumption) for assumption in self.assumptions]) + \
               ' ==> ' + "'" + str(self.conclusion) + "'"

    def variables(self) -> Set[str]:
        """Finds all atomic propositions (variables) in the current inference
        rule.

        Returns:
            A set of all atomic propositions used in the assumptions and in the
            conclusion of the current inference rule.
        """
        variable_set = set()
        for assumption in self.assumptions:
            variable_set |= assumption.variables()
        return variable_set | self.conclusion.variables()

    def specialize(self, specialization_map: SpecializationMap) -> \
            InferenceRule:
        """Specializes the current inference rule by simultaneously substituting
        each variable `v` that is a key in `specialization_map` with the
        formula `specialization_map[v]`.

        Parameters:
            specialization_map: mapping defining the specialization to be
                performed.

        Returns:
            The resulting inference rule.
        """
        for variable in specialization_map:
            assert is_variable(variable)
        new_assumptions = tuple(
            assumption.substitute_variables(specialization_map)
            for assumption in self.assumptions)
        new_conclusion = self.conclusion.substitute_variables(
            specialization_map)
        return InferenceRule(new_assumptions, new_conclusion)

    @staticmethod
    def merge_specialization_maps(
            specialization_map1: Union[SpecializationMap, None],
            specialization_map2: Union[SpecializationMap, None]) -> \
            Union[SpecializationMap, None]:
        """Merges the given specialization maps.

        Parameters:
            specialization_map1: first map to merge, or ``None``.
            specialization_map2: second map to merge, or ``None``.

        Returns:
            A single map containing all (key, value) pairs that appear in
            either of the given maps, or ``None`` if one of the given maps is
            ``None`` or if some key appears in both given maps but with
            different values.
        """
        if specialization_map1 is not None:
            for variable in specialization_map1:
                assert is_variable(variable)
        if specialization_map2 is not None:
            for variable in specialization_map2:
                assert is_variable(variable)
        if specialization_map1 is None or specialization_map2 is None:
            return None
        mapping = dict()
        for key in specialization_map1.keys():
            mapping[key] = specialization_map1[key]
        for key in specialization_map2.keys():
            if key in mapping and mapping[key] != specialization_map2[key]:
                return None
            else:
                mapping[key] = specialization_map2[key]
        return mapping

    @staticmethod
    def formula_specialization_map(general: Formula, specialization: Formula) \
            -> Union[SpecializationMap, None]:
        """Computes the minimal specialization map by which the given formula
        specializes to the given specialization.

        Parameters:
            general: non-specialized formula for which to compute the map.
            specialization: specialization for which to compute the map.

        Returns:
            The computed specialization map, or ``None`` if `specialization` is
            in fact not a specialization of `general`.
        """
        if is_constant(general.root):
            if general.root == specialization.root:  # else it is an error
                return {}
            return None
        if is_variable(general.root):  # replace the variable
            return {general.root: specialization}
        if is_unary(general.root):  # replace the terms of the unary
            if general.root != specialization.root:  # if it is an error
                return
            return InferenceRule \
                .formula_specialization_map(general.first,
                                            specialization.first)
        if is_binary(general.root):  # replace the terms of the binary
            if general.root != specialization.root:  # if it is an error
                return
            map1 = InferenceRule \
                .formula_specialization_map(general.first,
                                            specialization.first)
            map2 = InferenceRule \
                .formula_specialization_map(general.second,
                                            specialization.second)
            return InferenceRule.merge_specialization_maps(map1, map2)

    def specialization_map(self, specialization: InferenceRule) -> \
            Union[SpecializationMap, None]:
        """Computes the minimal specialization map by which the current
        inference rule specializes to the given specialization.

        Parameters:
            specialization: specialization for which to compute the map.

        Returns:
            The computed specialization map, or ``None`` if `specialization` is
            in fact not a specialization of the current rule.
        """
        mapping = {}
        if len(self.assumptions) != len(specialization.assumptions):
            return
        if len(self.assumptions) == 0:
            return InferenceRule \
                .formula_specialization_map(self.conclusion,
                                            specialization.conclusion)
        for assumption, speciality in zip(self.assumptions,
                                          specialization.assumptions):
            new_dct = InferenceRule.formula_specialization_map(assumption,
                                                               speciality)
            mapping = InferenceRule.merge_specialization_maps(mapping, new_dct)
        if mapping is None:
            return
        string_conclusion = str(self.conclusion.substitute_variables(mapping))
        # if it is indeed the correct map, return it
        if string_conclusion == str(specialization.conclusion):
            return mapping

    def is_specialization_of(self, general: InferenceRule) -> bool:
        """Checks if the current inference rule is a specialization of the given
        inference rule.

        Parameters:
            general: non-specialized inference rule to check.

        Returns:
            ``True`` if the current inference rule is a specialization of
            `general`, ``False`` otherwise.
        """
        return general.specialization_map(self) is not None


@frozen
class Proof:
    """A frozen deductive proof, comprised of a statement in the form of an
    inference rule, a set of inference rules that may be used in the proof, and
    a proof in the form of a list of lines that prove the statement via these
    inference rules.

    Attributes:
        statement (`InferenceRule`): the statement of the proof.
        rules (`~typing.AbstractSet`\\[`InferenceRule`]): the allowed rules of
            the proof.
        lines (`~typing.Tuple`\\[`Line`]): the lines of the proof.
    """
    statment: InferenceRule
    rules: FrozenSet[InferenceRule]
    lines: Tuple[Proof.Line, ...]

    def __init__(self, statement: InferenceRule,
                 rules: AbstractSet[InferenceRule],
                 lines: Iterable[Proof.Line]) -> None:
        """Initializes a `Proof` from its statement, allowed inference rules,
        and lines.

        Parameters:
            statement: the statement for the proof.
            rules: the allowed rules for the proof.
            lines: the lines for the proof.
        """
        self.statement = statement
        self.rules = frozenset(rules)
        self.lines = tuple(lines)

    @frozen
    class Line:
        """An immutable line in a deductive proof, comprised of a formula which
        is either justified as an assumption of the proof, or as the conclusion
        of a specialization of an allowed inference rule of the proof, the
        assumptions of which are justified by previous lines in the proof.

        Attributes:
            formula (`~propositions.syntax.Formula`): the formula justified by
                the line.
            rule (`~typing.Optional`\\[`InferenceRule`]): the inference rule
                out of those allowed in the proof, a specialization of which
                concludes the formula, or ``None`` if the formula is justified
                as an assumption of the proof.
            assumptions
                (`~typing.Optional`\\[`~typing.Tuple`\\[`int`]): a tuple of
                zero or more indices of previous lines in the proof whose
                formulae are the respective assumptions of the specialization
                of the rule that concludes the formula, if the formula is not
                justified as an assumption of the proof.
        """
        formula: Formula
        rule: Optional[InferenceRule]
        assumptions: Optional[Tuple[int, ...]]

        def __init__(self, formula: Formula,
                     rule: Optional[InferenceRule] = None,
                     assumptions: Optional[Iterable[int]] = None) -> None:
            """Initializes a `~Proof.Line` from its formula, and optionally its
            rule and indices of justifying previous lines.

            Parameters:
                formula: the formula to be justified by this line.
                rule: the inference rule out of those allowed in the proof, a
                    specialization of which concludes the formula, or ``None``
                    if the formula is to be justified as an assumption of the
                    proof.
                assumptions: an iterable over indices of previous lines in the
                    proof whose formulae are the respective assumptions of the
                    specialization of the rule that concludes the formula, or
                    ``None`` if the formula is to be justified as an assumption
                    of the proof.
            """
            assert (rule is None and assumptions is None) or \
                   (rule is not None and assumptions is not None)
            self.formula = formula
            self.rule = rule
            if assumptions is not None:
                self.assumptions = tuple(assumptions)

        def __repr__(self) -> str:
            """Computes a string representation of the current proof line.

            Returns:
                A string representation of the current proof line.
            """
            if self.rule is None:
                return str(self.formula)
            else:
                return str(self.formula) + ' Inference Rule ' + \
                       str(self.rule) + \
                       ((" on " + str(self.assumptions))
                        if len(self.assumptions) > 0 else '')

        def is_assumption(self) -> bool:
            """Checks if the current proof line is justified as an assumption
            of the proof.

            Returns:
                ``True`` if the current proof line is justified as an
                assumption of the proof, ``False`` otherwise.
            """
            return self.rule is None

    def __repr__(self) -> str:
        """Computes a string representation of the current proof.

        Returns:
            A string representation of the current proof.
        """
        r = 'Proof for ' + str(self.statement) + ' via inference rules:\n'
        for rule in self.rules:
            r += '  ' + str(rule) + '\n'
        r += "Lines:\n"
        for i in range(len(self.lines)):
            r += ("%3d) " % i) + str(self.lines[i]) + '\n'
        return r

    def rule_for_line(self, line_number: int) -> Union[InferenceRule, None]:
        """Computes the inference rule whose conclusion is the formula justified
        by the specified line, and whose assumptions are the formulae justified
        by the lines specified as the assumptions of that line.

        Parameters:
            line_number: index of the line according to which to construct the
                inference rule.

        Returns:
            The constructed inference rule, with assumptions ordered in the
            order of their indices in the specified line, or ``None`` if the
            specified line is justified as an assumption.
        """
        assert line_number < len(self.lines)
        line = self.lines[line_number]
        if line.is_assumption():
            return
        # not assumption
        assumptions = [self.lines[i].formula for i in list(line.assumptions)]
        return InferenceRule(assumptions, line.formula)

    def is_line_valid(self, line_number: int) -> bool:
        """Checks if the specified line validly follows from its justifications.

        Parameters:
            line_number: index of the line to check.

        Returns:
            If the specified line is justified as an assumption, then ``True``
            if the formula justified by this line is an assumption of the
            current proof, ``False`` otherwise. Otherwise (i.e., if the
            specified line is justified as a conclusion of an inference rule),
            then ``True`` if and only if all of the following hold:

            1. The rule specified for that line is one of the allowed inference
               rules in the current proof.
            2. Some specialization of the rule specified for that line has
               the formula justified by that line as its conclusion, and the
               formulae justified by the lines specified as the assumptions of
               that line (in the order of their indices in this line) as its
               assumptions.
        """
        assert line_number < len(self.lines)
        line = self.lines[line_number]
        if line.is_assumption():
            for assumption in self.statement.assumptions:
                if str(assumption) == str(line):
                    return True
            return False
        # this is not an assumption
        if line.rule not in self.rules:
            return False
        # every assumption is before this line
        for assumption in line.assumptions:
            if line_number <= assumption:
                return False
        return self.rule_for_line(line_number).is_specialization_of(line.rule)

    def is_valid(self) -> bool:
        """Checks if the current proof is a valid proof of its claimed statement
        via its inference rules.

        Returns:
            ``True`` if the current proof is a valid proof of its claimed
            statement via its inference rules, ``False`` otherwise.
        """
        for i in range(len(self.lines)):
            if self.is_line_valid(i) is False:
                return False
        return str(self.lines[-1].formula) == str(self.statement.conclusion)


# Chapter 5 tasks
def specialize_line(line: Proof.Line, mapping) -> Proof.Line:
    """
    :param line: a line
    :param mapping: the mapping of variables
    :return: the specialized line with the mapping
    """
    new_statement = line.formula.substitute_variables(mapping)
    if line.is_assumption():
        return Proof.Line(new_statement)
    return Proof.Line(new_statement, line.rule, line.assumptions)


def prove_specialization(proof: Proof, specialization: InferenceRule) -> Proof:
    """Converts the given proof of an inference rule into a proof of the given
    specialization of that inference rule.

    Parameters:
        proof: valid proof to convert.
        specialization: specialization of the conclusion of the given proof.

    Returns:
        A valid proof of the given specialization via the same inference rules
        as the given proof.
    """
    assert proof.is_valid()
    assert specialization.is_specialization_of(proof.statement)
    mapping = proof.statement.specialization_map(specialization)
    new_lines = [specialize_line(proof.lines[i], mapping)
                 for i in range(len(proof.lines))]
    new_statement = proof.statement.specialize(mapping)
    return Proof(new_statement, proof.rules, new_lines)


def find_rule(lemma_line: Proof.Line, main_line: Proof.Line,
              main_proof: Proof):
    """
    :param lemma_line: a lemma line (assumption in the lemma)
    :param main_line: a main proof line to replace
    :param main_proof: the proof of the main proof
    :return: the rule and assumptions of the lemma line in the main proof
    """
    for assumption in main_line.assumptions:
        line = main_proof.lines[assumption]
        if lemma_line.formula == line.formula:
            if line.is_assumption():
                return None, None
            return line.rule, line.assumptions


def create_lemma_lines(main_proof: Proof, lemma_proof: Proof,
                       line_number: int) -> List[Proof.Line]:
    """
    :param main_proof: the main proof
    :param lemma_proof: the lemma proof
    :param line_number: the line to change
    :return: the new lines of the lemma proof
    """
    new_lines = []
    for i in range(len(lemma_proof.lines)):
        if lemma_proof.lines[i].is_assumption():
            rule, assumptions = find_rule(lemma_proof.lines[i],
                                          main_proof.lines[line_number],
                                          main_proof)
            new_lines.append(Proof.Line(lemma_proof.lines[i].formula, rule,
                                        assumptions))
        else:
            f = lambda x: (x + line_number)
            new_lines.append(update_line_assumptions(lemma_proof.lines[i], f))
    return new_lines


def convert_lines(main_proof: Proof, lemma_proof: Proof,
                  line_number: int) -> List[Proof.Line]:
    """
    :param main_proof: the main proof
    :param lemma_proof: the lemma proof
    :param line_number: the line to change
    :return: the new lines of the combined proof
    """
    new_lines = [main_proof.lines[i] for i in range(line_number)]
    lemma_lines = create_lemma_lines(main_proof, lemma_proof, line_number)
    new_lines.extend(lemma_lines)
    update_num = len(lemma_lines) - 1
    for i in range(line_number + 1, len(main_proof.lines)):
        if main_proof.lines[i].is_assumption():
            new_lines.append(main_proof.lines[i])
        else:
            f = lambda x: (x + update_num if line_number <= x else x)
            new_lines.append(update_line_assumptions(main_proof.lines[i], f))
    return new_lines


def inline_proof_once(main_proof: Proof, line_number: int,
                      lemma_proof: Proof) -> Proof:
    """Inlines the given proof of a "lemma" inference rule into the given proof
    that uses that "lemma" rule, eliminating the usage of (a specialization of)
    that "lemma" rule in the specified line in the latter proof.

    Parameters:
        main_proof: valid proof to inline into.
        line_number: index of the line in `main_proof` that should be replaced.
        lemma_proof: valid proof of the inference rule of the specified line
        (an allowed inference rule of `main_proof`).

    Returns:
        A valid proof obtained by replacing the specified line in `main_proof`
        with a full (specialized) list of lines proving the formula of the
        specified line from the lines specified as the assumptions of that
        line, and updating line indices specified throughout the proof to
        maintain the validity of the proof. The set of allowed inference rules
        in the returned proof is the union of the rules allowed in the two
        given proofs, but the "lemma" rule that is used in the specified line
        in `main_proof` is no longer used in the corresponding lines in the
        returned proof (and thus, this "lemma" rule is used one less time in
        the returned proof than in `main_proof`).
    """
    assert main_proof.lines[line_number].rule == lemma_proof.statement
    assert lemma_proof.is_valid()
    line_rule = main_proof.rule_for_line(line_number)
    lemma_specialized = prove_specialization(lemma_proof, line_rule)
    #  create the new rules
    new_rules = add_rules(main_proof, lemma_proof.rules)
    #  create the new lines
    new_lines = convert_lines(main_proof, lemma_specialized, line_number)
    return Proof(main_proof.statement, new_rules, new_lines)


def inline_proof(main_proof: Proof, lemma_proof: Proof) -> Proof:
    """Inlines the given proof of a "lemma" inference rule into the given proof
    that uses that "lemma" rule, eliminating all usages of (any specialization
    of) that "lemma" rule in the latter proof.

    Parameters:
        main_proof: valid proof to inline into.
        lemma_proof: valid proof of one of the allowed inference rules of
            `main_proof`.

    Returns:
        A valid proof obtained from `main_proof` by inlining (an appropriate
        specialization of) `lemma_proof` in lieu of each line that specifies
        the "lemma" inference rule proved by `lemma_proof` as its
        justification. The set of allowed inference rules in the returned proof
         is the union of th e rules allowed in the two given proofs but without
          the "lemma" rule proved by lemma_proof`.
    """
    new_proof = main_proof
    i = 0
    while i < len(new_proof.lines):
        if not new_proof.lines[i].is_assumption() and \
                lemma_proof.statement.is_specialization_of(
                    new_proof.lines[i].rule):
            new_proof = inline_proof_once(new_proof, i, lemma_proof)
        i += 1
    return Proof(new_proof.statement,
                 delete_rule(new_proof, lemma_proof.statement),
                 new_proof.lines)


def add_rule(proof: Proof, rule: InferenceRule) -> AbstractSet[InferenceRule]:
    """
    :param proof: a proof
    :param rule: a rule
    :return: the combined rules of the proof and the rule
    """
    return {rule} | proof.rules


def add_rules(proof: Proof, rules: AbstractSet[InferenceRule]) \
        -> AbstractSet[InferenceRule]:
    """
    :param proof: a proof
    :param rules: the rules to add
    :return: the combined rules of the proof and the rules
    """
    return proof.rules | rules


def delete_rule(proof: Proof, rule: InferenceRule) \
        -> AbstractSet[InferenceRule]:
    """
    :param proof: a proof
    :param rule: a rule
    :return: return the rules of proof without the given rule
    """
    return {new_rules for new_rules in proof.rules
            if not rule.is_specialization_of(new_rules)}


def update_line_assumptions(line: Proof.Line, f) -> Proof.Line:
    """
    :param line: a line
    :param f: the function to apply on assumptions
    :return: if the line is an assumption, return it else apply f on every
    assumption
    """
    if line.is_assumption():
        return line
    return Proof.Line(line.formula, line.rule,
                      tuple(f(assumption) for assumption in line.assumptions))


def change_statement_conclusion(statement: InferenceRule,
                                conclusion: Formula) -> InferenceRule:
    """
    :param statement: the current statement
    :param conclusion: the new conclusion for the statement
    :return: a new statement with the statement assumptions and the given
    conclusion
    """
    return InferenceRule(statement.assumptions, conclusion)


def add_assumption(statement: InferenceRule,
                   assumption: Formula) -> InferenceRule:
    """
    :param statement: the statement to edit
    :param assumption: the assumption to add
    :return: returns a new statement with the combined assumptions
    """
    tup = [formula for formula in statement.assumptions]
    tup.append(assumption)
    return InferenceRule(tuple(tup), statement.conclusion)


def add_assumptions(statement1: InferenceRule,
                    statement2: InferenceRule) -> InferenceRule:
    """
    :param statement1: the first statement
    :param statement2: the second statement
    :return: a new statement with the combined assumption and the conclusion
    of the first one
    """
    tup = {formula for formula in statement1.assumptions} | \
          {formula for formula in statement2.assumptions}
    return InferenceRule(tuple(tup), statement1.conclusion)


def combine_rules(rules1: AbstractSet[InferenceRule],
                  rules2: AbstractSet[InferenceRule]) \
        -> AbstractSet[InferenceRule]:
    """
    :param rules1: gets a set of rules
    :param rules2: gets a set of other rules
    :return: a set of the combined rules
    """
    return rules1 | rules2
