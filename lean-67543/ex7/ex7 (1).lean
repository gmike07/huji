import data.nat.basic
import data.list.basic
open list
open nat

-- i used parts of your solution because they were way more elegent
open function

#print surjective

namespace hidden1
universes u v w
variables {α : Type u} {β : Type v} {γ : Type w}
open function

lemma surjective_comp {g : β → γ} {f : α → β}
  (hg : surjective g) (hf : surjective f) :
surjective (g ∘ f) :=
    λ lg,
    match (hg lg) with exists.intro (b: β) (beq : g b = lg) :=
        match (hf b) with exists.intro (a : α) (aeq : f a = b) :=
            begin
                existsi a,
                simp [aeq, beq]
            end
        end
    end
end hidden1

namespace hidden

def add (m n: ℕ): ℕ := nat.rec_on n m (λ n mul_m_n, nat.succ mul_m_n)

def mul (m n : ℕ) : ℕ := nat.rec_on n 0 (λ n mul_m_n, add m mul_m_n)

def pred (n : ℕ) : ℕ := nat.rec_on n 0 (λ n pred_n, n)

def sub (m n : ℕ) : ℕ := nat.rec_on n m (λ n sub_m_n, pred sub_m_n)

def exp (m n : ℕ) : ℕ := nat.rec_on n 1 (λ n exp_m_n, mul m exp_m_n)

@[simp] theorem mul_zero (n: ℕ): mul n 0 = 0 := rfl
@[simp] theorem add_zero (n: ℕ): add n 0 = n := rfl
@[simp] theorem add_one (n: ℕ): add n 1 = nat.succ n := rfl
@[simp] theorem one_more (n: ℕ): add n 1 = nat.succ n := rfl
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


def random_shit : ℕ → ℕ → ℕ
| 0     0           := 0
| 0     n           := n
| m     0           := m
| (m+1)     (n+1)   := random_shit m n