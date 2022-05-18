# (c) This file is part of the course
# Mathematical Logic through Programming
# by Gonczarowski and Nisan.
# File name: predicates/some_proofs.py

from predicates.syntax import *
from predicates.proofs import *
from predicates.prover import *
from predicates.deduction import *
# from predicates.deduction import *
# from predicates.prenex import equivalence_of

def syllogism_proof(print_as_proof_forms: bool = False) -> Proof:
    """Proves from the assumptions:

    1. All men are mortal (``'Ax[(Man(x)->Mortal(x))]'``), and
    2. Aristotle is a man (``'Man(aristotle)'``)

    the conclusion: Aristotle is mortal (``'Mortal(aristotle)'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover({'Ax[(Man(x)->Mortal(x))]', 'Man(aristotle)'},
                    print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Man(x)->Mortal(x))]')
    step2 = prover.add_instantiated_assumption(
        '(Ax[(Man(x)->Mortal(x))]->(Man(aristotle)->Mortal(aristotle)))',
        Prover.UI, {'R': '(Man(_)->Mortal(_))', 'c': 'aristotle'})
    step3 = prover.add_mp('(Man(aristotle)->Mortal(aristotle))', step1, step2)
    step4 = prover.add_assumption('Man(aristotle)')
    step5 = prover.add_mp('Mortal(aristotle)', step4, step3)
    return prover.qed()


def syllogism_proof_with_universal_instantiation(print_as_proof_forms: bool =
                                                 False) -> Proof:
    """Using the method `~predicates.prover.Prover.add_universal_instantiation`,
    proves from the assumptions:

    1. All men are mortal (``'Ax[(Man(x)->Mortal(x))]'``), and
    2. Aristotle is a man (``'Man(aristotle)'``)

    the conclusion: Aristotle is mortal (``'Mortal(aristotle)'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof, constructed using the method
        `~predicates.prover.Prover.add_universal_instantiation`, of the above
        inference via `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover({'Ax[(Man(x)->Mortal(x))]', 'Man(aristotle)'},
                    print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Man(x)->Mortal(x))]')
    step2 = prover.add_universal_instantiation(
        '(Man(aristotle)->Mortal(aristotle))', step1, 'aristotle')
    step3 = prover.add_assumption('Man(aristotle)')
    step4 = prover.add_mp('Mortal(aristotle)', step3, step2)
    return prover.qed()


def syllogism_all_all_proof(print_as_proof_forms: bool = False) -> Proof:
    """Proves from the assumptions:

    1. All Greeks are human (``'Ax[(Greek(x)->Human(x))]'``), and
    2. All humans are mortal (``'Ax[(Human(x)->Mortal(x))]'``)

    the conclusion: All Greeks are mortal (``'Ax[(Greek(x)->Mortal(x))]'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover({'Ax[(Greek(x)->Human(x))]', 'Ax[(Human(x)->Mortal(x))]'},
                    print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Greek(x)->Human(x))]')
    step2 = prover.add_universal_instantiation(
        '(Greek(x)->Human(x))', step1, 'x')
    step3 = prover.add_assumption('Ax[(Human(x)->Mortal(x))]')
    step4 = prover.add_universal_instantiation(
        '(Human(x)->Mortal(x))', step3, 'x')
    step5 = prover.add_tautology(
        '((Greek(x)->Human(x))->((Human(x)->Mortal(x))->(Greek(x)->Mortal(x))))')
    step6 = prover.add_mp(
        '((Human(x)->Mortal(x))->(Greek(x)->Mortal(x)))', step2, step5)
    step7 = prover.add_mp('(Greek(x)->Mortal(x))', step4, step6)
    step8 = prover.add_ug('Ax[(Greek(x)->Mortal(x))]', step7)
    return prover.qed()


def syllogism_all_all_proof_with_tautological_implication(print_as_proof_forms:
bool = False) -> \
        Proof:
    """Using the method
    `~predicates.prover.Prover.add_tautological_implication`, proves from the
    assumptions:

    1. All Greeks are human (``'Ax[(Greek(x)->Human(x))]'``), and
    2. All humans are mortal (``'Ax[(Human(x)->Mortal(x))]'``)

    the conclusion: All Greeks are mortal (``'Ax[(Greek(x)->Mortal(x))]'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof, constructed using the method
        `~predicates.prover.Prover.add_tautological_implication`, of the above
        inference via `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover({'Ax[(Greek(x)->Human(x))]', 'Ax[(Human(x)->Mortal(x))]'},
                    print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Greek(x)->Human(x))]')
    step2 = prover.add_universal_instantiation(
        '(Greek(x)->Human(x))', step1, 'x')
    step3 = prover.add_assumption('Ax[(Human(x)->Mortal(x))]')
    step4 = prover.add_universal_instantiation(
        '(Human(x)->Mortal(x))', step3, 'x')
    step5 = prover.add_tautological_implication(
        '(Greek(x)->Mortal(x))', {step2, step4})
    step6 = prover.add_ug('Ax[(Greek(x)->Mortal(x))]', step5)
    return prover.qed()


def syllogism_all_exists_proof(print_as_proof_forms: bool = False) -> Proof:
    """Proves from the assumptions:

    1. All men are mortal (``'Ax[(Man(x)->Mortal(x))]'``), and
    2. Some men exist (``'Ex[Man(x)]'``)
    
    the conclusion: Some mortals exist (``'Ex[Mortal(x)]'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover({'Ax[(Man(x)->Mortal(x))]', 'Ex[Man(x)]'},
                    print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Man(x)->Mortal(x))]')
    step2 = prover.add_assumption('Ex[Man(x)]')
    step3 = prover.add_universal_instantiation(
        '(Man(x)->Mortal(x))', step1, 'x')
    step4 = prover.add_instantiated_assumption(
        '(Mortal(x)->Ex[Mortal(x)])', Prover.EI,
        {'R': 'Mortal(_)', 'c': 'x'})
    step5 = prover.add_tautological_implication(
        '(Man(x)->Ex[Mortal(x)])', {step3, step4})
    step6 = prover.add_ug('Ax[(Man(x)->Ex[Mortal(x)])]', step5)
    step7 = prover.add_instantiated_assumption(
        '((Ax[(Man(x)->Ex[Mortal(x)])]&Ex[Man(x)])->Ex[Mortal(x)])', Prover.ES,
        {'R': 'Man(_)', 'Q': 'Ex[Mortal(x)]'})
    step8 = prover.add_tautological_implication(
        'Ex[Mortal(x)]', {step2, step6, step7})
    return prover.qed()


def syllogism_all_exists_proof_with_existential_derivation(
        print_as_proof_forms:
        bool = False) -> \
        Proof:
    """Using the method `~predicates.prover.Prover.add_existential_derivation`,
    proves from the assumptions:

    1. All men are mortal (``'Ax[(Man(x)->Mortal(x))]'``), and
    2. Some men exist (``'Ex[Man(x)]'``)
    
    the conclusion: Some mortals exist (``'Ex[Mortal(x)]'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof, constructed using the method
        `~predicates.prover.Prover.add_existential_derivation`, of the above
        inference via `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover({'Ax[(Man(x)->Mortal(x))]', 'Ex[Man(x)]'},
                    print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Man(x)->Mortal(x))]')
    step2 = prover.add_assumption('Ex[Man(x)]')
    step3 = prover.add_universal_instantiation(
        '(Man(x)->Mortal(x))', step1, 'x')
    step4 = prover.add_instantiated_assumption(
        '(Mortal(x)->Ex[Mortal(x)])', Prover.EI, {'R': 'Mortal(_)', 'c': 'x'})
    step5 = prover.add_tautological_implication(
        '(Man(x)->Ex[Mortal(x)])', {step3, step4})
    step6 = prover.add_existential_derivation('Ex[Mortal(x)]', step2, step5)
    return prover.qed()


def lovers_proof(print_as_proof_forms: bool = False) -> Proof:
    """Proves from the assumptions:

    1. Everybody loves somebody (``'Ax[Ey[Loves(x,y)]]'``), and
    2. Everybody loves a lover (``'Ax[Az[Ay[(Loves(x,y)->Loves(z,x))]]]'``)
    
    the conclusion: Everybody loves everybody (``'Ax[Az[Loves(z,x)]]'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover({'Ax[Ey[Loves(x,y)]]',
                     'Ax[Az[Ay[(Loves(x,y)->Loves(z,x))]]]'},
                    print_as_proof_forms)
    step1 = prover.add_assumption('Ax[Ey[Loves(x,y)]]')
    step2 = prover.add_universal_instantiation("Ey[Loves(x,y)]", step1, 'x')
    step3 = prover.add_assumption('Ax[Az[Ay[(Loves(x,y)->Loves(z,x))]]]')
    step4 = prover.add_universal_instantiation(
        "Az[Ay[(Loves(x,y)->Loves(z,x))]]", step3, 'x')
    step5 = prover.add_universal_instantiation(
        "Ay[(Loves(x,y)->Loves(z,x))]", step4, 'z')
    step6 = prover.add_universal_instantiation(
        "(Loves(x,y)->Loves(z,x))", step5, 'y')
    step7 = prover.add_existential_derivation("Loves(z,x)", step2, step6)
    step8 = prover.add_ug("Az[Loves(z,x)]", step7)
    step9 = prover.add_ug("Ax[Az[Loves(z,x)]]", step8)
    return prover.qed()


def homework_proof(print_as_proof_forms: bool = False) -> Proof:
    """Proves from the assumptions:

    1. No homework is fun (``'~Ex[(Homework(x)&Fun(x))]'``), and
    2. Some reading is homework (``'Ex[(Homework(x)&Reading(x))]'``)
    
    the conclusion: Some reading is not fun (``'Ex[(Reading(x)&~Fun(x))]'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover({'~Ex[(Homework(x)&Fun(x))]',
                     'Ex[(Homework(x)&Reading(x))]'}, print_as_proof_forms)
    step1 = prover.add_assumption('~Ex[(Homework(x)&Fun(x))]')
    step2 = prover.add_instantiated_assumption(
        '((Homework(x)&Fun(x))->Ex[(Homework(x)&Fun(x))])', Prover.EI,
        {'R': '(Homework(_)&Fun(_))', 'c': 'x', 'x': 'x'})
    #use the magic of tautological_implication that uses tautology, which
    #will take this sound claim and add to the proof
    step3 = prover.add_tautological_implication(
        '((Homework(x)&Reading(x))->(Reading(x)&~Fun(x)))', {step1, step2})
    step4 = prover.add_instantiated_assumption(
        '((Reading(x)&~Fun(x))->Ex[(Reading(x)&~Fun(x))])', Prover.EI,
        {'R': '(Reading(_)&~Fun(_))', 'c': 'x'})
    step5 = prover.add_tautological_implication(
       '((Homework(x)&Reading(x))->Ex[(Reading(x)&~Fun(x))])', {step4, step3})
    step6 = prover.add_assumption('Ex[(Homework(x)&Reading(x))]')
    # #just as written in the book :)
    step7 = prover.add_existential_derivation('Ex[(Reading(x)&~Fun(x))]',
                                                   step6, step5)
    return prover.qed()


#: The three group axioms
GROUP_AXIOMS = frozenset({'plus(0,x)=x', 'plus(minus(x),x)=0',
                          'plus(plus(x,y),z)=plus(x,plus(y,z))'})


def right_neutral_proof(stop_before_flipped_equality: bool,
                        stop_before_free_instantiation: bool,
                        stop_before_substituted_equality: bool,
                        stop_before_chained_equality: bool,
                        print_as_proof_forms: bool = False) -> Proof:
    """Proves from the group axioms that x+0=x (``'plus(x,0)=x'``).

    Parameters:
        stop_before_flipped_equality: flag specifying to stop proving just
            before the first call to
            `~predicates.prover.Prover.add_flipped_equality` and to return the
            prefix of the proof constructed up to that point.
        stop_before_free_instantiation: flag specifying to stop proving just
            before the first call to
            `~predicates.prover.Prover.add_free_instantiation` and to return the
            prefix of the proof constructed up to that point.
        stop_before_substituted_equality: flag specifying stop proving just
            before the first call to
            `~predicates.prover.Prover.add_substituted_equality` and to return
            the prefix of the proof constructed up to that point.
        stop_before_chained_equality: flag specifying to stop proving just
            before the first call to
            `~predicates.prover.Prover.add_chained_equality` and to return the
            prefix of the proof constructed up to that point.
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover(GROUP_AXIOMS, print_as_proof_forms)
    zero = prover.add_assumption('plus(0,x)=x')
    negation = prover.add_assumption('plus(minus(x),x)=0')
    associativity = prover.add_assumption(
        'plus(plus(x,y),z)=plus(x,plus(y,z))')
    if stop_before_flipped_equality:
        return prover.qed()
    flipped_zero = prover.add_flipped_equality('x=plus(0,x)', zero)
    flipped_negation = prover.add_flipped_equality(
        '0=plus(minus(x),x)', negation)
    flipped_associativity = prover.add_flipped_equality(
        'plus(x,plus(y,z))=plus(plus(x,y),z)', associativity)
    if stop_before_free_instantiation:
        return prover.qed()
    step7 = prover.add_free_instantiation(
        '0=plus(minus(minus(x)),minus(x))', flipped_negation,
        {'x': 'minus(x)'})
    step8 = prover.add_flipped_equality(
        'plus(minus(minus(x)),minus(x))=0', step7)
    step9 = prover.add_free_instantiation(
        'plus(plus(minus(minus(x)),minus(x)),x)='
        'plus(minus(minus(x)),plus(minus(x),x))',
        associativity, {'x': 'minus(minus(x))', 'y': 'minus(x)', 'z': 'x'})
    step10 = prover.add_free_instantiation('plus(0,0)=0', zero, {'x': '0'})
    step11 = prover.add_free_instantiation(
        'plus(x,0)=plus(0,plus(x,0))', flipped_zero, {'x': 'plus(x,0)'})
    step12 = prover.add_free_instantiation(
        'plus(0,plus(x,0))=plus(plus(0,x),0)', flipped_associativity,
        {'x': '0', 'y': 'x', 'z': '0'})
    if stop_before_substituted_equality:
        return prover.qed()
    step13 = prover.add_substituted_equality(
        'plus(plus(0,x),0)=plus(plus(plus(minus(minus(x)),minus(x)),x),0)',
        step7, 'plus(plus(_,x),0)')
    step14 = prover.add_substituted_equality(
        'plus(plus(plus(minus(minus(x)),minus(x)),x),0)='
        'plus(plus(minus(minus(x)),plus(minus(x),x)),0)',
        step9, 'plus(_,0)')
    step15 = prover.add_substituted_equality(
        'plus(plus(minus(minus(x)),plus(minus(x),x)),0)='
        'plus(plus(minus(minus(x)),0),0)',
        negation, 'plus(plus(minus(minus(x)),_),0)')
    step16 = prover.add_free_instantiation(
        'plus(plus(minus(minus(x)),0),0)=plus(minus(minus(x)),plus(0,0))',
        associativity, {'x': 'minus(minus(x))', 'y': '0', 'z': '0'})
    step17 = prover.add_substituted_equality(
        'plus(minus(minus(x)),plus(0,0))=plus(minus(minus(x)),0)',
        step10, 'plus(minus(minus(x)),_)')
    step18 = prover.add_substituted_equality(
        'plus(minus(minus(x)),0)=plus(minus(minus(x)),plus(minus(x),x))',
        flipped_negation, 'plus(minus(minus(x)),_)')
    step19 = prover.add_free_instantiation(
        'plus(minus(minus(x)),plus(minus(x),x))='
        'plus(plus(minus(minus(x)),minus(x)),x)', flipped_associativity,
        {'x': 'minus(minus(x))', 'y': 'minus(x)', 'z': 'x'})
    step20 = prover.add_substituted_equality(
        'plus(plus(minus(minus(x)),minus(x)),x)=plus(0,x)', step8, 'plus(_,x)')
    if stop_before_chained_equality:
        return prover.qed()
    step21 = prover.add_chained_equality(
        'plus(x,0)=x',
        [step11, step12, step13, step14, step15, step16, step17, step18,
         step19,
         step20, zero])
    return prover.qed()


def unique_zero_proof(print_as_proof_forms: bool = False) -> Proof:
    """Proves from the group axioms and from the assumption a+c=a
    (``'plus(a,c)=a'``) that c=0 (``'c=0'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover(GROUP_AXIOMS.union({'plus(a,c)=a'}), print_as_proof_forms)
    zero = prover.add_assumption('plus(0,x)=x')
    negation = prover.add_assumption('plus(minus(x),x)=0')
    associativity = prover.add_assumption(
        'plus(plus(x,y),z)=plus(x,plus(y,z))')
    # -a + a = 0
    step0 = prover.add_free_instantiation('plus(minus(a),a)=0', negation,
                                          {'x': 'a'})
    step1 = prover.add_assumption('plus(a,c)=a')
    # -a + (a + c) = -a + a
    step2 = prover.add_substituted_equality(
        'plus(minus(a),plus(a,c))=plus(minus(a),a)', step1, 'plus(minus(a),_)')
    # (-a + a) + c = -a + (a + c)
    step3 = prover.add_free_instantiation(
        'plus(plus(minus(a),a),c)=plus(minus(a),plus(a,c))',
        associativity, {'x': 'minus(a)', 'y': 'a', 'z': 'c'})

    # 0 + c = (-a + a) + c
    step4 = prover.add_flipped_equality('0=plus(minus(a),a)', step0)
    step5 = prover.add_substituted_equality(
        'plus(0,c)=plus(plus(minus(a),a),c)', step4, 'plus(_,c)')

    # c = 0 + c
    step6 = prover.add_free_instantiation('plus(0,c)=c', zero, {'x': 'c'})
    step7 = prover.add_flipped_equality('c=plus(0,c)', step6)
    step8 = prover.add_chained_equality('c=0',
                                        [step7, step5, step3, step2, step0])
    return prover.qed()


#: The six field axioms
FIELD_AXIOMS = frozenset(GROUP_AXIOMS.union(
    {'plus(x,y)=plus(y,x)', 'times(x,1)=x', 'times(x,y)=times(y,x)',
     'times(times(x,y),z)=times(x,times(y,z))', '(~x=0->Ey[times(y,x)=1])',
     'times(x,plus(y,z))=plus(times(x,y),times(x,z))'}))


def multiply_zero_proof(print_as_proof_forms: bool = False) -> Proof:
    """Proves from the field axioms that 0*x=0 (``'times(0,x)=0'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover(FIELD_AXIOMS, print_as_proof_forms)
    zero = prover.add_assumption('plus(0,x)=x')
    negation = prover.add_assumption('plus(minus(x),x)=0')
    associativity = prover.add_assumption(
        'plus(plus(x,y),z)=plus(x,plus(y,z))')

    associativity1 = prover.add_assumption(
        'times(x,plus(y,z))=plus(times(x,y),times(x,z))')

    step1 = prover.add_free_instantiation(
        'times(x,plus(0,0))=plus(times(x,0),times(x,0))',
        associativity1, {'x': 'x',
                         'y': '0',
                         'z': '0'})
    step2 = prover.add_flipped_equality(
        'plus(times(x,0),times(x,0))=times(x,plus(0,0))', step1)

    step3 = prover.add_free_instantiation('plus(0,0)=0', zero, {'x': '0'})
    step4 = prover.add_substituted_equality('times(x,plus(0,0))=times(x,0)',
                                            step3, 'times(x,_)')
    step5 = prover.add_chained_equality(
        'plus(times(x,0),times(x,0))=times(x,0)',
        [step2, step4])

    # new theme prove add
    step6 = prover.add_free_instantiation(
        'plus(minus(times(x,0)),times(x,0))=0',
        negation, {'x': 'times(x,0)'})
    #  -a + (a + c) = -a + a
    step7 = prover.add_substituted_equality(
        'plus(minus(times(x,0)),plus(times(x,0),times(x,0)))=plus(minus(times(x,0)),times(x,0))',
        step5, 'plus(minus(times(x,0)),_)')
    # (-a + a) + c = -a + (a + c)
    step8 = prover.add_free_instantiation(
        'plus(plus(minus(times(x,0)),times(x,0)),times(x,0))=plus(minus(times(x,0)),plus(times(x,0),times(x,0)))',
        associativity,
        {'x': 'minus(times(x,0))', 'y': 'times(x,0)', 'z': 'times(x,0)'})
    # # 0 + c = (-a + a) + c
    step9 = prover.add_flipped_equality('0=plus(minus(times(x,0)),times(x,0))',
                                        step6)
    step10 = prover.add_substituted_equality(
        'plus(0,times(x,0))=plus(plus(minus(times(x,0)),times(x,0)),times(x,0))',
        step9, 'plus(_,times(x,0))')
    # # c = 0 + c
    step11 = prover.add_free_instantiation('plus(0,times(x,0))=times(x,0)',
                                           zero, {'x': 'times(x,0)'})
    step12 = prover.add_flipped_equality('times(x,0)=plus(0,times(x,0))',
                                         step11)
    step13 = prover.add_chained_equality('times(x,0)=0',
                                         [step12, step10, step8, step7, step6])
    commutative = prover.add_assumption('times(x,y)=times(y,x)')
    #0*x = 0 --> x* 0 = 0
    step14 = prover.add_free_instantiation('times(0,x)=times(x,0)',
                                           commutative, {'x': '0', 'y': 'x'})
    step15 = prover.add_chained_equality('times(0,x)=0', [step14, step13])
    return prover.qed()


#: The induction axiom
INDUCTION_AXIOM = Schema(
    Formula.parse('((R(0)&Ax[(R(x)->R(s(x)))])->Ax[R(x)])'), {'R'})
#: The six axioms of Peano arithmetic
PEANO_AXIOMS = frozenset({'(s(x)=s(y)->x=y)', '(~x=0->Ey[s(y)=x])', '~s(x)=0',
                          'plus(x,0)=x', 'plus(x,s(y))=s(plus(x,y))',
                          'times(x,0)=0', 'times(x,s(y))=plus(times(x,y),x)',
                          INDUCTION_AXIOM})


def peano_zero_proof(print_as_proof_forms: bool = False) -> Proof:
    """Proves from the axioms of Peano arithmetic that 0+x=x
    (``'plus(0,x)=x'``).

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover(PEANO_AXIOMS, print_as_proof_forms)
    zero = prover.add_assumption('plus(x,0)=x')
    adder = prover.add_assumption('plus(x,s(y))=s(plus(x,y))')
    # base induction
    step0 = prover.add_free_instantiation('plus(0,0)=0', zero, {'x': '0'})
    # final induction
    induction_move = prover.add_instantiated_assumption(
        '((plus(0,0)=0&Ax[(plus(0,x)=x->plus(0,s(x))=s(x))])->Ax[plus(0,x)=x])',
        INDUCTION_AXIOM, {'R': 'plus(0,_)=_'})

    mapping = {'R': Formula.parse('plus(0,s(x))=s(_)'),
               'c': Term.parse('plus(0,x)'), 'd': Term('x')}
    step1 = prover.add_instantiated_assumption(Prover.ME.instantiate(mapping),
                                               Prover.ME, mapping)
    step2 = prover.add_free_instantiation('plus(0,s(x))=s(plus(0,x))', adder,
                                          {'x': '0', 'y': 'x'})
    #get the induction claim
    step3 = prover.add_tautological_implication(
        '(plus(0,x)=x->plus(0,s(x))=s(x))',
        {step2, step1})
    #change format into induction
    step4 = prover.add_ug('Ax[(plus(0,x)=x->plus(0,s(x))=s(x))]', step3)
    #claim deduction, (p -> (q -> (p-> (p&q))))
    step5 = prover.add_tautological_implication(
        'Ax[plus(0,x)=x]', {step0, step4, induction_move})
    step6 = prover.add_universal_instantiation('plus(0,x)=x', step5, 'x')
    return prover.qed()


#: The axiom schema of (unrestricted) comprehension
COMPREHENSION_AXIOM = Schema(
    Formula.parse('Ey[Ax[((In(x,y)->R(x))&(R(x)->In(x,y)))]]'), {'R'})


def russell_paradox_proof(print_as_proof_forms: bool = False) -> Proof:
    """Proves from the axioms schema of unrestricted comprehension the
    contradiction ``'(z=z&~z=z)'``.

    Parameters:
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    prover = Prover({COMPREHENSION_AXIOM}, print_as_proof_forms)
    formula1 = 'Ax[((In(x,y)->~In(x,x))&(~In(x,x)->In(x,y)))]'
    formula2 = '((In(y,y)->~In(y,y))&(~In(y,y)->In(y,y)))'
    step1 = prover.add_instantiated_assumption(
        '(' + formula1 + '->' + formula2 + ')',
        Prover.UI,
        {'x': 'x', 'c': 'y', 'R': '((In(_,y)->~In(_,_))&(~In(_,_)->In(_,y)))'})
    # false -> false = tautology
    step2 = prover.add_tautological_implication(
        '(' + formula1 + '->(z=z&~z=z))', {step1})
    #use the axiom to contradict
    step3 = prover.add_instantiated_assumption('Ey[' + formula1 + ']',
                                               COMPREHENSION_AXIOM,
                                               {'R': '~In(_,_)'})
    step4 = prover.add_existential_derivation('(z=z&~z=z)', step3, step2)
    return prover.qed()


def not_exists_not_implies_all_proof(formula: Formula, variable: str,
                                     print_as_proof_forms: bool = False) -> \
        Proof:
    """Proves that
    ``'(~E``\ `variable`\ ``[~``\ `formula`\ ``]->A``\ `variable`\ ``[``\ `formula`\ ``])'``.

    Parameters:
        formula: predicate for the universal quantification in the formula to be
            proven.
        variable: variable name for the quantifications in the formula to be
            proven.
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    assert is_variable(variable)
    not_exists = Formula('~', Formula('E', variable, Formula('~', formula)))
    prover = Prover({not_exists}, print_as_proof_forms)

    mapping1 = {'R' : Formula('~', formula.substitute({variable: Term('_')})), 'c' : Term(variable), 'x' : variable}
    step1 = prover.add_assumption(not_exists)
    step2 = prover.add_instantiated_assumption(Prover.EI.instantiate(mapping1),
                                               Prover.EI, mapping1)
    step3 = prover.add_tautological_implication(formula, {step1 ,step2})
    step4 = prover.add_ug(Formula('A', variable, formula), step3)
    return remove_assumption(prover.qed(), not_exists)


def exists_not_implies_not_all_proof(formula: Formula, variable: str,
                                     print_as_proof_forms: bool = False) -> \
        Proof:
    """Proves that
    ``'(E``\ `variable`\ ``[~``\ `formula`\ ``]->~A``\ `variable`\ ``[``\ `formula`\ ``])'``.

    Parameters:
        formula: predicate for the universal quantification in the formula to be
            proven.
        variable: variable name for the quantifications in the formula to be
            proven.
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    assert is_variable(variable)
    exists = Formula('E', variable, Formula('~', formula))
    prover = Prover({exists}, print_as_proof_forms)

    mapping1 = {'R': formula.substitute({variable: Term('_')}),
                'c': Term(variable), 'x': variable}
    step1 = prover.add_assumption(exists)
    f = Prover.UI.instantiate(mapping1)
    step2 = prover.add_instantiated_assumption(f, Prover.UI, mapping1)
    step3 = prover.add_tautological_implication(Formula('->', Formula('~', f.second), Formula('~', f.first)), {step1, step2})
    step4 = prover.add_existential_derivation(Formula('~', f.first), step1, step3)
    return remove_assumption(prover.qed(), exists)


def not_all_iff_exists_not_proof(formula: Formula, variable: str,
                                 print_as_proof_forms: bool = False) -> Proof:
    """Proves that
    `equivalence_of`\ ``('(~A``\ `variable`\ ``[``\ `formula`\ ``]', 'E``\ `variable`\ ``[~``\ `formula`\ ``]')``.

    Parameters:
        formula: predicate for the universal quantification in the formula to be
            proven.
        variable: variable name for the quantifications in the formula to be
            proven.
        print_as_proof_forms: flag specifying whether the proof is to be printed
            in real time as it is being constructed.

    Returns:
        A valid proof of the above inference via
        `~predicates.prover.Prover.AXIOMS`.
    """
    assert is_variable(variable)
    prover = Prover({}, print_as_proof_forms)
    proof1 = not_exists_not_implies_all_proof(formula, variable,
                                              print_as_proof_forms)
    step1 = prover.add_proof(proof1.conclusion, proof1)
    proof2 = exists_not_implies_not_all_proof(formula, variable,
                                              print_as_proof_forms)
    step2 = prover.add_proof(proof2.conclusion, proof2)

    #((~Ax[R(x)]->Ex[~R(x)])&(Ex[~R(x)]->~Ax[R(x)])))
    forall = Formula('~', Formula('A', variable, formula))
    not_exists = Formula('E', variable, Formula('~', formula))
    helper = Formula('&', Formula('->',  forall, not_exists),
                   Formula('->', not_exists, forall))
    step3 = prover.add_tautological_implication(helper, {step1, step2})
    return  prover.qed()
