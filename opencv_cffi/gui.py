from characteristic import Attribute, attributes

from _opencv import lib


ESCAPE = "\x1b"
_KEYCODES_TO_NAMES = {
    62232 : "up",
    62233 : "down",
    62234 : "left",
    62235 : "right",
}


@attributes(
    [
        Attribute(name="name"),
        # TODO: Support sizing modes
    ],
)
class Window(object):
    """
    A GUI window.

    """

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        lib.cvDestroyWindow(self.name)

    def _show(self, image):
        lib.cvShowImage(self.name, image._cv_arr)

    def show_until_keypress(self, image, delay=None):
        self._show(image)
        keycode = lib.cvWaitKey(0)
        return _keycode_to_key(keycode)


    def loop_over(self, images, handle_input=lambda key : None, delay=25):
        for image in images:
            self._show(image)

            keycode = lib.cvWaitKey(delay)
            nothing_was_pressed = keycode == -1
            if nothing_was_pressed:
                continue

            handle_input(key=_keycode_to_key(keycode))


def _keycode_to_key(keycode):
    if 0 <= keycode <= 255:
        return chr(keycode)
    return _KEYCODES_TO_NAMES.get(keycode, keycode)
