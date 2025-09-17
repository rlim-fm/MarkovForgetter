# MarkovForgetter
`MarkovForgetter` is a Python-based image generation project
that uses Markov chains to recreate images to simulate how an image might be
gradually 'forgotten.'


## Dependencies
- Python 3.x
- NumPy
- OpenCV-Python

## Usage
The project can be run from the command line.
```bash
python forgetter.py --image_path <image_path> --order <order> --arrangement <arrangement> --block_size <block_size> --save <save>
```
### Parameters
- `--image_path`: Path to the input image file.
- `--order`: Order of the Markov chain.
- `--arrangement`: Order in which the markov chain processes the image
- `--block_size`: Size of the blocks to divide the image into.
- `--save`: Whether to save the output images. Images will be saved in the `examples` directory.
- `--show`: Whether to display the output images.

## Discussion
As someone interested in cognitive science, I am interested in using computational modeling to study possible mechanisms of human cognition.
This project is a loose model of working (short-term) memory in the human brain, since it often relies on constant effort to retain information.
While not a perfect model, I hoped to use it to explore how probabilistic methods can be used to simulate memory processes.

In this project, I challenged myself by starting out with very general code (such as implementing a general Markov chain class) and then specializing it to this project.
This made it somewhat abstract and difficult to implement without knowing exact inputs.
However, the generality of my code allows me to reuse code in future projects, and also helps me understand how different parameters of the Markov chain may be changed, ultimately leading to a better understanding of Markov chains in general.
One challenge that I encountered was in

My next steps for this project include implementing more patterns for iteration, particularly those that preserve local features of the image.