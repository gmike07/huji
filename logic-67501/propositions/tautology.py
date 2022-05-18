# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: propositions/tautology.py

"""The Tautology Theorem and its implications."""

from typing import List, Union

from logic_utils import frozendict
from typing import Callable
from propositions.syntax import *
from propositions.proofs import *
from propositions.deduction import *
from propositions.semantics import *
from propositions.axiomatic_systems import *


def formulae_capturing_model(model: Model) -> List[Formula]:
    """Computes the formulae that capture the given model: ``'``\ `x`\ ``'``
    for each variable `x` that is assigned the value ``True`` in the given
    model, and ``'~``\ `x`\ ``'`` for each variable x that is assigned the
    value ``False``.

    Parameters:
        model: model to construct the formulae for.

    Returns:
        A list of the constructed formulae, ordered alphabetically by variable
        name.

    Examples:
        >>> formulae_capturing_model({'p2': False, 'p1': True, 'q': True})
        [p1, ~p2, q]
    """
    assert is_model(model)
    return [Formula(key) if model[key] else Formula('~', Formula(key))
            for key in sorted(model.keys())]


def prove_in_model(formula: Formula, model: Model) -> Proof:
    """Either proves the given formula or proves its negation, from the
    formulae that capture the given model.

    Parameters:
        formula: formula that contains no constants or operators beyond
        ``'->'`` and ``'~'``, whose affirmation or negation is to prove.
        model: model from whose formulae to prove.

    Returns:
        If the given formula evaluates to ``True`` in the given model, then
        a proof of the formula, otherwise a proof of ``'~``\ `formula`\ ``'``.
        The returned proof is from the formulae that capture the given model,
        in the order returned by `formulae_capturing_model`\
        ``(``\ `model`\ ``)``, via
        `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM`.
    """
    assert formula.operators().issubset({'->', '~'})
    assert is_model(model)
    return prove_arrow_unary(formula, model, formulae_capturing_model(model))


def prove_arrow_unary(formula: Formula, model: Model,
                      assumptions: List[Formula]) -> Proof:
    """
    :param formula: the formula to prove
    :param model: the model to prove in
    :param assumptions: the assumptions of the proof
    :return: the proof for the model
    """
    if str(formula) in model.keys():
        return handle_variable_case(assumptions, formula, model,
                                    AXIOMATIC_SYSTEM)
    if formula.root == '->':
        return handle_arrow_case(assumptions, formula, model,
                                 prove_arrow_unary)
    # this is ~p
    return handle_unary_case(assumptions, formula, model, prove_arrow_unary)


def reduce_assumption(proof_from_affirmation: Proof,
                      proof_from_negation: Proof) -> Proof:
    """Combines the given two proofs, both of the same formula `conclusion` and
    from the same assumptions except that the last assumption of the latter is
    the negation of that of the former, into a single proof of `conclusion`
    from only the common assumptions.

    Parameters:
        proof_from_affirmation: valid proof of `conclusion` from one or more
            assumptions, the last of which is an assumption `assumption`.
        proof_from_negation: valid proof of `conclusion` from the same
            assumptions and inference rules of `proof_from_affirmation`,
            but with the last assumption being ``'~``\ `assumption` ``'``
            instead of `assumption`.

    Returns:
        A valid proof of `conclusion` from only the assumptions common to the
        given proofs (i.e., without the last assumption of each), via the same
        inference rules of the given proofs and in addition
        `~propositions.axiomatic_systems.MP`,
        `~propositions.axiomatic_systems.I0`,
        `~propositions.axiomatic_systems.I1`,
        `~propositions.axiomatic_systems.D`, and
        `~propositions.axiomatic_systems.R`.

    Examples:
        If the two given proofs are of ``['p', 'q'] ==> '(q->p)'`` and of
        ``['p', '~q'] ==> ('q'->'p')``, then the returned proof is of
        ``['p'] ==> '(q->p)'``.
    """
    assert proof_from_affirmation.is_valid()
    assert proof_from_negation.is_valid()
    assert proof_from_affirmation.statement.conclusion == \
           proof_from_negation.statement.conclusion
    assert len(proof_from_affirmation.statement.assumptions) > 0
    assert len(proof_from_negation.statement.assumptions) > 0
    assert proof_from_affirmation.statement.assumptions[:-1] == \
           proof_from_negation.statement.assumptions[:-1]
    assert Formula('~', proof_from_affirmation.statement.assumptions[-1]) == \
           proof_from_negation.statement.assumptions[-1]
    assert proof_from_affirmation.rules == proof_from_negation.rules
    return combine_proofs(remove_assumption(proof_from_affirmation),
                          remove_assumption(proof_from_negation),
                          proof_from_negation.statement.conclusion,
                          R)


def prove_tautology(tautology: Formula, model: Model = frozendict()) -> Proof:
    """Proves the given tautology from the formulae that capture the given
    model.

    Parameters:
        tautology: tautology that contains no constants or operators beyond
            ``'->'`` and ``'~'``, to prove.
        model: model over a (possibly empty) prefix (with respect to the
            alphabetical order) of the variables of `tautology`, from whose
            formulae to prove.

    Returns:
        A valid proof of the given tautology from the formulae that capture the
        given model, in the order returned by
        `formulae_capturing_model`\ ``(``\ `model`\ ``)``, via
        `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM`.

    Examples:
        If the given model is the empty dictionary, then the returned proof is
        of the given tautology from no assumptions.
    """
    assert is_tautology(tautology)
    assert tautology.operators().issubset({'->', '~'})
    assert is_model(model)
    assert sorted(tautology.variables())[:len(model)] == sorted(model.keys())
    if len(model.keys()) == len(tautology.variables()):
        return prove_in_model(tautology, model)
    variables_sorted = sorted(tautology.variables())
    length = len(model.keys())
    new_model = {key: model[key] for key in model.keys()}
    new_model[variables_sorted[length]] = False
    p1 = prove_tautology(tautology, new_model)
    new_model[variables_sorted[length]] = True
    p2 = prove_tautology(tautology, new_model)
    return reduce_assumption(p2, p1)


def proof_or_counterexample(formula: Formula) -> Union[Proof, Model]:
    """Either proves the given formula or finds a model in which it does not
    hold.

    Parameters:
        formula: formula that contains no constants or operators beyond
        ``'->'`` and ``'~'``, to either prove or find a counterexample for.

    Returns:
        If the given formula is a tautology, then an assumptionless proof
        of the formula via `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM`,
        otherwise a model in which the given formula does not hold.
    """
    assert formula.operators().issubset({'->', '~'})
    models = all_models(list(formula.variables()))
    for model in models:
        if evaluate(formula, model) is False:
            return model
    return prove_tautology(formula)


def encode_as_formula(rule: InferenceRule) -> Formula:
    """Encodes the given inference rule as a formula consisting of a chain of
    implications.

    Parameters:
        rule: inference rule to encode.

    Returns:
        The formula encoding the given rule.

    Examples:
        >>> encode_as_formula(InferenceRule([Formula('p1'), Formula('p2'),
        ...                                  Formula('p3'), Formula('p4')],
        ...                                 Formula('q')))
        (p1->(p2->(p3->(p4->q))))
        >>> encode_as_formula(InferenceRule([], Formula('q')))
        q
    """
    formula = rule.conclusion
    for i in range(len(rule.assumptions) - 1, -1, -1):
        formula = Formula('->', rule.assumptions[i], formula)
    return formula


def prove_sound_inference(rule: InferenceRule) -> Proof:
    """Proves the given sound inference rule.

    Parameters:
        rule: sound inference rule whose assumptions and conclusion that
        contain no constants or operators beyond ``'->'``
        and ``'~'``, to prove.

    Returns:
        A valid assumptionless proof of the given sound inference rule via
        `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM`.
    """
    assert is_sound_inference(rule)
    for formula in rule.assumptions + (rule.conclusion,):
        assert formula.operators().issubset({'->', '~'})
    formula = encode_as_formula(rule)
    proof = prove_tautology(formula)
    new_lines = [line for line in proof.lines]
    for assumption in rule.assumptions:
        new_lines.extend(
            [
                Proof.Line(assumption),
                Proof.Line(formula.second,
                           MP,
                           [len(new_lines), len(new_lines) - 1])
            ])
        formula = formula.second
    return Proof(rule, AXIOMATIC_SYSTEM, new_lines)


def model_or_inconsistency(formulae: List[Formula]) -> Union[Model, Proof]:
    """Either finds a model in which all the given formulae hold, or proves
    ``'~(p->p)'`` from these formula.

    Parameters:
        formulae: formulae that use only the operators ``'->'`` and ``'~'``, to
            either find a model for or prove ``'~(p->p)'`` from.

    Returns:
        A model in which all of the given formulae hold if such exists,
        otherwise a proof of '~(p->p)' from the given formulae via
        `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM`.
    """
    for formula in formulae:
        assert formula.operators().issubset({'->', '~'})
    vars = set()
    for formula in formulae:
        vars |= formula.variables()
    models = all_models(list(vars))
    for model in models:
        if all([evaluate(formula, model) for formula in formulae]) is True:
            return model
    rule = InferenceRule(formulae, Formula.parse('~(p->p)'))
    return prove_sound_inference(rule)


def prove_in_model_full(formula: Formula, model: Model) -> Proof:
    """Either proves the given formula or proves its negation, from the
    formulae that capture the given model.

    Parameters:
        formula: formula that contains no operators beyond ``'->'``, ``'~'``,
            ``'&'``, and ``'|'``, whose affirmation or negation is to prove.
        model: model from whose formulae to prove.

    Returns:
        If the given formula evaluates to ``True`` in the given model, then
        a proof of the formula, otherwise a proof of ``'~``\ `formula`\ ``'``.
        The returned proof is from the formulae that capture the given model,
        in the order returned by `formulae_capturing_model`\
        ``(``\ `model`\ ``)``, via
        `~propositions.axiomatic_systems.AXIOMATIC_SYSTEM_FULL`.
    """
    assert formula.operators().issubset({'T', 'F', '->', '~', '&', '|'})
    assert is_model(model)
    return prove_full(formula, model, formulae_capturing_model(model))


def prove_full(formula: Formula, model: Model, assumptions: List[Formula]) \
        -> Proof:
    """
    :param formula: the formula to prove
    :param model: the model to prove in
    :param assumptions: the assumptions of the proof
    :return: the proof for the model
    """
    if formula.root == 'T':  # if it is T
        return Proof(InferenceRule(assumptions, formula),
                     AXIOMATIC_SYSTEM_FULL,
                     [Proof.Line(formula, T, [])])
    if formula.root == 'F':  # if it is F
        formula = Formula('~', formula)
        return Proof(InferenceRule(assumptions, formula),
                     AXIOMATIC_SYSTEM_FULL,
                     [Proof.Line(formula, NF, [])])
    if str(formula) in model.keys():  # if it is a variable
        return handle_variable_case(assumptions, formula, model,
                                    AXIOMATIC_SYSTEM_FULL)
    if formula.root == '->':  # if it is p->q
        return handle_arrow_case(assumptions, formula, model, prove_full)
    if formula.root == '&':  # if it is p&q
        return handle_and_case(assumptions, formula, model)
    if formula.root == '|':  # if it is p&q
        return handle_or_case(assumptions, formula, model)
    # this is ~p
    return handle_unary_case(assumptions, formula, model, prove_full)


def handle_arrow_case(assumptions: List[Formula], formula: Formula,
                      model: Model, prove_model: Callable[[Formula, Model,
                                                           List[Formula]],
                                                          Proof]) \
        -> Proof:
    """
    :param assumptions: the assumption of the proof
    :param formula: the formula to prove that is of type p->q
    :param model: the model to prove in
    :param prove_model: the function to prove recursively with
    :return: the proof of the formula for this model
    """
    if evaluate(formula.second, model):  # if q is true then prove
        proof = prove_model(formula.second, model, assumptions)
        return prove_corollary(proof, formula, I1)
    if not evaluate(formula.first, model):  # if p is false then prove
        proof = prove_model(formula.first, model, assumptions)
        return prove_corollary(proof, formula, I2)
    # p is true and q is false then unprove
    proof1 = prove_model(formula.first, model, assumptions)
    proof2 = prove_model(formula.second, model, assumptions)
    return combine_proofs(proof1, proof2, Formula('~', formula), NI)


def handle_unary_case(assumptions: List[Formula], formula: Formula,
                      model: Model, prove_model: Callable[[Formula, Model,
                                                           List[Formula]],
                                                          Proof]) \
        -> Proof:
    """
    :param assumptions: the assumption of the proof
    :param formula: the formula to prove that is of type ~p
    :param model: the model to prove in
    :param prove_model: the function to prove recursively with
    :return: the proof of the formula for this model
    """
    proof = prove_model(formula.first, model, assumptions)
    if evaluate(formula, model):  # p is false
        return proof
    else:  # p is true
        return prove_corollary(proof, Formula('~', formula), NN)


def handle_variable_case(assumptions: List[Formula], formula: Formula,
                         model: Model, rules: AbstractSet[InferenceRule])\
        -> Proof:
    """
    :param assumptions: the assumption of the proof
    :param formula: the formula to prove that is a variable
    :param model: the model to prove in
    :param rules: the rules of the current proof
    :return: the prove for this assumptions
    """
    key = formula.root
    formula = formula if model[key] else Formula('~', formula)
    return Proof(InferenceRule(assumptions, formula), rules,
                 [Proof.Line(formula)])


def handle_or_case(assumptions: List[Formula], formula: Formula,
                   model: Model) -> Proof:
    """
    :param assumptions: the assumption of the proof
    :param formula: the formula to prove that is of type p|q
    :param model: the model to prove in
    :return: the prove for this formula
    """
    if evaluate(formula.first, model):  # p is true
        proof = prove_full(formula.first, model, assumptions)
        return prove_corollary(proof, formula, O2)
    if evaluate(formula.second, model):  # q is true
        proof = prove_full(formula.second, model, assumptions)
        return prove_corollary(proof, formula, O1)
    # p is false and q is false
    proof1 = prove_full(formula.first, model, assumptions)
    proof2 = prove_full(formula.second, model, assumptions)
    return combine_proofs(proof1, proof2, Formula('~', formula), NO)


def handle_and_case(assumptions: List[Formula], formula: Formula,
                    model: Model) -> Proof:
    """
    :param assumptions: the assumption of the proof
    :param formula: the formula to prove that is of type p&q
    :param model: the model to prove in
    :return: the prove for this formula
    """
    if not evaluate(formula.first, model):  # p is false
        proof = prove_full(formula.first, model, assumptions)
        return prove_corollary(proof, Formula('~', formula), NA2)
    if not evaluate(formula.second, model):  # p is false
        proof = prove_full(formula.second, model, assumptions)
        return prove_corollary(proof, Formula('~', formula), NA1)
    # p&q is true
    proof1 = prove_full(formula.first, model, assumptions)
    proof2 = prove_full(formula.second, model, assumptions)
    return combine_proofs(proof1, proof2, formula, A)
