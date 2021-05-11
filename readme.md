# IMGToText

## Black and white image to text converter

This application is a simple application using pygame that allows the creation of small clipboard text in braille that will display the black and white image, but in text form.

## Getting Started

To run the project:

1. Ensure you are using Python 3.5+
2. Download the following libraries: Pygame, NumPy and Pandas
3. Run main.py

### Prerequisites

Python 3.5+, Pygame, NumPy and Pandas.

## Using the Application

The application does not display what keys/mouse buttons work.

- Press/Hold MOUSE1 (left mouse) to draw pixels.
- Press/Hold MOUSE2 (right mouse) to delete pixels.
- Press and release 'e' to copy the drawing to clipboard.
- Press and release 'r' to clear the drawing.
- Press and release 'a' to decrease the stroke width (minimum is 1).
- Press and release 'w' to increase the stroke width.
- Press and release 's' to toggle between rectangle drawing mode and circular drawing modes
- Press and release 'm' to zoom in.
- Press and release 'n' to zoom out.

Note that the internal resolution cannot be changed while the program is running - it can only be changed pre-compilation.
The default resolution is set to (120 x 120) pixels.
