variables p q r : Prop

example : p ∨ false ↔ p := by simp*
example : p ∧ false ↔ false := by simp*
example : (p → q) → (¬q → ¬p) :=
    by {intros hpq hnq, show ¬p, {intro hp, show false, from hnq (hpq hp)}}