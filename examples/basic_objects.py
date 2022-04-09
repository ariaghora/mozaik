import sys

sys.path.append("../")

from mozaik import Presentation, Slide, presentation
from mozaik.objects.textbox_with_title import TextboxWithTitle

slide = Slide(
    """
    ba
    bc
    """,
    title="An awesome slide",
)
slide["a"].set_object(
    TextboxWithTitle(
        "Basic info",
        "A tabby is any domestic cat (Felis catus) with a distinctive 'M'-shaped marking on its forehead; stripes by its eyes and across its cheeks, along its back, and around its legs and tail",
    )
)
slide["c"].set_object(
    TextboxWithTitle(
        "History",
        "Well-known tabby cats include Think Think, one of two cats belonging to the President of Taiwan, Tsai Ing-wen. One of the first mass-produced stuffed toys, the Ithaca Kitty, was inspired by a grey tabby cat with seven toes on each front foot.",
    )
)
slide["b"].set_picture("tabby.jpg")

presentation = Presentation(presentation_width=10, presentation_height=7.5)
presentation.add_slide(slide)
presentation.save("test.pptx")
