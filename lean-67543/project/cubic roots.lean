import data.real.basic
import algebra.invertible
import tactic.linarith
import order.filter.at_top_bot
import algebra.ring
import data.nat.basic
import data.complex.basic
import data.complex.exponential
open filter

section ring
section field
variables {R : Type*}

lemma third_power (x y: ℂ): (x + y)^3 = x*x*x + 3* x*x * y + 3 * x * y * y + y * y * y := by ring

lemma helper {a: ℂ} (ha : a ≠ 0): a * a⁻¹ = 1 := mul_inv_cancel ha

lemma helper1 {x y t s: ℂ} (hxy: y = x): t * (x - y) * s = 0 := by {rw hxy, simp}

lemma helper2 {x y s: ℂ} (h: (x - y) * s = 0) (hnxy: x ≠ y): s = 0 :=
      begin
      have hnxy1: x - y ≠ 0, exact sub_ne_zero.mpr hnxy,
      calc
            s = 1 * s : by simp
            ... = (x - y) * (x - y)⁻¹ * s : by rw helper hnxy1
            ... = (x - y)⁻¹  * ((x - y) * s) : by ring
            ... = (x - y)⁻¹ * 0: by rw h
            ... = 0: by simp
      end
lemma helper3 {x y t: ℂ} (h: (x - y) * (x - t) = 0) (hnxy: x ≠ y): x = t :=
      begin
            have h1: x - t = 0, exact helper2 h hnxy,
            exact sub_eq_zero.mp h1
      end
lemma helper4 {x y t s: ℂ} (h: (x - y) * (x - s) * (x - t) = 0) (hnxy: x ≠ y) (hnxs: x ≠ s): x = t :=
      begin
            have h': (x - y) * ((x - s) * (x - t)) = 0,
                  calc
                        (x - y) * ((x - s) * (x - t)) = (x - y) * (x - s) * (x - t) : by ring
                        ... = 0: by rw h,

            have h1: (x - s) * (x - t) = 0, exact helper2 h' hnxy,
            have h2: x - t = 0, exact helper2 h1 hnxs,
            exact sub_eq_zero.mp h2
      end

lemma helper5 (x: ℂ): (x^(1/3))^(3) = x := sorry
-- note this is true for R, not for C :( but this means to change all the proofs and start from 0
-- because lean doesn't support operations on real with complex and doenst support real powers,
-- the proof will become very hard
lemma helper55 (x: ℂ): (x^(3))^(1/3) = x := sorry

lemma helper6 {a b: ℂ}: (a + b) * (a - b) = a^2 - b^2 := by ring

lemma simplify_roots {a b p q r: ℂ} (ha: a = (-q/2 + r)^(1/3))
      (hb: b= (-q/2 - r)^(1/3)) (hr: r^2 = q^2/4 + p^3/27) : 3 * a * b = -p :=
      by calc
            3 * a * b = (3) * (-q/2 + r)^(1/3) * (-q/2 - r)^(1/3): by rw [ha, hb]
            ... = 3 * (((-q/2 - r) * (-q/2 + r)))^(1/3): by ring
            ... = 3 * (((-q/2)^2 - r^2))^(1/3): by ring
            ... = 3 * (((-q/2)^2 - (q^2/4 + p^3/27)))^(1/3): by rw hr
            ... = 3 * ((q^2/4 - (q^2/4 + p^3/27)))^(1/3): by ring
            ... = 3 * ((-p^3/27)^(1/3)): by ring
            -- note, this is true but again due to lean's not developed power tactics it doesn't see it even when I attempt to rewrite it
            -- I asked in zulip and currently the answer is to develop all the tools from scratch, but it is too dificult so I leave it with sorry
            -- until the tools will be created
            ... = (3^3)^(1/3) * ((-p^3/27)^(1/3)): by sorry
            ... = ((27) * (27⁻¹) * (-p^3))^(1/3): by ring
            ... = (3*3*3 * (27⁻¹) * (-p^3))^(1/3): by ring
            ... = ((27 * 27⁻¹) * (-p^3))^(1/3): by ring
            ... = (1 * (-p^3))^(1/3): by ring
            ... = (-1)^(1/3) * (p^3)^(1/3): by ring
            ... = ((-1)^(1/3)) * p: by rw (helper55 p)
            ... = (-1) * p: by sorry
            ... = -p: by simp



lemma div_pol2 {x x1 x2: ℂ} : (x - x1) * (x - x2) = 0 ↔ (x = x1) ∨ (x = x2) :=
begin
      apply iff.intro,
      have hx1: (x = x1) ∨ ¬(x = x1), from classical.em (x = x1),
      have hx2: (x = x2) ∨ ¬(x = x2), from classical.em (x = x2),
      {assume h, apply or.elim hx1, {assume h1, apply or.inl h1},
      {assume hn1, apply or.inr (helper3 h hn1)}},
      {assume h, apply or.elim h, {intro h1, rw h1, simp*}, {intro h2, rw h2, simp*}}
end

lemma div_pol3 {x x1 x2 x3: ℂ} : (x - x1) * (x - x2) * (x - x3) = 0 ↔ (x = x1) ∨ (x = x2) ∨ (x = x3) :=
begin
      apply iff.intro,
      have hx1: (x = x1) ∨ ¬(x = x1), from classical.em (x = x1),
      have hx2: (x = x2) ∨ ¬(x = x2), from classical.em (x = x2),
      {assume h, apply or.elim hx1, {assume h1, apply or.inl h1},
      {assume hn1, apply or.elim hx2, {assume h2, apply or.inr (or.inl h2)},
      {assume hn2, apply or.inr (or.inr (helper4 h hn1 hn2))}}},
      {assume h, apply or.elim h, {intro h1, rw h1, simp*}, {intro h11, apply or.elim h11,
      {intro h2, rw h2, simp*}, {intro h3, rw h3, simp*}}}
end

lemma div_pol32 {a x x1 x2 x3: ℂ} (ha: a ≠ 0): a * (x - x1) * (x - x2) * (x - x3) = 0 ↔ (x = x1) ∨ (x = x2) ∨ (x = x3) :=
begin
      apply iff.intro,
      {assume h,
      have h1: (x - x1) * (x - x2) * (x - x3) = 0,
            calc
            (x - x1) * (x - x2) * (x - x3) = (x - x1) * (x - x2) * (x - x3) * 1: by simp
            ... = (x - x1) * (x - x2) * (x - x3) * (a * a⁻¹): by rw helper ha
            ... = a * (x - x1) * (x - x2) * (x - x3) * a⁻¹: by ring
            ... = 0 * a⁻¹: by rw h
            ... = 0: by simp,
      exact div_pol3.mp h1
      },
      {assume h, apply or.elim h, {intro h1, rw h1, simp*}, {intro h11, apply or.elim h11,
      {intro h2, rw h2, simp*}, {intro h3, rw h3, simp*}}}
end


lemma convert_polynom {a b c d p q x t: ℂ} (ha: a ≠ 0)
      (hp: p = (3*a*c-b*b) * (1 / 3) * (1 / a) * (1 / a))
      (hq: q = (2*b*b*b - 9*a*b*c +27*a*a*d) * (1 / 27) * (1 / a) * (1 / a) * (1 / a))
      (ht: t = x + b * (1 / 3) * (1 / a)) :
      a * (t^3 + p*t + q) = a * x^3 + b * x^2 + c*x + d :=
      by calc
            a * (t^3 + p*t + q) = a * (x * x * x + 3 * x * x * (b * 3⁻¹ * a⁻¹) + 3 * x * (b * 3⁻¹ * a⁻¹) * (b * 3⁻¹ * a⁻¹) + b * 3⁻¹ * a⁻¹ * (b * 3⁻¹ * a⁻¹) * (b * 3⁻¹ * a⁻¹) + (3 * a * c - b * b) * 3⁻¹ * a⁻¹ * a⁻¹ * (x + b * 3⁻¹ * a⁻¹) + (2 * b * b * b - 9 * a * b * c + 27 * a * a * d) * 27⁻¹ * a⁻¹ * a⁻¹ * a⁻¹): by {rw [hp, hq, ht, (third_power x (b * (1 / 3) * (1 / a)))], simp*}
            ... =  a * (x^3 + 3 * x^2 * (b * 3⁻¹ * a⁻¹) + 3 * x * (b^2 * 9⁻¹ * (a⁻¹)^2) + (b^3 * 27⁻¹ * (a⁻¹)^3) + (3 * a * c - b * b) * 3⁻¹ * (a⁻¹)^2 * x + (3 * a * c - b * b) * 9⁻¹ * (a⁻¹)^3 * b + (2 * b^3 - 9 * a * b * c + 27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... =  a * (x^3 + x^2 * (b * a⁻¹) + x * (b^2 * 3⁻¹ * (a⁻¹)^2) + (b^3 * 27⁻¹ * (a⁻¹)^3) + (3 * a * c - b * b) * 3⁻¹ * (a⁻¹)^2 * x + (3 * a * c - b * b) * 9⁻¹ * (a⁻¹)^3 * b + (2 * b^3 - 9 * a * b * c + 27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... =  a * (x^3 + x^2 * (b * a⁻¹) + x * (b^2 * 3⁻¹ * (a⁻¹)^2 + (3 * a * c - b * b) * 3⁻¹ * (a⁻¹)^2) + (b^3 * 27⁻¹ * (a⁻¹)^3) + (3 * a * c - b^2) * 3 *  27⁻¹ * (a⁻¹)^3 * b + (2 * b^3 - 9 * a * b * c + 27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... =  a * (x^3 + x^2 * (b * a⁻¹) + x * ((b^2 + (3 * a * c - b^2)) * 3⁻¹ * (a⁻¹)^2) + (b^3 * 27⁻¹ * (a⁻¹)^3) + (3 * a * c - b^2) * 3 *  27⁻¹ * (a⁻¹)^3 * b + (2 * b^3 - 9 * a * b * c + 27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... =  a * (x^3 + x^2 * (b * a⁻¹) + x * (3 * a * c * 3⁻¹ * (a⁻¹)^2) + (b^3 * 27⁻¹ * (a⁻¹)^3) + (3 * a * c - b^2) * 3 *  27⁻¹ * (a⁻¹)^3 * b + (2 * b^3 - 9 * a * b * c + 27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... =  a * (x^3 + x^2 * (b * a⁻¹) + x * (3 * a * c * 3⁻¹ * (a⁻¹)^2) + (b^3 * 27⁻¹ * (a⁻¹)^3) + ((3 * a * c - b^2) * 3 * b + 2 * b^3 - 9 * a * b * c + 27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... = a * (x^3 + x^2 * (b * a⁻¹) + x * (3 * a * c * 3⁻¹ * (a⁻¹)^2) + (b^3 + (3 * a * c - b^2) * 3 * b + 2 * b^3 - 9 * a * b * c + 27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... = a * (x^3 + x^2 * (b * a⁻¹) + x * (3 * a * c * 3⁻¹ * (a⁻¹)^2) + (b^3 + 9 * a * b * c - 3*b^3 + 2 * b^3 - 9 * a * b * c + 27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... = a * (x^3 + x^2 * (b * a⁻¹) + x * (3 * a * c * 3⁻¹ * (a⁻¹)^2) + (9 * a * b * c - 3*b^3 + 3 * b^3 - 9 * a * b * c + 27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... = a * (x^3 + x^2 * (b * a⁻¹) + x * (3 * a * c * 3⁻¹ * (a⁻¹)^2) + (27 * a^2 * d) * 27⁻¹ * (a⁻¹)^3) : by ring
            ... = a * (x^3 + x^2 * (b * a⁻¹) + x * (a * c * (a⁻¹)^2) + (a^2 * d) * (a⁻¹)^3) : by ring
            ... = a * x^3 + x^2 * (b * a⁻¹ * a) + x * (a * a * c * (a⁻¹)^2) + (a * a^2 * d) * (a⁻¹)^3 : by ring
            ... = a * x^3 + x^2 * (b * a⁻¹ * a) + x * (a^2 * c * (a⁻¹)^2) + (a^3 * d) * (a⁻¹)^3 : by ring
            ... = a * x^3 + x^2 * b * (a * a⁻¹) + x * c * (a * a⁻¹)^2 + d * (a * a⁻¹)^3 : by ring
            ... = a * x^3 + x^2 * b * (a * a⁻¹) + x * c * (a * a⁻¹)^2 + d * (a * a⁻¹)^3 : by ring
            ... = a * x^3 + x^2 * b * 1 + x * c * 1^2 + d * 1^3 : by rw helper ha
            ... = a * x^3 + x^2 * b * 1 + x * c * 1 + d * 1 : by ring
            ... = a * x^3 + x^2 * b + x * c + d : by ring
            ... = a * x^3 + b * x^2 + c * x + d : by ring

noncomputable def smart_pol (t w1 w2 r: ℂ): ℂ  :=
      (t - (w1 + w2)) *
      (t - (w1 * (-1 + r*complex.I) / 2 + w2 * (-1 - r*complex.I) / 2)) *
      (t - (w1 * (-1 - r*complex.I) / 2 + w2 * (-1 + r*complex.I) / 2))

lemma expansion_roots {w1 w2 t r: ℂ} (hr: r^2=3): smart_pol t w1 w2 r = t^3 - 3*w1*w2*t -w1^3 - w2^3 :=
by {rw smart_pol, ring, rw hr, simp*, ring}


lemma simplify_roots2 {w1 w2 p q W: ℂ} (hw1: w1 = (-q/2 + W)^(1/3))
      (hw2: w2 = (-q/2 - W)^(1/3)) (hW: W^2 = q^2/4 + p^3/27): -w1^3 - w2^3 = q :=
      by calc
            -w1^3 - w2^3 = -((-q/2 + W)^(1/3))^(3) - ((-q/2 - W)^(1/3))^3: by rw [hw1, hw2]
            ... = -(-q/2 + W) - (-q/2 - W): by rw [helper5 (-q/2 + W), helper5 (-q/2 - W) ]
            ... = q / 2 + q/2 : by ring
            ... = q : by simp


lemma equal_polynoms2 {r w1 w2 W p q t : ℂ} (hw1: w1 = (-q/2 + W)^(1/3))
      (hw2: w2 = (-q/2 - W)^(1/3)) (hW: W^2 = q^2/4 + p^3/27) (hr: r^2=3):
      smart_pol t w1 w2 r = t^3 + p*t + q :=
by calc
      smart_pol t w1 w2 r = t^3 - 3*w1*w2*t -w1^3 - w2^3 : by rw expansion_roots hr
      ... = t^3 - 3*w1*w2*t + (-w1^3 - w2^3): by ring
      ... = t^3 - 3*w1*w2*t + q: by rw simplify_roots2 hw1 hw2 hW
      ... = t^3 - (-p)*t + q: by rw simplify_roots hw1 hw2 hW
      ... = t^3 + p*t + q: by simp


lemma equal_polynoms3 {r w1 w2 W a b c d p q x t: ℂ} (ha: a ≠ 0)
      (hp: p = (3*a*c-b*b) * (1 / 3) * (1 / a) * (1 / a))
      (hq: q = (2*b*b*b - 9*a*b*c +27*a*a*d) * (1 / 27) * (1 / a) * (1 / a) * (1 / a))
      (ht: t = x + b * (1 / 3) * (1 / a)) (hw1: w1 = (-q/2 + W)^(1/3))
      (hw2: w2 = (-q/2 - W)^(1/3)) (hW: W^2 = q^2/4 + p^3/27) (hr: r^2=3):
      a * (smart_pol t w1 w2 r) = a * x^3 + b*x^2 + c * x + d :=
by calc
      a * (smart_pol t w1 w2 r) = a * (t^3 + p*t + q): by rw equal_polynoms2 hw1 hw2 hW hr
      ... = a * x^3 + b*x^2 + c*x + d: by rw convert_polynom ha hp hq ht

lemma iff_zero {r w1 w2 W a b c d p q x t: ℂ} (ha: a ≠ 0)
      (hp: p = (3*a*c-b*b) * (1 / 3) * (1 / a) * (1 / a))
      (hq: q = (2*b*b*b - 9*a*b*c +27*a*a*d) * (1 / 27) * (1 / a) * (1 / a) * (1 / a))
      (ht: t = x + b * (1 / 3) * (1 / a)) (hw1: w1 = (-q/2 + W)^(1/3))
      (hw2: w2 = (-q/2 - W)^(1/3)) (hW: W^2 = q^2/4 + p^3/27) (hr: r^2=3):
      a * x^3 + b*x^2 + c * x + d = 0 ↔ smart_pol t w1 w2 r = 0 :=
      begin
            apply iff.intro,
            {assume h,
            calc
                  smart_pol t w1 w2 r = (1) * (smart_pol t w1 w2 r): by simp
                  ... = (a * a⁻¹) * (smart_pol t w1 w2 r): by rw helper ha
                  ... = a⁻¹ * (a * (smart_pol t w1 w2 r)): by ring
                  ... = a⁻¹ * (a * x^3 + b*x^2 + c * x + d): by rw equal_polynoms3 ha hp hq ht hw1 hw2 hW hr
                  ... = a⁻¹ * 0: by rw h
                  ... = 0: by ring
            },
            {assume h,
            calc
                  a * x^3 + b*x^2 + c * x + d = a * (smart_pol t w1 w2 r): by rw equal_polynoms3 ha hp hq ht hw1 hw2 hW hr
                  ... = a * 0: by rw h
                  ... = 0: by ring
            }
      end

def roots (t w1 w2 r: ℂ): Prop  :=
      (t = (w1 + w2))
      ∨ (t = (w1 * (-1 + r*complex.I) / 2 + w2 * (-1 - r*complex.I) / 2))
      ∨ (t = ((w1 * (-1 - r*complex.I) / 2 + w2 * (-1 + r*complex.I) / 2)))

lemma roots1 {r w1 w2 t: ℂ}: smart_pol t w1 w2 r = 0 ↔ roots t w1 w2 r :=
      begin
            apply iff.intro,
            {
                  assume h,
                  show roots t w1 w2 r, exact div_pol3.mp h
            },
            {
                  assume h,
                  show (t - (w1 + w2)) * (t - (w1 * (-1 + r*complex.I) / 2 + w2 * (-1 - r*complex.I) / 2)) *(t - (w1 * (-1 - r*complex.I) / 2 + w2 * (-1 + r*complex.I) / 2)) = 0, exact div_pol3.mpr h
            }
      end


lemma roots2 {r w1 w2 W a b c d p q x t: ℂ} (ha: a ≠ 0)
      (hp: p = (3*a*c-b*b) * (1 / 3) * (1 / a) * (1 / a))
      (hq: q = (2*b*b*b - 9*a*b*c +27*a*a*d) * (1 / 27) * (1 / a) * (1 / a) * (1 / a))
      (ht: t = x + b * (1 / 3) * (1 / a)) (hw1: w1 = (-q/2 + W)^(1/3))
      (hw2: w2 = (-q/2 - W)^(1/3)) (hW: W^2 = q^2/4 + p^3/27) (hr: r^2=3):
      a*x^3 + b*x^2 + c*x + d = 0 ↔ roots t w1 w2 r :=
      begin
            apply iff.intro,
            {
                  assume h,
                  exact roots1.mp ((iff_zero ha hp hq ht hw1 hw2 hW hr).mp h)
            },
            {
                  assume h,
                  exact (iff_zero ha hp hq ht hw1 hw2 hW hr).mpr (roots1.mpr h)
            }
      end

def rootsx (x a b r w1 w2:ℂ): Prop :=
      (x = (w1 + w2) - b * (1 / 3) * (1 / a))
      ∨ (x = (w1 * (-1 + r*complex.I) / 2 + w2 * (-1 - r*complex.I) / 2) - b * (1 / 3) * (1 / a))
      ∨ (x = ((w1 * (-1 - r*complex.I) / 2 + w2 * (-1 + r*complex.I) / 2)) - b * (1 / 3) * (1 / a))

lemma roots3_helper {z x t: ℂ} (ht: t = x + z): x = t - z := by {rw ht, ring}
lemma roots3_helper2 {x t z s: ℂ} (ht1: t = x + z) (ht2: t = s): x = s - z :=
      by calc
            x = t - z : by rw roots3_helper ht1
            ... = s - z: by rw ht2

lemma roots3_helper3 {x t z s: ℂ} (ht1: t = x + z) (hx2: x = s - z): t = s :=
      by calc
            t = x + z : by rw ht1
            ... = s - z + z: by rw hx2
            ... = s: by simp


lemma roots3 {r w1 w2 W a b c d p q x t: ℂ} (ha: a ≠ 0)
      (hp: p = (3*a*c-b*b) * (1 / 3) * (1 / a) * (1 / a))
      (hq: q = (2*b*b*b - 9*a*b*c +27*a*a*d) * (1 / 27) * (1 / a) * (1 / a) * (1 / a))
      (ht: t = x + b * (1 / 3) * (1 / a)) (hw1: w1 = (-q/2 + W)^(1/3))
      (hw2: w2 = (-q/2 - W)^(1/3)) (hW: W^2 = q^2/4 + p^3/27) (hr: r^2=3):
      roots t w1 w2 r ↔ rootsx x a b r w1 w2 :=
      begin
      apply iff.intro,
      {assume h, apply or.elim h,
            {assume h1, apply or.inl (roots3_helper2 ht h1)},
            {assume h23, apply or.elim h23,
                  {assume h1, apply or.inr (or.inl (roots3_helper2 ht h1))},
                  {assume h1, apply or.inr (or.inr (roots3_helper2 ht h1))}
            }
      },
      {assume h, apply or.elim h,
            {assume h1, apply or.inl (roots3_helper3 ht h1)},
            {assume h23, apply or.elim h23,
                  {assume h1, apply or.inr (or.inl (roots3_helper3 ht h1))},
                  {assume h1, apply or.inr (or.inr (roots3_helper3 ht h1))}
            }
      }
      end

-- notice that we know a, b, we can calculate p,q then calculate W, then w1, w2 and r is just sqrt(3) so we
-- got a concrete formula for the roots of a cubic equation
lemma roots_formula {r w1 w2 W a b c d p q x t: ℂ} (ha: a ≠ 0)
      (hp: p = (3*a*c-b*b) * (1 / 3) * (1 / a) * (1 / a))
      (hq: q = (2*b*b*b - 9*a*b*c +27*a*a*d) * (1 / 27) * (1 / a) * (1 / a) * (1 / a))
      (ht: t = x + b * (1 / 3) * (1 / a)) (hw1: w1 = (-q/2 + W)^(1/3))
      (hw2: w2 = (-q/2 - W)^(1/3)) (hW: W^2 = q^2/4 + p^3/27) (hr: r^2=3):
      a * x^3 + b*x^2 + c * x + d = 0 ↔ rootsx x a b r w1 w2 :=
      begin
            apply iff.intro,
            {
                  assume h,
                  exact (roots3 ha hp hq ht hw1 hw2 hW hr).mp ((roots2 ha hp hq ht hw1 hw2 hW hr).mp h)
            },
            {
                  assume h,
                  exact (roots2 ha hp hq ht hw1 hw2 hW hr).mpr ((roots3 ha hp hq ht hw1 hw2 hW hr).mpr h)
            }
      end


end field
end ring