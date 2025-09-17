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
This is out of my comfort zone as most projects I have been involved in have been well-defined with specific inputs and outputs, and, due to this project's open-endedness,
I have had to make many more design choices.
The generality made it somewhat abstract and difficult to implement without knowing exact inputs.
However, the generality of my code allows me to reuse code in future projects, and also helps me understand how different parameters of the Markov chain may be changed, ultimately leading to a better understanding of Markov chains in general.
Thus, it was an important challenge that built up my ability to handle real-world problems which are often open-ended.
My next steps for this project include implementing more patterns for iteration, particularly those that preserve local features of the image.
I'd also like to experiment with more types of images and parameters to see how they affect the output.

I believe that, in this state, my project would not be considered computationally creative. The most 'different' 
an output gets is merely noise with the color palette of the original image, which I would not consider of value. 
At its most similar, the output is a recreation of the original image, which fails the novelty criterion.
Where there is some room for debate is in 'unfaithful recreations' of the original image, such as forgotten_beemovie_row.jpg.
I argue that it is novel since one would not accept it as an alternative to the orignal image and is thus a difference in kind.
However, I find the artistic value limited in this case as it lacks intentionality.

## Image sources
- [Athletic Bear](https://www.bowdoin.edu/communications/images/styleguide_athletic_bear.jpg)
- [Bee Movie](https://www.rottentomatoes.com/m/bee_movie)
- Garkov: Canvas page