# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: propositions/semantics.py

"""Semantic analysis of propositional-logic constructs."""

from typing import AbstractSet, Iterable, Iterator, List, Mapping
from itertools import product
from propositions.syntax import *
from propositions.proofs import *

Model = Mapping[str, bool]


def calculate_formula(formula, model):
    """calculate the formula for this model

        Parameters:
            formula: the formula to calculate
            model: the model to calculate with

        Returns:
            the truth of the formula with the given model
        """
    if is_binary(formula.root):
        first_bool = calculate_formula(formula.first, model)
        second_bool = calculate_formula(formula.second, model)
        return OPERATOR_BOOLEAN_DICT[formula.root](first_bool, second_bool)
    if is_unary(formula.root):
        first_bool = calculate_formula(formula.first, model)
        return OPERATOR_BOOLEAN_DICT[formula.root](first_bool)
    if is_constant(formula.root):
        return formula.root == 'T'
    # variable return its value
    return model[formula.root]


def is_model(model: Model) -> bool:
    """Checks if the given dictionary a model over some set of variables.

    Parameters:
        model: dictionary to check.

    Returns:
        ``True`` if the given dictionary is a model over some set of variables,
        ``False`` otherwise.
    """
    for key in model:
        if not (is_variable(key) and type(model[key]) is bool):
            return False
    return True


def variables(model: Model) -> AbstractSet[str]:
    """Finds all variables over which the given model is defined.

    Parameters:
        model: model to check.

    Returns:
        A set of all variables over which the given model is defined.
    """
    assert is_model(model)
    return model.keys()


def evaluate(formula: Formula, model: Model) -> bool:
    """Calculates the truth value of the given formula in the given model.

    Parameters:
        formula: formula to calculate the truth value of.
        model: model over (possibly a superset of) the variables of the
        formula, to calculate the truth value in.

    Returns:
        The truth value of the given formula in the given model.
    """
    assert is_model(model)
    assert formula.variables().issubset(variables(model))
    return calculate_formula(formula, model)


def all_models(variables: List[str]) -> Iterable[Model]:
    """Calculates all possible models over the given variables.

    Parameters:
        variables: list of variables over which to calculate the models.

    Returns:
        An iterable over all possible models over the given variables. The
        order of the models is lexicographic according to the order of the
        given variables, where False precedes True.

    Examples:
        >>> list(all_models(['p', 'q']))
        [{'p': False, 'q': False}, {'p': False, 'q': True},
        {'p': True, 'q': False}, {'p': True, 'q': True}]
    """
    for v in variables:
        assert is_variable(v)
    for element in list(product([False, True], repeat=len(variables))):
        yield {variables[i]: element[i] for i in range(len(variables))}


def truth_values(formula: Formula, models: Iterable[Model]) -> Iterable[bool]:
    """Calculates the truth value of the given formula in each of the given
    model.

    Parameters:
        formula: formula to calculate the truth value of.
        models: iterable over models to calculate the truth value in.

    Returns:
        An iterable over the respective truth values of the given formula in
        each of the given models, in the order of the given models.
    """
    for model in models:
        yield evaluate(formula, model)


def print_truth_table(formula: Formula) -> None:
    """Prints the truth table of the given formula, with variable-name columns
    sorted alphabetically.

    Parameters:
        formula: formula to print the truth table of.

    Examples:
        >>> print_truth_table(Formula.parse('~(p&q76)'))
        | p | q76 | ~(p&q76) |
        |---|-----|----------|
        | F | F   | T        |
        | F | T   | T        |
        | T | F   | T        |
        | T | T   | F        |
    """
    formula_variables = sorted(formula.variables())
    # print first row
    print_table_first_row(formula, formula_variables)
    # print second row
    print_table_second_row(formula, formula_variables)
    # print answers
    print_answers(formula, formula_variables)


def print_answers(formula, formula_variables):
    """Prints the truth table of the given formula, with variable-name columns
        sorted alphabetically, only the answers themselves

    Parameters:
        formula: formula to print the truth table of.
        formula_variables: the variables of the formula to show in the  table

    Examples:
        | F | F   | T        |
        | F | T   | T        |
        | T | F   | T        |
        | T | T   | F        |
     """
    models = all_models(list(formula_variables))
    for model in models:
        s = '| '
        for var in formula_variables:
            s += truth_false_string(model[var]) + ' ' * (len(var) - 1) + ' | '
        s += truth_false_string(evaluate(formula, model)) \
             + ' ' * (len(str(formula)) - 1) + ' | '
        print(s[:-1])


def print_table_second_row(formula, formula_variables):
    """Prints the truth table of the given formula, with variable-name columns
    sorted alphabetically, only the separate line

    Parameters:
        formula: formula to print the truth table of.
        formula_variables: the variables of the formula to show in the table

    Examples:
        |---|-----|----------|
    """
    s = '|-'
    for var in formula_variables:
        s += '-' * len(var) + '-|-'
    s += '-' * len(str(formula)) + '-|-'
    print(s[:-1])


def print_table_first_row(formula, formula_variables):
    """Prints the truth table of the given formula, with variable-name columns
    sorted alphabetically, only the headers

    Parameters:
        formula: formula to print the truth table of.
        formula_variables: the variables of the formula to show in the table

    Examples:
        | p | q76 | ~(p&q76) |
    """
    s = '| '
    for var in formula_variables:
        s += var + ' | '
    s += str(formula) + ' | '
    print(s[:-1])


def truth_false_string(boolean):
    """Parameters:
           boolean: boolean to check

       Returns:
           'T' if s is True else 'F', i.e. the string rep of this boolean
       """
    if boolean:
        return 'T'
    return 'F'


def is_tautology(formula: Formula) -> bool:
    """Checks if the given formula is a tautology.

    Parameters:
        formula: formula to check.

    Returns:
        ``True`` if the given formula is a tautology, ``False`` otherwise.
    """
    models = all_models(list(formula.variables()))
    for model in models:
        if evaluate(formula, model) is False:
            return False
    return True


def is_contradiction(formula: Formula) -> bool:
    """Checks if the given formula is a contradiction.

    Parameters:
        formula: formula to check.

    Returns:
        ``True`` if the given formula is a contradiction, ``False`` otherwise.
    """
    models = all_models(list(formula.variables()))
    for model in models:
        if evaluate(formula, model) is True:
            return False
    return True


def is_satisfiable(formula: Formula) -> bool:
    """Checks if the given formula is satisfiable.

    Parameters:
        formula: formula to check.

    Returns:
        ``True`` if the given formula is satisfiable, ``False`` otherwise.
    """
    models = all_models(list(formula.variables()))
    for model in models:
        if evaluate(formula, model) is True:
            return True
    return False


def join_formulas(formulas, op):
    """ a formula that represents a combination of all the formulas with the
    given binary operation

    Parameters:
        formulas: a list of formulas to join
        op: a string that to join the formulas with

    Returns:
        The joined formula
    """
    if len(formulas) == 1:
        return formulas[0]
    formula = Formula(op, formulas[0], formulas[1])
    for i in range(2, len(formulas)):
        formula = Formula(op, formula, formulas[i])
    return formula


def synthesize_for_model(model: Model) -> Formula:
    """Synthesizes a propositional formula in the form of a single clause that
      evaluates to ``True`` in the given model, and to ``False`` in any other
      model over the same variables.

    Parameters:
        model: model in which the synthesized formula is to hold.

    Returns:
        The synthesized formula.
    """
    assert is_model(model)
    formulas = [Formula(var) if model[var] else Formula('~', Formula(var))
                for var in model.keys()]
    return join_formulas(formulas, '&')


def synthesize(variables: List[str], values: Iterable[bool]) -> Formula:
    """Synthesizes a propositional formula in DNF over the given variables, from
    the given specification of which value the formula should have on each
    possible model over these variables.

    Parameters:
        variables: the set of variables for the synthesize formula.
        values: iterable over truth values for the synthesized formula in every
            possible model over the given variables, in the order returned by
            `all_models`\ ``(``\ `~synthesize.variables`\ ``)``.

    Returns:
        The synthesized formula.

    Examples:
        >>> formula = synthesize(['p', 'q'], [True, True, True, False])
        >>> for model in all_models(['p', 'q']):
        ...     evaluate(formula, model)
        True
        True
        True
        False
    """
    assert len(variables) > 0
    formulas = [synthesize_for_model(model) for value, model
                in zip(values, all_models(variables)) if value]
    if len(formulas) == 0:
        return Formula('&', Formula(variables[0]),
                       Formula('~', Formula(variables[0])))
    return join_formulas(formulas, '|')


# Tasks for Chapter 4

def evaluate_inference(rule: InferenceRule, model: Model) -> bool:
    """Checks if the given inference rule holds in the given model.

    Parameters:
        rule: inference rule to check.
        model: model to check in.

    Returns:
        ``True`` if the given inference rule holds in the given model,
        ``False`` otherwise.
    """
    assert is_model(model)
    if all([evaluate(assumption, model) for assumption in rule.assumptions]) \
            and not evaluate(rule.conclusion, model):
        return False
    return True


def is_sound_inference(rule: InferenceRule) -> bool:
    """Checks if the given inference rule is sound, i.e., whether its
    conclusion is a semantically correct implication of its assumptions.

    Parameters:
        rule: inference rule to check.

    Returns:
        ``True`` if the given inference rule is sound, ``False`` otherwise.
    """
    for model in all_models(list(rule.variables())):
        if not evaluate_inference(rule, model):
            return False
    return True
