# silhucam

Python script for creating vector silhouettes from webcam images

## Requirements

 * [pygame](http://www.pygame.org/), Install with Pip (```pip install pygame```) or some other method
 * [Pillow](https://python-pillow.org/), Install with Pip (```pip install Pillow```) or some other method
 * [Potrace](http://potrace.sourceforge.net/), Install with package manager (```sudo apt-get install potrace```)
 * [Inkscape](https://inkscape.org/), Install with package manager (```sudo apt-get install inkscape```)

## Usage

Start the script after installing requirements with ```python cam.py```. ESC exits the script and ENTER or SPACE save currently displayed webcam image to disk, vectorize it with Potrace and open resulting SVG image in Inkscape.
