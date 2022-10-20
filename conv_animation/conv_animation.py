from typing import Any
import sys
import os
sys.path.append(os.path.dirname(__file__))
import numpy as np
from convolution import convImage
from manim import *



class ConvAnim(MovingCameraScene):
    def construct(self) -> None:
        #self.camera.background_color = GRAY
        image_size = 5
        num_kernel = 3
        kernel_size = image_size/28 * num_kernel
        img_path = "../data/img.png"
        img, conved_img, conv = convImage(img_path)

        img_obj = ImageMobject(img_path)
        img_obj.height = image_size
        img_obj.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        
        # image solid
        img_square = Square(side_length=image_size)
        img_square.set_stroke(WHITE, width=1, opacity=0.5)

        # image hlines
        img_hlines = []
        line = Line()
        for i in range(28-1):
            img_hlines.append(line.copy())
            img_hlines[i].set_stroke(WHITE, width=1, opacity=0.5)
            img_hlines[i].set_length(image_size)
            img_hlines[i].shift(image_size/2*UP + image_size/28*(i+1)*DOWN)
        img_hlines = VGroup(*img_hlines)

        # image vlines
        img_vlines = []
        line.put_start_and_end_on(UP, DOWN)
        for i in range(28-1):
            img_vlines.append(line.copy())
            img_vlines[i].set_stroke(WHITE, width=1, opacity=0.5)
            img_vlines[i].set_length(image_size)
            img_vlines[i].shift(image_size/2*LEFT + image_size/28*(i+1)*RIGHT)
        img_vlines = VGroup(*img_vlines)

        # kernel on image
        kernel_on_img = Square(side_length=kernel_size)
        kernel_on_img.set_stroke(RED, width=2)
        kernel_on_img.shift(image_size/2*LEFT - kernel_size/2*LEFT)
        kernel_on_img.shift(image_size/2*UP - kernel_size/2*UP)

        # kernel
        kernel = Square(side_length=kernel_size)
        kernel.set_stroke(RED, width=2)
        kernel.shift(image_size/2*LEFT - kernel_size/2*LEFT)
        kernel.shift(image_size/2*UP + kernel_size*UP)

        # kernel lines
        kernel_lines = []
        line = Line()
        for i in range(num_kernel-1):
            kernel_lines.append(line.copy())
            kernel_lines[i].set_stroke(RED, width=2)
            kernel_lines[i].set_length(kernel_size)
            kernel_lines[i].shift(image_size/2*LEFT - kernel_size/2*LEFT)
            kernel_lines[i].shift(image_size/2*UP + kernel_size*1.5*UP + image_size/28*(i+1)*DOWN)
        line.put_start_and_end_on(UP, DOWN)
        for i in range(num_kernel-1):
            kernel_lines.append(line.copy())
            kernel_lines[num_kernel-1+i].set_stroke(RED, width=2)
            kernel_lines[num_kernel-1+i].set_length(kernel_size)
            kernel_lines[num_kernel-1+i].shift(image_size/2*LEFT + image_size/28*(i+1)*RIGHT)
            kernel_lines[num_kernel-1+i].shift(image_size/2*UP + kernel_size*UP)
        kernel_lines = VGroup(*kernel_lines)

        # kernel text on image
        kernel_text_on_img = []
        for i in range(num_kernel*num_kernel):
            tex = f"w_{{{i}}}"
            text = MathTex(tex, font_size=12)
            text.shift(image_size/2*LEFT + image_size/28/2*RIGHT + image_size/28*(i%3)*RIGHT)
            text.shift(image_size/2*UP + kernel_size*UP + image_size/28*UP + image_size/28*(i//3)*DOWN)
            kernel_text_on_img.append(text)
        kernel_text_on_img = VGroup(*kernel_text_on_img)

        # kernel text
        kernel_text = []
        for i in range(num_kernel*num_kernel):
            tex = f"x_{{{i}}}"
            text = MathTex(tex, font_size=12)
            text.shift(image_size/2*LEFT + image_size/28/2*RIGHT + image_size/28*(i%3)*RIGHT)
            text.shift(image_size/2*UP + image_size/28/2*DOWN + image_size/28*(i//3)*DOWN)
            kernel_text.append(text)
        kernel_text = VGroup(*kernel_text)

        # show
        self.add(img_obj)
        self.play(Create(img_square), Create(img_hlines), Create(img_vlines))
        self.play(FadeIn(kernel_on_img), FadeIn(kernel), FadeIn(kernel_lines))

        self.play(self.camera.frame.animate.move_to(kernel_on_img))
        self.play(self.camera.frame.animate.set(width=kernel_on_img.width*10))

        self.play(Write(kernel_text_on_img), Write(kernel_text))
