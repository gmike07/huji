# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: propositions/deduction.py

"""Useful proof manipulation maneuvers in propositional logic."""

from propositions.syntax import *
from propositions.proofs import *
from propositions.axiomatic_systems import *


def prove_corollary(antecedent_proof: Proof, consequent: Formula,
                    conditional: InferenceRule) -> Proof:
    """Converts the given proof of a formula `antecedent` into a proof of the
    given formula `consequent` by using the given assumptionless inference rule
    of which ``'(``\ `antecedent`\ ``->``\ `consequent`\ ``)'`` is a
    specialization.

    Parameters:
        antecedent_proof: valid proof of `antecedent`.
        consequent: formula to prove.
        conditional: assumptionless inference rule of which the assumptionless
            inference rule with conclusion
            ``'(``\ `antecedent`\ ``->``\ `consequent`\ ``)'`` is a
            specialization.

    Returns:
        A valid proof of `consequent` from the same assumptions as the given
        proof, via the same inference rules as the given proof and in addition
        `~propositions.axiomatic_systems.MP` and `conditional`.
    """
    assert antecedent_proof.is_valid()
    assert InferenceRule([],
                         Formula('->', antecedent_proof.statement.conclusion,
                                 consequent)).is_specialization_of(conditional)
    new_rule = Formula('->', antecedent_proof.statement.conclusion, consequent)
    lines = [line for line in antecedent_proof.lines]
    lines.extend(
        [
            Proof.Line(new_rule, conditional, []),
            Proof.Line(consequent, MP, [len(lines) - 1, len(lines)])
        ])
    proof = Proof(change_statement_conclusion(antecedent_proof.statement,
                                              consequent),
                  add_rule(antecedent_proof, conditional),
                  lines)
    return proof


def combine_proofs(antecedent1_proof: Proof, antecedent2_proof: Proof,
                   consequent: Formula, double_conditional: InferenceRule) -> \
        Proof:
    """Combines the given proofs of two formulae `antecedent1` and `antecedent2`
    into a proof of the given formula `consequent` by using the given
    assumptionless inference rule of which
    ``('``\ `antecedent1`\ ``->(``\ `antecedent2`\ ``->``\ `consequent`\ ``))'`
    is a specialization.

    Parameters:
        antecedent1_proof: valid proof of `antecedent1`.
        antecedent2_proof: valid proof of `antecedent2` from the same
            assumptions and inference rules as `antecedent1_proof`.
        consequent: formula to prove.
        double_conditional: assumptionless inference rule of which the
            assumptionless inference rule with conclusion
            ``'(``\ `antecedent1`\ ``->(``\ `antecedent2`\ ``->``\
            `consequent`\ ``))'``
            is a specialization.

    Returns:
        A valid proof of `consequent` from the same assumptions as the given
        proofs, via the same inference rules as the given proofs and in
        addition `~propositions.axiomatic_systems.MP` and `conditional`.
    """
    assert antecedent1_proof.is_valid()
    assert antecedent2_proof.is_valid()
    assert antecedent1_proof.statement.assumptions == \
           antecedent2_proof.statement.assumptions
    assert antecedent1_proof.rules == antecedent2_proof.rules
    assert InferenceRule(
        [], Formula('->', antecedent1_proof.statement.conclusion,
                    Formula('->', antecedent2_proof.statement.conclusion,
                            consequent))
    ).is_specialization_of(double_conditional)

    formula1 = Formula('->', antecedent1_proof.statement.conclusion,
                       Formula('->', antecedent2_proof.statement.conclusion,
                               consequent))
    formula2 = Formula('->', antecedent2_proof.statement.conclusion,
                       consequent)
    lines = [line for line in antecedent1_proof.lines]
    lines.extend(
        [
            Proof.Line(formula1, double_conditional, []),
            Proof.Line(formula2, MP, [len(lines) - 1, len(lines)])
        ])
    number = len(lines) - 1
    f = lambda x: x + number + 1
    lines.extend(
        [
            update_line_assumptions(line, f)
            for line in antecedent2_proof.lines
        ])
    lines.extend(
        [
            Proof.Line(consequent, MP, [len(lines) - 1, number])
        ])
    rules = add_rules(antecedent1_proof, antecedent2_proof.rules)
    proof = Proof(change_statement_conclusion(antecedent1_proof.statement,
                                              consequent),
                  combine_rules(rules, {double_conditional}),
                  lines)
    return proof


def remove_assumption_rule_not_mp(new_lines: List[Proof.Line],
                                  line: Proof.Line,
                                  last_assumption: Formula) -> None:
    """
    :param new_lines: the new lines of the proof to write
    :param line: the current line to replace (with a rule not mp)
    :param last_assumption: the last assumption of the original proof
    added the proof of the line to the new lines
    """
    formula = Formula('->', line.formula,
                      Formula('->', last_assumption, line.formula))
    new_lines.extend(
        [
            Proof.Line(line.formula, line.rule, []),
            Proof.Line(formula, I1, []),
            Proof.Line(formula.second, MP, [len(new_lines),
                                            len(new_lines) + 1])
        ])


def remove_assumption_not_last_assumption(new_lines: List[Proof.Line],
                                          line: Proof.Line,
                                          last_assumption: Formula) -> None:
    """
    :param new_lines: the new lines of the proof to write
    :param line: the current line to replace (an assumption not the last one)
    :param last_assumption: the last assumption of the original proof
    added the proof of the line to the new lines
    """
    formula = Formula('->', line.formula,
                      Formula('->', last_assumption, line.formula))
    new_lines.extend(
        [
            Proof.Line(line.formula),
            Proof.Line(formula, I1, []),
            Proof.Line(formula.second, MP, [len(new_lines),
                                            len(new_lines) + 1])
        ])


def remove_assumption(proof: Proof) -> Proof:
    """Converts a proof of some `conclusion` formula, the last assumption of
    which is an assumption `assumption`, into a proof of
    ``'(``\ `assumption`\ ``->``\ `conclusion`\ ``)'`` from the same
    assumptions except `assumption`.

    Parameters:
        proof: valid proof to convert, with at least one assumption, via some
            set of inference rules all of which have no assumptions except
            perhaps `~propositions.axiomatic_systems.MP`.

    Return:
        A valid proof of ``'(``\ `assumptions`\ ``->``\ `conclusion`\ ``)'``
        from the same assumptions as the given proof except the last one, via
        the same inference rules as the given proof and in addition
        `~propositions.axiomatic_systems.MP`,
        `~propositions.axiomatic_systems.I0`,
        `~propositions.axiomatic_systems.I1`, and
        `~propositions.axiomatic_systems.D`.
    """
    assert proof.is_valid()
    assert len(proof.statement.assumptions) > 0
    for rule in proof.rules:
        assert rule == MP or len(rule.assumptions) == 0
    new_lines = []
    last_assumption = proof.statement.assumptions[-1]
    mapping = {}
    for i in range(len(proof.lines)):
        line = proof.lines[i]
        if line.is_assumption():
            if line.formula == last_assumption:
                formula = Formula('->', line.formula, line.formula)
                new_lines.extend([Proof.Line(formula, I0, [])])
            else:
                remove_assumption_not_last_assumption(new_lines, line,
                                                      last_assumption)
        else:
            if line.rule != MP:
                remove_assumption_rule_not_mp(new_lines, line, last_assumption)
            else:  # MP
                remove_assumptions_mp(last_assumption, line, mapping,
                                      new_lines, proof.lines)
        mapping[i] = len(new_lines) - 1
    assumptions = [assumption for assumption in proof.statement.assumptions
                   if assumption != last_assumption]
    return Proof(InferenceRule(assumptions, new_lines[-1].formula),
                 add_rules(proof, {MP, I0, I1, D}), new_lines)


def remove_assumptions_mp(last_assumption: Formula, line: Proof.Line, mapping,
                          new_lines: List[Proof.Line],
                          lines: Tuple[Proof.Line]) -> None:
    """
    :param last_assumption: the last assumption of the original proof
    :param line: the current line to replace (MP)
    :param mapping: the mapping of the old lines of the proof in the new one
    :param new_lines: the new lines of the proof to write
    :param lines: the lines of the old proof
    added the proof of the line to the new lines
    """
    asum1, asum2 = line.assumptions[0], line.assumptions[1]
    formula1 = lines[asum1].formula
    formula2 = lines[asum2].formula.second
    formula = Formula('->',
                      Formula('->', last_assumption,
                              Formula('->', formula1, formula2)),
                      Formula('->', Formula('->', last_assumption, formula1),
                              Formula('->', last_assumption, formula2)))
    new_lines.extend(
        [
            Proof.Line(formula, D, []),
            Proof.Line(formula.second, MP, [mapping[asum2], len(new_lines)]),
            Proof.Line(formula.second.second, MP,
                       [mapping[asum1], len(new_lines) + 1])
        ])


def proof_from_inconsistency(proof_of_affirmation: Proof,
                             proof_of_negation: Proof, conclusion: Formula) \
        -> Proof:
    """Combines the given proofs of a formula `affirmation` and its negation
    ``'~``\ `affirmation`\ ``'`` into a proof of the given formula.

    Parameters:
        proof_of_affirmation: valid proof of `affirmation`.
        proof_of_negation: valid proof of ``'~``\ `affirmation`\ ``'`` from the
            same assumptions and inference rules of `proof_of_affirmation`.
        conclusion: the conclusion of the inconsistency
    Returns:
        A valid proof of `conclusion` from the same assumptions as the given
        proofs, via the same inference rules as the given proofs and in
        addition `~propositions.axiomatic_systems.MP` and
        `~propositions.axiomatic_systems.I2`.
    """
    assert proof_of_affirmation.is_valid()
    assert proof_of_negation.is_valid()
    assert proof_of_affirmation.statement.assumptions == \
           proof_of_negation.statement.assumptions
    assert Formula('~', proof_of_affirmation.statement.conclusion) == \
           proof_of_negation.statement.conclusion
    assert proof_of_affirmation.rules == proof_of_negation.rules
    return combine_proofs(proof_of_negation, proof_of_affirmation, conclusion,
                          I2)


def prove_by_contradiction(proof: Proof) -> Proof:
    """Converts the given proof of ``'~(p->p)'``, the last assumption of which
    is an assumption ``'~``\ `formula`\ ``'``, into a proof of `formula` from
    the same assumptions except ``'~``\ `formula`\ ``'``.

    Parameters:
        proof: valid proof of ``'~(p->p)'`` to convert, the last assumption of
            which is of the form ``'~``\ `formula`\ ``'``, via some set of
            inference rules all of which have no assumptions except perhaps
            `~propositions.axiomatic_systems.MP`.

    Return:
        A valid proof of `formula` from the same assumptions as the given proof
        except the last one, via the same inference rules as the given proof
        and in addition `~propositions.axiomatic_systems.MP`,
        `~propositions.axiomatic_systems.I0`,
        `~propositions.axiomatic_systems.I1`,
        `~propositions.axiomatic_systems.D`, and
        `~propositions.axiomatic_systems.N`.
    """
    assert proof.is_valid()
    assert proof.statement.conclusion == Formula.parse('~(p->p)')
    assert len(proof.statement.assumptions) > 0
    assert proof.statement.assumptions[-1].root == '~'
    for rule in proof.rules:
        assert rule == MP or len(rule.assumptions) == 0

    proof1 = remove_assumption(proof)
    p = proof.statement.conclusion.first  # (p->p)
    q = proof.statement.assumptions[-1].first  # q
    notq_then_not_p = Formula('->', Formula('~', q), Formula('~', p))
    p_then_q = Formula('->', p, q)
    new_lines = [line for line in proof1.lines]
    new_lines.extend(
        [
            Proof.Line(Formula('->', notq_then_not_p, p_then_q), N, []),
            Proof.Line(p_then_q, MP, [len(new_lines) - 1, len(new_lines)]),
            Proof.Line(p, I0, []),
            Proof.Line(q, MP, [len(new_lines) + 2, len(new_lines) + 1])
        ])
    return Proof(InferenceRule(proof1.statement.assumptions, q),
                 add_rules(proof1, {MP, I0, I1, D, N, NI}), new_lines)
