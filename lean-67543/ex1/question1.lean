--question 1
def Do_Twice {α: Type*} (f: α → α) (x: α) : α := f(f x)

/-
-- test question 1
def double: ℕ → ℕ := λ x, x+x
def square: ℕ → ℕ := λ x, x * x
def do_twice: (ℕ → ℕ) → ℕ → ℕ := λ f x, f (f x)
#eval Do_Twice square 1 -- 1=1*1
#eval Do_Twice do_twice double 2 -- 2+2 first, 4+4 second, 8+8 third, 16+16 fourth=32
-/