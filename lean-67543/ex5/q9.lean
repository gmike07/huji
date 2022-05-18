variable  U : Type
variables R : U → U → Prop

example : (∃ x, ∀ y, R x y) → ∀ y, ∃ x, R x y :=
begin
  intro h,
  intro y,
  cases h with x hy,
  existsi x,
  exact hy y
end