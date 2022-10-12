from typing import Any
import sys
import os
sys.path.append(os.path.dirname(__file__))
import numpy as np
from convolution import convImage
from manim import *



class ConvAnim(MovingCameraScene):
    def construct(self) -> None:
        image_size = 5
        square_size = image_size/28 * 3
        img_path = "../data/img.png"
        img, conved_img, conv = convImage(img_path)

        img_obj = ImageMobject(img_path)
        img_obj.height = image_size
        img_obj.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])

        # image hlines
        hlines = []
        line = Line()
        for i in range(28-1):
            hlines.append(line.copy())
            hlines[i].set_stroke(WHITE, width=1, opacity=0.7)
            hlines[i].set_length(image_size)
            hlines[i].shift(image_size/2*UP + image_size/28*(i+1)*DOWN)
        hlines = VGroup(*hlines)

        # image vlines
        vlines = []
        line.put_start_and_end_on(UP, DOWN)
        for i in range(28-1):
            vlines.append(line.copy())
            vlines[i].set_stroke(WHITE, width=1, opacity=0.7)
            vlines[i].set_length(image_size)
            vlines[i].shift(image_size/2*LEFT + image_size/28*(i+1)*RIGHT)
        vlines = VGroup(*vlines)

        square = Square(side_length=square_size)
        square.set_stroke(RED, width=4)
        square.shift(image_size/2*LEFT - square_size/2*LEFT)
        square.shift(image_size/2*UP - square_size/2*UP)

        self.add(img_obj)
        self.play(Create(hlines))
        self.play(Create(vlines))
        self.play(FadeIn(square))
        self.play(self.camera.frame.animate.move_to(square))
        self.play(self.camera.frame.animate.set(width=square.width*5))
