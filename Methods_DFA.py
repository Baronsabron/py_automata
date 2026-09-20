"""Methods working with DFA"""

from automata.fa import dfa



class DFA2(dfa.DFA):
    """The DFA2 is a subclass of DFA. It Implements new methods for deterministic finite
    automatons

    Parameters(same as DFA)
    -----------------------
    states : AbstractSet[DFAStateT]
        Set of the DFA's valid states.
    input_symbols : AbstractSet[str]
        Set of the DFA's valid input symbols, each of which is a singleton
        string
    transitions : Mapping[DFAStateT, Mapping[str, DFAStateT]]
        Dict consisting of the transitions for each state. Each key is a
        state name, and each value is another dict which maps a symbol
        (the key) to a state (the value).
    initial_state : DFAStateT
        The initial state for this DFA.
    final_states : AbstractSet[DFAStateT]
        A set of final states for this DFA
    allow_partial : bool, default: False
        By default, each DFA state must have a transition to
        every input symbol; if this parameter is `True`, you can disable this
        characteristic (such that any DFA state can have fewer transitions than input
        symbols). Note that a DFA must always have every state represented in the
        transition dictionary, even if there are no transitions on input symbols
        leaving a state (dictionary is left empty in that case).
    """

    def __init__(self, *, states, input_symbols, transitions,
                initial_state, final_states, allow_partial):
        """Initialize a complete DFA."""
        super().__init__(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
            allow_partial=allow_partial,
        )


    """
    Method for listing all the accessible DFA's states from one state which is by default 
    the initial state.
    
    Parameters
    ----------
    state : AbstractSet[DFAStateT]
        starting state of this methode(by default the initial state
    Returns
    -------
    already_visited : Set[DFAStateT]
        all the accessible DFA's states
    """
    def accessibles_states(self, state= None):
        if state is None:
            state = self.initial_state
        to_visit = [state]
        already_visited = set()
        alphabet = self.input_symbols
        while len(to_visit) != 0:
            state = to_visit.pop()
            already_visited.add(state)
            for symbol in alphabet:
                new_state = self.transitions[state].get(symbol)
                if new_state is not None and new_state not in already_visited:
                    to_visit.append(new_state)
        return already_visited

    """
    Method for listing all the coaccessible DFA's states from a list of states which are 
    by default the finals states.

    Parameters
    ----------
    state : AbstractSet[DFAStateT]
        starting state of this methode(by default the initial state
       
    Returns 
    -------
    already_visited : Set[DFAStateT]
        all the coaccessible DFA's states
    """
    def coaccessibles_states(self, states=None):
        if states is None:
            states = self.final_states
        reverse_transitions = {state: [] for state in self.states}
        #reversal of the transition dictionary
        for state in self.states:
            if state in self.transitions:
                for symbol, next_state in self.transitions[state].items():
                    if next_state is not None:
                        reverse_transitions[next_state].append(state)
        to_visit = list(states)
        already_visited = set()
        while to_visit:
            current_state = to_visit.pop()
            already_visited.add(current_state)
            for prev_state in reverse_transitions.get(current_state, []):
                if prev_state not in already_visited:
                    to_visit.append(prev_state)
        return already_visited

    """
    Method for trimming the DFA
    (erasing all states which are not accessible AND coaccessible)
    
    Parameters
    ----------
    None
    
    Returns
    -------
    DFA2
    a new instance of the DFA2 automaton which is trimmed
    """
    def trimming(self):
        accessible_states = self.accessibles_states()
        coaccessible_states = self.coaccessibles_states()
        new_states = accessible_states.intersection(coaccessible_states)
        new_final_states = self.final_states.intersection(new_states)
        new_transitions = {}
        for state in new_states:
            new_transitions[state] = {}
            for symbol, target_state in self.transitions[state].items():
                if target_state in new_states:
                    new_transitions[state][symbol] = target_state

        return DFA2(
            states=new_states,
            input_symbols=self.input_symbols,
            transitions=new_transitions,
            initial_state=self.initial_state,
            final_states=new_final_states,
            allow_partial=True#erasing of branch so the automaton is likely partial
        )






test1 = DFA2(states={'1', '2', '3'},
    input_symbols={'a', 'b'},
    transitions={
        '1': {'a': '2', 'b': '3'},
        '2': {'a': '2', 'b': '3'},
        '3': {'a': '3', 'b': '3'}
    },
    initial_state='1',
    final_states={'2'},
    allow_partial=False)
print(test1.accessibles_states())
print(test1.coaccessibles_states())
trimmed = test1.trimming()
print(trimmed.accessibles_states())
print(trimmed.coaccessibles_states())