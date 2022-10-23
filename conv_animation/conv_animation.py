from typing import Any

import numpy as np
from convolution import convImage
from manim import (
    BLACK,
    DOWN,
    LEFT,
    RED,
    RESAMPLING_ALGORITHMS,
    RIGHT,
    UP,
    WHITE,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    ImageMobject,
    Line,
    MathTex,
    MovingCameraScene,
    Square,
    Tex,
    Uncreate,
    VGroup,
    config,
)


def img_unNorm(img: Any) -> Any:
    if (img.dtype == np.float32) | (img.dtype == np.float64):
        img = (img - img.min()) / (img.max() - img.min())
        img *= 255
        img = img.astype(np.uint8)
    return img


class ConvAnim(MovingCameraScene):
    def construct(self) -> None:
        img_path = "../data/img.png"
        img, conved_img, kernel = convImage(img_path)
        img = img_unNorm(img[0])
        conved_img = img_unNorm(conved_img)
        kernel = img_unNorm(kernel.weight.detach().numpy()[0][0])

        img_obj_size = 5
        kernel_size = kernel.shape[0]
        img_size = img.shape[0]
        kernel_obj_size = img_obj_size / img_size * kernel_size

        img_obj = ImageMobject(img)
        img_obj.height = img_obj_size
        img_obj.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])

        # image square
        img_square = Square(side_length=img_obj_size)
        img_square.set_stroke(WHITE, width=1, opacity=0.5)

        # image hlines
        img_hlines = VGroup()
        line = Line()
        for i in range(img_size - 1):
            img_hlines.add(line.copy())
            img_hlines[i].set_stroke(WHITE, width=1, opacity=0.5)
            img_hlines[i].set_length(img_obj_size)
            img_hlines[i].shift(
                img_obj.get_edge_center(UP) + img_obj_size / img_size * (i + 1) * DOWN
            )

        # image vlines
        img_vlines = VGroup()
        line.put_start_and_end_on(UP, DOWN)
        for i in range(img_size - 1):
            img_vlines.add(line.copy())
            img_vlines[i].set_stroke(WHITE, width=1, opacity=0.5)
            img_vlines[i].set_length(img_obj_size)
            img_vlines[i].shift(
                img_obj.get_edge_center(LEFT) + img_obj_size / img_size * (i + 1) * RIGHT
            )

        # image name
        img_name = Tex("Input Image", font_size=18)
        img_name.set_color(WHITE)
        img_name.shift(img_obj.get_edge_center(UP) + 0.1 * UP)

        # kernel
        kernel_obj = ImageMobject(kernel)
        kernel_obj.height = kernel_obj_size
        kernel_obj.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        kernel_obj.shift(
            img_obj.get_corner(UP + LEFT) + kernel_obj_size / 2 * RIGHT + kernel_obj_size * UP
        )

        # kernel name
        kernel_name = MathTex("Kernel", font_size=18)
        kernel_name.set_color(RED)
        kernel_name.shift(kernel_obj.get_edge_center(UP) + 0.1 * UP)

        # kernel square
        kernel_square = Square(side_length=kernel_obj_size)
        kernel_square.set_stroke(RED, width=2)
        kernel_square.shift(kernel_obj.get_corner(UP + LEFT) + kernel_obj_size / 2 * (DOWN + RIGHT))

        # kernel square on image
        kernel_square_on_img = Square(side_length=kernel_obj_size)
        kernel_square_on_img.set_stroke(RED, width=2)
        kernel_square_on_img.shift(
            img_obj.get_corner(UP + LEFT) + kernel_obj_size / 2 * (DOWN + RIGHT)
        )

        # kernel lines
        kernel_lines = VGroup()
        line = Line()
        for i in range(kernel_size - 1):
            kernel_lines.add(line.copy())
            kernel_lines[i].set_stroke(RED, width=2)
            kernel_lines[i].set_length(kernel_obj_size)
            kernel_lines[i].shift(
                kernel_obj.get_edge_center(UP) + img_obj_size / img_size * (i + 1) * DOWN
            )
        line.put_start_and_end_on(UP, DOWN)
        for i in range(kernel_size - 1):
            kernel_lines.add(line.copy())
            kernel_lines[kernel_size - 1 + i].set_stroke(RED, width=2)
            kernel_lines[kernel_size - 1 + i].set_length(kernel_obj_size)
            kernel_lines[kernel_size - 1 + i].shift(
                kernel_obj.get_edge_center(LEFT) + img_obj_size / img_size * (i + 1) * RIGHT
            )

        # kernel text
        kernel_text_on_img = VGroup()
        for i in range(kernel_size * kernel_size):
            tex = f"w_{{{i}}}"
            text = MathTex(tex, font_size=12)
            text.set_color(BLACK if kernel[i // kernel_size][i % kernel_size] > 128 else WHITE)
            text.shift(
                kernel_square.get_corner(UP + LEFT) + img_obj_size / img_size / 2 * (DOWN + RIGHT)
            )
            text.shift(
                img_obj_size / img_size * (i % kernel_size) * RIGHT
                + img_obj_size / img_size * (i // kernel_size) * DOWN
            )
            kernel_text_on_img.add(text)

        # kernel text on image
        kernel_text = VGroup()
        for i in range(kernel_size * kernel_size):
            tex = f"x_{{{i}}}"
            text = MathTex(tex, font_size=12)
            text.set_color(BLACK if img[i // img_size][i % img_size] > 128 else WHITE)
            text.shift(
                kernel_square_on_img.get_corner(UP + LEFT)
                + img_obj_size / img_size / 2 * (DOWN + RIGHT)
            )
            text.shift(
                img_obj_size / img_size * (i % kernel_size) * RIGHT
                + img_obj_size / img_size * (i // kernel_size) * DOWN
            )
            kernel_text.add(text)

        # kernel connection
        kernel_connection1 = DashedLine(
            config.left_side, config.right_side, dash_length=0.9, dashed_ratio=0.5
        )
        kernel_connection1.set_stroke(RED, width=2)
        kernel_connection1.put_start_and_end_on(
            kernel_square.get_corner(DOWN + LEFT), kernel_square_on_img.get_corner(UP + LEFT)
        )
        kernel_connection2 = DashedLine(
            config.left_side, config.right_side, dash_length=0.9, dashed_ratio=0.5
        )
        kernel_connection2.set_stroke(RED, width=2)
        kernel_connection2.put_start_and_end_on(
            kernel_square.get_corner(DOWN + RIGHT), kernel_square_on_img.get_corner(UP + RIGHT)
        )

        # conved pixel
        conved_pixel_obj = ImageMobject(np.uint8([[conved_img[0][0][0][0]]]))
        conved_pixel_obj.height = img_obj_size / img_size
        conved_pixel_obj.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        conved_pixel_obj.shift(kernel_square.get_corner(RIGHT + DOWN) + kernel_obj_size * 2 * RIGHT)

        # conv equation
        tex = r"a_0w_0+a_1w_1+a_2w_2+\\a_3w_3+a_4w_4+a_5w_5+\\a_6w_6+a_7w_7+a_8w_8="
        conv_eq_text = MathTex(tex, font_size=12)
        conv_eq_text.shift(conved_pixel_obj.get_edge_center(UP) + img_obj_size / img_size * 2 * UP)

        # kernel detail
        kernel_detail1 = Line(
            kernel_square.get_corner(RIGHT + UP), conved_pixel_obj.get_corner(LEFT + UP)
        )
        kernel_detail1.set_stroke(RED, width=2)
        kernel_detail2 = Line(
            kernel_square_on_img.get_corner(RIGHT + DOWN), conved_pixel_obj.get_corner(LEFT + DOWN)
        )
        kernel_detail2.set_stroke(RED, width=2)

        # show
        self.add(img_obj)
        self.play(Create(img_name))
        # self.wait()
        self.play(Create(img_square), Create(img_hlines), Create(img_vlines))
        self.play(FadeIn(kernel_obj), FadeIn(kernel_square), FadeIn(kernel_lines))

        self.play(self.camera.frame.animate.scale(0.4).move_to(kernel_square_on_img))

        self.play(FadeIn(kernel_name))
        # self.wait()

        self.play(Create(kernel_connection1), Create(kernel_connection2))
        self.play(FadeIn(kernel_square_on_img))

        self.play(FadeIn(kernel_text_on_img), FadeIn(kernel_text))

        self.add(conved_pixel_obj)
        self.play(Create(kernel_detail1), Create(kernel_detail2), Create(conv_eq_text))
        # self.wait(2)

        self.play(
            Uncreate(kernel_name),
            Uncreate(conv_eq_text),
            Uncreate(kernel_text),
            Uncreate(kernel_text_on_img),
        )
        self.play(Uncreate(kernel_detail1), Uncreate(kernel_detail2))
        self.play(
            FadeOut(kernel_square_on_img),
            Uncreate(kernel_connection1),
            Uncreate(kernel_connection2),
            kernel_square.animate.shift(
                kernel_square_on_img.get_corner(UP + LEFT) - kernel_square.get_corner(UP + LEFT)
            ),
            kernel_lines.animate.shift(
                kernel_square_on_img.get_corner(UP + LEFT) - kernel_lines.get_corner(UP + LEFT)
            ),
            kernel_obj.animate.shift(
                kernel_square_on_img.get_corner(UP + LEFT) - kernel_obj.get_corner(UP + LEFT)
            ),
        )

        self.play(self.camera.frame.animate.scale(1 / 0.4).move_to(img_obj))

        self.play(
            conved_pixel_obj.animate.shift(
                img_square.get_corner(UP + RIGHT)
                - conved_pixel_obj.get_corner(UP + LEFT)
                + kernel_obj_size * RIGHT
                + img_obj_size / img_size * DOWN
            ),
        )

        kernel_detail1.put_start_and_end_on(
            kernel_square.get_corner(RIGHT + UP), conved_pixel_obj.get_corner(LEFT + UP)
        )
        kernel_detail2.put_start_and_end_on(
            kernel_square.get_corner(RIGHT + DOWN), conved_pixel_obj.get_corner(LEFT + DOWN)
        )

        self.play(Create(kernel_detail1), Create(kernel_detail2))
        self.wait()
