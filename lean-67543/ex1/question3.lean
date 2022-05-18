--question 3
universe u
constant vec: Type u → ℕ → Type u
constant vec_add: Π (n: ℕ), (vec ℕ n) → (vec ℕ n) → (vec ℕ n)
constant vec_reverse: Π (α: Type u) (n: ℕ), (vec α n) → (vec α n)

/-
-- test question 3

#check vec_reverse (vec bool 5)
#check vec_reverse (vec bool 3)
#check vec_reverse (vec ℕ 5)
#check vec_reverse (vec ℕ 3)

constant vec1: vec ℕ 3
constant vec2: vec ℕ 4
constant vec3: vec bool 4
#check vec_add 3 vec1 vec1
#check vec_add 4 vec2 vec2

-- should not compile
-- #check vec_add 3 vec1 vec2
-- #check vec_add 4 vec3 vec3
-/