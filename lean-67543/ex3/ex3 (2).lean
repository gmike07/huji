import data.nat.basic
import data.real.basic
open classical



-- question 2
variables (α : Type*) (p q : α → Prop)
variable r : Prop


example : α → ((∀ x : α, r) ↔ r) := 
    assume a: α,
    iff.intro
    (
        assume h: ∀ x : α, r, h a
    )
    (
        assume hr: r, λ _, hr
    )


example : (∀ x, p x ∨ r) ↔ (∀ x, p x) ∨ r := 
    iff.intro
    (
        assume h: ∀ x, p x ∨ r,
        have hnrr: r ∨ ¬r, from classical.em r,
        hnrr.elim
        (
            assume hr: r,
            show (∀ x, p x) ∨ r, from or.inr hr
        )
        (
            assume hnr: ¬r,
            show (∀ x, p x) ∨ r, from or.inl
                (
                    assume x,
                    have hn: p x ∨ r, from h x,
                    hn.elim
                    (
                        assume hpx: p x,
                        show p x, from hpx
                    )
                    (
                        assume hr: r,
                        false.elim (hnr hr)
                    )
                )
        )

    )
    (
        assume h: (∀ x, p x) ∨ r,
        h.elim
        (
            assume hp: ∀ x, p x,
            assume x,
            show p x ∨ r, from or.inl (hp x)
        )
        (
            assume hr: r,
            assume x,
            show p x ∨ r, from or.inr hr
        )
    )

example : (∀ x, r → p x) ↔ (r → ∀ x, p x) := 
    iff.intro
    (
        assume h: ∀ x, r → p x,
        assume hr: r,
        assume x,
        have hrp: r → p x, from h x,
        show p x, from hrp hr
    )
    (
        assume h: r → ∀ x, p x,
        assume x,
        assume hr: r,
        have hp: ∀ x, p x, from h hr,
        show p x, from hp x
    )



--question 3

variables (men : Type*) (barber : men)
variable  (shaves : men → men → Prop)

example (h : ∀ x : men, shaves barber x ↔ ¬ shaves x x) :
  false := 
    have hbarber: shaves barber barber ↔ ¬ shaves barber barber, from h barber,
    by_cases
    (
        assume hnnbarber: shaves barber barber,
        show false, from (iff.elim_left hbarber hnnbarber) hnnbarber
    )
    (
        assume hnbarber: ¬shaves barber barber,
        show false, from hnbarber (iff.elim_right hbarber hnbarber)
    )



--question 4
-- You can enter the '∣' character by typing \mid

def prime (n : ℕ) : Prop := ∀ (p: ℕ), ((1 < p) ∧ (p < n)) → (¬(p ∣ n))

def infinitely_many_primes : Prop := ∀ (n: ℕ), ∃(p: ℕ), (p > n ∧ prime(p))

def Fermat_number(n: ℕ) : Prop := ∃(m: ℕ), n=(2^(2^m)) + 1

def Fermat_prime (n : ℕ) : Prop := Fermat_number(n) ∧ prime(n)

def infinitely_many_Fermat_primes : Prop := ∀ (n: ℕ), ∃(p: ℕ), (p > n ∧ Fermat_prime(p))

def goldbach_conjecture : Prop := ∀(n: ℕ), 2 ≤ n → ∃(p q: ℕ), prime(p) ∧ prime(q) ∧ (n = p + q)

def Goldbach's_weak_conjecture : Prop := ∀(n: ℕ), (5 ≤ n ∧ ¬(2 ∣ n)) → ∃(p q z: ℕ), prime(p) ∧ prime(q) ∧ prime(z) ∧ (n = p + q + z)

def Fermat's_last_theorem : Prop := ∀(n: ℕ), 2 < n → ∀(a b c: ℕ), a^n + b^n ≠ c^n



--question 6

variables log exp     : real → real
variable  log_exp_eq : ∀ x, log (exp x) = x
variable  exp_log_eq : ∀ {x}, x > 0 → exp (log x) = x
variable  exp_pos    : ∀ x, exp x > 0
variable  exp_add    : ∀ x y, exp (x + y) = exp x * exp y

-- this ensures the assumptions are available in tactic proofs
include log_exp_eq exp_log_eq exp_pos exp_add

example (x y z : real) :
  exp (x + y + z) = exp x * exp y * exp z :=
by rw [exp_add, exp_add]

example (y : real) (h : y > 0)  : exp (log y) = y :=
exp_log_eq h

theorem log_mul {x y : real} (hx : x > 0) (hy : y > 0) :
  log (x * y) = log x + log y :=
    by rw [←exp_log_eq hx, ←exp_log_eq hy, ←exp_add, log_exp_eq, log_exp_eq, log_exp_eq]

