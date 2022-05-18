import data.nat.basic
import data.list.basic
open list
open nat

-- i used parts of your solution because they were way more elegent

namespace hidden

def mul (m n : ℕ) : ℕ := nat.rec_on n 0 (λ n mul_m_n, m + mul_m_n)

def pred (n : ℕ) : ℕ := nat.rec_on n 0 (λ n pred_n, n)

def sub (m n : ℕ) : ℕ := nat.rec_on n m (λ n sub_m_n, pred sub_m_n)

def exp (m n : ℕ) : ℕ := nat.rec_on n 1 (λ n exp_m_n, mul m exp_m_n)

@[simp] theorem mul_zero (n: ℕ): mul n 0 = 0 := rfl

end hidden


namespace hidden
variable α: Type

def my_reverse: list α → list α
    | [] := []
    | (a :: l) := l ++ [a]

def my_length: list α → ℕ
    | [] := 0
    | (a :: l) := (my_length l) + 1

end hidden


variable α: Type
@[simp] theorem nil_len: length (@nil α) = 0 := rfl
@[simp] theorem nil_add (l: list α): @nil α ++ l = l := rfl
@[simp] theorem add_zero_length (l: list α): length(@nil α ++ l) = length l := by {rw nil_add}

@[simp] theorem plus_one (a: α) (l: list α): length (a::l) = length(l) + 1 := rfl
@[simp] theorem reverse_nil: reverse(@nil α) = @nil α := rfl
@[simp] theorem reverse_one (a: α) (l: list α): reverse (a::l) = (reverse l) ++ [a] := by {simp}

@[simp] example (s t: list α): length(s ++ t) = length(s) + length(t) := by {cases t; simp}
@[simp] example (l: list α): length (reverse l) = length(l) := by {cases l, refl, simp}
@[simp] example (l: list α): reverse (reverse l) = l := by {cases l, refl, simp}



inductive ex: Type
    | const (n: ℕ) : ex
    | var (n: ℕ) : ex
    | plus (s t: ex) : ex
    | mul (s t: ex) : ex

def eval: (ℕ → ℕ) → ex → ℕ
    | (l: ℕ → ℕ) (ex.const n) := n
    | (l: ℕ → ℕ) (ex.var n) := l n
    | (l: ℕ → ℕ) (ex.plus n m) := (eval l n) + (eval l m)
    | (l: ℕ → ℕ) (ex.mul n m) := (eval l n) * (eval l m)



inductive prop: Type
    | false: prop
    | true: prop
    | var: ℕ → prop
    | not (np: prop): prop
    | or (p q: prop): prop
    | and (p q: prop): prop

def eval_prop: prop → (ℕ → bool) → bool
    | (prop.false) (l: ℕ → bool) := false
    | (prop.true) (l: ℕ → bool) := true
    | (prop.var n) (l: ℕ → bool) := l n
    | (prop.not np) (l: ℕ → bool) := not (eval_prop np l)
    | (prop.or p q) (l: ℕ → bool) := or (eval_prop p l) (eval_prop q l)
    | (prop.and p q) (l: ℕ → bool) := and (eval_prop p l) (eval_prop q l)

def complexity: prop → ℕ
    | (prop.false) := 1
    | (prop.true) := 1
    | (prop.var n) := 1
    | (prop.not np) := 1 + complexity(np)
    | (prop.or p q) := 1 + complexity(p) + complexity(q)
    | (prop.and p q) := 1 + complexity(p) + complexity(q)

def replace: prop → ℕ → prop → prop
    | (prop.false) (n: ℕ) p := prop.false
    | (prop.true) (n: ℕ) p := prop.true
    | (prop.var n) (m: ℕ) p := if (n=m) then p else prop.var n
    | (prop.not np) (n: ℕ) p := (prop.not np)
    | (prop.or p q) (n: ℕ) np := (prop.or p q)
    | (prop.and p q) (n: ℕ) np := (prop.and p q)



inductive even_odd : (ℕ × bool) → Prop
    | my_zero: even_odd (0, true)
    | even_rule: ∀ (n: ℕ), even_odd(n, true) → even_odd(n + 1, false)
    | odd_rule: ∀ (n: ℕ), even_odd(n, false) → even_odd(n + 1, true)


theorem true_is_even (n: ℕ) : even_odd ((2*n), true) :=
    nat.rec_on n
        (show even_odd (0, true), from even_odd.my_zero)
        (assume nn, assume h, even_odd.odd_rule (2*nn + 1) (even_odd.even_rule (2*nn) h))

theorem false_is_odd (n: ℕ) : even_odd ((2*n + 1), false) :=
    even_odd.even_rule (2*n) (true_is_even n)
