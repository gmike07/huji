open classical


variables (α : Type*) (p q : α → Prop)
variable r : Prop

example : α → ((∀ x : α, r) ↔ r) := 
    by {intro a, apply iff.intro, {intro hrall, exact hrall a}, {intro hr, exact λ x, hr}}

example : (∀ x, p x ∨ r) ↔ (∀ x, p x) ∨ r := 
    begin
        apply iff.intro,
        {
            intro hprx,
            apply or.elim (em r),
            {intro hr, simp*},
            {intro hnr, simp* at *}
        },
        {intro hpxr, intro x, apply or.elim hpxr, {intro hpx, simp*}, {intro hr, simp*}}
    end

example : (∀ x, r → p x) ↔ (r → ∀ x, p x) := 
    begin
        apply iff.intro,
        {intros hprx hr, intro x, simp*},
        {intro hrpx, intro x, apply or.elim (em r), {intro hr, simp*}, {intro hnr, simp*}}
    end
