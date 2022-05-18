open classical

lemma remove_double_negation {p: Prop}: ¬¬p → p :=
    assume hnnp: ¬¬p,
    by_contradiction
    (assume hnp: ¬p, show false, from hnnp hnp)


lemma qpq {p q: Prop}: q → (p → q) := 
    assume hq: q,
    assume hp: p,
    hq


lemma nppq {p q: Prop}: ¬p → (p → q) := 
    assume hnp: ¬p,
    assume hp: p,
    by_contradiction (assume hnq: ¬q, show false, from hnp hp)


variables p q r s : Prop

-- commutativity of ∧ and ∨

example : p ∨ q ↔ q ∨ p := 
    ⟨λ h, h.elim (λ hp:p, or.inr hp) (λ hq:q, or.inl hq),
     λ h, h.elim (λ hq:q, or.inr hq) (λ hp:p, or.inl hp)⟩ 

 -- associativity of ∧ and ∨

example : (p ∨ q) ∨ r ↔ p ∨ (q ∨ r) := 
    ⟨λ h, h.elim (λ hpq, hpq.elim (λ hp, or.inl hp) (λ hq, or.inr (or.inl hq))) (λ hr, or.inr (or.inr hr)),
     λ h, h.elim (λ hp, or.inl (or.inl hp)) (λ hqr, hqr.elim (λ hq, or.inl (or.inr hq)) (λ hr, or.inr hr))⟩ 

 -- distributivity

example : p ∧ (q ∨ r) ↔ (p ∧ q) ∨ (p ∧ r) := 
    ⟨λ h, or.elim h.right (λ hq, or.inl (and.intro h.left hq)) (λ hr, or.inr (and.intro h.left hr)), 
     λ h, h.elim (λ hpq, and.intro hpq.left (or.inl hpq.right)) (λ hpr, and.intro hpr.left (or.inr hpr.right))⟩ 

 -- other properties

example : ¬(p ∨ q) ↔ ¬p ∧ ¬q := 
    iff.intro
    (   
        assume h: ¬(p ∨ q),
        have hnp: ¬p, from (assume hp: p, show false, from h (or.inl hp)),
        have hnq: ¬q, from (assume hq: q, show false, from h (or.inr hq)),
        and.intro hnp hnq
    )
    (   
        assume h: ¬p ∧ ¬q,
        show ¬(p ∨ q), from 
        (   
            assume hn: (p ∨ q),
            hn.elim (λ hp, show false, from h.left hp) (λ hq, show false, from h.right hq)
        )
    )

example : p ∧ false ↔ false := 
    ⟨λ h, h.right, λ h, false.elim h⟩

example : (p → q) → (¬q → ¬p) := 
    assume h: p → q,
    assume hnq: ¬q,
    by_contradiction
    (   
        assume hnnp: ¬¬p,
        have hp: p, from remove_double_negation hnnp,
        have hq: q, from h hp,
        show false, from hnq hq
    )


example : (p → r ∨ s) → ((p → r) ∨ (p → s)) := 
    assume h: p → r ∨ s,
    by_cases
    (   
        assume hp: p,
        have hrs: r ∨ s, from h hp,
        hrs.elim (λ hr, or.inl (qpq hr)) (λ hs, or.inr (qpq hs))
    )
    (
        assume hnq: ¬p,
        have hpr: (p → r), from nppq hnq,
        or.inl hpr
    )


example : ¬(p ∧ q) → ¬p ∨ ¬q := 
    assume h: ¬(p ∧ q),
    by_cases
    (   
        assume hp: p,
        have hnq: ¬q, from 
            (assume hq: q, show false, from h (and.intro hp hq)),or.inr hnq)
    (assume hnp: ¬p, or.inl hnp)


example : ¬(p → q) → p ∧ ¬q := 
    assume h: ¬(p → q),
    have hnnp: ¬¬p, from (assume hnp: ¬p, show false, from h (nppq hnp)),
    have hp: p, from remove_double_negation hnnp,
    have hnq: ¬q, from (assume hq: q, show false, from h (qpq hq)),
    and.intro hp hnq