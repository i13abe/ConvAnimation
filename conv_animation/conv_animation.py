from typing import Any
import sys
import os
import numpy as np
from convolution import convImage
from manim import *


def img_unNorm(img: Any) -> Any:
    if (img.dtype == np.float32) | (img.dtype == np.float64):
        img = (img - img.min())/(img.max() - img.min())
        img *= 255
        img = img.astype(np.uint8)
    return img




class ConvAnim(MovingCameraScene):
    def construct(self) -> None:
        #self.camera.background_color = GRAY
        img_path = "../data/img.png"
        img, conved_img, kernel = convImage(img_path)
        img = img_unNorm(img[0])
        conved_img = img_unNorm(conved_img)
        kernel = img_unNorm(kernel.weight.detach().numpy()[0][0])

        img_obj_size = 5
        kernel_size = kernel.shape[0]
        img_size = img.shape[0]
        kernel_obj_size = img_obj_size/img_size * kernel_size

        img_obj = ImageMobject(img)
        img_obj.height = img_obj_size
        img_obj.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        
        # image square
        img_square = Square(side_length=img_obj_size)
        img_square.set_stroke(WHITE, width=1, opacity=0.5)

        # image hlines
        img_hlines = VGroup()
        line = Line()
        for i in range(img_size-1):
            img_hlines.add(line.copy())
            img_hlines[i].set_stroke(WHITE, width=1, opacity=0.5)
            img_hlines[i].set_length(img_obj_size)
            img_hlines[i].shift(img_obj_size/2*UP + img_obj_size/img_size*(i+1)*DOWN)

        # image vlines
        img_vlines = VGroup()
        line.put_start_and_end_on(UP, DOWN)
        for i in range(img_size-1):
            img_vlines.add(line.copy())
            img_vlines[i].set_stroke(WHITE, width=1, opacity=0.5)
            img_vlines[i].set_length(img_obj_size)
            img_vlines[i].shift(img_obj_size/2*LEFT + img_obj_size/img_size*(i+1)*RIGHT)

        # kernel name
        kernel_name = MathTex("Kernel", font_size=18)
        kernel_name.set_color(RED)
        kernel_name.shift(img_obj_size/2*LEFT + img_obj_size/img_size/2*RIGHT + img_obj_size/img_size*RIGHT)
        kernel_name.shift(img_obj_size/2*UP + kernel_obj_size*1.8*UP)

        # kernel
        kernel_obj = ImageMobject(kernel)
        kernel_obj.height = kernel_obj_size
        kernel_obj.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        kernel_obj.shift(img_obj_size/2*LEFT - kernel_obj_size/2*LEFT)
        kernel_obj.shift(img_obj_size/2*UP + kernel_obj_size*UP)

        # kernel square on image
        kernel_square_on_img = Square(side_length=kernel_obj_size)
        kernel_square_on_img.set_stroke(RED, width=2)
        kernel_square_on_img.shift(img_obj_size/2*LEFT - kernel_obj_size/2*LEFT)
        kernel_square_on_img.shift(img_obj_size/2*UP - kernel_obj_size/2*UP)

        # kernel square
        kernel_square = Square(side_length=kernel_obj_size)
        kernel_square.set_stroke(RED, width=2)
        kernel_square.shift(img_obj_size/2*LEFT - kernel_obj_size/2*LEFT)
        kernel_square.shift(img_obj_size/2*UP + kernel_obj_size*UP)

        # kernel lines
        kernel_lines = VGroup()
        line = Line()
        for i in range(kernel_size-1):
            kernel_lines.add(line.copy())
            kernel_lines[i].set_stroke(RED, width=2)
            kernel_lines[i].set_length(kernel_obj_size)
            kernel_lines[i].shift(img_obj_size/2*LEFT - kernel_obj_size/2*LEFT)
            kernel_lines[i].shift(img_obj_size/2*UP + kernel_obj_size*1.5*UP + img_obj_size/img_size*(i+1)*DOWN)
        line.put_start_and_end_on(UP, DOWN)
        for i in range(kernel_size-1):
            kernel_lines.add(line.copy())
            kernel_lines[kernel_size-1+i].set_stroke(RED, width=2)
            kernel_lines[kernel_size-1+i].set_length(kernel_obj_size)
            kernel_lines[kernel_size-1+i].shift(img_obj_size/2*LEFT + img_obj_size/img_size*(i+1)*RIGHT)
            kernel_lines[kernel_size-1+i].shift(img_obj_size/2*UP + kernel_obj_size*UP)

        # kernel text on image
        kernel_text_on_img = VGroup()
        for i in range(kernel_size*kernel_size):
            tex = f"w_{{{i}}}"
            text = MathTex(tex, font_size=12)
            text.set_color(BLACK if kernel[i//kernel_size][i%kernel_size]>128 else WHITE)
            text.shift(img_obj_size/2*LEFT + img_obj_size/img_size/2*RIGHT + img_obj_size/img_size*(i%kernel_size)*RIGHT)
            text.shift(img_obj_size/2*UP + kernel_obj_size*UP + img_obj_size/img_size*UP + img_obj_size/img_size*(i//kernel_size)*DOWN)
            kernel_text_on_img.add(text)

        # kernel text
        kernel_text = VGroup()
        for i in range(kernel_size*kernel_size):
            tex = f"x_{{{i}}}"
            text = MathTex(tex, font_size=12)
            text.set_color(BLACK if img[i//img_size][i%img_size]>128 else WHITE)
            text.shift(img_obj_size/2*LEFT + img_obj_size/img_size/2*RIGHT + img_obj_size/img_size*(i%kernel_size)*RIGHT)
            text.shift(img_obj_size/2*UP + img_obj_size/img_size/2*DOWN + img_obj_size/img_size*(i//kernel_size)*DOWN)
            kernel_text.add(text)

        # kernel connection
        kernel_connection = VGroup()
        dashedline = DashedLine(config.left_side, config.right_side, dash_length=0.9, dashed_ratio=0.5)
        dashedline.set_stroke(RED, width=2)
        dashedline.put_start_and_end_on(UP, DOWN)
        dashedline.set_length(kernel_obj_size)
        for i in range(2):
            kernel_connection.add(dashedline.copy())
            kernel_connection[i].shift(img_obj_size/2*LEFT + i*kernel_obj_size*RIGHT)
            kernel_connection[i].shift(img_obj_size/2*UP + kernel_obj_size//2*UP)
        
        # conved pixel
        conved_pixel_obj = ImageMobject(np.uint8([[conved_img[0][0][0][0]]]))
        conved_pixel_obj.height = img_obj_size/img_size
        corner = kernel_square.get_corner(RIGHT+DOWN)
        conved_pixel_obj.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        conved_pixel_obj.shift(corner+kernel_obj_size*2*RIGHT)

        # conv equation
        tex = r"a_0w_0+a_1w_1+a_2w_2+\\a_3w_3+a_4w_4+a_5w_5+\\a_6w_6+a_7w_7+a_8w_8="
        conv_eq_text = MathTex(tex, font_size=12)
        conv_eq_text.shift(conved_pixel_obj.get_edge_center(UP)+img_obj_size/img_size*2*UP)

        # kernel detail
        kernel_detail = VGroup()
        corner=kernel_square.get_corner(RIGHT+UP)
        line = Line(corner, conved_pixel_obj.get_corner(LEFT+UP))
        line.set_stroke(RED, width=2)
        kernel_detail.add(line)
        corner=kernel_square_on_img.get_corner(RIGHT+DOWN)
        line = Line(corner, conved_pixel_obj.get_corner(LEFT+DOWN))
        line.set_stroke(RED, width=2)
        kernel_detail.add(line)

        # show
        self.add(img_obj)
        self.wait()
        self.play(Create(img_square), Create(img_hlines), Create(img_vlines))
        self.play(FadeIn(kernel_obj), FadeIn(kernel_square), FadeIn(kernel_lines))

        self.play(self.camera.frame.animate.move_to(kernel_square_on_img))
        self.play(self.camera.frame.animate.set(width=kernel_square_on_img.width*10))

        self.play(FadeIn(kernel_name))
        self.wait()

        self.play(Create(kernel_connection))
        self.play(FadeIn(kernel_square_on_img))

        self.play(FadeIn(kernel_text_on_img), FadeIn(kernel_text))

        self.add(conved_pixel_obj)
        self.play(Create(kernel_detail), Write(conv_eq_text))
