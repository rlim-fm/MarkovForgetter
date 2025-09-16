import numpy as np
import itertools
import random

class MarkovChain:
    def __init__(self, pad=True, order=1):
        self.order = order
        self.transitions = {}
        self.states = set()
        self.pad = pad
        self.generated_sequence = []

    def learn(self, sequences):
        for seq in sequences:
            self.states.update(seq)
            if self.pad:
                seq = [None]*self.order + seq + [None]*self.order
            for i in range(len(seq) - self.order):
                state = tuple(seq[i : i + self.order])
                next_state = seq[i + self.order]
                self.transitions[state] = self.transitions.get(state, {})
                self.transitions[state][next_state] = self.transitions[state].get(next_state, 0) + 1

        # Normalize probabilities
        self.probs = {}
        for state, next_states in self.transitions.items():
            total = sum(next_states.values())
            self.probs[state] = {k: v/total for k, v in next_states.items()}

    def generate_next(self, current_state=None):
        """
        Generate the next state based on the current state.

        :param current_state:
        :return:
        """

        # By default, use the last 'order' states from the generated sequence, padding None if necessary
        if current_state is None:
            current_state = self.generated_sequence[-min(self.order, len(self.generated_sequence)):]
            while len(current_state) < self.order:
                current_state.insert(0, None)
        next_states = self.probs.get(tuple(current_state), {None: 1.0}) # if state not found, return end token
        next_state = np.random.choice(list(next_states.keys()), p=list(next_states.values()))
        if next_state is not None:
            self.generated_sequence.append(next_state)
            return next_state
        else:
            return self.generate_next([None]*self.order) # resample from start tokens if end token is reached (i.e. None)

class BlockIterator:
    def __init__(self, shape, block_size=1, axis=0, pattern=None, seed=None):
        """
        Iterate over a 2D array in blocks along a specified axis.

        :param shape:
        :param start:
        :param block_size:
        :param axis:
        :param zigzag:
        :param continue_from_end:
        """

        self.shape = shape
        self.block_size = block_size
        if shape[0] % block_size != 0 or shape[1] % block_size != 0:
            raise ValueError("shape[0] and shape[1] must be divisible by block_size")
        self.axis = axis
        self.pattern = pattern
        if pattern == 'random' and seed is None:
            seed = random.randint(0, 2 ** 32 - 1)
        self.seed = seed

    def __iter__(self):
        x_start, x_end = 0, self.shape[0]
        y_start, y_end = 0, self.shape[1]
        if self.block_size < 0:
            x_start, x_end = self.shape[0] - 1, -1
            y_start, y_end = self.shape[1] - 1, -1

        x = range(x_start, x_end, self.block_size)
        y = range(y_start, y_end, self.block_size)
        if self.axis == 1:
            x, y = y, x
        corners = list(itertools.product(x, y))
        if self.pattern == 'random':
            random.shuffle(corners)
        return corners.__iter__()

    def copy(self):
        return BlockIterator(self.shape, self.block_size, self.axis, self.pattern, self.seed)


class Block:
    """
    A hashable block of an image.
    """
    def __init__(self, arr: np.ndarray):
        self.arr = arr

    def __hash__(self):
        return hash(tuple(self.arr.flatten()))

    def __eq__(self, other):
        return tuple(self.arr.flatten() == other.arr.flatten())

