# Mozaik

Create PowerPoint presentations programmatically based on the grid-based layout with Python.

```python
from mozaik import Slide, Presentation

slide1 = Slide(
    """
    ab
    ac
    """,
    title="An awesome slide",
)
slide1["a"].set_picture("tabby.jpg", size_mode="stretch")
slide1["b"].set_picture("dog.jpg")
slide1["c"].set_text(
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    "Etiam quis blandit justo. Duis eget tempor diam. Nullam"
    "luctus placerat felis sed aliquam."
)

slide2 = Slide(
    "🐶🐱",
    title="Another awesome slide",
)
slide2["🐶"].set_picture("dog.jpg", size_mode="fit")
slide2["🐱"].set_picture("tabby.jpg")  # default size_mode is 'cover'

presentation = Presentation(presentation_width=10, presentation_height=7.5)
presentation.add_slide(slide1)
presentation.add_slide(slide2)
presentation.save("test.pptx")
```

This package is highly opinionated with very limited customizability for the sake of consistency.
If you need more freedom, this might be not for you.

- [x] Mosaic grid layout creation
- [ ] Markdown support for textboxes
- [ ] Custom object support