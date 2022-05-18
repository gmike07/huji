# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: predicates/prenex.py

"""Conversion of predicate-logic formulas into prenex normal form."""

from typing import Tuple

from logic_utils import fresh_variable_name_generator

from predicates.syntax import *
from predicates.proofs import *
from predicates.prover import *
from predicates.deduction import *

#: Additional axioms of quantification for first-order predicate logic.
ADDITIONAL_QUANTIFICATION_AXIOMS = (
    Schema(Formula.parse('((~Ax[R(x)]->Ex[~R(x)])&(Ex[~R(x)]->~Ax[R(x)]))'),
           {'x', 'R'}),
    Schema(Formula.parse('((~Ex[R(x)]->Ax[~R(x)])&(Ax[~R(x)]->~Ex[R(x)]))'),
           {'x', 'R'}),
    Schema(Formula.parse('(((Ax[R(x)]&Q())->Ax[(R(x)&Q())])&'
                         '(Ax[(R(x)&Q())]->(Ax[R(x)]&Q())))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Ex[R(x)]&Q())->Ex[(R(x)&Q())])&'
                         '(Ex[(R(x)&Q())]->(Ex[R(x)]&Q())))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Q()&Ax[R(x)])->Ax[(Q()&R(x))])&'
                         '(Ax[(Q()&R(x))]->(Q()&Ax[R(x)])))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Q()&Ex[R(x)])->Ex[(Q()&R(x))])&'
                         '(Ex[(Q()&R(x))]->(Q()&Ex[R(x)])))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Ax[R(x)]|Q())->Ax[(R(x)|Q())])&'
                         '(Ax[(R(x)|Q())]->(Ax[R(x)]|Q())))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Ex[R(x)]|Q())->Ex[(R(x)|Q())])&'
                         '(Ex[(R(x)|Q())]->(Ex[R(x)]|Q())))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Q()|Ax[R(x)])->Ax[(Q()|R(x))])&'
                         '(Ax[(Q()|R(x))]->(Q()|Ax[R(x)])))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Q()|Ex[R(x)])->Ex[(Q()|R(x))])&'
                         '(Ex[(Q()|R(x))]->(Q()|Ex[R(x)])))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Ax[R(x)]->Q())->Ex[(R(x)->Q())])&'
                         '(Ex[(R(x)->Q())]->(Ax[R(x)]->Q())))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Ex[R(x)]->Q())->Ax[(R(x)->Q())])&'
                         '(Ax[(R(x)->Q())]->(Ex[R(x)]->Q())))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Q()->Ax[R(x)])->Ax[(Q()->R(x))])&'
                         '(Ax[(Q()->R(x))]->(Q()->Ax[R(x)])))'), {'x','R','Q'}),
    Schema(Formula.parse('(((Q()->Ex[R(x)])->Ex[(Q()->R(x))])&'
                         '(Ex[(Q()->R(x))]->(Q()->Ex[R(x)])))'), {'x','R','Q'}),
    Schema(Formula.parse('(((R(x)->Q(x))&(Q(x)->R(x)))->'
                         '((Ax[R(x)]->Ay[Q(y)])&(Ay[Q(y)]->Ax[R(x)])))'),
           {'x', 'y', 'R', 'Q'}),
    Schema(Formula.parse('(((R(x)->Q(x))&(Q(x)->R(x)))->'
                         '((Ex[R(x)]->Ey[Q(y)])&(Ey[Q(y)]->Ex[R(x)])))'),
           {'x', 'y', 'R', 'Q'}))


NEGATION_MAP = {'A' : ADDITIONAL_QUANTIFICATION_AXIOMS[0], 'E' : ADDITIONAL_QUANTIFICATION_AXIOMS[1]}
OPPOSITE_QUANT = {'A': 'E', 'E' : 'A'}
AXIOM_ALL_EXISTS = {'A': ADDITIONAL_QUANTIFICATION_AXIOMS[-2],
                    'E' : ADDITIONAL_QUANTIFICATION_AXIOMS[-1]}

BINARY_LEFT_MAP = {('&', 'A'): ADDITIONAL_QUANTIFICATION_AXIOMS[2],
                   ('&', 'E'): ADDITIONAL_QUANTIFICATION_AXIOMS[3],
                   ('|', 'A'): ADDITIONAL_QUANTIFICATION_AXIOMS[6],
                   ('|', 'E'): ADDITIONAL_QUANTIFICATION_AXIOMS[7],
                   ('->', 'A'): ADDITIONAL_QUANTIFICATION_AXIOMS[10],
                   ('->', 'E'): ADDITIONAL_QUANTIFICATION_AXIOMS[11]}

OPPOSITE_QUANT_BINARY = {('&', 'A'): 'A',
                         ('&', 'E'): 'E',
                         ('|', 'A'): 'A',
                         ('|', 'E'): 'E',
                         ('->', 'A'): 'E',
                         ('->', 'E'): 'A'}

BINARY_RIGHT_MAP = {('&', 'A'): ADDITIONAL_QUANTIFICATION_AXIOMS[4],
                    ('&', 'E'): ADDITIONAL_QUANTIFICATION_AXIOMS[5],
                    ('|', 'A'): ADDITIONAL_QUANTIFICATION_AXIOMS[8],
                    ('|', 'E'): ADDITIONAL_QUANTIFICATION_AXIOMS[9],
                    ('->', 'A'): ADDITIONAL_QUANTIFICATION_AXIOMS[12],
                    ('->', 'E'): ADDITIONAL_QUANTIFICATION_AXIOMS[13]}

def is_quantifier_free(formula: Formula) -> bool:
    """Checks if the given formula contains any quantifiers.

    Parameters:
        formula: formula to check.

    Returns:
        ``False`` if the given formula contains any quantifiers, ``True``
        otherwise.
    """
    if is_equality(formula.root) or is_relation(formula.root):
        return True
    if is_unary(formula.root):
        return is_quantifier_free(formula.first)
    if is_binary(formula.root):
        return is_quantifier_free(formula.first) and is_quantifier_free(formula.second)
    return False


def is_in_prenex_normal_form(formula: Formula) -> bool:
    """Checks if the given formula is in prenex normal form.

    Parameters:
        formula: formula to check.

    Returns:
        ``True`` if the given formula in prenex normal form, ``False``
        otherwise.
    """
    if is_quantifier(formula.root):
        return is_in_prenex_normal_form(formula.predicate)
    return is_quantifier_free(formula)


def equivalence_of(formula1: Formula, formula2: Formula) -> Formula:
    """States the equivalence of the two given formulas as a formula.

    Parameters:
        formula1: first of the formulas the equivalence of which is to be
            stated.
        formula2: second of the formulas the equivalence of which is to be
            stated.

    Returns:
        The formula ``'((``\ `formula1`\ ``->``\ `formula2`\ ``)&(``\ `formula2`\ ``->``\ `formula1`\ ``))'``.
    """
    return Formula('&', Formula('->', formula1, formula2),
                   Formula('->', formula2, formula1))

def has_uniquely_named_variables(formula: Formula) -> bool:
    """Checks if the given formula has uniquely named variables.

    Parameters:
        formula: formula to check.

    Returns:
        ``False`` if in the given formula some variable name has both quantified
        and free occurrences or is quantified by more than one quantifier,
        ``True`` otherwise.
    """
    forbidden_variables = set(formula.free_variables())
    def has_uniquely_named_variables_helper(formula: Formula) -> bool:
        if is_unary(formula.root):
            return has_uniquely_named_variables_helper(formula.first)
        elif is_binary(formula.root):
            return has_uniquely_named_variables_helper(formula.first) and \
                   has_uniquely_named_variables_helper(formula.second)
        elif is_quantifier(formula.root):
            if formula.variable in forbidden_variables:
                return False
            forbidden_variables.add(formula.variable)
            return has_uniquely_named_variables_helper(formula.predicate)
        else:
            assert is_relation(formula.root) or is_equality(formula.root)
            return True

    return has_uniquely_named_variables_helper(formula)

def uniquely_rename_quantified_variables(formula: Formula) -> \
        Tuple[Formula, Proof]:
    """Converts the given formula to an equivalent formula with uniquely named
    variables, and proves the equivalence of these two formulas.

    Parameters:
        formula: formula to convert, which contains no variable names starting
            with ``z``.

    Returns:
        A pair. The first element of the pair is a formula equivalent to the
        given formula, with the exact same structure but with the additional
        property of having uniquely named variables, obtained by consistently
        replacing each variable name that is bound in the given formula with a
        new variable name obtained by calling
        `next`\ ``(``\ `~logic_utils.fresh_variable_name_generator`\ ``)``. The
        second element of the pair is a proof of the equivalence of the given
        formula and the returned formula (i.e., a proof of
        `equivalence_of`\ ``(``\ `formula`\ ``,``\ `returned_formula`\ ``)``)
        via `~predicates.prover.Prover.AXIOMS` and
        `ADDITIONAL_QUANTIFICATION_AXIOMS`.
    """
    prover = Prover(set(ADDITIONAL_QUANTIFICATION_AXIOMS), False)
    if is_relation(formula.root) or is_equality(formula.root):
        prover.add_tautology(equivalence_of(formula, formula))
        return formula, prover.qed()

    if is_unary(formula.root):
        first, proof = uniquely_rename_quantified_variables(formula.first)
        step1 = prover.add_proof(proof.conclusion, proof)
        helper = equivalence_of(formula, Formula('~', first))
        step2 = prover.add_tautological_implication(helper, {step1})
        return Formula(formula.root, first), prover.qed()

    if is_binary(formula.root):
        first, proof1 = uniquely_rename_quantified_variables(formula.first)
        step1 = prover.add_proof(proof1.conclusion, proof1)
        second, proof2 = uniquely_rename_quantified_variables(formula.second)
        step2 = prover.add_proof(proof2.conclusion, proof2)
        helper = equivalence_of(formula, Formula(formula.root, first, second))
        step3 = prover.add_tautological_implication(helper, {step1, step2})
        return Formula(formula.root, first, second), prover.qed()


    if is_quantifier(formula.root):
        new_name = next(fresh_variable_name_generator)
        predicate, proof = uniquely_rename_quantified_variables(formula.predicate)
        step1 = prover.add_proof(proof.conclusion, proof)
        mapping = {'x' : formula.variable, 'y' : new_name,
                   'R' : formula.predicate.substitute({formula.variable: Term('_')}),
                   'Q' : predicate.substitute({formula.variable: Term('_')})}
        AXIOM = AXIOM_ALL_EXISTS[formula.root]
        new_formula = AXIOM.instantiate(mapping)
        step2 = prover.add_instantiated_assumption(new_formula, AXIOM, mapping)
        step3 = prover.add_mp(new_formula.second, step1, step2)
        return new_formula.second.first.second, prover.qed()
    # Task 11.5


def pull_out_quantifications_across_negation(formula: Formula) -> \
        Tuple[Formula, Proof]:
    """Converts the given formula with uniquely named variables of the form
    ``'~``\ `Q1`\ `x1`\ ``[``\ `Q2`\ `x2`\ ``[``...\ `Qn`\ `xn`\ ``[``\ `inner_formula`\ ``]``...\ ``]]'``
    to an equivalent formula of the form
    ``'``\ `Q'1`\ `x1`\ ``[``\ `Q'2`\ `x2`\ ``[``...\ `Q'n`\ `xn`\ ``[~``\ `inner_formula`\ ``]``...\ ``]]'``,
    and proves the equivalence of these two formulas.

    Parameters:
        formula: formula to convert, whose root is a negation, i.e., which is of
            the form
            ``'~``\ `Q1`\ `x1`\ ``[``\ `Q2`\ `x2`\ ``[``...\ `Qn`\ `xn`\ ``[``\ `inner_formula`\ ``]``...\ ``]]'``
            where `n`>=0, each `Qi` is a quantifier, each `xi` is a variable
            name, and `inner_formula` does not start with a quantifier.

    Returns:
        A pair. The first element of the pair is a formula equivalent to the
        given formula, but of the form
        ``'``\ `Q'1`\ `x1`\ ``[``\ `Q'2`\ `x2`\ ``[``...\ `Q'n`\ `xn`\ ``[~``\ `inner_formula`\ ``]``...\ ``]]'``
        where each `Q'i` is a quantifier, and where the `xi` variable names and
        `inner_formula` are the same as in the given formula. The second element
        of the pair is a proof of the equivalence of the given formula and the
        returned formula (i.e., a proof of
        `equivalence_of`\ ``(``\ `formula`\ ``,``\ `returned_formula`\ ``)``)
        via `~predicates.prover.Prover.AXIOMS` and
        `ADDITIONAL_QUANTIFICATION_AXIOMS`.

    Examples:
        >>> formula = Formula.parse('~Ax[Ey[R(x,y)]]')
        >>> returned_formula, proof = pull_out_quantifications_across_negation(
        ...     formula)
        >>> returned_formula
        Ex[Ay[~R(x,y)]]
        >>> proof.is_valid()
        True
        >>> proof.conclusion == equivalence_of(formula, returned_formula)
        True
        >>> proof.assumptions == Prover.AXIOMS.union(
        ...     ADDITIONAL_QUANTIFICATION_AXIOMS)
        True
    """
    assert is_unary(formula.root)
    quantified = formula.first

    prover = Prover(set(ADDITIONAL_QUANTIFICATION_AXIOMS), False)
    if not is_quantifier(quantified.root):
        prover.add_tautology(equivalence_of(formula, formula))
        return formula, prover.qed()

    root, predicate, variable = quantified.root, quantified.predicate, quantified.variable

    new_formula, proof = pull_out_quantifications_across_negation(Formula('~', predicate))
    step1 = prover.add_proof(proof.conclusion, proof)
    new_formula, conclusion, step3 = conclude(prover, proof.conclusion, OPPOSITE_QUANT[root], variable, step1)
    mapping = {'x': variable, 'R': predicate.substitute({variable: Term('_')})}
    AXIOM = NEGATION_MAP[root]
    formula2 = AXIOM.instantiate(mapping)
    step4 = prover.add_instantiated_assumption(formula2, AXIOM, mapping)
    step5 = prover.add_tautological_implication(equivalence_of(formula, new_formula), {step3, step4})
    return new_formula, prover.qed()



def pull_out_quantifications_from_left_across_binary_operator(formula:
                                                              Formula) -> \
        Tuple[Formula, Proof]:
    """Converts the given formula with uniquely named variables of the form
    ``'(``\ `Q1`\ `x1`\ ``[``\ `Q2`\ `x2`\ ``[``...\ `Qn`\ `xn`\ ``[``\ `inner_first`\ ``]``...\ ``]]``\ `*`\ `second`\ ``)'``
    to an equivalent formula of the form
    ``'``\ `Q'1`\ `x1`\ ``[``\ `Q'2`\ `x2`\ ``[``...\ `Q'n`\ `xn`\ ``[(``\ `inner_first`\ `*`\ `second`\ ``)]``...\ ``]]'``
    and proves the equivalence of these two formulas.

    Parameters:
        formula: formula with uniquely named variables to convert, whose root
            is a binary operator, i.e., which is of the form
            ``'(``\ `Q1`\ `x1`\ ``[``\ `Q2`\ `x2`\ ``[``...\ `Qn`\ `xn`\ ``[``\ `inner_first`\ ``]``...\ ``]]``\ `*`\ `second`\ ``)'``
            where `*` is a binary operator, `n`>=0, each `Qi` is a quantifier,
            each `xi` is a variable name, and `inner_first` does not start with
            a quantifier.

    Returns:
        A pair. The first element of the pair is a formula equivalent to the
        given formula, but of the form
        ``'``\ `Q'1`\ `x1`\ ``[``\ `Q'2`\ `x2`\ ``[``...\ `Q'n`\ `xn`\ ``[(``\ `inner_first`\ `*`\ `second`\ ``)]``...\ ``]]'``
        where each `Q'i` is a quantifier, and where the operator `*`, the `xi`
        variable names, `inner_first`, and `second` are the same as in the given
        formula. The second element of the pair is a proof of the equivalence of
        the given formula and the returned formula (i.e., a proof of
        `equivalence_of`\ ``(``\ `formula`\ ``,``\ `returned_formula`\ ``)``)
        via `~predicates.prover.Prover.AXIOMS` and
        `ADDITIONAL_QUANTIFICATION_AXIOMS`.

    Examples:
        >>> formula = Formula.parse('(Ax[Ey[R(x,y)]]&Ez[P(1,z)])')
        >>> returned_formula, proof = pull_out_quantifications_from_left_across_binary_operator(
        ...     formula)
        >>> returned_formula
        Ax[Ey[(R(x,y)&Ez[P(1,z)])]]
        >>> proof.is_valid()
        True
        >>> proof.conclusion == equivalence_of(formula, returned_formula)
        True
        >>> proof.assumptions == Prover.AXIOMS.union(
        ...     ADDITIONAL_QUANTIFICATION_AXIOMS)
        True
    """
    assert has_uniquely_named_variables(formula)
    assert is_binary(formula.root)
    quantified = formula.first
    prover = Prover(set(ADDITIONAL_QUANTIFICATION_AXIOMS), False)
    if not is_quantifier(quantified.root):
        prover.add_tautology(equivalence_of(formula, formula))
        return formula, prover.qed()

    root, predicate, variable = quantified.root, quantified.predicate, quantified.variable

    new_formula, proof = pull_out_quantifications_from_left_across_binary_operator(Formula(formula.root, predicate, formula.second))
    step1 = prover.add_proof(proof.conclusion, proof)
    new_formula, conclusion, step3 = conclude(prover, proof.conclusion,
                                              OPPOSITE_QUANT_BINARY[(formula.root, root)],
                                              variable,
                                              step1)
    mapping = {'x': variable, 'R': predicate.substitute({variable: Term('_')}),
               'Q': formula.second}
    AXIOM = BINARY_LEFT_MAP[(formula.root, root)]
    formula2 = AXIOM.instantiate(mapping)
    step4 = prover.add_instantiated_assumption(formula2, AXIOM, mapping)
    step5 = prover.add_tautological_implication(
        equivalence_of(formula, new_formula), {step3, step4})
    return new_formula, prover.qed()


def pull_out_quantifications_from_right_across_binary_operator(formula:
                                                               Formula) -> \
        Tuple[Formula, Proof]:
    """Converts the given formula with uniquely named variables of the form
    ``'(``\ `first`\ `*`\ `Q1`\ `x1`\ ``[``\ `Q2`\ `x2`\ ``[``...\ `Qn`\ `xn`\ ``[``\ `inner_second`\ ``]``...\ ``]])'``
    to an equivalent formula of the form
    ``'``\ `Q'1`\ `x1`\ ``[``\ `Q'2`\ `x2`\ ``[``...\ `Q'n`\ `xn`\ ``[(``\ `first`\ `*`\ `inner_second`\ ``)]``...\ ``]]'``
    and proves the equivalence of these two formulas.

    Parameters:
        formula: formula with uniquely named variables to convert, whose root
            is a binary operator, i.e., which is of the form
            ``'(``\ `first`\ `*`\ `Q1`\ `x1`\ ``[``\ `Q2`\ `x2`\ ``[``...\ `Qn`\ `xn`\ ``[``\ `inner_second`\ ``]``...\ ``]])'``
            where `*` is a binary operator, `n`>=0, each `Qi` is a quantifier,
            each `xi` is a variable name, and `inner_second` does not start with
            a quantifier.

    Returns:
        A pair. The first element of the pair is a formula equivalent to the
        given formula, but of the form
        ``'``\ `Q'1`\ `x1`\ ``[``\ `Q'2`\ `x2`\ ``[``...\ `Q'n`\ `xn`\ ``[(``\ `first`\ `*`\ `inner_second`\ ``)]``...\ ``]]'``
        where each `Q'i` is a quantifier, and where the operator `*`, the `xi`
        variable names, `first`, and `inner_second` are the same as in the given
        formula. The second element of the pair is a proof of the equivalence of
        the given formula and the returned formula (i.e., a proof of
        `equivalence_of`\ ``(``\ `formula`\ ``,``\ `returned_formula`\ ``)``)
        via `~predicates.prover.Prover.AXIOMS` and
        `ADDITIONAL_QUANTIFICATION_AXIOMS`.

    Examples:
        >>> formula = Formula.parse('(Ax[Ey[R(x,y)]]|Ez[P(1,z)])')
        >>> returned_formula, proof = pull_out_quantifications_from_right_across_binary_operator(
        ...     formula)
        >>> returned_formula
        Ez[(Ax[Ey[R(x,y)]]|P(1,z))]
        >>> proof.is_valid()
        True
        >>> proof.conclusion == equivalence_of(formula, returned_formula)
        True
        >>> proof.assumptions == Prover.AXIOMS.union(
        ...     ADDITIONAL_QUANTIFICATION_AXIOMS)
        True
    """
    assert has_uniquely_named_variables(formula)
    assert is_binary(formula.root)
    quantified = formula.second
    prover = Prover(set(ADDITIONAL_QUANTIFICATION_AXIOMS), False)
    if not is_quantifier(quantified.root):
        prover.add_tautology(equivalence_of(formula, formula))
        return formula, prover.qed()

    root, predicate, variable = quantified.root, quantified.predicate, quantified.variable
    new_formula, proof = pull_out_quantifications_from_right_across_binary_operator(
        Formula(formula.root, formula.first, predicate))
    step1 = prover.add_proof(proof.conclusion, proof)
    new_formula, conclusion, step3 = conclude(prover, proof.conclusion,
                                              root, variable, step1)

    mapping = {'x': variable, 'R': predicate.substitute({variable: Term('_')}),
               'Q': formula.first}

    AXIOM = BINARY_RIGHT_MAP[(formula.root, root)]
    formula2 = AXIOM.instantiate(mapping)
    step4 = prover.add_instantiated_assumption(formula2, AXIOM, mapping)
    step5 = prover.add_tautological_implication(
        equivalence_of(formula, new_formula), {step3, step4})
    return new_formula, prover.qed()


def conclude(prover: Prover, conclusion: Formula, root: str, variable: str, step: int):
    """
    :return: new formula, new conclusion, the new line
    """
    mapping = {'x': variable, 'y': variable,
               'R': conclusion.first.first.substitute({variable: Term('_')}),
               'Q': conclusion.first.second.substitute({variable: Term('_')})}
    AXIOM = AXIOM_ALL_EXISTS[root]
    formula2 = AXIOM.instantiate(mapping)
    step1 = prover.add_instantiated_assumption(formula2, AXIOM, mapping)
    step2 = prover.add_mp(formula2.second, step, step1)
    return formula2.second.first.second, formula2.second, step2

def recurse(prover, formula):
    if is_quantifier(formula.root):
        formula1, conclusion, step = recurse(prover, formula.predicate)
        return conclude(prover, conclusion, formula.root, formula.variable, step)
    formula1, proof = pull_out_quantifications_from_right_across_binary_operator(formula)
    step = prover.add_proof(proof.conclusion, proof)
    return formula1, proof.conclusion, step


def pull_out_quantifications_across_binary_operator(formula: Formula) -> \
        Tuple[Formula, Proof]:
    """Converts the given formula with uniquely named variables of the form
    ``'(``\ `Q1`\ `x1`\ ``[``\ `Q2`\ `x2`\ ``[``...\ `Qn`\ `xn`\ ``[``\ `inner_first`\ ``]``...\ ``]]``\ `*`\ `P1`\ `y1`\ ``[``\ `P2`\ `y2`\ ``[``...\ `Pm`\ `ym`\ ``[``\ `inner_second`\ ``]``...\ ``]])'``
    to an equivalent formula of the form
    ``'``\ `Q'1`\ `x1`\ ``[``\ `Q'2`\ `x2`\ ``[``...\ `Q'n`\ `xn`\ ``[``\ `P'1`\ `y1`\ ``[``\ `P'2`\ `y2`\ ``[``...\ `P'm`\ `ym`\ ``[(``\ `inner_first`\ `*`\ `inner_second`\ ``)]``...\ ``]]]``...\ ``]]'``
    and proves the equivalence of these two formulas.

    Parameters:
        formula: formula with uniquely named variables to convert, whose root
            is a binary operator, i.e., which is of the form
            ``'(``\ `Q1`\ `x1`\ ``[``\ `Q2`\ `x2`\ ``[``...\ `Qn`\ `xn`\ ``[``\ `inner_first`\ ``]``...\ ``]]``\ `*`\ `P1`\ `y1`\ ``[``\ `P2`\ `y2`\ ``[``...\ `Pm`\ `ym`\ ``[``\ `inner_second`\ ``]``...\ ``]])'``
            where `*` is a binary operator, `n`>=0, `m`>=0, each `Qi` and `Pi`
            is a quantifier, each `xi` and `yi` is a variable name, and neither
            `inner_first` nor `inner_second` starts with a quantifier.

    Returns:
        A pair. The first element of the pair is a formula equivalent to the
        given formula, but of the form
        ``'``\ `Q'1`\ `x1`\ ``[``\ `Q'2`\ `x2`\ ``[``...\ `Q'n`\ `xn`\ ``[``\ `P'1`\ `y1`\ ``[``\ `P'2`\ `y2`\ ``[``...\ `P'm`\ `ym`\ ``[(``\ `inner_first`\ `*`\ `inner_second`\ ``)]``...\ ``]]]``...\ ``]]'``
        where each `Q'i` and `P'i` is a quantifier, and where the operator `*`,
        the `xi` and `yi` variable names, `inner_first`, and `inner_second` are
        the same as in the given formula. The second element of the pair is a
        proof of the equivalence of the given formula and the returned formula
        (i.e., a proof of
        `equivalence_of`\ ``(``\ `formula`\ ``,``\ `returned_formula`\ ``)``)
        via `~predicates.prover.Prover.AXIOMS` and
        `ADDITIONAL_QUANTIFICATION_AXIOMS`.

    Examples:
        >>> formula = Formula.parse('(Ax[Ey[R(x,y)]]->Ez[P(1,z)])')
        >>> returned_formula, proof = pull_out_quantifications_across_binary_operator(
        ...     formula)
        >>> returned_formula
        Ex[Ay[Ez[(R(x,y)->P(1,z))]]]
        >>> proof.is_valid()
        True
        >>> proof.conclusion == equivalence_of(formula, returned_formula)
        True
        >>> proof.assumptions == Prover.AXIOMS.union(
        ...     ADDITIONAL_QUANTIFICATION_AXIOMS)
        True
    """
    assert has_uniquely_named_variables(formula)
    assert is_binary(formula.root)
    formula1, proof1 = pull_out_quantifications_from_left_across_binary_operator(
        formula)
    prover = Prover(proof1.assumptions, False)
    step1 = prover.add_proof(proof1.conclusion, proof1)
    formula2, conclusion2, step2 = recurse(prover, formula1)
    step3 = prover.add_tautological_implication(equivalence_of(formula, formula2), {step1, step2})
    return formula2, prover.qed()


def to_prenex_normal_form_from_uniquely_named_variables(formula: Formula) -> \
        Tuple[Formula, Proof]:
    """Converts the given formula with uniquely named variables to an equivalent
    formula in prenex normal form, and proves the equivalence of these two
    formulas.

    Parameters:
        formula: formula with uniquely named variables to convert.

    Returns:
        A pair. The first element of the pair is a formula equivalent to the
        given formula, but in prenex normal form. The second element of the pair
        is a proof of the equivalence of the given formula and the returned
        formula (i.e., a proof of
        `equivalence_of`\ ``(``\ `formula`\ ``,``\ `returned_formula`\ ``)``)
        via `~predicates.prover.Prover.AXIOMS` and
        `ADDITIONAL_QUANTIFICATION_AXIOMS`.

    Examples:
        >>> formula = Formula.parse('(~(Ax[Ey[R(x,y)]]->Ez[P(1,z)])|S(w))')
        >>> returned_formula, proof = to_prenex_normal_form_from_uniquely_named_variables(
        ...     formula)
        >>> returned_formula
        Ax[Ey[Az[(~(R(x,y)->P(1,z))|S(w))]]]
        >>> proof.is_valid()
        True
        >>> proof.conclusion == equivalence_of(formula, returned_formula)
        True
        >>> proof.assumptions == Prover.AXIOMS.union(
        ...     ADDITIONAL_QUANTIFICATION_AXIOMS)
        True
    """
    assert has_uniquely_named_variables(formula)
    prover = Prover(set(ADDITIONAL_QUANTIFICATION_AXIOMS), False)
    if is_quantifier_free(formula):
        prover.add_tautology(equivalence_of(formula, formula))
        return formula, prover.qed()

    if is_quantifier(formula.root):
        new_formula, proof = to_prenex_normal_form_from_uniquely_named_variables(formula.predicate)
        step = prover.add_proof(proof.conclusion, proof)
        new_formula, conclusion, step = conclude(prover, proof.conclusion,
                                                 formula.root,
                                                 formula.variable, step)
        return new_formula, prover.qed()


    if is_unary(formula.root):
        new_formula, proof = to_prenex_normal_form_from_uniquely_named_variables(formula.first)
        step1 = prover.add_proof(proof.conclusion, proof)
        new_formula, proof = pull_out_quantifications_across_negation(Formula('~', new_formula))
        step2 = prover.add_proof(proof.conclusion, proof)
        step3 = prover.add_tautological_implication(equivalence_of(formula, new_formula), {step1, step2})
        return new_formula, prover.qed()

    if is_binary(formula.root):
        first, proof1 = to_prenex_normal_form_from_uniquely_named_variables(
            formula.first)
        second, proof2 = to_prenex_normal_form_from_uniquely_named_variables(
            formula.second)
        step1 = prover.add_proof(proof1.conclusion, proof1)
        step2 = prover.add_proof(proof2.conclusion, proof2)
        new_formula, proof = pull_out_quantifications_across_binary_operator(
            Formula(formula.root, first, second))
        step3 = prover.add_proof(proof.conclusion, proof)
        step4 = prover.add_tautological_implication(
            equivalence_of(formula, new_formula), {step1, step2, step3})
        return new_formula, prover.qed()


def to_prenex_normal_form(formula: Formula) -> Tuple[Formula, Proof]:
    """Converts the given formula to an equivalent formula in prenex normal
    form, and proves the equivalence of these two formulas.

    Parameters:
        formula: formula to convert, which contains no variable names starting
            with ``z``.

    Returns:
        A pair. The first element of the pair is a formula equivalent to the
        given formula, but in prenex normal form. The second element of the pair
        is a proof of the equivalence of the given formula and the returned
        formula (i.e., a proof of
        `equivalence_of`\ ``(``\ `formula`\ ``,``\ `returned_formula`\ ``)``)
        via `~predicates.prover.Prover.AXIOMS` and
        `ADDITIONAL_QUANTIFICATION_AXIOMS`.
    """
    prover = Prover(set(ADDITIONAL_QUANTIFICATION_AXIOMS), False)
    formula1, proof = uniquely_rename_quantified_variables(formula)
    step1 = prover.add_proof(proof.conclusion, proof)
    formula2, proof = to_prenex_normal_form_from_uniquely_named_variables(formula1)
    step2 = prover.add_proof(proof.conclusion, proof)
    step3 = prover.add_tautological_implication(equivalence_of(formula, formula2), {step1, step2})
    return formula2, prover.qed()
