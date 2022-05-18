# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: predicates/deduction.py

"""Useful proof manipulation maneuvers in predicate logic."""

from predicates.syntax import *
from predicates.proofs import *
from predicates.prover import *

def remove_assumption(proof: Proof, assumption: Formula,
                      print_as_proof_forms: bool = False) -> Proof:
    """Converts the given proof of some `conclusion` formula, an assumption of
    which is `assumption`, to a proof of
    ``'(``\ `assumption`\ ``->``\ `conclusion`\ ``)'`` from the same assumptions
    except `assumption`.

    Parameters:
        proof: valid proof to convert, from assumptions/axioms that include
            `~predicates.prover.Prover.AXIOMS`.
        assumption: formula that is a simple assumption (i.e., without any
            templates) of the given proof, such that no line of the given proof
            is a UG line over a variable that is free in this assumption.

    Returns:
        A valid proof of ``'(``\ `assumption`\ ``->``\ `conclusion`\ ``)'``
        from the same assumptions/axioms as the given proof except `assumption`.
    """        
    assert proof.is_valid()
    assert Schema(assumption) in proof.assumptions
    assert proof.assumptions.issuperset(Prover.AXIOMS)
    for line in proof.lines:
        if isinstance(line, Proof.UGLine):
            assert line.formula.variable not in assumption.free_variables()
    assumptions = {assumption1 for assumption1 in proof.assumptions
                   if assumption1.formula != assumption}
    # assumptions |= Prover.AXIOMS
    prover = Prover(assumptions, print_as_proof_forms)
    mapping = {}
    for i in range(len(proof.lines)):
        line = proof.lines[i]
        formula = Formula('->', assumption, line.formula)
        if type(line) == Proof.AssumptionLine:
            if line.formula == assumption:
                step1 = prover.add_tautology(formula)
                mapping[i] = step1
            else:
                step1 = prover.add_instantiated_assumption(line.formula,
                                                           line.assumption,
                                                           line.instantiation_map)
                step2 = prover.add_tautological_implication(formula, {step1})
                mapping[i] = step2
        elif type(line) == Proof.TautologyLine:
            step1 = prover.add_tautology(line.formula)
            step2 = prover.add_tautological_implication(formula, {step1})
            mapping[i] = step2
        elif type(line) == Proof.MPLine:
            steps = {mapping[line.antecedent_line_number],
                     mapping[line.conditional_line_number]}
            step1 = prover.add_tautological_implication(formula, steps)
            mapping[i] = step1
        else:  # this is UGLine, phi->R(x),Ax[phi->R(x)], phi->Ax[R(x)]
            # Ax[phi->R(x)]
            helper_map = {'x': line.formula.variable, 'Q': assumption,
                          'R': line.formula.predicate.substitute(
                              {line.formula.variable: Term('_')})}
            formula = Prover.US.instantiate(helper_map)
            step1 = prover.add_ug(formula.first,
                                  mapping[line.predicate_line_number])
            step2 = prover.add_instantiated_assumption(formula, Prover.US,
                                                       helper_map)
            step3 = prover.add_mp(formula.second, step1, step2)
            mapping[i] = step3
    return prover.qed()


def proof_by_way_of_contradiction(proof: Proof, assumption: Formula,
                                  print_as_proof_forms: bool = False) -> Proof:
    """Converts the given proof of a contradiction, an assumption of which is
    `assumption`, to a proof of ``'~``\ `assumption`\ ``'`` from the same
    assumptions except `assumption`.

    Parameters:
        proof: valid proof of a contradiction (i.e., a formula whose negation is
            a tautology) to convert, from assumptions/axioms that include
            `~predicates.prover.Prover.AXIOMS`.
        assumption: formula that is a simple assumption (i.e., without any
            templates) of the given proof, such that no line of the given proof
            is a UG line over a variable that is free in this assumption.

    Return:
        A valid proof of ``'~``\ `assumption`\ ``'`` from the same
        assumptions/axioms as the given proof except `assumption`.
    """
    assert proof.is_valid()
    assert Schema(assumption) in proof.assumptions
    assert proof.assumptions.issuperset(Prover.AXIOMS)
    for line in proof.lines:
        if isinstance(line, Proof.UGLine):
            assert line.formula.variable not in assumption.free_variables()
    proof_helper = remove_assumption(proof, assumption, print_as_proof_forms)
    prover = Prover(proof_helper.assumptions, print_as_proof_forms)
    step1 = prover.add_proof(proof_helper.conclusion, proof_helper)
    step2 = prover.add_tautology(Formula('~', proof.conclusion))
    step3 = prover.add_tautological_implication(Formula('~', assumption), {step1, step2})
    return prover.qed()
