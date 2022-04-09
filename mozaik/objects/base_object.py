from __future__ import annotations
from abc import ABCMeta, abstractmethod
from pptx.slide import SlideShapes

import mozaik.slide


class BaseObject:
    @abstractmethod
    def attach(cls, slide: SlideShapes, rect: mozaik.slide.Rect) -> None:
        raise NotImplementedError()
