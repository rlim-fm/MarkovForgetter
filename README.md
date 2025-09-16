# MarkovForgetter
`MarkovForgetter` is a Python-based image generation project
that uses Markov chains to .
This project is a loose model of working (short-term) memory in the human brain, since
it often relies on constant effort to retain information.

## Dependencies
- Python 3.x
- NumPy
- OpenCV-Python

## Usage
The project can be run from the command line.
```bash
python forgetter.py --image_path <image_path> --order <order> --arrangement <arrangement> --block_size <block_size>
```
### Parameters
- `--image_path`: Path to the input image file.
- `--order`: Order of the Markov chain (default is 1).
- `--arrangement`: Order in which the markov chain processes the image
- `--block_size`: Size of the blocks to divide the image into.

