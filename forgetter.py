"""
Name: Richard Lim
Course: CSCI 3725
Assignment: M1
Date: 09-16-2025
Description: An image forgetter that uses a Markov Chain to iteratively replace blocks of the image.
Bugs: None known
"""

import argparse
import cv2
from util import MarkovChain, BlockIterator, Block
import os


class Forgetter:
    """
    An image forgetter that uses a Markov Chain to iteratively replace blocks of the image.
    """
    def __init__(self, image_path, **kwargs):
        """
        Initialize the Forgetter with an image and Markov Chain parameters.

        Args:
            image_path: str: Path to the input image.
            **kwargs: {
                'order': int: Order of the Markov Chain.
                'arrangement': str: Arrangement pattern: 'row', 'random'.
                'block_size': int: Size of the blocks to replace.
            }
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
        """
        Loads or initializes the Markov Chain with the given parameters.
        Args:
            **kwargs: see __init__ for details.

        """
        self.markov_chain = MarkovChain(order=kwargs.pop('order', 1))
        self.arrangement = kwargs['arrangement']
        if not self.iterator:
            self.get_iterator()
        self.update_markov_chain()

    def update_markov_chain(self):
        """
        Updates the Markov Chain with the current image blocks.
        """
        sequence = []
        for start in self.iterator.copy():
            a, b, c, d = start[0], start[0] + self.block_size, start[1], start[1] + self.block_size
            block = Block((self.image[a:b, c:d, ...].copy()))
            sequence.append(block)
        self.markov_chain.learn([sequence])

    def get_iterator(self):
        """
        Initializes the BlockIterator based on the arrangement pattern.
        """
        if self.arrangement == 'row':
            self.iterator = BlockIterator(self.image.shape, self.block_size)
        elif self.arrangement == 'random':
            self.iterator = BlockIterator(self.image.shape, self.block_size, pattern='random')
        else:
            raise ValueError(f"Unknown arrangement: {self.arrangement}")


    def forget(self, show=False):
        """
        Iteratively replaces blocks of the image using the Markov Chain.
        """
        for i, corner in enumerate(self.iterator.copy()):
            a, b, c, d = corner[0], corner[0] + self.block_size, corner[1], corner[1] + self.block_size
            block = self.markov_chain.generate_next()
            self.image[a:b, c:d, ...] = block.arr
            if show:
                cv2.imshow('image', self.image)
                cv2.waitKey(1)

    def save_image(self, path):
        """
        Saves the current image to the specified path.
        """
        cv2.imwrite(path, self.image)
        # log the parameters used to generate the image in a .log file
        with open(path + '.log', 'w') as f:
            f.write(f"block_size: {self.block_size}\n")
            f.write(f"arrangement: {self.arrangement}\n")
            f.write(f"order: {self.markov_chain.order}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default='test/garkov_2.png', help='Path to the input image.')
    parser.add_argument('--order', type=int, default=5, help='Order of the Markov Chain.')
    parser.add_argument('--arrangement', type=str, default='left', help='Arrangement pattern: row, random.')
    parser.add_argument('--block_size', type=int, default=5, help='Size of the blocks to replace.')
    parser.add_argument('--save', action='store_true', help='Save the examples image.')
    parser.add_argument('--show', action='store_true', help='Show animation of the regeneration.')
    args = parser.parse_args()

    forgetter = Forgetter(args.image_path, order=args.order, arrangement=args.arrangement, block_size=args.block_size)
    forgetter.forget(args.show)

    if args.save:
        forgetter.save_image('examples/forgotten_' + os.path.basename(args.image_path))