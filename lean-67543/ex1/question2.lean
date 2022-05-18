-- question 2
def curry (α β γ: Type*) (f: α × β → γ) : α → β → γ := λ a b, f (a, b)

def uncurry (α β γ: Type*) (f: α → β → γ) : α × β → γ := λ ab, f ab.1 ab.2

/-
-- test question 2
def h (x: ℕ) (y: ℕ): ℕ := x + y
def g (xy: ℕ × ℕ) : ℕ := xy.1 + xy.2

#check g --g : ℕ × ℕ → ℕ
#check h --h : ℕ → ℕ → ℕ

#check curry ℕ ℕ ℕ g -- ⊢ ℕ → ℕ → ℕ
#check uncurry ℕ ℕ ℕ h -- ⊢ ℕ × ℕ → ℕ

#check curry ℕ ℕ ℕ (uncurry ℕ ℕ ℕ h) -- ⊢ ℕ → ℕ → ℕ
#check uncurry ℕ ℕ ℕ (curry ℕ ℕ ℕ g) -- ⊢ ℕ × ℕ → ℕ
-/