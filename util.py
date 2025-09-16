import numpy as np
from typing import Literal
from itertools import chain

class MarkovChain:
    def __init__(self, pad=True, order=1):
        self.order = order
        self.transitions = {}
        self.states = set()
        self.pad = pad

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

    def get_next(self, current_state=None):
        if current_state is None:
            current_state = [None]*self.order
        next_states = self.probs.get(tuple(current_state), {})
        if not next_states:
            print(f"Warning: State following {current_state} not found. Choosing random state.")
            return np.random.choice(list(self.states))
        return np.random.choice(list(next_states.keys()), p=list(next_states.values()))

    def generate_sequence(self, start=None, length=10):
        if start is None:
            start = [None]*self.order
        current = list(start)
        sequence = list(current)
        for _ in range(length):
            next_state = None
            while next_state is None:
                next_state = self.get_next(current)
                sequence.append(next_state)
                current = sequence[-self.order:]
        sequence = [s for s in sequence if s is not None]
        return sequence

class BlockIterator:
    def __init__(self, shape, block_size=1, axis=0, continue_from_end: Literal[True, False, 'zigzag']=False, start=None):
        """
        Iterate over a 2D array in blocks along a specified axis.

        :param shape:
        :param start:
        :param block_size:
        :param axis:
        :param direction:
        :param continue_from_end:
        """

        self.shape = shape
        self.block_size = block_size
        if shape[0] % block_size != 0 or shape[1] % block_size != 0:
            raise ValueError("shape[0] and shape[1] must be divisible by block_size")
        if start is None:
            start = [0]*len(shape)
            if block_size < 0:
                start[axis] = shape[axis] - block_size
        self.curr = start
        self.axis = axis
        self.continue_from_end = continue_from_end

    def __iter__(self):
        if not self.continue_from_end:
            return self
        if self.continue_from_end == 'zigzag':
            self.curr[0 if self.axis == 1 else self.axis + 1] += self.block_size
            next_iter = BlockIterator(self.shape, -self.block_size, self.axis, 'zigzag', self.curr)
            return chain(self, next_iter)

        self.curr[0 if self.axis == 1 else self.axis + 1] += self.block_size
        next_iter = BlockIterator(self.shape, self.block_size, self.axis, True, self.curr)
        return chain(self, next_iter)

    def __next__(self):
        if self.curr[self.axis] + self.block_size>= self.shape[self.axis] and self.block_size > 0:
            raise StopIteration
        self.curr[self.axis] += self.block_size
        return self.curr.copy()

class RowColIterator(BlockIterator):
    def __init__(self, shape, start=None, block_size=1, axis=0, direction: Literal[1, -1]=1):
        """
        Iterate over rows of a 2D array in blocks.

        :param shape: shape of the array
        :param start: starting position
        :param block_size: size of each block
        :param axis: 0 for rows, 1 for columns
        :param direction: 1 for forward, -1 for backward
        """
        super().__init__(shape, start, block_size)
        self.axis = axis
        self.block_size = direction * self.block_size
        if start is None:
            self.curr[axis] = 0 if direction == 1 else shape[axis] - block_size

def test_markov_chain():
    test_file = 'test/mobydick.txt'
    with open(test_file, 'r') as f:
        sequence = []
        for line in f:
            sequence.extend(line.strip().split())
    mc = MarkovChain(order=6)
    mc.learn([sequence])
    print(" ".join(mc.generate_sequence(length=100)))

if __name__ == "__main__":
    from PIL import Image
    img = Image.new("RGB", (50, 100), color=(73, 109, 137))
    test_array = np.array(img)
    test_array[0, 0] = [255, 0, 0]
    test_array[0, 1] = [0, 255, 0]
    test_array[0, 2] = [0, 0, 255]
    test_array[1, 0] = [255, 255, 0]
