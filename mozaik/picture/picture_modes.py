from typing import Any

from pptx.util import Inches

from ..slide import Rect


def set_picture_stretch_mode(pic: Any, rect: Rect) -> None:
    """
    Set picture to stretch mode.
    """
    # First, store the gap between the picture and the rect.
    # The picture sizes are subtracted from the bounding box since
    # the rect sizes are guaranteed to be larger than the picture.
    dw = Inches(rect.width_inch) - pic.width
    dh = Inches(rect.height_inch) - pic.height
    # Then directly stretch the picture to the bounding box.
    pic.height += dh
    pic.width += dw


def set_picture_cover_mode(pic: Any, rect: Rect) -> None:
    """
    Set picture to cover mode.
    """
    # First, store the gap between the picture and the rect.
    # The picture sizes are subtracted from the bounding box since
    # the rect sizes are guaranteed to be larger than the picture.
    dw = Inches(rect.width_inch) - pic.width
    dh = Inches(rect.height_inch) - pic.height

    # Temporarily store current picture size to get the size before
    # gap filling.
    picture_width = pic.width
    picture_height = pic.height

    # fill the gap between the picture and the bounding box
    pic.height += dh
    pic.width += dw

    # Then fix the aspect ratio of the picture
    rect_pict_height_ratio = Inches(rect.height_inch) / picture_height
    rect_pict_width_ratio = Inches(rect.width_inch) / picture_width

    if pic.width < pic.height:
        pic.width = int(picture_width * rect_pict_height_ratio)
    elif pic.width > pic.height:
        pic.height = int(picture_height * rect_pict_width_ratio)

    # Get the difference between the picture and the bounding box.
    # Now since the picture will be larger than the bounding box,
    # the rect sizes will be subtracted from the picture sizes instead.
    new_dw = pic.width - Inches(rect.width_inch)
    new_dh = pic.height - Inches(rect.height_inch)

    # get ratio of the difference and the picture
    dw_ratio = new_dw / pic.width
    dh_ratio = new_dh / pic.height

    # Apply crop symmetrically
    pic.crop_left = dw_ratio / 2
    pic.crop_right = dw_ratio / 2
    pic.crop_top = dh_ratio / 2
    pic.crop_bottom = dh_ratio / 2

    # Readjust picture size with respect to the bounding box
    pic.height = Inches(rect.height_inch)
    pic.width = Inches(rect.width_inch)
