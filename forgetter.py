import PIL.Image

from util import MarkovChain, BlockIterator
from PIL import Image
import numpy as np

class Forgetter:
    def __init__(self, image_path, **kwargs):
        """
        Initialize the Forgetter with an image and Markov Chain parameters.

        :param image_path:
        :param kwargs: a dictionary of parameters for the markov chain.
        """
        self.image = Image.open(image_path)
        self.image = Image.new("RGB", (10, 10))
        self.block_size = kwargs.get('block_size', 1)
        if self.image.size[0] % self.block_size != 0 or self.image.size[1] % self.block_size != 0:
            closest_dims = (self.image.size[0] - self.image.size[0] % self.block_size,
                            self.image.size[1] - self.image.size[1] % self.block_size)
            self.image = self.image.resize(closest_dims)
        self.forgetting_rate = kwargs.pop('forgetting_rate', 0.2)
        self.iterator = []
        self.image = np.asarray(self.image)
        self.load_markov_chain(**kwargs)

    def load_markov_chain(self, **kwargs):
        self.markov_chain = MarkovChain(kwargs.pop('pad', True), kwargs.pop('order', 1))
        self.arrangement = kwargs['arrangement']
        if not self.iterator:
            self.get_iterator()
        sequence = []
        for start in self.iterator:
            print(start)
            a, b, c, d = start[0], start[0] + self.block_size, start[1], start[1] + self.block_size
            sequence.append(self.image[a:b, c:d, ...].copy())
        self.markov_chain.learn([sequence])

    def get_iterator(self):
        if self.arrangement == 'row_left':
            self.iterator = BlockIterator(self.image.shape, self.block_size, axis=0, continue_from_end=True)
        elif self.arrangement == 'row_right':
            self.iterator = BlockIterator(self.image.shape, -self.block_size, axis=0, continue_from_end=True)
        elif self.arrangement == 'col_up':
            self.iterator = BlockIterator(self.image.shape, -self.block_size, axis=1, continue_from_end=True)
        elif self.arrangement == 'col_down':
            self.iterator = BlockIterator(self.image.shape, self.block_size, axis=1, continue_from_end=True)
        elif self.arrangement == 'zigzag':
            self.iterator = BlockIterator(self.image.shape, self.block_size, axis=0, continue_from_end='zigzag')
        else:
            raise ValueError(f"Unknown arrangement: {self.arrangement}")


    def forget(self):
        blocks = self.markov_chain.generate_sequence(self.image.shape[0] * self.image.shape[1] // self.block_size)
        for i, block in enumerate(self.iterator):
            a, b, c, d = block[0], block[0] + self.block_size, block[1], block[1] + self.block_size
            print(self.image.shape)
            self.image[a:b, c:d, ...] = blocks[i]
            print(self.image.shape)
            PIL.Image.fromarray(self.image).show()


def test_forgetter():
    forgetter = Forgetter('test/garkov_2.png', order=6, arrangement='row_left', block_size=5)
    forgetter.forget()

if __name__ == "__main__":
    test_forgetter()
