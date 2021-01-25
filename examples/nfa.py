from micropm4py.nfa import parse_regex

nfa = parse_regex.parse("^a?b.((def)+|(ghi)*)*lm$")
del parse_regex

from micropm4py.nfa import semantics

print(semantics.accept(nfa, {0}, "abzdefdefghideflm"))
