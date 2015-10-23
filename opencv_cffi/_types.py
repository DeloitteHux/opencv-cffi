from characteristic import Attribute, attributes

from _opencv import ffi, lib


@attributes(
    [
        Attribute(name="_cv_seq"),
        Attribute(name="type"),
    ],
)
class Sequence(object):
    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError(index)
        return self.type.from_chars(lib.cvGetSeqElem(self._cv_seq, index))

    def __len__(self):
        return self._cv_seq.total


@attributes(
    [
        Attribute(name="_cv_rect"),
    ],
)
class Rectangle(object):
    @classmethod
    def from_chars(cls, chars):
        return cls(cv_rect=ffi.cast("CvRect *", chars))

    def draw_onto(self, frame):
        lib.cvRectangle(
            frame,
            self.top_left,
            self.bottom_right,
            lib.cvScalar(255, 0, 0, 0),
            1,
            8,
            0,
        )

    @property
    def top_left(self):
        return self.x, self.y

    @property
    def bottom_right(self):
        return self.x + self.width, self.y + self.height

    @property
    def width(self):
        return self._cv_rect.width

    @property
    def height(self):
        return self._cv_rect.height

    @property
    def x(self):
        return self._cv_rect.x

    @property
    def y(self):
        return self._cv_rect.y