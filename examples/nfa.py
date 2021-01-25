from micropm4py.nfa import parse_regex, semantics


def main():
    nfa = parse_regex.parse("^a?b.((def)+|(ghi)*)*lm$")
    reach_start = semantics.reachable_invisible(nfa, 0)
    en_trans = semantics.enabled_transitions(nfa, {0})
    print(en_trans)
    print(semantics.accept(nfa, {0}, "abzdefdefghideflm"))


if __name__ == "__main__":
    main()
