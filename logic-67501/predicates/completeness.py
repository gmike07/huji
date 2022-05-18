# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: predicates/completeness.py

from typing import AbstractSet, Container, Set, Union

from logic_utils import fresh_constant_name_generator

from predicates.syntax import *
from predicates.semantics import *
from predicates.proofs import *
from predicates.prover import *
from itertools import product
from predicates.deduction import *
from predicates.prenex import *


def get_constants(formulas: AbstractSet[Formula]) -> Set[str]:
    """Finds all constant names in the given formulas.

    Parameters:
        formulas: formulas to find all constant names in.

    Returns:
        A set of all constant names used in one or more of the given formulas.
    """
    constants = set()
    for formula in formulas:
        constants.update(formula.constants())
    return constants


def is_closed(sentences: AbstractSet[Formula]) -> bool:
    """Checks whether the given set of prenex-normal-form sentences is closed.

    Parameters:
        sentences: set of prenex-normal-form sentences to check.

    Returns:
        ``True`` if the given set of sentences is primitively, universally, and
        existentially closed, ``False`` otherwise.
    """
    for sentence in sentences:
        assert is_in_prenex_normal_form(sentence) and \
               len(sentence.free_variables()) == 0
    return is_primitively_closed(sentences) and \
           is_universally_closed(sentences) and \
           is_existentially_closed(sentences)


def is_primitively_closed(sentences: AbstractSet[Formula]) -> bool:
    """Checks whether the given set of prenex-normal-form sentences is
    primitively closed.

    Parameters:
        sentences: set of prenex-normal-form sentences to check.

    Returns:
        ``True`` if for every n-ary relation name from the given sentences, and
        for every n (not necessarily distinct) constant names from the given
        sentences, either the invocation of this relation name over these
        constant names (in order), or the negation of this invocation, is one of
        the given sentences, ``False`` otherwise.
    """
    for sentence in sentences:
        assert is_in_prenex_normal_form(sentence) and \
               len(sentence.free_variables()) == 0
    constants = get_constants(sentences)
    for sentence in sentences:
        for relation_name, unary in sentence.relations():
            for combination in product(constants, repeat=unary):
                args = [Term(var) for var in combination]
                f1 = Formula(relation_name, args)
                f2 = Formula('~', f1)
                if f1 not in sentences and f2 not in sentences:
                    return False
    return True


def is_universally_closed(sentences: AbstractSet[Formula]) -> bool:
    """Checks whether the given set of prenex-normal-form sentences is
    universally closed.

    Parameters:
        sentences: set of prenex-normal-form sentences to check.

    Returns:
        ``True`` if for every universally quantified sentence of the given
        sentences, and for every constant name from the given sentences, the
        predicate of this quantified sentence, with every free occurrence of the
        universal quantification variable replaced with this constant name, is
        one of the given sentences, ``False`` otherwise.
    """
    for sentence in sentences:
        assert is_in_prenex_normal_form(sentence) and \
               len(sentence.free_variables()) == 0
    constants = get_constants(sentences)
    for sentence in sentences:
        if sentence.root == 'A':
            predicate = sentence.predicate
            for constant in constants:
                mapping = {sentence.variable: Term(constant)}
                new_predicate = predicate.substitute(mapping)
                if new_predicate not in sentences:
                    return False
    return True


def is_existentially_closed(sentences: AbstractSet[Formula]) -> bool:
    """Checks whether the given set of prenex-normal-form sentences is
    existentially closed.

    Parameters:
        sentences: set of prenex-normal-form sentences to check.

    Returns:
        ``True`` if for every existentially quantified sentence of the given
        sentences there exists a constant name such that the predicate of this
        quantified sentence, with every free occurrence of the existential
        quantification variable replaced with this constant name, is one of the
        given sentences, ``False`` otherwise.
    """
    for sentence in sentences:
        assert is_in_prenex_normal_form(sentence) and \
               len(sentence.free_variables()) == 0
    constants = get_constants(sentences)
    for sentence in sentences:
        if sentence.root == 'E':
            found = False
            predicate = sentence.predicate
            for constant in constants:
                mapping = {sentence.variable: Term(constant)}
                new_predicate = predicate.substitute(mapping)
                if new_predicate in sentences:
                    found = True
            if not found:
                return False
    return True


def find_unsatisfied_quantifier_free_sentence(sentences: Container[Formula],
                                              model: Model[str],
                                              unsatisfied: Formula) -> Formula:
    """
    Given a closed set of prenex-normal-form sentences, given a model whose
    universe is the set of all constant names from the given sentences, and
    given a sentence from the given set that the given model does not satisfy,
    finds a quantifier-free sentence from the given set that the given model
    does not satisfy.
    
    Parameters:
        sentences: closed set of prenex-normal-form sentences, which is only to
            be accessed using containment queries, i.e., using the ``in``
            operator as in:

            >>> if sentence in sentences:
            ...     print('contained!')

        model: model for all element names from the given sentences, whose
            universe is `get_constants`\ ``(``\ `sentences`\ ``)``.
        unsatisfied: sentence (which possibly contains quantifiers) from the
            given sentences that is not satisfied by the given model.

    Returns:
        A quantifier-free sentence from the given sentences that is not
        satisfied by the given model.
    """
    # We assume that every sentence in sentences is of type formula, is in
    # prenex normal form, and has no free variables, and furthermore that the
    # set of constants that appear somewhere in sentences is model.universe;
    # but we cannot assert these since we cannot iterate over sentences.
    for constant in model.universe:
        assert is_constant(constant)
    assert is_in_prenex_normal_form(unsatisfied)
    assert len(unsatisfied.free_variables()) == 0
    assert unsatisfied in sentences
    assert not model.evaluate_formula(unsatisfied)

    return find_unsatisfied_quantifier_free_sentence_helper(sentences, model,
                                                            unsatisfied)


def find_unsatisfied_quantifier_free_sentence_helper(
        sentences: Container[Formula],
        model: Model[str],
        unsatisfied: Formula) -> Formula:
    constants = model.universe
    if is_quantifier(unsatisfied.root):
        for constant in constants:
            mapping = {unsatisfied.variable: Term(constant)}
            new_formula = unsatisfied.predicate.substitute(mapping)
            if new_formula in sentences and not model.evaluate_formula(
                    new_formula):
                return find_unsatisfied_quantifier_free_sentence_helper(
                    sentences, model, new_formula)
    return unsatisfied


def get_primitives(quantifier_free: Formula) -> Set[Formula]:
    """Finds all primitive subformulas of the given quantifier-free formula.

    Parameters:
        quantifier_free: quantifier-free formula whose subformulas are to
            be searched.

    Returns:
        The primitive subformulas (i.e., relation invocations) of the given
        quantifier-free formula.

    Examples:
        The primitive subformulas of ``'(R(c1,d)|~(Q(c1)->~R(c2,a)))'`` are
        ``'R(c1,d)'``, ``'Q(c1)'``, and ``'R(c2,a)'``.
    """
    assert is_quantifier_free(quantifier_free)
    return get_primitives_helper(quantifier_free)


def get_primitives_helper(quantifier_free: Formula) -> Set[Formula]:
    if is_unary(quantifier_free.root):
        return get_primitives_helper(quantifier_free.first)
    if is_binary(quantifier_free.root):
        return get_primitives_helper(quantifier_free.first) | \
               get_primitives_helper(quantifier_free.second)
    # this is a relation
    return {quantifier_free}


def create_model(sentences: AbstractSet[Formula], constants) ->  Model:
    constant_meaning = {constant: constant for constant in constants}
    relation_meaning = {}
    for sentence in sentences:
        if is_relation(sentence.root):
            if sentence.root not in relation_meaning:
                relation_meaning[sentence.root] = set()
            relation_meaning[sentence.root] |= {tuple(str(arg) for arg in sentence.arguments)}
    return Model(constants, constant_meaning, relation_meaning)


def check_if_valid_model(sentences: AbstractSet[Formula], model: Model):
    for sentence in sentences:
        if not model.evaluate_formula(sentence):
            return sentence
    return True


def prove_inconsistency(assumptions, unsatisfied):
    prover = Prover(assumptions | {unsatisfied})

    step_set = set()
    for assumption in assumptions:
        step = prover.add_assumption(assumption)
        step_set |= {step}

    step_unsatisfied = prover.add_assumption(unsatisfied)
    unsatisfied2 = Formula('~', unsatisfied)
    step_unsatisfied2 = prover.add_tautological_implication(unsatisfied2, step_set)
    contradiction = Formula('&', unsatisfied2, unsatisfied)
    step_contradiction = prover.add_tautological_implication(contradiction,
                                                             {step_unsatisfied2,
                                                              step_unsatisfied})
    return prover.qed()


def model_or_inconsistency(sentences: AbstractSet[Formula]) -> \
        Union[Model[str], Proof]:
    """Either finds a model in which the given closed set of prenex-normal-form
    sentences holds, or proves a contradiction from these sentences.

    Parameters:
        sentences: closed set of prenex-normal-form sentences to either find a
            model for or prove a contradiction from.

    Returns:
        A model in which all of the given sentences hold if such exists,
        otherwise a valid proof of  a contradiction from the given formulas via
        `~predicates.prover.Prover.AXIOMS`.
    """
    assert is_closed(sentences)
    constants = get_constants(sentences)
    model = create_model(sentences, constants)
    formula_truth = check_if_valid_model(sentences, model)
    if formula_truth is True:
        return model

    unsatisfied = find_unsatisfied_quantifier_free_sentence(sentences,
                                                            model,
                                                            formula_truth)
    assumptions = set(assumption if assumption in sentences else Formula('~', assumption)
                     for assumption in get_primitives(unsatisfied))
    return prove_inconsistency(assumptions, unsatisfied)


def combine_contradictions(proof_from_affirmation: Proof,
                           proof_from_negation: Proof) -> Proof:
    """Combines the given two proofs of contradictions, both from the same
    assumptions/axioms except that the latter has an extra assumption that is
    the negation of an extra assumption that the former has, into a single proof
    of a contradiction from only the common assumptions/axioms.

    Parameters:
        proof_from_affirmation: valid proof of a contradiction from one or more
            assumptions/axioms that are all sentences and that include
            `~predicates.prover.Prover.AXIOMS`.
        proof_from_negation: valid proof of a contradiction from the same
            assumptions/axioms of `proof_from_affirmation`, but with one
            simple assumption `assumption` replaced with its negation
            ``'~``\ `assumption` ``'``.

    Returns:
        A valid proof of a contradiction from only the assumptions/axioms common
        to the given proofs (i.e., without `assumption` or its negation).
    """
    assert proof_from_affirmation.is_valid()
    assert proof_from_negation.is_valid()
    common_assumptions = proof_from_affirmation.assumptions.intersection(
        proof_from_negation.assumptions)
    assert len(common_assumptions) == \
           len(proof_from_affirmation.assumptions) - 1
    assert len(common_assumptions) == len(proof_from_negation.assumptions) - 1
    affirmed_assumption = list(
        proof_from_affirmation.assumptions.difference(common_assumptions))[0]
    negated_assumption = list(
        proof_from_negation.assumptions.difference(common_assumptions))[0]
    assert len(affirmed_assumption.templates) == 0
    assert len(negated_assumption.templates) == 0
    assert negated_assumption.formula == \
           Formula('~', affirmed_assumption.formula)
    assert proof_from_affirmation.assumptions.issuperset(Prover.AXIOMS)
    assert proof_from_negation.assumptions.issuperset(Prover.AXIOMS)
    for assumption in common_assumptions.union({affirmed_assumption,
                                                negated_assumption}):
        assert len(assumption.formula.free_variables()) == 0
    proof1 = proof_by_way_of_contradiction(proof_from_affirmation,
                                           affirmed_assumption.formula)
    proof2 = proof_by_way_of_contradiction(proof_from_negation,
                                           negated_assumption.formula)
    prover = Prover(proof1.assumptions)
    step1 = prover.add_proof(proof1.conclusion, proof1)
    step2 = prover.add_proof(proof2.conclusion, proof2)
    f = Formula('&', proof_from_affirmation.conclusion, proof_from_negation.conclusion)
    step3 = prover.add_tautological_implication(f, {step1, step2})
    return prover.qed()


def eliminate_universal_instantiation_assumption(proof: Proof, constant: str,
                                                 instantiation: Formula,
                                                 universal: Formula) -> Proof:
    """Converts the given proof of a contradiction, whose assumptions/axioms
    include `universal` and `instantiation`, where the latter is a universal
    instantiation of the former, to a proof of a contradiction from the same
    assumptions without `instantiation`.

    Parameters:
        proof: valid proof of a contradiction from one or more
            assumptions/axioms that are all sentences and that include
            `~predicates.prover.Prover.AXIOMS`.
        universal: assumption of the given proof that is universally quantified.
        instantiation: assumption of the given proof that is obtained from the
            predicate of `universal` by replacing all free occurrences of the
            universal quantification variable by some constant.

    Returns:
        A valid proof of a contradiction from the assumptions/axioms of the
        proof except `instantiation`.
    """
    assert proof.is_valid()
    assert is_constant(constant)
    assert Schema(instantiation) in proof.assumptions
    assert Schema(universal) in proof.assumptions
    assert universal.root == 'A'
    assert instantiation == \
           universal.predicate.substitute({universal.variable: Term(constant)})
    for assumption in proof.assumptions:
        assert len(assumption.formula.free_variables()) == 0
    proof1 = proof_by_way_of_contradiction(proof, instantiation)
    assumptions = {assumption for assumption in proof.assumptions
                   if assumption.formula != instantiation}

    prover = Prover(assumptions)
    step1 = prover.add_proof(proof1.conclusion, proof1)
    mapping = {'c' : Term(constant), 'x' : universal.variable,
               'R' : instantiation.substitute({constant : Term('_')})}
    step2 = prover.add_assumption(universal)
    step3 = prover.add_instantiated_assumption(Prover.UI.instantiate(mapping),
                                               Prover.UI, mapping)
    step4 = prover.add_mp(instantiation, step2, step3)
    step5 = prover.add_tautological_implication(proof.conclusion, {step1, step4})
    return prover.qed()


def universal_closure_step(sentences: AbstractSet[Formula]) -> Set[Formula]:
    """Augments the given sentences with all universal instantiations of each
    universally quantified sentence from these sentences, with respect to all
    constant names from these sentences.

    Parameters:
        sentences: prenex-normal-form sentences to augment with their universal
            instantiations.

    Returns:
        A set of all of the given sentences, and in addition any formula that
        can be obtained replacing in the predicate of any universally quantified
        sentence from the given sentences, all occurrences of the quantification
        variable with some constant from the given sentences.
    """
    for sentence in sentences:
        assert is_in_prenex_normal_form(sentence) and \
               len(sentence.free_variables()) == 0
    new_sentences = set()
    constants = get_constants(sentences)
    for sentence in sentences:
        if sentence.root == 'A':
            for constant in constants:
                mapping = {sentence.variable: Term(constant)}
                new_sentences |= {sentence.predicate.substitute(mapping)}
        new_sentences |= {sentence}
    return new_sentences

def replace_schema(schema, constant, variable):
    mapping = {constant : Term(variable)}
    templates = {template if template != Term(constant) else Term(variable)
                 for template in schema.templates}
    return Schema(schema.formula.substitute(mapping), templates)

def replace_constant(proof: Proof, constant: str, variable: str = 'zz') -> \
        Proof:
    """Replaces all occurrences of the given constant in the given proof with
    the given variable.

    Parameters:
        proof: a valid proof.
        constant: a constant name that does not appear as a template constant
            name in any of the assumptions of the given proof.
        variable: a variable name that does not appear anywhere in given the
            proof or in its assumptions.

    Returns:
        A valid proof where every occurrence of the given constant name in the
        given proof and in its assumptions is replaced with the given variable
        name.
    """
    assert proof.is_valid()
    assert is_constant(constant)
    assert is_variable(variable)
    for assumption in proof.assumptions:
        assert constant not in assumption.templates
        assert variable not in assumption.formula.variables()
    for line in proof.lines:
        assert variable not in line.formula.variables()

    mapping = {constant: Term(variable)}
    assumptions = {replace_schema(assumption, constant, variable) for assumption in proof.assumptions}
    prover = Prover(assumptions)
    for line in proof.lines:
        formula = line.formula.substitute(mapping)
        if type(line) == Proof.MPLine:
            prover.add_mp(formula, line.antecedent_line_number, line.conditional_line_number)
        if type(line) == Proof.TautologyLine:
            prover.add_tautology(formula)
        if type(line) == Proof.UGLine:
            prover.add_ug(formula, line.predicate_line_number)
        if type(line) == Proof.AssumptionLine:
            new_mapping = {}
            for key in line.instantiation_map.keys():
                if type(line.instantiation_map[key]) == Formula or \
                    type(line.instantiation_map[key]) == Term:
                    new_mapping[key] = line.instantiation_map[key].substitute(mapping)
                elif is_relation(line.instantiation_map[key]):
                    new_mapping[key] = str(Formula.parse(line.instantiation_map[key]).substitute(mapping))
                else:
                    new_mapping[key] = str(Term.parse(line.instantiation_map[key]).substitute(mapping))
            schema = replace_schema(line.assumption, constant, variable)
            prover.add_instantiated_assumption(formula, schema, new_mapping)
    return prover.qed()


def eliminate_existential_witness_assumption(proof: Proof, constant: str,
                                             witness: Formula,
                                             existential: Formula) -> Proof:
    """Converts the given proof of a contradiction, whose assumptions/axioms
    include `existential` and `witness`, where the latter is an existential
    witness of the former, to a proof of a contradiction from the same
    assumptions without `witness`.

    Parameters:
        proof: valid proof of a contradiction from one or more
            assumptions/axioms that are all sentences and that include
            `~predicates.prover.Prover.AXIOMS`.
        existential: assumption of the given proof that is existentially
            quantified.
        witness: assumption of the given proof that is obtained from the
            predicate of `existential` by replacing all free occurrences of the
            existential quantification variable by some constant that does not
            appear in any assumption of the given proof except for this
            assumption.

    Returns:
        A valid proof of a contradiction from the assumptions/axioms of the
        proof except `witness`.
    """
    assert proof.is_valid()
    assert is_constant(constant)
    assert Schema(witness) in proof.assumptions
    assert Schema(existential) in proof.assumptions
    assert existential.root == 'E'
    assert witness == \
           existential.predicate.substitute(
               {existential.variable: Term(constant)})
    for assumption in proof.assumptions:
        assert len(assumption.formula.free_variables()) == 0
    for assumption in proof.assumptions.difference({Schema(witness)}):
        assert constant not in assumption.formula.constants()

    replaced_var_proof = replace_constant(proof, constant)

    witness1 = witness.substitute({constant: Term('zz')})
    contradiction = proof_by_way_of_contradiction(replaced_var_proof, witness1)

    prover = Prover(contradiction.assumptions)
    step0 = prover.add_proof(contradiction.conclusion, contradiction)
    witness = contradiction.conclusion.substitute({'zz' : Term(existential.variable)}).first
    step1 = prover.add_free_instantiation(Formula('~', witness),
                                          step0, {'zz' : Term(existential.variable)})
    step2 = prover.add_assumption(existential)
    not_exists = Formula('~', existential)
    formula = Formula('->', witness, not_exists)
    step3 = prover.add_tautological_implication(formula, {step1})
    step4 = prover.add_existential_derivation(not_exists, step2, step3)
    step5 = prover.add_tautological_implication(Formula('&', existential, not_exists), {step2, step4})

    return prover.qed()

def existential_closure_step(sentences: AbstractSet[Formula]) -> Set[Formula]:
    """Augments the given sentences with an existential witness that uses a new
    constant name, for each existentially quantified sentences from these
    sentences for which an existential witness is missing.

    Parameters:
        sentences: prenex-normal-form sentences to augment with any missing
            existential witnesses.

    Returns:
        A set of all of the given sentences, and in addition for every
        existentially quantified sentence from the given sentences, a formula
        obtained from the predicate of that quantified sentence by replacing all
        occurrences of the quantification variable with a new constant name
        obtained by calling
        `next`\ ``(``\ `~logic_utils.fresh_constant_name_generator`\ ``)``.
    """
    for sentence in sentences:
        assert is_in_prenex_normal_form(sentence) and \
               len(sentence.free_variables()) == 0
    closure = set(sentences)
    constants = get_constants(sentences)
    for sentence in sentences:
        if sentence.root == 'E':
            add_exists_to_closure(sentence, closure, constants, {})
    return closure


def add_exists_to_closure(sentence, closure, constants, mapping):
    for constant in constants:
        mapping[sentence.variable] = Term(constant)
        f = sentence.predicate.substitute(mapping)
        if f in closure:
            return

    # new formula to add!
    mapping[sentence.variable] = Term(next(fresh_constant_name_generator))
    closure.update({sentence.predicate.substitute(mapping)})
