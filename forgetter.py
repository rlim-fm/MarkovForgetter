import argparse
import cv2
from util import MarkovChain, BlockIterator, Block


# Parameters
image_path = 'test/garkov_2.png'
order = 5
arrangement = 'row_left'  # Options: 'row_left', 'row_right' 'random'
block_size = 5


class Forgetter:
    """
    An image forgetter that uses a Markov Chain to iteratively replace blocks of the image.
    """
    def __init__(self, image_path, **kwargs):
        """
        Initialize the Forgetter with an image and Markov Chain parameters.

        :param image_path:
        :param kwargs: a dictionary of parameters for the markov chain.
        """
        self.image = cv2.imread(image_path)
        self.block_size = kwargs.get('block_size', 1)

        # Ensure image dimensions are divisible by block_size
        if self.image.shape[0] % self.block_size != 0 or self.image.shape[1] % self.block_size != 0:
            closest_dims = (self.image.shape[0] - self.image.shape[0] % self.block_size,
                            self.image.shape[1] - self.image.shape[1] % self.block_size)

            # If not divisible, rop to closest divisible dimensions
            self.image = self.image[:closest_dims[0], :closest_dims[1], ...]
        self.iterator = []
        self.load_markov_chain(**kwargs)

    def load_markov_chain(self, **kwargs):
        self.markov_chain = MarkovChain(kwargs.pop('pad', True), kwargs.pop('order', 1))
        self.arrangement = kwargs['arrangement']
        if not self.iterator:
            self.get_iterator()
        sequence = []
        for start in self.iterator.copy():
            a, b, c, d = start[0], start[0] + self.block_size, start[1], start[1] + self.block_size
            block = Block((self.image[a:b, c:d, ...].copy()))
            sequence.append(block)
        self.markov_chain.learn([sequence])

    def get_iterator(self):
        if self.arrangement == 'row_left':
            self.iterator = BlockIterator(self.image.shape, self.block_size, axis=0)
        elif self.arrangement == 'row_right':
            self.iterator = BlockIterator(self.image.shape, -self.block_size, axis=0)
        elif self.arrangement == 'col_up':
            self.iterator = BlockIterator(self.image.shape, -self.block_size, axis=1)
        elif self.arrangement == 'col_down':
            self.iterator = BlockIterator(self.image.shape, self.block_size, axis=1)
        elif self.arrangement == 'random':
            self.iterator = BlockIterator(self.image.shape, self.block_size, pattern='random')
        else:
            raise ValueError(f"Unknown arrangement: {self.arrangement}")


    def forget(self):
        for i, corner in enumerate(self.iterator.copy()):
            a, b, c, d = corner[0], corner[0] + self.block_size, corner[1], corner[1] + self.block_size
            block = self.markov_chain.generate_next()
            self.image[a:b, c:d, ...] = block.arr
            cv2.imshow('image', self.image)
            cv2.waitKey(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default='test/garkov_2.png', help='Path to the input image.')
    parser.add_argument('--order', type=int, default=5, help='Order of the Markov Chain.')
    parser.add_argument('--arrangement', type=str, default='row_left', help='Arrangement pattern: row_left, row_right, col_up, col_down, random.')
    parser.add_argument('--block_size', type=int, default=5, help='Size of the blocks to replace.')
    args = parser.parse_args()

    forgetter = Forgetter(args.image_path, order=args.order, arrangement=args.arrangement, block_size=args.block_size)
    forgetter.forget()