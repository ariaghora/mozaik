from __future__ import annotations

from typing import Any, Dict, List, Optional

from pptx.util import Inches


def _check_bounds_validity(bounds: List[Rect]) -> None:
    for bound in bounds:
        if bound.width < 1 or bound.height < 1:
            raise ValueError(f"Invalid bounds: {bound}")

    # check if all bounds are not intersecting
    for bound in bounds:
        for other_bound in bounds:
            if bound == other_bound:
                continue
            if (
                bound.left < other_bound.left
                and bound.top < other_bound.top
                and bound.left + bound.width > other_bound.left
                and bound.top + bound.height > other_bound.top
            ):
                raise Exception(
                    f"Intersecting bounds detected: {bound.char} and {other_bound.char}"
                )


class Rect:
    """
    This class represents a rectangle on the slide, defining its position, size, and
    content in the slide.
    """

    def __init__(
        self,
        char: str,
        left: float,
        top: float,
        width: float,
        height: float,
        left_margin: float = 0.1,
        top_margin: float = 0.1,
        right_margin: float = 0.1,
        bottom_margin: float = 0.1,
    ) -> None:
        self.char = char
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.left_inch: float = None
        self.top_inch: float = None
        self.width_inch: float = None
        self.height_inch: float = None
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.right_margin = right_margin
        self.bottom_margin = bottom_margin

        self.content: Dict[str, Any] = {"type": None}

    def __repr__(self) -> str:
        return f"{self.char}: {self.left}, {self.top}, {self.width}, {self.height}"

    def calculate_inches(
        self,
        slide,
        presentation_width,
        slide_content_height,
        config,
    ) -> None:
        """
        Calculate the position and size of the rect in inches.
        """
        self.left_inch = self.left / slide.n_cols * presentation_width
        self.top_inch = self.top / slide.n_rows * slide_content_height
        self.width_inch = self.width / slide.n_cols * presentation_width
        self.height_inch = self.height / slide.n_rows * slide_content_height

        self.left_inch += config["slide_left_padding"]
        self.top_inch += config["slide_top_padding"]
        self.width_inch -= config["slide_left_padding"] + config["slide_right_padding"]
        self.height_inch -= config["slide_top_padding"] + config["slide_bottom_padding"]

        if slide.title:
            # shift top_inch by title height
            self.top_inch += config["slide_title_font_size"]
            self.top_inch += config["slide_title_top_margin"]
            self.top_inch += config["slide_title_bottom_margin"]

    def apply_margin(self) -> None:
        self.left_inch += self.left_margin
        self.top_inch += self.top_margin
        self.width_inch -= self.left_margin + self.right_margin
        self.height_inch -= self.top_margin + self.bottom_margin

    def set_picture(
        self,
        path: str,
        size_mode: str = "cover",
        picture_width: Optional[float] = None,
        picture_height: Optional[float] = None,
    ) -> None:
        self.content["type"] = "picture"
        self.content["picture_path"] = path
        self.content["picture_size_mode"] = size_mode
        self.content["picture_width"] = self.width_inch
        self.content["picture_height"] = self.height_inch
        if picture_width is not None:
            self.content["picture_width"] = picture_width
        if picture_height is not None:
            self.content["picture_height"] = picture_height

    def set_text(self, text: str) -> None:
        self.content["type"] = "text"
        self.content["text"] = text


class Slide:
    """
    This class represents the model of a slide.
    """

    def __init__(self, layout_mosaic: str, title: Optional[str] = None):
        self.layout_mosaic = layout_mosaic
        self.title = title
        self.rects: Dict[str, Rect] = dict()
        self.n_rows: int = None
        self.n_cols: int = None

        self._populate_rects()
        _check_bounds_validity(self.rects.values())

    def __getitem__(self, char: str) -> Rect:
        return self.rects[char]

    def _populate_rects(self) -> None:
        rows = [row.strip() for row in self.layout_mosaic.strip().split("\n")]
        self.n_rows = len(rows)
        self.n_cols = max([len(row) for row in rows])

        # Get unique non whitespace characters
        unique_chars = set(self.layout_mosaic.replace(" ", ""))
        if "\n" in unique_chars:
            unique_chars.remove("\n")

        for current_char in unique_chars:
            min_row_index = len(rows)
            max_row_index = 0
            min_col_index = len(rows[0])
            max_col_index = 0
            for row_index, row in enumerate(rows):
                # get index of current char
                for col_index, char in enumerate(row):
                    if char == current_char:
                        min_row_index = min(min_row_index, row_index)
                        max_row_index = max(max_row_index, row_index)
                        min_col_index = min(min_col_index, col_index)
                        max_col_index = max(max_col_index, col_index)

            self.rects[current_char] = Rect(
                current_char,
                min_col_index,
                min_row_index,
                max_col_index - min_col_index + 1,
                max_row_index - min_row_index + 1,
            )
