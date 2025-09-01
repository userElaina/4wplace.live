import tkinter as tk
from PIL import Image, ImageTk

DEFAULT_ALPHA = 0.4
MIN_ALPHA = 0.05
MAX_ALPHA = 1.0
STEP_ALPHA = 0.05

MARGIN = 0

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020


class FloatImageApp:
    def __init__(self, path):
        self.root = tk.Tk()
        self.root.title('Elysia')
        # self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.alpha = DEFAULT_ALPHA
        self.root.attributes('-alpha', self.alpha)

        self.bg = tk.Frame(self.root, bg='#111111')
        self.bg.pack(fill='both', expand=True)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label='T', command=self.toggle_click_through)
        self.menu.add_separator()
        self.menu.add_command(label='EXIT', command=self.root.destroy)

        self._img_path = path
        self._pil_img = None
        self._photo = None
        self._canvas = tk.Canvas(
            self.bg, highlightthickness=0, bg='#000000', cursor='fleur'
        )
        self._canvas.pack(
            fill='both', expand=True, padx=MARGIN, pady=MARGIN
        )

        img = Image.open(path).convert('RGBA')
        # 4k; 81x87; Windows paint Fullscreen
        w, h = 324, 348
        l, t = 5, 125
        img = img.resize((w, h), Image.LANCZOS)
        self._pil_img = img
        self._photo = ImageTk.PhotoImage(img)
        self._canvas.config(width=w, height=h)

        self.root.geometry(
            f'{w + MARGIN*2}x{h + MARGIN*2}+{l}+{t}'
        )
        self._canvas.delete('all')
        self._canvas.create_image(0, 0, image=self._photo, anchor='nw')

        self._offset = (0, 0)
        for w in (self.bg, self._canvas):
            w.bind('<Button-1>', self._start_move)
            # w.bind('<B1-Motion>', self._do_move)
        self.root.bind('<Key-t>', self.toggle_click_through)
        self.root.bind('<MouseWheel>', self._wheel_alpha)

        self._click_through = False

    def toggle_click_through(self, event=None):
        print('toggle_click_through', not self._click_through)
        self.set_click_through(not self._click_through)

    def set_click_through(self, enable: bool):
        import sys
        if not sys.platform.startswith('win'):
            return
        import ctypes
        from ctypes import windll, wintypes
        hWnd = ctypes.windll.user32.GetParent(
            self.root.winfo_id()
        ) or self.root.winfo_id()
        style = windll.user32.GetWindowLongW(hWnd, GWL_EXSTYLE)
        if enable:
            dwNewLong = style | WS_EX_LAYERED | WS_EX_TRANSPARENT
        else:
            dwNewLong = style & ~WS_EX_TRANSPARENT | WS_EX_LAYERED
        windll.user32.SetWindowLongW(hWnd, GWL_EXSTYLE, dwNewLong)
        self._click_through = enable

    def _start_move(self, e):
        self._offset = (
            e.x_root - self.root.winfo_x(),
            e.y_root - self.root.winfo_y()
        )

    # def _do_move(self, e):
    #     x = e.x_root - self._offset[0]
    #     y = e.y_root - self._offset[1]
    #     self.root.geometry(f'+{x}+{y}')

    def _wheel_alpha(self, e):
        delta = STEP_ALPHA if e.delta > 0 else -STEP_ALPHA
        self.alpha = max(MIN_ALPHA, min(MAX_ALPHA, self.alpha + delta))
        self.root.attributes('-alpha', self.alpha)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    path = '1.png'
    app = FloatImageApp(path)
    app.run()
