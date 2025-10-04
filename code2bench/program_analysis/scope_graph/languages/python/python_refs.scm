;; refs

;;[a, b, c]
(list
  (identifier) @local.reference)

;; f-strings
(interpolation
  (identifier) @local.reference)

;; [ *a ]
(list_splat
  (identifier) @local.reference)

;; {a: A}
;; a is ignored
;; A is a ref
(dictionary
  (pair
    (identifier)
    (identifier) @local.reference))

;; **dict
(dictionary_splat
  (identifier) @local.reference)

;; {a, b, c}
(set
  (identifier) @local.reference)

;; a.b
;; `a` is a ref
;; `b` is ignored
(attribute
  .
  (identifier) @local.reference)

;; if we have self.field(), we can resolve field
;; safely
(attribute 
  (identifier) @_self_ident
  (identifier) @local.reference
  (#eq? @_self_ident "self"))

;; a[b]
(subscript
  (identifier) @local.reference)

;; a[i:j]
(slice
  (identifier) @local.reference)

;; a()
(call
  (identifier) @local.reference)

;; call arguments
(argument_list
  (identifier) @local.reference)

;; call(keyword=arg)
;; `keyword` is ignored
;; `arg` is a ref
(keyword_argument
  (_)
  (identifier) @local.reference)

;; (a, b, c)
(tuple 
  (identifier) @local.reference)

;; for t in item
;;
;; `item` is a reference
(for_in_clause
  "in"
  (identifier) @local.reference)

;; for a in b:
;;
;; `b` is a ref
(for_statement
  "in"
  .
  (identifier) @local.reference)

;; with a as b:
;;
;; `a` is a ref
(as_pattern
  (identifier) @local.reference)

;; (a for a in ..)
(generator_expression
  (identifier) @local.reference)

;; await x
(await
  (identifier) @local.reference)

;; return x
(return_statement
  (identifier) @local.reference)

;; a + b
(binary_operator
  (identifier) @local.reference)

;; ~a
(unary_operator
  (identifier) @local.reference)

;; a and b
(boolean_operator
  (identifier) @local.reference)

;; not a 
(not_operator
  (identifier) @local.reference)

;; a in b
;; a < b
(comparison_operator
  (identifier) @local.reference)

;; a += 1
(augmented_assignment
  (identifier) @local.reference)

;; (a)
(parenthesized_expression
  (identifier) @local.reference)

;; a, b, c
(expression_list
  (identifier) @local.reference)

;; a;
(expression_statement
  (identifier) @local.reference)

;; z if x else y
(conditional_expression
  (identifier) @local.reference)

;; comprehensions
(list_comprehension
  (identifier) @local.reference)
(dictionary_comprehension
  (pair 
    (identifier) @local.reference))
(set_comprehension
  (identifier) @local.reference)

;; decorators
(decorator
  (identifier) @local.reference)

;; type refs
;;
;; def foo(a: T)
(parameters
  (typed_parameter
    (type
      (identifier) @local.reference)))

;; def foo() -> T:
(function_definition 
  return_type: 
  (type
    (identifier) @local.reference))

;; var: T = init()
(assignment 
  type:
  (type 
    (identifier) @local.reference))