import sys

sys.path.append("../")

import matplotlib.pyplot as plt
import numpy as np

from mozaik import Presentation, Slide

table_data = [
    ["Name", "Age", "Job"],
    ["John", "25", "Programmer"],
    ["Jane", "24", "Designer"],
    ["Jack", "26", "Architect"],
    ["Jill", "27", "Scientist"],
    ["Joe", "28", "Engineer"],
]

# random sinusoidal data
x = np.linspace(0, 10, 100)
y = np.sin(x)
y2 = np.sin(x + 0.5)
plt.figure(figsize=(5, 2))
plt.plot(x, y)
plt.plot(x, y2)
plt.title("Sinusoidal data")
plt.savefig("sinusoidal.png", bbox_inches="tight")

slide = Slide(
    """
    aab
    cdd
    """,
    title="An awesome slide",
)
slide["a"].set_table(table_data, size_mode="stretch")
slide["b"].set_text("This is the description of the table in the left.")
slide["c"].set_text(
    "Look, we can also add an irrelevant figure on the right. "
    "Who cares about the table, we can add a picture or a text.",
    horizontal_alignment="right",
)
slide["d"].set_picture("sinusoidal.png", size_mode="fit")

presentation = Presentation(presentation_width=10, presentation_height=7.5)
presentation.add_slide(slide)
presentation.save("test.pptx")
