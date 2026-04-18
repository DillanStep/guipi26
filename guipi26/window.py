# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 2026

@author: dillan stephenson
"""

from dataclasses import dataclass, field
import ctypes
from ctypes import wintypes
from typing import List, Optional, Tuple


user32 = ctypes.WinDLL("user32", use_last_error=True)
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

# WARNING (Yes, this is the bit you don’t casually fiddle with)
#
# The definitions below map Python ctypes to the Win32 API.
# In plain English: this is the low-level plumbing that keeps the window
# behaving like a window instead of a small, unpredictable disaster.
#
# You are not directly poking memory with a stick, but you are close enough
# that guessing values or “just trying something” may result in crashes,
# graphical chaos, or the application quietly giving up on life.
#
# If everything is currently working, consider that a success and proceed
# with caution. If you must make changes, do so with intent, understanding,
# and ideally a backup (or at least a mild sense of regret prepared in advance).
#
# For additional APIs and constants, refer to the official Microsoft Win32
# documentation and follow the patterns used below. Do not invent numbers.
#
# You have been warned. Carry on.

HANDLE = wintypes.HANDLE
LRESULT = ctypes.c_ssize_t
COLORREF = wintypes.DWORD
UINT_PTR = ctypes.c_size_t
HGDIOBJ = HANDLE
HINSTANCE = HANDLE
HICON = HANDLE
HCURSOR = HANDLE
HBRUSH = HANDLE
HDC = HANDLE
HFONT = HANDLE
HPEN = HANDLE
HBITMAP = HANDLE


CS_HREDRAW = 0x0002
CS_VREDRAW = 0x0001
CW_USEDEFAULT = -2147483648
DEFAULT_CHARSET = 1
DEFAULT_PITCH = 0
DT_CENTER = 0x00000001
DT_END_ELLIPSIS = 0x00008000
DT_LEFT = 0x00000000
DT_RIGHT = 0x00000002
DT_SINGLELINE = 0x00000020
DT_VCENTER = 0x00000004
FW_LIGHT = 300
FW_NORMAL = 400
IDC_ARROW = 32512
IDI_APPLICATION = 32512
LOGPIXELSY = 90
PS_SOLID = 0
SRCCOPY = 0x00CC0020
SW_SHOW = 5
TME_LEAVE = 0x00000002
TRANSPARENT = 1
WM_CLOSE = 0x0010
WM_DESTROY = 0x0002
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_MOUSELEAVE = 0x02A3
WM_MOUSEMOVE = 0x0200
WM_MOUSEWHEEL = 0x020A
WM_PAINT = 0x000F
WM_SETCURSOR = 0x0020
WM_SIZE = 0x0005
WM_CHAR = 0x0102
WM_KEYDOWN = 0x0100
WM_TIMER = 0x0113
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_VISIBLE = 0x10000000

VK_BACK = 0x08
VK_TAB = 0x09
VK_RETURN = 0x0D
VK_END = 0x23
VK_HOME = 0x24
VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28
VK_DELETE = 0x2E

# Cursor shape resource IDs (used with LoadCursorW(NULL, ...)).
IDC_HAND = 32649
IDC_IBEAM = 32513
IDC_SIZEWE = 32644

# MessageBox flag combinations
MB_OK = 0x00000000
MB_OKCANCEL = 0x00000001
MB_YESNO = 0x00000004
MB_YESNOCANCEL = 0x00000003
MB_ICONINFORMATION = 0x00000040
MB_ICONWARNING = 0x00000030
MB_ICONERROR = 0x00000010
MB_ICONQUESTION = 0x00000020
IDOK = 1
IDCANCEL = 2
IDYES = 6
IDNO = 7

# Accelerator modifier bitmask used by GUIpi26 accelerators.
MOD_CTRL = 0x01
MOD_SHIFT = 0x02
MOD_ALT = 0x04

# Tooltip + caret blink timer IDs.
TIMER_TOOLTIP = 0x701
TIMER_CARET = 0x702
TOOLTIP_DELAY_MS = 500
CARET_BLINK_MS = 530


def _rgb_to_colorref(color):
    color = color.lstrip("#")
    if len(color) != 6:
        raise ValueError("Color values must use #RRGGBB format.")

    red = int(color[0:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)
    return red | (green << 8) | (blue << 16)


def _hex_to_rgb(color):
    color = color.lstrip("#")
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def _rgb_to_hex(red, green, blue):
    return f"#{red:02x}{green:02x}{blue:02x}"


def _blend(color_a, color_b, progress):
    progress = max(0.0, min(1.0, progress))
    red_a, green_a, blue_a = _hex_to_rgb(color_a)
    red_b, green_b, blue_b = _hex_to_rgb(color_b)
    red = int(red_a + (red_b - red_a) * progress)
    green = int(green_a + (green_b - green_a) * progress)
    blue = int(blue_a + (blue_b - blue_a) * progress)
    return _rgb_to_hex(red, green, blue)


def _get_x_lparam(value):
    return ctypes.c_short(value & 0xFFFF).value


def _get_y_lparam(value):
    return ctypes.c_short((value >> 16) & 0xFFFF).value


def _make_int_resource(value):
    return ctypes.cast(ctypes.c_void_p(value), wintypes.LPCWSTR)


def _rect_contains(left, top, right, bottom, x_pos, y_pos):
    return left <= x_pos <= right and top <= y_pos <= bottom


WNDPROC = ctypes.WINFUNCTYPE(
    LRESULT,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)


class WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]


class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", POINT),
        ("lPrivate", wintypes.DWORD),
    ]


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hdc", HDC),
        ("fErase", wintypes.BOOL),
        ("rcPaint", RECT),
        ("fRestore", wintypes.BOOL),
        ("fIncUpdate", wintypes.BOOL),
        ("rgbReserved", ctypes.c_byte * 32),
    ]


class TRACKMOUSEEVENT(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("hwndTrack", wintypes.HWND),
        ("dwHoverTime", wintypes.DWORD),
    ]


class SIZE(ctypes.Structure):
    _fields_ = [("cx", wintypes.LONG), ("cy", wintypes.LONG)]

# -------------------------------------------------------------------------
# WARNING: HERE BE DRAGONS (AND BY DRAGONS, WE MEAN THE WINDOWS API)
#
# The declarations below define argument and return types for a selection
# of Win32 functions using ctypes. This is the layer where Python politely
# asks Windows to do something, and Windows either complies… or immediately
# falls over if we’ve asked incorrectly (partly becuase micrsoft forgot how to
# make a decent os since xp)
#
# In essence, this is the contract between your code and the operating system.
# If the types match what Windows expects, everything behaves. If they do not,
# you may experience crashes, graphical nonsense, input issues, or the sort of
# bugs that make you question your life choices.
#
# A few important points for the brave:
#
# - These are not arbitrary definitions. Every type and parameter order must
#   match the official Win32 API exactly.
# - “Close enough” is not a thing here. It either is correct, or it is broken.
# - If something stops working after a change, this is an excellent place to
#   start looking (after a cup of tea and a quiet moment).
#
# Functions covered here include:
#   - Window creation and lifecycle (CreateWindowExW, DestroyWindow, ShowWindow)
#   - Message loop handling (GetMessageW, DispatchMessageW, TranslateMessage)
#   - Input and events (mouse, keyboard, timers)
#   - Drawing and rendering (BeginPaint, EndPaint, DrawTextW, BitBlt)
#   - GDI objects (fonts, brushes, pens, bitmaps)
#
# If you need to extend this:
#   1. Look up the function in the official Microsoft Win32 documentation
#   2. Copy the exact signature
#   3. Map types carefully using ctypes/wintypes
#   4. Do not improvise numbers or guess parameters
#
# If everything is working:
#   Consider leaving this section entirely alone.
#
# If you absolutely must change it:
#   Do so with intent, understanding, and ideally version control.
#
# You have been warned. Carry on.
# -------------------------------------------------------------------------

user32.BeginPaint.argtypes = [wintypes.HWND, ctypes.POINTER(PAINTSTRUCT)]
user32.BeginPaint.restype = HDC
user32.CreateWindowExW.argtypes = [
    wintypes.DWORD,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.HWND,
    wintypes.HMENU,
    HINSTANCE,
    wintypes.LPVOID,
]
user32.CreateWindowExW.restype = wintypes.HWND
user32.DefWindowProcW.argtypes = [
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
]
user32.DefWindowProcW.restype = LRESULT
user32.DestroyWindow.argtypes = [wintypes.HWND]
user32.DestroyWindow.restype = wintypes.BOOL
user32.DispatchMessageW.argtypes = [ctypes.POINTER(MSG)]
user32.DispatchMessageW.restype = LRESULT
user32.DrawTextW.argtypes = [HDC, wintypes.LPCWSTR, ctypes.c_int, ctypes.POINTER(RECT), wintypes.UINT]
user32.DrawTextW.restype = ctypes.c_int
user32.EndPaint.argtypes = [wintypes.HWND, ctypes.POINTER(PAINTSTRUCT)]
user32.EndPaint.restype = wintypes.BOOL
user32.FillRect.argtypes = [HDC, ctypes.POINTER(RECT), HBRUSH]
user32.FillRect.restype = ctypes.c_int
user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(RECT)]
user32.GetClientRect.restype = wintypes.BOOL
user32.GetDC.argtypes = [wintypes.HWND]
user32.GetDC.restype = HDC
user32.GetMessageW.argtypes = [ctypes.POINTER(MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
user32.GetMessageW.restype = wintypes.BOOL
user32.MessageBoxW.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT]
user32.MessageBoxW.restype = ctypes.c_int
user32.SetCursor.argtypes = [HCURSOR]
user32.SetCursor.restype = HCURSOR
user32.GetKeyState.argtypes = [ctypes.c_int]
user32.GetKeyState.restype = ctypes.c_short
kernel32.GetTickCount.restype = wintypes.DWORD
kernel32.GetTickCount.argtypes = []
user32.InvalidateRect.argtypes = [wintypes.HWND, ctypes.POINTER(RECT), wintypes.BOOL]
user32.InvalidateRect.restype = wintypes.BOOL
user32.IsWindow.argtypes = [wintypes.HWND]
user32.IsWindow.restype = wintypes.BOOL
user32.KillTimer.argtypes = [wintypes.HWND, UINT_PTR]
user32.KillTimer.restype = wintypes.BOOL
user32.LoadCursorW.argtypes = [HINSTANCE, wintypes.LPCWSTR]
user32.LoadCursorW.restype = HCURSOR
user32.LoadIconW.argtypes = [HINSTANCE, wintypes.LPCWSTR]
user32.LoadIconW.restype = HICON
user32.PostQuitMessage.argtypes = [ctypes.c_int]
user32.PostQuitMessage.restype = None
user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSW)]
user32.RegisterClassW.restype = wintypes.ATOM
user32.ReleaseDC.argtypes = [wintypes.HWND, HDC]
user32.ReleaseDC.restype = ctypes.c_int
user32.SetTimer.argtypes = [wintypes.HWND, UINT_PTR, wintypes.UINT, wintypes.LPVOID]
user32.SetTimer.restype = UINT_PTR
user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
user32.ShowWindow.restype = wintypes.BOOL
user32.TrackMouseEvent.argtypes = [ctypes.POINTER(TRACKMOUSEEVENT)]
user32.TrackMouseEvent.restype = wintypes.BOOL
user32.TranslateMessage.argtypes = [ctypes.POINTER(MSG)]
user32.TranslateMessage.restype = wintypes.BOOL
user32.UpdateWindow.argtypes = [wintypes.HWND]
user32.UpdateWindow.restype = wintypes.BOOL
gdi32.BitBlt.argtypes = [HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, HDC, ctypes.c_int, ctypes.c_int, wintypes.DWORD]
gdi32.BitBlt.restype = wintypes.BOOL
gdi32.CreateCompatibleBitmap.argtypes = [HDC, ctypes.c_int, ctypes.c_int]
gdi32.CreateCompatibleBitmap.restype = HBITMAP
gdi32.CreateCompatibleDC.argtypes = [HDC]
gdi32.CreateCompatibleDC.restype = HDC
gdi32.CreateFontW.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.LPCWSTR,
]
gdi32.CreateFontW.restype = HFONT
gdi32.CreatePen.argtypes = [ctypes.c_int, ctypes.c_int, COLORREF]
gdi32.CreatePen.restype = HPEN
gdi32.CreateSolidBrush.argtypes = [COLORREF]
gdi32.CreateSolidBrush.restype = HBRUSH
gdi32.DeleteDC.argtypes = [HDC]
gdi32.DeleteDC.restype = wintypes.BOOL
gdi32.GetTextExtentPoint32W.argtypes = [HDC, wintypes.LPCWSTR, ctypes.c_int, ctypes.POINTER(SIZE)]
gdi32.GetTextExtentPoint32W.restype = wintypes.BOOL
gdi32.DeleteObject.argtypes = [HGDIOBJ]
gdi32.DeleteObject.restype = wintypes.BOOL
gdi32.GetDeviceCaps.argtypes = [HDC, ctypes.c_int]
gdi32.GetDeviceCaps.restype = ctypes.c_int
gdi32.RoundRect.argtypes = [HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
gdi32.RoundRect.restype = wintypes.BOOL
gdi32.SelectObject.argtypes = [HDC, HGDIOBJ]
gdi32.SelectObject.restype = HGDIOBJ
gdi32.SetBkMode.argtypes = [HDC, ctypes.c_int]
gdi32.SetBkMode.restype = ctypes.c_int
gdi32.SetTextColor.argtypes = [HDC, COLORREF]
gdi32.SetTextColor.restype = COLORREF
kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
kernel32.GetModuleHandleW.restype = HINSTANCE


@dataclass
class Theme:
    background: str = "#f3f3f3"
    surface: str = "#ffffff"
    surface_alt: str = "#fafafa"
    accent: str = "#005fb8"
    accent_soft: str = "#d7ebff"
    text_primary: str = "#1f1f1f"
    text_secondary: str = "#616161"
    border: str = "#e5e5e5"
    button_face: str = "#fbfbfb"
    button_hover: str = "#f0f0f0"
    button_border: str = "#d9d9d9"
    button_text: str = "#1f1f1f"


@dataclass
class Label:
    text: str
    x: int = 24
    y: int = 24
    width: int = 460
    height: int = 34
    color: Optional[str] = None
    style: str = "body"
    tab: Optional[str] = None


@dataclass
class Button:
    text: str
    x: int = 24
    y: int = 72
    width: int = 180
    height: int = 44
    command: object = None
    background: Optional[str] = None
    foreground: Optional[str] = None
    border: Optional[str] = None
    accent: Optional[str] = None
    tab: Optional[str] = None
    tooltip: Optional[str] = None
    hover_progress: float = 0.0
    hover_target: float = 0.0

    def contains(self, x_pos, y_pos):
        return _rect_contains(self.x, self.y, self.x + self.width, self.y + self.height, x_pos, y_pos)


@dataclass
class TabItem:
    title: str
    x: int = 0
    width: int = 120
    close_width: int = 20
    hover_progress: float = 0.0
    hover_target: float = 0.0

    def contains(self, tab_bar, x_pos, y_pos):
        return _rect_contains(self.x, tab_bar.y, self.x + self.width, tab_bar.y + tab_bar.height, x_pos, y_pos)


@dataclass
class TabBar:
    tabs: List[TabItem]
    x: int = 24
    y: int = 24
    width: int = 420
    height: int = 36
    active_tab: Optional[str] = None
    on_change: object = None
    indicator_x: float = 0.0
    indicator_width: float = 0.0
    target_indicator_x: float = 0.0
    target_indicator_width: float = 0.0


@dataclass
class NavAction:
    text: str
    accent: bool = False


@dataclass
class NavBar:
    title: str
    x: int = 24
    y: int = 96
    width: int = 640
    height: int = 54
    subtitle: Optional[str] = None
    actions: Optional[List[NavAction]] = None
    tab: Optional[str] = None


@dataclass
class Panel:
    title: str
    x: int = 24
    y: int = 160
    width: int = 320
    height: int = 220
    subtitle: Optional[str] = None
    accent: Optional[str] = None
    tab: Optional[str] = None


@dataclass
class Card:
    title: str
    value: str
    x: int = 24
    y: int = 160
    width: int = 220
    height: int = 120
    subtitle: Optional[str] = None
    accent: Optional[str] = None
    tab: Optional[str] = None
    collision_safety: bool = True


@dataclass
class Grid:
    columns: List[str]
    rows: List[List[str]]
    x: int = 24
    y: int = 160
    width: int = 520
    row_height: int = 34
    tab: Optional[str] = None


@dataclass
class Chart:
    title: str
    points: List[Tuple[str, float]]
    x: int = 24
    y: int = 160
    width: int = 360
    height: int = 240
    accent: Optional[str] = None
    tab: Optional[str] = None


@dataclass
class LayoutCell:
    x: int
    y: int
    width: int
    height: int


@dataclass
class HorizontalGrid:
    x: int
    y: int
    width: int
    item_width: int
    height: int
    gap: int
    cells: List[LayoutCell]


@dataclass
class VerticalGrid:
    x: int
    y: int
    width: int
    item_height: int
    gap: int
    cells: List[LayoutCell]


@dataclass
class NavEntry:
    key: str
    title: str
    subtitle: Optional[str] = None


@dataclass
class CollapsibleNavBar:
    title: str
    x: int = 52
    y: int = 212
    width: int = 248
    collapsed_width: int = 76
    height: int = 440
    items: Optional[List[NavEntry]] = None
    selected_key: Optional[str] = None
    collapsed: bool = False
    tab: Optional[str] = None


@dataclass
class TextInput:
    value: str = ""
    placeholder: str = ""
    x: int = 24
    y: int = 24
    width: int = 240
    height: int = 36
    on_change: object = None
    on_submit: object = None
    tab: Optional[str] = None
    password: bool = False
    max_length: Optional[int] = None
    caret: int = 0
    focused: bool = False
    hover_progress: float = 0.0
    hover_target: float = 0.0

    def contains(self, x_pos, y_pos):
        return _rect_contains(self.x, self.y, self.x + self.width, self.y + self.height, x_pos, y_pos)


@dataclass
class Checkbox:
    label: str = ""
    checked: bool = False
    x: int = 24
    y: int = 24
    width: int = 220
    height: int = 28
    on_change: object = None
    tab: Optional[str] = None
    hover_progress: float = 0.0
    hover_target: float = 0.0

    def contains(self, x_pos, y_pos):
        return _rect_contains(self.x, self.y, self.x + self.width, self.y + self.height, x_pos, y_pos)


@dataclass
class Switch:
    label: str = ""
    on: bool = False
    x: int = 24
    y: int = 24
    width: int = 220
    height: int = 28
    on_change: object = None
    tab: Optional[str] = None
    hover_progress: float = 0.0
    hover_target: float = 0.0

    def contains(self, x_pos, y_pos):
        return _rect_contains(self.x, self.y, self.x + self.width, self.y + self.height, x_pos, y_pos)


@dataclass
class RadioOption:
    key: str
    label: str


@dataclass
class RadioGroup:
    options: List[RadioOption]
    selected: Optional[str] = None
    x: int = 24
    y: int = 24
    width: int = 240
    item_height: int = 28
    on_change: object = None
    tab: Optional[str] = None

    @property
    def height(self):
        return len(self.options) * self.item_height

    def contains(self, x_pos, y_pos):
        return _rect_contains(self.x, self.y, self.x + self.width, self.y + self.height, x_pos, y_pos)

    def hit_option(self, x_pos, y_pos):
        if not self.contains(x_pos, y_pos):
            return None
        local_y = y_pos - self.y
        index = local_y // self.item_height
        if 0 <= index < len(self.options):
            return self.options[index]
        return None


@dataclass
class Slider:
    value: float = 0.0
    minimum: float = 0.0
    maximum: float = 100.0
    step: float = 0.0  # 0 means continuous
    x: int = 24
    y: int = 24
    width: int = 240
    height: int = 36
    on_change: object = None
    tab: Optional[str] = None
    dragging: bool = False
    hover_progress: float = 0.0
    hover_target: float = 0.0

    def contains(self, x_pos, y_pos):
        # Wider hit-test so the handle is grabbable a few px outside the bar.
        return _rect_contains(self.x - 4, self.y, self.x + self.width + 4, self.y + self.height, x_pos, y_pos)

    def normalized(self):
        if self.maximum == self.minimum:
            return 0.0
        return max(0.0, min(1.0, (self.value - self.minimum) / (self.maximum - self.minimum)))

    def value_at(self, x_pos):
        track_left = self.x + 8
        track_right = self.x + self.width - 8
        ratio = 0.0 if track_right <= track_left else (x_pos - track_left) / (track_right - track_left)
        ratio = max(0.0, min(1.0, ratio))
        raw = self.minimum + ratio * (self.maximum - self.minimum)
        if self.step and self.step > 0:
            steps = round((raw - self.minimum) / self.step)
            raw = self.minimum + steps * self.step
        return max(self.minimum, min(self.maximum, raw))


@dataclass
class Dropdown:
    options: List[str]
    selected: Optional[str] = None
    placeholder: str = "Select..."
    x: int = 24
    y: int = 24
    width: int = 240
    height: int = 36
    on_change: object = None
    tab: Optional[str] = None
    expanded: bool = False
    hover_progress: float = 0.0
    hover_target: float = 0.0

    def contains_header(self, x_pos, y_pos):
        return _rect_contains(self.x, self.y, self.x + self.width, self.y + self.height, x_pos, y_pos)

    def option_height(self):
        return 32

    def panel_rect(self):
        item_h = self.option_height()
        top = self.y + self.height + 4
        bottom = top + len(self.options) * item_h + 8
        return self.x, top, self.x + self.width, bottom

    def hit_option(self, x_pos, y_pos):
        left, top, right, bottom = self.panel_rect()
        if not _rect_contains(left, top, right, bottom, x_pos, y_pos):
            return None
        item_h = self.option_height()
        index = (y_pos - top - 4) // item_h
        if 0 <= index < len(self.options):
            return self.options[index]
        return None


@dataclass
class ProgressBar:
    value: float = 0.0  # 0.0 .. 1.0
    x: int = 24
    y: int = 24
    width: int = 240
    height: int = 8
    accent: Optional[str] = None
    show_label: bool = False
    tab: Optional[str] = None


@dataclass
class ListBox:
    items: List[str]
    selected_index: int = -1
    x: int = 24
    y: int = 24
    width: int = 280
    height: int = 220
    item_height: int = 28
    scroll_offset: int = 0  # row index at top of viewport
    on_change: object = None
    tab: Optional[str] = None
    tooltip: Optional[str] = None

    def visible_rows(self):
        return max(1, (self.height - 8) // self.item_height)

    def max_offset(self):
        return max(0, len(self.items) - self.visible_rows())

    def contains(self, x_pos, y_pos):
        return _rect_contains(self.x, self.y, self.x + self.width, self.y + self.height, x_pos, y_pos)

    def hit_index(self, y_pos):
        local_y = y_pos - self.y - 4
        if local_y < 0:
            return -1
        index = self.scroll_offset + (local_y // self.item_height)
        if 0 <= index < len(self.items):
            return int(index)
        return -1


@dataclass
class TreeNode:
    label: str
    key: Optional[str] = None
    children: List["TreeNode"] = field(default_factory=list)
    expanded: bool = True


@dataclass
class TreeView:
    nodes: List[TreeNode]
    selected_key: Optional[str] = None
    x: int = 24
    y: int = 24
    width: int = 300
    height: int = 280
    row_height: int = 26
    on_select: object = None
    tab: Optional[str] = None
    tooltip: Optional[str] = None
    # Cached flat layout: list of (node, depth, row_rect_top, has_children)
    _flat: List = field(default_factory=list, repr=False)

    def contains(self, x_pos, y_pos):
        return _rect_contains(self.x, self.y, self.x + self.width, self.y + self.height, x_pos, y_pos)


@dataclass
class MenuItem:
    label: str
    command: object = None
    shortcut: Optional[str] = None  # e.g. "Ctrl+S" — display only


@dataclass
class Menu:
    title: str
    items: List[MenuItem]


@dataclass
class MenuBar:
    menus: List[Menu]
    x: int = 0
    y: int = 0
    height: int = 36
    open_index: int = -1
    hovered_index: int = -1


@dataclass
class Tooltip:
    """Internal: a transient popup attached to whichever control is hovered."""
    text: str = ""
    x: int = 0
    y: int = 0
    visible: bool = False


@dataclass
class Accelerator:
    """Keyboard shortcut registration (e.g. Ctrl+S)."""
    vk: int
    modifiers: int  # bitmask of MOD_CTRL / MOD_SHIFT / MOD_ALT
    callback: object
    description: Optional[str] = None


class Window:
    """A Windows-native custom-rendered GUI surface for GUIpi26."""

    _class_name = "GUIpi26WindowClass"
    _class_registered = False
    _instances = {}
    _wndproc = None

    def __init__(self, title="GUIpi26 Window", width=800, height=600):
        self.title = title
        self.width = width
        self.height = height
        self.theme = Theme()
        self.nav_bars = []
        self.collapsible_nav_bars = []
        self.panels = []
        self.cards = []
        self.grids = []
        self.charts = []
        self.labels = []
        self.buttons = []
        self.text_inputs = []
        self.checkboxes = []
        self.switches = []
        self.radio_groups = []
        self.sliders = []
        self.dropdowns = []
        self.progress_bars = []
        self.list_boxes = []
        self.tree_views = []
        self.menu_bar = None
        self.tab_bar = None
        self._font_cache = {}
        self._tracking_mouse = False
        self._hovered_button = None
        self._hovered_tab = None
        self._hovered_form = None
        self._focused_input = None
        self._dragging_slider = None
        self._tooltip = Tooltip()
        self._tooltip_target = None
        self._tooltip_pending_at = 0
        self._tooltip_timer_set = False
        self._mouse_x = -1
        self._mouse_y = -1
        self._accelerators = []
        self._cursor_arrow = user32.LoadCursorW(None, _make_int_resource(IDC_ARROW))
        self._cursor_hand = user32.LoadCursorW(None, _make_int_resource(IDC_HAND))
        self._cursor_ibeam = user32.LoadCursorW(None, _make_int_resource(IDC_IBEAM))
        self._layout_callbacks = []
        self._last_layout_size = (0, 0)
        self._register_window_class()

        hinstance = kernel32.GetModuleHandleW(None)
        self.hwnd = user32.CreateWindowExW(
            0,
            self._class_name,
            self.title,
            WS_OVERLAPPEDWINDOW | WS_VISIBLE,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            self.width,
            self.height,
            None,
            None,
            hinstance,
            None,
        )
        if not self.hwnd:
            raise ctypes.WinError(ctypes.get_last_error())

        self._instances[self.hwnd] = self
        user32.ShowWindow(self.hwnd, SW_SHOW)
        user32.UpdateWindow(self.hwnd)

    @classmethod
    def _register_window_class(cls):
        if cls._class_registered:
            return

        cls._wndproc = WNDPROC(cls._window_proc)
        hinstance = kernel32.GetModuleHandleW(None)
        window_class = WNDCLASSW()
        window_class.style = CS_HREDRAW | CS_VREDRAW
        window_class.lpfnWndProc = cls._wndproc
        window_class.cbClsExtra = 0
        window_class.cbWndExtra = 0
        window_class.hInstance = hinstance
        window_class.hIcon = user32.LoadIconW(None, _make_int_resource(IDI_APPLICATION))
        window_class.hCursor = user32.LoadCursorW(None, _make_int_resource(IDC_ARROW))
        window_class.hbrBackground = None
        window_class.lpszMenuName = None
        window_class.lpszClassName = cls._class_name

        atom = user32.RegisterClassW(ctypes.byref(window_class))
        if not atom and ctypes.get_last_error() != 1410:
            raise ctypes.WinError(ctypes.get_last_error())

        cls._class_registered = True

    @classmethod
    def _window_proc(cls, hwnd, message, w_param, l_param):
        instance = cls._instances.get(hwnd)

        if message == WM_DESTROY:
            if instance is not None:
                instance._dispose_fonts()
            cls._instances.pop(hwnd, None)
            user32.PostQuitMessage(0)
            return 0

        if instance is not None:
            handled = instance._handle_message(message, w_param, l_param)
            if handled is not None:
                return handled

        return user32.DefWindowProcW(hwnd, message, w_param, l_param)

    def _handle_message(self, message, w_param, l_param):
        if message == WM_PAINT:
            self._paint()
            return 0

        if message == WM_CLOSE:
            self.destroy()
            return 0

        if message == WM_SIZE:
            self._run_layout_callbacks()
            self.invalidate()
            return 0

        if message == WM_MOUSEMOVE:
            self._track_mouse_leave()
            x_pos, y_pos = _get_x_lparam(l_param), _get_y_lparam(l_param)
            self._mouse_x, self._mouse_y = x_pos, y_pos
            if self._dragging_slider is not None:
                self._update_slider_drag(x_pos)
                return 0
            self._update_hover_state(x_pos, y_pos)
            return 0

        if message == WM_MOUSELEAVE:
            self._tracking_mouse = False
            self._mouse_x = self._mouse_y = -1
            self._hide_tooltip()
            self._update_hover_state(-1, -1)
            return 0

        if message == WM_MOUSEWHEEL:
            delta = ctypes.c_short((w_param >> 16) & 0xFFFF).value
            self._handle_mouse_wheel(delta)
            return 0

        if message == WM_SETCURSOR:
            # Only override cursor inside the client area (LOWORD == HTCLIENT == 1).
            if (l_param & 0xFFFF) == 1 and self._apply_cursor():
                return 1
            return None

        if message == WM_LBUTTONDOWN:
            self._handle_press(_get_x_lparam(l_param), _get_y_lparam(l_param))
            return 0

        if message == WM_LBUTTONUP:
            self._handle_click(_get_x_lparam(l_param), _get_y_lparam(l_param))
            return 0

        if message == WM_CHAR:
            if self._focused_input is not None:
                self._handle_text_char(w_param)
                return 0

        if message == WM_KEYDOWN:
            if self._dispatch_accelerator(int(w_param)):
                return 0
            if self._focused_input is not None:
                self._handle_text_key(w_param)
                return 0
            # Allow tree/list keyboard nav even without focused input.
            if self._handle_navigation_key(int(w_param)):
                return 0

        if message == WM_TIMER:
            if int(w_param) == TIMER_TOOLTIP:
                self._on_tooltip_timer()
                return 0

        return None

    def _track_mouse_leave(self):
        if self._tracking_mouse:
            return

        track = TRACKMOUSEEVENT()
        track.cbSize = ctypes.sizeof(TRACKMOUSEEVENT)
        track.dwFlags = TME_LEAVE
        track.hwndTrack = self.hwnd
        track.dwHoverTime = 0
        user32.TrackMouseEvent(ctypes.byref(track))
        self._tracking_mouse = True

    def _get_font(self, role):
        config = {
            "title": (28, FW_LIGHT, "Segoe UI Light"),
            "subtitle": (14, FW_NORMAL, "Segoe UI"),
            "body": (12, FW_NORMAL, "Segoe UI"),
            "button": (12, FW_NORMAL, "Segoe UI Semibold"),
            "tab": (11, FW_NORMAL, "Segoe UI"),
            "caption": (10, FW_NORMAL, "Segoe UI"),
            "metric": (24, FW_LIGHT, "Segoe UI Light"),
        }
        if role not in self._font_cache:
            size, weight, family = config[role]
            height = self._point_to_pixels(size)
            self._font_cache[role] = gdi32.CreateFontW(
                -height,
                0,
                0,
                0,
                weight,
                0,
                0,
                0,
                DEFAULT_CHARSET,
                0,
                0,
                5,
                DEFAULT_PITCH,
                family,
            )
        return self._font_cache[role]

    def _point_to_pixels(self, points):
        desktop = user32.GetDC(self.hwnd)
        dpi = gdi32.GetDeviceCaps(desktop, LOGPIXELSY)
        user32.ReleaseDC(self.hwnd, desktop)
        return int(points * dpi / 72)

    def _dispose_fonts(self):
        for font in self._font_cache.values():
            if font:
                gdi32.DeleteObject(font)
        self._font_cache.clear()

    def _update_hover_state(self, x_pos, y_pos):
        hovered_button = None
        hovered_tab = None
        hovered_form = None

        for button in self.buttons:
            if self._is_control_visible(button) and button.contains(x_pos, y_pos):
                hovered_button = button
            button.hover_target = 1.0 if button is hovered_button else 0.0
            button.hover_progress = button.hover_target

        for control_list in (self.text_inputs, self.checkboxes, self.switches, self.sliders, self.dropdowns):
            for control in control_list:
                if hovered_form is None and self._is_control_visible(control) and control.contains(x_pos, y_pos):
                    hovered_form = control
                control.hover_target = 1.0 if control is hovered_form else 0.0
                control.hover_progress = control.hover_target

        # ListBox + TreeView hover (no per-row animation, just identity).
        for lb in self.list_boxes:
            if hovered_form is None and self._is_control_visible(lb) and lb.contains(x_pos, y_pos):
                hovered_form = lb
        for tv in self.tree_views:
            if hovered_form is None and self._is_control_visible(tv) and tv.contains(x_pos, y_pos):
                hovered_form = tv

        # MenuBar hover
        if self.menu_bar is not None:
            new_hover = self._menubar_hit(x_pos, y_pos)
            if new_hover != self.menu_bar.hovered_index:
                self.menu_bar.hovered_index = new_hover
                self.invalidate()

        if self.tab_bar is not None:
            for item in self.tab_bar.tabs:
                if item.contains(self.tab_bar, x_pos, y_pos):
                    hovered_tab = item
                item.hover_target = 1.0 if item is hovered_tab else 0.0
                item.hover_progress = item.hover_target

        if (
            hovered_button is not self._hovered_button
            or hovered_tab is not self._hovered_tab
            or hovered_form is not self._hovered_form
        ):
            self._hovered_button = hovered_button
            self._hovered_tab = hovered_tab
            self._hovered_form = hovered_form
            self.invalidate()

        self._maybe_schedule_tooltip()
        # Force cursor refresh — Windows caches WM_SETCURSOR result, so push it ourselves.
        self._apply_cursor()

    # ------------------------------------------------------------------
    # Cursor management
    # ------------------------------------------------------------------
    def _desired_cursor(self):
        if self._hovered_button is not None or self._hovered_tab is not None:
            return self._cursor_hand
        target = self._hovered_form
        if target is None:
            return self._cursor_arrow
        if isinstance(target, TextInput):
            return self._cursor_ibeam
        # Checkbox, Switch, Slider, Dropdown, ListBox, TreeView -> hand
        return self._cursor_hand

    def _apply_cursor(self):
        cursor = self._desired_cursor()
        if cursor:
            user32.SetCursor(cursor)
            return True
        return False

    # ------------------------------------------------------------------
    # Tooltips
    # ------------------------------------------------------------------
    def _hovered_tooltip_target(self):
        candidates = (self._hovered_button, self._hovered_form)
        for c in candidates:
            if c is None:
                continue
            text = getattr(c, "tooltip", None)
            if text:
                return c, text
        return None, None

    def _maybe_schedule_tooltip(self):
        target, text = self._hovered_tooltip_target()
        if target is None:
            self._hide_tooltip()
            self._tooltip_target = None
            return
        if target is self._tooltip_target and self._tooltip.visible:
            # Move follow-cursor tooltip with the mouse.
            self._tooltip.x = self._mouse_x + 14
            self._tooltip.y = self._mouse_y + 20
            self.invalidate()
            return
        if target is not self._tooltip_target:
            self._tooltip_target = target
            self._tooltip.visible = False
            self._tooltip.text = text
            user32.SetTimer(self.hwnd, TIMER_TOOLTIP, TOOLTIP_DELAY_MS, None)
            self._tooltip_timer_set = True

    def _on_tooltip_timer(self):
        # One-shot timer.
        user32.KillTimer(self.hwnd, TIMER_TOOLTIP)
        self._tooltip_timer_set = False
        target, text = self._hovered_tooltip_target()
        if target is None or target is not self._tooltip_target:
            return
        self._tooltip.text = text
        self._tooltip.x = self._mouse_x + 14
        self._tooltip.y = self._mouse_y + 20
        self._tooltip.visible = True
        self.invalidate()

    def _hide_tooltip(self):
        if self._tooltip_timer_set:
            user32.KillTimer(self.hwnd, TIMER_TOOLTIP)
            self._tooltip_timer_set = False
        if self._tooltip.visible:
            self._tooltip.visible = False
            self.invalidate()

    # ------------------------------------------------------------------
    # Mouse wheel — currently scrolls the hovered list box / tree view
    # ------------------------------------------------------------------
    def _handle_mouse_wheel(self, delta):
        # delta is 120 per notch; positive = scroll up.
        steps = -1 if delta < 0 else 1
        rows = abs(delta) // 120 or 1
        for lb in self.list_boxes:
            if not self._is_control_visible(lb):
                continue
            if lb.contains(self._mouse_x, self._mouse_y):
                new_offset = max(0, min(lb.max_offset(), lb.scroll_offset + steps * rows))
                if new_offset != lb.scroll_offset:
                    lb.scroll_offset = new_offset
                    self.invalidate()
                return
        for tv in self.tree_views:
            if not self._is_control_visible(tv):
                continue
            if tv.contains(self._mouse_x, self._mouse_y):
                # Trees scroll by mutating an offset stored on the tree.
                tv.scroll_offset = max(0, getattr(tv, "scroll_offset", 0) - steps * rows)
                self.invalidate()
                return

    # ------------------------------------------------------------------
    # Keyboard accelerators
    # ------------------------------------------------------------------
    def _current_modifiers(self):
        mods = 0
        if user32.GetKeyState(0x11) & 0x8000:  # VK_CONTROL
            mods |= MOD_CTRL
        if user32.GetKeyState(0x10) & 0x8000:  # VK_SHIFT
            mods |= MOD_SHIFT
        if user32.GetKeyState(0x12) & 0x8000:  # VK_MENU (Alt)
            mods |= MOD_ALT
        return mods

    def _dispatch_accelerator(self, vk):
        if not self._accelerators:
            return False
        mods = self._current_modifiers()
        for acc in self._accelerators:
            if acc.vk == vk and acc.modifiers == mods:
                if acc.callback is not None:
                    acc.callback()
                return True
        return False

    def _handle_navigation_key(self, vk):
        # Up/Down arrow scrolls the list box that has focus-by-hover.
        for lb in self.list_boxes:
            if not self._is_control_visible(lb):
                continue
            if not lb.contains(self._mouse_x, self._mouse_y):
                continue
            if vk == VK_UP and lb.selected_index > 0:
                lb.selected_index -= 1
                self._ensure_listbox_visible(lb)
                if lb.on_change:
                    lb.on_change(lb.selected_index)
                self.invalidate()
                return True
            if vk == VK_DOWN and lb.selected_index < len(lb.items) - 1:
                lb.selected_index += 1
                self._ensure_listbox_visible(lb)
                if lb.on_change:
                    lb.on_change(lb.selected_index)
                self.invalidate()
                return True
        return False

    def _ensure_listbox_visible(self, lb):
        if lb.selected_index < lb.scroll_offset:
            lb.scroll_offset = lb.selected_index
        elif lb.selected_index >= lb.scroll_offset + lb.visible_rows():
            lb.scroll_offset = lb.selected_index - lb.visible_rows() + 1
        lb.scroll_offset = max(0, min(lb.max_offset(), lb.scroll_offset))

    # ------------------------------------------------------------------
    # MenuBar hit-testing
    # ------------------------------------------------------------------
    def _menubar_hit(self, x_pos, y_pos):
        if self.menu_bar is None:
            return -1
        bar = self.menu_bar
        if not (bar.x <= x_pos <= bar.x + self._client_size()[0] and bar.y <= y_pos <= bar.y + bar.height):
            return -1
        cursor = bar.x + 12
        for index, menu in enumerate(bar.menus):
            w = self._menu_title_width(menu.title)
            if cursor <= x_pos <= cursor + w:
                return index
            cursor += w
        return -1

    def _menu_title_width(self, title):
        return max(60, len(title) * 8 + 24)

    def _menu_panel_rect(self, index):
        bar = self.menu_bar
        if bar is None or not (0 <= index < len(bar.menus)):
            return None
        cursor = bar.x + 12
        for i, menu in enumerate(bar.menus):
            w = self._menu_title_width(menu.title)
            if i == index:
                items = menu.items
                panel_w = 220
                panel_h = 8 + len(items) * 30
                return cursor, bar.y + bar.height, cursor + panel_w, bar.y + bar.height + panel_h
            cursor += w
        return None

    def _handle_press(self, x_pos, y_pos):
        # Slider drag-start has priority so the handle starts moving immediately.
        for slider in self.sliders:
            if not self._is_control_visible(slider):
                continue
            if slider.contains(x_pos, y_pos):
                slider.dragging = True
                self._dragging_slider = slider
                self._update_slider_drag(x_pos)
                return

    def _update_slider_drag(self, x_pos):
        slider = self._dragging_slider
        if slider is None:
            return
        new_value = slider.value_at(x_pos)
        if new_value != slider.value:
            slider.value = new_value
            if slider.on_change is not None:
                slider.on_change(slider.value)
            self.invalidate()

    def _handle_text_char(self, w_param):
        target = self._focused_input
        if target is None:
            return
        char_code = int(w_param)
        if char_code == 0x08:  # backspace
            if target.caret > 0:
                target.value = target.value[: target.caret - 1] + target.value[target.caret:]
                target.caret -= 1
                if target.on_change is not None:
                    target.on_change(target.value)
                self.invalidate()
            return
        if char_code in (0x0D, 0x0A):  # Enter
            if target.on_submit is not None:
                target.on_submit(target.value)
            return
        if char_code < 0x20:
            return
        if target.max_length is not None and len(target.value) >= target.max_length:
            return
        char = chr(char_code)
        target.value = target.value[: target.caret] + char + target.value[target.caret:]
        target.caret += 1
        if target.on_change is not None:
            target.on_change(target.value)
        self.invalidate()

    def _handle_text_key(self, vk):
        target = self._focused_input
        if target is None:
            return
        if vk == VK_LEFT and target.caret > 0:
            target.caret -= 1
            self.invalidate()
        elif vk == VK_RIGHT and target.caret < len(target.value):
            target.caret += 1
            self.invalidate()
        elif vk == VK_HOME:
            target.caret = 0
            self.invalidate()
        elif vk == VK_END:
            target.caret = len(target.value)
            self.invalidate()
        elif vk == VK_DELETE and target.caret < len(target.value):
            target.value = target.value[: target.caret] + target.value[target.caret + 1:]
            if target.on_change is not None:
                target.on_change(target.value)
            self.invalidate()
        elif vk == VK_TAB:
            self._focus_next_text_input()

    def _focus_next_text_input(self):
        visible = [t for t in self.text_inputs if self._is_control_visible(t)]
        if not visible:
            return
        if self._focused_input not in visible:
            self._set_focused_input(visible[0])
            return
        idx = visible.index(self._focused_input)
        self._set_focused_input(visible[(idx + 1) % len(visible)])

    def _set_focused_input(self, target):
        if self._focused_input is target:
            return
        if self._focused_input is not None:
            self._focused_input.focused = False
        self._focused_input = target
        if target is not None:
            target.focused = True
            target.caret = len(target.value)
        self.invalidate()

    def _handle_click(self, x_pos, y_pos):
        # Finalise slider drag (do not interpret as a tap-on-track click).
        if self._dragging_slider is not None:
            self._dragging_slider.dragging = False
            self._dragging_slider = None
            self.invalidate()
            return

        # Open menu panel owns the next click.
        if self.menu_bar is not None and self.menu_bar.open_index >= 0:
            panel = self._menu_panel_rect(self.menu_bar.open_index)
            if panel is not None and _rect_contains(panel[0], panel[1], panel[2], panel[3], x_pos, y_pos):
                items = self.menu_bar.menus[self.menu_bar.open_index].items
                local_y = y_pos - panel[1] - 4
                idx = local_y // 30
                if 0 <= idx < len(items):
                    item = items[int(idx)]
                    self.menu_bar.open_index = -1
                    self.invalidate()
                    if item.command is not None:
                        item.command()
                    return
            # Click outside open panel — close it and continue dispatch.
            self.menu_bar.open_index = -1
            self.invalidate()

        # MenuBar title click toggles its panel.
        if self.menu_bar is not None:
            hit = self._menubar_hit(x_pos, y_pos)
            if hit >= 0:
                self.menu_bar.open_index = -1 if self.menu_bar.open_index == hit else hit
                self.invalidate()
                return

        # Expanded dropdown owns the next click: select an option, toggle, or collapse.
        for dropdown in self.dropdowns:
            if not dropdown.expanded or not self._is_control_visible(dropdown):
                continue
            option = dropdown.hit_option(x_pos, y_pos)
            if option is not None:
                dropdown.selected = option
                dropdown.expanded = False
                if dropdown.on_change is not None:
                    dropdown.on_change(option)
                self.invalidate()
                return
            if dropdown.contains_header(x_pos, y_pos):
                dropdown.expanded = False
                self.invalidate()
                return
            # Click landed outside this dropdown — collapse it and continue dispatch.
            dropdown.expanded = False
            self.invalidate()

        if self.tab_bar is not None:
            for item in self.tab_bar.tabs:
                if item.contains(self.tab_bar, x_pos, y_pos):
                    self.set_active_tab(item.title)
                    return

        for nav_bar in self.collapsible_nav_bars:
            if not self._is_control_visible(nav_bar):
                continue
            toggle_left, toggle_top, toggle_right, toggle_bottom = self._nav_toggle_rect(nav_bar)
            if _rect_contains(toggle_left, toggle_top, toggle_right, toggle_bottom, x_pos, y_pos):
                nav_bar.collapsed = not nav_bar.collapsed
                self.invalidate()
                return

            for entry, item_rect in self._nav_item_rects(nav_bar):
                if _rect_contains(item_rect.x, item_rect.y, item_rect.x + item_rect.width, item_rect.y + item_rect.height, x_pos, y_pos):
                    nav_bar.selected_key = entry.key
                    self.invalidate()
                    return

        # Form controls (toggle / focus / select).
        clicked_input = None
        for text_input in self.text_inputs:
            if self._is_control_visible(text_input) and text_input.contains(x_pos, y_pos):
                clicked_input = text_input
                break
        if clicked_input is not None:
            self._set_focused_input(clicked_input)
            return

        for checkbox in self.checkboxes:
            if self._is_control_visible(checkbox) and checkbox.contains(x_pos, y_pos):
                checkbox.checked = not checkbox.checked
                if checkbox.on_change is not None:
                    checkbox.on_change(checkbox.checked)
                self._set_focused_input(None)
                self.invalidate()
                return

        for switch in self.switches:
            if self._is_control_visible(switch) and switch.contains(x_pos, y_pos):
                switch.on = not switch.on
                if switch.on_change is not None:
                    switch.on_change(switch.on)
                self._set_focused_input(None)
                self.invalidate()
                return

        for radio_group in self.radio_groups:
            if not self._is_control_visible(radio_group):
                continue
            option = radio_group.hit_option(x_pos, y_pos)
            if option is not None:
                if radio_group.selected != option.key:
                    radio_group.selected = option.key
                    if radio_group.on_change is not None:
                        radio_group.on_change(option.key)
                self._set_focused_input(None)
                self.invalidate()
                return

        for dropdown in self.dropdowns:
            if self._is_control_visible(dropdown) and dropdown.contains_header(x_pos, y_pos):
                dropdown.expanded = not dropdown.expanded
                self._set_focused_input(None)
                self.invalidate()
                return

        # Slider tap-to-jump (drag was already handled above).
        for slider in self.sliders:
            if self._is_control_visible(slider) and slider.contains(x_pos, y_pos):
                new_value = slider.value_at(x_pos)
                if new_value != slider.value:
                    slider.value = new_value
                    if slider.on_change is not None:
                        slider.on_change(slider.value)
                self.invalidate()
                return

        # ListBox row selection
        for lb in self.list_boxes:
            if not self._is_control_visible(lb):
                continue
            if lb.contains(x_pos, y_pos):
                index = lb.hit_index(y_pos)
                if index >= 0 and index != lb.selected_index:
                    lb.selected_index = index
                    if lb.on_change is not None:
                        lb.on_change(index)
                    self._set_focused_input(None)
                    self.invalidate()
                return

        # TreeView node toggle / select
        for tv in self.tree_views:
            if not self._is_control_visible(tv):
                continue
            if tv.contains(x_pos, y_pos):
                self._handle_treeview_click(tv, x_pos, y_pos)
                return

        for button in reversed(self.buttons):
            if self._is_control_visible(button) and button.contains(x_pos, y_pos):
                if button.command is not None:
                    button.command()
                self._set_focused_input(None)
                self.invalidate()
                return

        # Click landed on empty space — drop focus.
        self._set_focused_input(None)

    def _flatten_tree(self, tv):
        result = []

        def walk(node, depth):
            has_children = bool(node.children)
            result.append((node, depth, has_children))
            if node.expanded:
                for child in node.children:
                    walk(child, depth + 1)

        for root in tv.nodes:
            walk(root, 0)
        return result

    def _handle_treeview_click(self, tv, x_pos, y_pos):
        flat = self._flatten_tree(tv)
        scroll = getattr(tv, "scroll_offset", 0)
        local_y = y_pos - tv.y - 4
        if local_y < 0:
            return
        index = scroll + (local_y // tv.row_height)
        if not (0 <= index < len(flat)):
            return
        node, depth, has_children = flat[int(index)]
        chevron_left = tv.x + 8 + depth * 18
        if has_children and chevron_left <= x_pos <= chevron_left + 22:
            node.expanded = not node.expanded
        else:
            tv.selected_key = node.key if node.key is not None else node.label
            if tv.on_select is not None:
                tv.on_select(node)
        self.invalidate()

    def _layout_tabs(self):
        if self.tab_bar is None:
            return

        x_cursor = self.tab_bar.x + 10
        for item in self.tab_bar.tabs:
            item.width = max(132, len(item.title) * 8 + 58)
            item.x = x_cursor
            x_cursor += item.width + 6

        active = self._get_active_tab_item()
        if active is not None:
            self.tab_bar.target_indicator_x = active.x + 18
            self.tab_bar.target_indicator_width = max(34, active.width - 36)
            self.tab_bar.indicator_x = self.tab_bar.target_indicator_x
            self.tab_bar.indicator_width = self.tab_bar.target_indicator_width

    def _get_active_tab_item(self):
        if self.tab_bar is None:
            return None
        for item in self.tab_bar.tabs:
            if item.title == self.tab_bar.active_tab:
                return item
        return None

    def _is_control_visible(self, control):
        target = getattr(control, "tab", None)
        if target is None:
            return True

        if self.tab_bar is not None and target == self.tab_bar.active_tab:
            return True

        for nav_bar in self.collapsible_nav_bars:
            nav_scope = getattr(nav_bar, "tab", None)
            if self.tab_bar is not None and nav_scope is not None and nav_scope != self.tab_bar.active_tab:
                continue
            if target == nav_bar.selected_key:
                return True

        return False

    def _draw_text(self, device_context, text, rect, color, role, alignment):
        font = self._get_font(role)
        old_font = gdi32.SelectObject(device_context, font)
        gdi32.SetBkMode(device_context, TRANSPARENT)
        gdi32.SetTextColor(device_context, _rgb_to_colorref(color))
        user32.DrawTextW(device_context, text, -1, ctypes.byref(rect), alignment | DT_SINGLELINE | DT_END_ELLIPSIS)
        gdi32.SelectObject(device_context, old_font)

    def _draw_round_rect(self, device_context, left, top, right, bottom, radius, fill, border):
        brush = gdi32.CreateSolidBrush(_rgb_to_colorref(fill))
        pen = gdi32.CreatePen(PS_SOLID, 1, _rgb_to_colorref(border))
        old_brush = gdi32.SelectObject(device_context, brush)
        old_pen = gdi32.SelectObject(device_context, pen)
        gdi32.RoundRect(device_context, left, top, right, bottom, radius, radius)
        gdi32.SelectObject(device_context, old_brush)
        gdi32.SelectObject(device_context, old_pen)
        gdi32.DeleteObject(brush)
        gdi32.DeleteObject(pen)

    def _fill_rect(self, device_context, left, top, right, bottom, fill):
        fill_rect = RECT(left, top, right, bottom)
        brush = gdi32.CreateSolidBrush(_rgb_to_colorref(fill))
        user32.FillRect(device_context, ctypes.byref(fill_rect), brush)
        gdi32.DeleteObject(brush)

    def _client_size(self):
        rect = RECT()
        user32.GetClientRect(self.hwnd, ctypes.byref(rect))
        return rect.right - rect.left, rect.bottom - rect.top

    def client_size(self):
        """Return the current (width, height) of the window's client area."""
        return self._client_size()

    def on_layout(self, callback):
        """Register a callback fired on resize with (width, height).

        Use it to recompute control positions for responsive layouts. The
        callback runs immediately after registration and on every WM_SIZE.
        """
        self._layout_callbacks.append(callback)
        try:
            width, height = self._client_size()
            if width and height:
                callback(width, height)
                self._last_layout_size = (width, height)
        except Exception:
            pass
        return callback

    def _run_layout_callbacks(self):
        if not self._layout_callbacks:
            return
        width, height = self._client_size()
        if (width, height) == self._last_layout_size:
            return
        self._last_layout_size = (width, height)
        for callback in list(self._layout_callbacks):
            callback(width, height)

    def _resolve_card_overlaps(self, gap=12):
        """Push safety-on cards down so they don't overlap previously-placed cards."""
        visible = [card for card in self.cards if self._is_control_visible(card)]
        placed = []  # list of (left, top, right, bottom)
        for card in visible:
            left, right = card.x, card.x + card.width
            top, bottom = card.y, card.y + card.height
            if card.collision_safety:
                changed = True
                # Iterate a few times in case nudging into one card collides with another
                for _ in range(len(placed) + 1):
                    if not changed:
                        break
                    changed = False
                    for pl, pt, pr, pb in placed:
                        if left < pr and right > pl and top < pb and bottom > pt:
                            shift = (pb + gap) - top
                            top += shift
                            bottom += shift
                            changed = True
                if top != card.y:
                    card.y = top
            placed.append((left, top, right, bottom))

    def _nav_current_width(self, nav_bar):
        return nav_bar.collapsed and nav_bar.collapsed_width or nav_bar.width

    def _sidebar_bounds(self, nav_bar):
        _, client_height = self._client_size()
        return 0, 0, self._nav_current_width(nav_bar), client_height

    def _primary_sidebar(self):
        for nav_bar in self.collapsible_nav_bars:
            if self._is_control_visible(nav_bar):
                return nav_bar
        return None

    def content_origin_x(self, padding=24):
        sidebar = self._primary_sidebar()
        if sidebar is None:
            return padding
        return self._nav_current_width(sidebar) + padding

    def _nav_toggle_rect(self, nav_bar):
        width = self._nav_current_width(nav_bar)
        return (width - 38, 18, width - 14, 42)

    def _nav_item_rects(self, nav_bar):
        width = self._nav_current_width(nav_bar)
        item_height = 44
        top = 92
        rects = []
        for index, entry in enumerate(nav_bar.items or []):
            item_y = top + index * (item_height + 4)
            rects.append((entry, LayoutCell(8, item_y, width - 16, item_height)))
        return rects

    def _draw_collapsible_nav_bar(self, device_context, nav_bar):
        left, top, right, bottom = self._sidebar_bounds(nav_bar)
        sidebar_bg = "#212529"
        sidebar_text = "#f8f9fa"
        sidebar_muted = "#adb5bd"
        divider = _blend(sidebar_bg, "#ffffff", 0.12)
        accent = self.theme.accent

        self._fill_rect(device_context, left, top, right, bottom, sidebar_bg)

        brand_label = nav_bar.title[:1] if nav_bar.collapsed else nav_bar.title
        brand_rect = RECT(left + 20, top + 18, right - 50, top + 60)
        self._draw_text(device_context, brand_label, brand_rect, sidebar_text, "subtitle", DT_LEFT | DT_VCENTER)
        self._fill_rect(device_context, left + 16, top + 74, right - 16, top + 75, divider)

        toggle_left, toggle_top, toggle_right, toggle_bottom = self._nav_toggle_rect(nav_bar)
        self._draw_round_rect(
            device_context,
            toggle_left,
            toggle_top,
            toggle_right,
            toggle_bottom,
            6,
            _blend(sidebar_bg, "#ffffff", 0.08),
            _blend(sidebar_bg, "#ffffff", 0.18),
        )
        glyph = ">" if nav_bar.collapsed else "<"
        self._draw_text(
            device_context,
            glyph,
            RECT(toggle_left, toggle_top, toggle_right, toggle_bottom),
            sidebar_text,
            "caption",
            DT_CENTER | DT_VCENTER,
        )

        for entry, item_rect in self._nav_item_rects(nav_bar):
            selected = entry.key == nav_bar.selected_key
            item_left = item_rect.x
            item_top = item_rect.y
            item_right = item_rect.x + item_rect.width
            item_bottom = item_rect.y + item_rect.height

            if selected:
                self._draw_round_rect(device_context, item_left, item_top, item_right, item_bottom, 6, accent, accent)
                text_color = "#ffffff"
                sub_color = _blend("#ffffff", accent, 0.35)
                dot_color = "#ffffff"
            else:
                text_color = sidebar_text
                sub_color = sidebar_muted
                dot_color = sidebar_muted

            dot_left = item_left + 14
            dot_top = item_top + (item_rect.height // 2) - 4
            self._draw_round_rect(device_context, dot_left, dot_top, dot_left + 8, dot_top + 8, 4, dot_color, dot_color)

            if not nav_bar.collapsed:
                title_rect = RECT(item_left + 32, item_top + 6, item_right - 10, item_top + 26)
                self._draw_text(device_context, entry.title, title_rect, text_color, "caption", DT_LEFT | DT_VCENTER)
                if entry.subtitle:
                    subtitle_rect = RECT(item_left + 32, item_top + 22, item_right - 10, item_top + 40)
                    self._draw_text(device_context, entry.subtitle, subtitle_rect, sub_color, "caption", DT_LEFT | DT_VCENTER)

    def _draw_nav_bar(self, device_context, nav_bar):
        self._draw_round_rect(
            device_context,
            nav_bar.x,
            nav_bar.y,
            nav_bar.x + nav_bar.width,
            nav_bar.y + nav_bar.height,
            10,
            self.theme.surface_alt,
            self.theme.border,
        )
        title_rect = RECT(nav_bar.x + 16, nav_bar.y + 6, nav_bar.x + 260, nav_bar.y + 28)
        self._draw_text(device_context, nav_bar.title, title_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)
        if nav_bar.subtitle:
            subtitle_rect = RECT(nav_bar.x + 16, nav_bar.y + 24, nav_bar.x + 320, nav_bar.y + 46)
            self._draw_text(device_context, nav_bar.subtitle, subtitle_rect, self.theme.text_secondary, "caption", DT_LEFT | DT_VCENTER)

        if not nav_bar.actions:
            return

        action_right = nav_bar.x + nav_bar.width - 14
        for action in reversed(nav_bar.actions):
            action_width = max(86, len(action.text) * 8 + 28)
            action_left = action_right - action_width
            fill = action.accent and self.theme.accent or self.theme.button_face
            border = action.accent and self.theme.accent or self.theme.button_border
            text_color = action.accent and "#ffffff" or self.theme.button_text
            self._draw_round_rect(device_context, action_left, nav_bar.y + 10, action_right, nav_bar.y + 38, 8, fill, border)
            text_rect = RECT(action_left + 10, nav_bar.y + 10, action_right - 10, nav_bar.y + 38)
            self._draw_text(device_context, action.text, text_rect, text_color, "caption", DT_CENTER | DT_VCENTER)
            action_right = action_left - 8

    def _draw_panel(self, device_context, panel):
        accent = panel.accent or self.theme.accent
        self._draw_round_rect(
            device_context,
            panel.x,
            panel.y,
            panel.x + panel.width,
            panel.y + panel.height,
            12,
            self.theme.surface_alt,
            self.theme.border,
        )
        self._draw_round_rect(device_context, panel.x + 16, panel.y + 16, panel.x + 70, panel.y + 20, 4, accent, accent)
        title_rect = RECT(panel.x + 18, panel.y + 30, panel.x + panel.width - 18, panel.y + 56)
        self._draw_text(device_context, panel.title, title_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)
        if panel.subtitle:
            subtitle_rect = RECT(panel.x + 18, panel.y + 56, panel.x + panel.width - 18, panel.y + 86)
            self._draw_text(device_context, panel.subtitle, subtitle_rect, self.theme.text_secondary, "caption", DT_LEFT | DT_VCENTER)

    def _draw_card(self, device_context, card):
        accent = card.accent or self.theme.accent
        self._draw_round_rect(
            device_context,
            card.x,
            card.y,
            card.x + card.width,
            card.y + card.height,
            12,
            self.theme.surface,
            self.theme.border,
        )
        self._draw_round_rect(device_context, card.x + 16, card.y + 16, card.x + 34, card.y + 34, 8, accent, accent)
        title_rect = RECT(card.x + 44, card.y + 12, card.x + card.width - 16, card.y + 36)
        self._draw_text(device_context, card.title, title_rect, self.theme.text_secondary, "caption", DT_LEFT | DT_VCENTER)
        value_rect = RECT(card.x + 16, card.y + 42, card.x + card.width - 16, card.y + 88)
        self._draw_text(device_context, card.value, value_rect, self.theme.text_primary, "metric", DT_LEFT | DT_VCENTER)
        if card.subtitle:
            subtitle_rect = RECT(card.x + 16, card.y + card.height - 34, card.x + card.width - 16, card.y + card.height - 12)
            self._draw_text(device_context, card.subtitle, subtitle_rect, self.theme.text_secondary, "caption", DT_LEFT | DT_VCENTER)

    def _draw_grid(self, device_context, grid):
        total_rows = len(grid.rows) + 1
        grid_height = total_rows * grid.row_height + 2
        self._draw_round_rect(
            device_context,
            grid.x,
            grid.y,
            grid.x + grid.width,
            grid.y + grid_height,
            10,
            self.theme.surface,
            self.theme.border,
        )
        self._fill_rect(device_context, grid.x + 1, grid.y + 1, grid.x + grid.width - 1, grid.y + grid.row_height + 1, self.theme.surface_alt)
        column_width = max(80, (grid.width - 2) // max(1, len(grid.columns)))

        for index, column in enumerate(grid.columns):
            left = grid.x + 12 + index * column_width
            header_rect = RECT(left, grid.y + 4, left + column_width - 18, grid.y + grid.row_height)
            self._draw_text(device_context, column, header_rect, self.theme.text_secondary, "caption", DT_LEFT | DT_VCENTER)
            if index > 0:
                sep_x = grid.x + index * column_width
                self._fill_rect(device_context, sep_x, grid.y + 8, sep_x + 1, grid.y + grid_height - 8, _blend(self.theme.border, self.theme.surface, 0.2))

        for row_index, row in enumerate(grid.rows):
            row_top = grid.y + grid.row_height + row_index * grid.row_height
            self._fill_rect(device_context, grid.x + 8, row_top, grid.x + grid.width - 8, row_top + 1, _blend(self.theme.border, self.theme.surface, 0.12))
            for column_index, value in enumerate(row):
                left = grid.x + 12 + column_index * column_width
                cell_rect = RECT(left, row_top + 2, left + column_width - 18, row_top + grid.row_height)
                self._draw_text(device_context, value, cell_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)

    def _draw_chart(self, device_context, chart):
        accent = chart.accent or self.theme.accent
        self._draw_round_rect(
            device_context,
            chart.x,
            chart.y,
            chart.x + chart.width,
            chart.y + chart.height,
            12,
            self.theme.surface,
            self.theme.border,
        )
        title_rect = RECT(chart.x + 16, chart.y + 12, chart.x + chart.width - 16, chart.y + 36)
        self._draw_text(device_context, chart.title, title_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)

        plot_left = chart.x + 24
        plot_right = chart.x + chart.width - 20
        plot_top = chart.y + 52
        plot_bottom = chart.y + chart.height - 32
        self._fill_rect(device_context, plot_left, plot_bottom, plot_right, plot_bottom + 1, _blend(self.theme.border, self.theme.text_secondary, 0.1))

        if not chart.points:
            return

        max_value = max(point[1] for point in chart.points) or 1.0
        slot_width = max(24, (plot_right - plot_left) // len(chart.points))
        bar_width = max(14, slot_width - 22)

        for index, point in enumerate(chart.points):
            label, value = point
            bar_left = plot_left + index * slot_width + 10
            bar_right = min(bar_left + bar_width, plot_right - 6)
            bar_height = int((value / max_value) * max(16, plot_bottom - plot_top - 8))
            bar_top = plot_bottom - bar_height
            fill = _blend(accent, "#ffffff", 0.12 + (index % 3) * 0.12)
            self._draw_round_rect(device_context, bar_left, bar_top, bar_right, plot_bottom, 6, fill, fill)

            value_rect = RECT(bar_left - 10, bar_top - 22, bar_right + 10, bar_top - 2)
            self._draw_text(device_context, str(int(value)), value_rect, self.theme.text_secondary, "caption", DT_CENTER | DT_VCENTER)
            label_rect = RECT(bar_left - 12, plot_bottom + 8, bar_right + 12, plot_bottom + 28)
            self._draw_text(device_context, label, label_rect, self.theme.text_secondary, "caption", DT_CENTER | DT_VCENTER)

    # ------------------------------------------------------------------
    # Form controls
    # ------------------------------------------------------------------
    def _measure_text_width(self, device_context, text, role):
        if not text:
            return 0
        font = self._get_font(role)
        old_font = gdi32.SelectObject(device_context, font)
        size = SIZE()
        gdi32.GetTextExtentPoint32W(device_context, text, len(text), ctypes.byref(size))
        gdi32.SelectObject(device_context, old_font)
        return int(size.cx)

    def _draw_text_input(self, device_context, control):
        focused = control.focused
        hover = control.hover_progress
        fill = _blend(self.theme.surface, self.theme.surface_alt, 0.4 + 0.2 * hover)
        if focused:
            border = self.theme.accent
        else:
            border = _blend(self.theme.border, self.theme.text_secondary, 0.1 + hover * 0.2)
        self._draw_round_rect(
            device_context,
            control.x,
            control.y,
            control.x + control.width,
            control.y + control.height,
            8,
            fill,
            border,
        )
        display = control.value
        if control.password and display:
            display = "•" * len(display)
        text_color = self.theme.text_primary
        placeholder_color = _blend(self.theme.text_secondary, self.theme.surface_alt, 0.3)
        text_rect = RECT(control.x + 12, control.y, control.x + control.width - 12, control.y + control.height)
        if display:
            self._draw_text(device_context, display, text_rect, text_color, "body", DT_LEFT | DT_VCENTER)
        elif control.placeholder:
            self._draw_text(device_context, control.placeholder, text_rect, placeholder_color, "body", DT_LEFT | DT_VCENTER)
        if focused:
            caret_text = display[: control.caret] if display else ""
            caret_offset = self._measure_text_width(device_context, caret_text, "body")
            caret_x = control.x + 12 + caret_offset
            caret_top = control.y + 8
            caret_bottom = control.y + control.height - 8
            caret_rect = RECT(caret_x, caret_top, caret_x + 2, caret_bottom)
            brush = gdi32.CreateSolidBrush(_rgb_to_colorref(self.theme.accent))
            user32.FillRect(device_context, ctypes.byref(caret_rect), brush)
            gdi32.DeleteObject(brush)

    def _draw_checkbox(self, device_context, control):
        box_size = 20
        box_top = control.y + (control.height - box_size) // 2
        box_left = control.x
        hover = control.hover_progress
        if control.checked:
            fill = self.theme.accent
            border = _blend(self.theme.accent, "#000000", 0.1)
        else:
            fill = _blend(self.theme.surface, self.theme.surface_alt, 0.5 + hover * 0.3)
            border = _blend(self.theme.border, self.theme.accent, hover * 0.4)
        self._draw_round_rect(
            device_context,
            box_left,
            box_top,
            box_left + box_size,
            box_top + box_size,
            5,
            fill,
            border,
        )
        if control.checked:
            check_color = "#ffffff"
            check_rect = RECT(box_left, box_top, box_left + box_size, box_top + box_size)
            self._draw_text(device_context, "✓", check_rect, check_color, "button", DT_CENTER | DT_VCENTER)
        if control.label:
            label_rect = RECT(box_left + box_size + 12, control.y, control.x + control.width, control.y + control.height)
            self._draw_text(device_context, control.label, label_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)

    def _draw_switch(self, device_context, control):
        track_w = 44
        track_h = 22
        track_top = control.y + (control.height - track_h) // 2
        track_left = control.x
        if control.on:
            fill = self.theme.accent
            border = _blend(self.theme.accent, "#000000", 0.1)
        else:
            fill = _blend(self.theme.surface_alt, self.theme.border, 0.5 + control.hover_progress * 0.2)
            border = _blend(self.theme.border, self.theme.text_secondary, 0.1)
        self._draw_round_rect(
            device_context,
            track_left,
            track_top,
            track_left + track_w,
            track_top + track_h,
            track_h // 2,
            fill,
            border,
        )
        knob_size = track_h - 4
        knob_x = track_left + (track_w - knob_size - 2) if control.on else track_left + 2
        knob_y = track_top + 2
        self._draw_round_rect(
            device_context,
            knob_x,
            knob_y,
            knob_x + knob_size,
            knob_y + knob_size,
            knob_size // 2,
            "#ffffff",
            _blend("#ffffff", "#000000", 0.1),
        )
        if control.label:
            label_rect = RECT(track_left + track_w + 12, control.y, control.x + control.width, control.y + control.height)
            self._draw_text(device_context, control.label, label_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)

    def _draw_radio_group(self, device_context, control):
        for index, option in enumerate(control.options):
            row_top = control.y + index * control.item_height
            circle_size = 18
            circle_top = row_top + (control.item_height - circle_size) // 2
            circle_left = control.x
            selected = control.selected == option.key
            if selected:
                outer_fill = self.theme.accent
                outer_border = _blend(self.theme.accent, "#000000", 0.1)
            else:
                outer_fill = _blend(self.theme.surface, self.theme.surface_alt, 0.5)
                outer_border = self.theme.border
            self._draw_round_rect(
                device_context,
                circle_left,
                circle_top,
                circle_left + circle_size,
                circle_top + circle_size,
                circle_size // 2,
                outer_fill,
                outer_border,
            )
            if selected:
                inner = 8
                inner_left = circle_left + (circle_size - inner) // 2
                inner_top = circle_top + (circle_size - inner) // 2
                self._draw_round_rect(
                    device_context,
                    inner_left,
                    inner_top,
                    inner_left + inner,
                    inner_top + inner,
                    inner // 2,
                    "#ffffff",
                    "#ffffff",
                )
            label_rect = RECT(circle_left + circle_size + 12, row_top, control.x + control.width, row_top + control.item_height)
            self._draw_text(device_context, option.label, label_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)

    def _draw_slider(self, device_context, control):
        track_top = control.y + control.height // 2 - 3
        track_left = control.x + 8
        track_right = control.x + control.width - 8
        # Track background
        self._draw_round_rect(
            device_context,
            track_left,
            track_top,
            track_right,
            track_top + 6,
            3,
            _blend(self.theme.surface_alt, self.theme.border, 0.4),
            _blend(self.theme.surface_alt, self.theme.border, 0.5),
        )
        ratio = control.normalized()
        fill_right = int(track_left + (track_right - track_left) * ratio)
        if fill_right > track_left:
            self._draw_round_rect(
                device_context,
                track_left,
                track_top,
                fill_right,
                track_top + 6,
                3,
                self.theme.accent,
                self.theme.accent,
            )
        knob = 18
        knob_x = fill_right - knob // 2
        knob_y = control.y + control.height // 2 - knob // 2
        self._draw_round_rect(
            device_context,
            knob_x,
            knob_y,
            knob_x + knob,
            knob_y + knob,
            knob // 2,
            "#ffffff",
            _blend(self.theme.accent, "#000000", 0.05),
        )

    def _draw_progress(self, device_context, control):
        accent = control.accent or self.theme.accent
        ratio = max(0.0, min(1.0, control.value))
        radius = max(2, control.height // 2)
        self._draw_round_rect(
            device_context,
            control.x,
            control.y,
            control.x + control.width,
            control.y + control.height,
            radius,
            _blend(self.theme.surface_alt, self.theme.border, 0.3),
            _blend(self.theme.surface_alt, self.theme.border, 0.4),
        )
        fill_right = control.x + int(control.width * ratio)
        if fill_right > control.x:
            self._draw_round_rect(
                device_context,
                control.x,
                control.y,
                fill_right,
                control.y + control.height,
                radius,
                accent,
                accent,
            )
        if control.show_label:
            text_rect = RECT(control.x, control.y - 22, control.x + control.width, control.y - 4)
            self._draw_text(device_context, f"{int(ratio * 100)}%", text_rect, self.theme.text_secondary, "caption", DT_LEFT | DT_VCENTER)

    def _draw_dropdown(self, device_context, control):
        hover = control.hover_progress
        fill = _blend(self.theme.surface, self.theme.surface_alt, 0.4 + 0.2 * hover)
        border = _blend(self.theme.border, self.theme.accent, 0.05 + (0.4 if control.expanded else hover * 0.2))
        self._draw_round_rect(
            device_context,
            control.x,
            control.y,
            control.x + control.width,
            control.y + control.height,
            8,
            fill,
            border,
        )
        display = control.selected if control.selected else control.placeholder
        text_color = self.theme.text_primary if control.selected else _blend(self.theme.text_secondary, self.theme.surface_alt, 0.3)
        text_rect = RECT(control.x + 14, control.y, control.x + control.width - 32, control.y + control.height)
        self._draw_text(device_context, display, text_rect, text_color, "body", DT_LEFT | DT_VCENTER)
        # Caret indicator
        caret_rect = RECT(control.x + control.width - 28, control.y, control.x + control.width - 12, control.y + control.height)
        caret_glyph = "˅" if not control.expanded else "˄"
        self._draw_text(device_context, caret_glyph, caret_rect, self.theme.text_secondary, "body", DT_CENTER | DT_VCENTER)

        if not control.expanded:
            return

        left, top, right, bottom = control.panel_rect()
        self._draw_round_rect(
            device_context,
            left,
            top,
            right,
            bottom,
            10,
            self.theme.surface,
            _blend(self.theme.border, self.theme.accent, 0.2),
        )
        item_h = control.option_height()
        for idx, option in enumerate(control.options):
            row_top = top + 4 + idx * item_h
            row_rect = RECT(left + 4, row_top, right - 4, row_top + item_h)
            is_selected = option == control.selected
            if is_selected:
                self._draw_round_rect(
                    device_context,
                    left + 4,
                    row_top,
                    right - 4,
                    row_top + item_h,
                    6,
                    _blend(self.theme.accent, self.theme.surface, 0.85),
                    _blend(self.theme.accent, self.theme.surface, 0.85),
                )
            label_rect = RECT(left + 16, row_top, right - 16, row_top + item_h)
            self._draw_text(device_context, option, label_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)

    def _draw_listbox(self, dc, lb):
        self._draw_round_rect(
            dc, lb.x, lb.y, lb.x + lb.width, lb.y + lb.height,
            10, self.theme.surface, self.theme.border,
        )
        rows = lb.visible_rows()
        item_h = lb.item_height
        for offset in range(rows):
            index = lb.scroll_offset + offset
            if index >= len(lb.items):
                break
            row_top = lb.y + 4 + offset * item_h
            row_left = lb.x + 4
            row_right = lb.x + lb.width - 4
            if index == lb.selected_index:
                self._draw_round_rect(
                    dc, row_left, row_top, row_right, row_top + item_h - 2, 6,
                    _blend(self.theme.accent, self.theme.surface, 0.82),
                    _blend(self.theme.accent, self.theme.surface, 0.82),
                )
            label_rect = RECT(row_left + 12, row_top, row_right - 12, row_top + item_h)
            self._draw_text(dc, str(lb.items[index]), label_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)

        # Scroll indicator
        if lb.max_offset() > 0:
            track_x = lb.x + lb.width - 6
            track_top = lb.y + 6
            track_bottom = lb.y + lb.height - 6
            track_h = max(1, track_bottom - track_top)
            self._fill_rect(dc, track_x, track_top, track_x + 3, track_bottom,
                            _blend(self.theme.border, self.theme.surface, 0.3))
            visible_ratio = rows / max(1, len(lb.items))
            thumb_h = max(20, int(track_h * visible_ratio))
            thumb_top = track_top + int((track_h - thumb_h) * (lb.scroll_offset / max(1, lb.max_offset())))
            self._draw_round_rect(
                dc, track_x - 1, thumb_top, track_x + 4, thumb_top + thumb_h, 2,
                self.theme.accent, self.theme.accent,
            )

    def _draw_treeview(self, dc, tv):
        self._draw_round_rect(
            dc, tv.x, tv.y, tv.x + tv.width, tv.y + tv.height,
            10, self.theme.surface, self.theme.border,
        )
        flat = self._flatten_tree(tv)
        scroll = getattr(tv, "scroll_offset", 0)
        visible = max(1, (tv.height - 8) // tv.row_height)
        scroll = max(0, min(max(0, len(flat) - visible), scroll))
        tv.scroll_offset = scroll
        for offset in range(visible):
            index = scroll + offset
            if index >= len(flat):
                break
            node, depth, has_children = flat[index]
            row_top = tv.y + 4 + offset * tv.row_height
            row_left = tv.x + 4
            row_right = tv.x + tv.width - 4
            key_value = node.key if node.key is not None else node.label
            if tv.selected_key == key_value:
                self._draw_round_rect(
                    dc, row_left, row_top, row_right, row_top + tv.row_height - 2, 5,
                    _blend(self.theme.accent, self.theme.surface, 0.82),
                    _blend(self.theme.accent, self.theme.surface, 0.82),
                )
            chevron_x = tv.x + 8 + depth * 18
            if has_children:
                glyph = "▾" if node.expanded else "▸"
                chev_rect = RECT(chevron_x, row_top, chevron_x + 18, row_top + tv.row_height)
                self._draw_text(dc, glyph, chev_rect, self.theme.text_secondary, "body", DT_LEFT | DT_VCENTER)
            label_rect = RECT(chevron_x + 22, row_top, row_right - 8, row_top + tv.row_height)
            self._draw_text(dc, node.label, label_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)

    def _draw_menubar(self, dc, width):
        bar = self.menu_bar
        self._fill_rect(
            dc, bar.x, bar.y, bar.x + width, bar.y + bar.height,
            _blend(self.theme.surface_alt, self.theme.surface, 0.5),
        )
        self._fill_rect(
            dc, bar.x, bar.y + bar.height - 1, bar.x + width, bar.y + bar.height,
            self.theme.border,
        )
        cursor = bar.x + 12
        for index, menu in enumerate(bar.menus):
            w = self._menu_title_width(menu.title)
            is_open = index == bar.open_index
            is_hover = index == bar.hovered_index
            if is_open or is_hover:
                fill = _blend(self.theme.accent, self.theme.surface, 0.85 if is_hover and not is_open else 0.7)
                self._draw_round_rect(
                    dc, cursor + 2, bar.y + 4, cursor + w - 2, bar.y + bar.height - 6, 5, fill, fill,
                )
            text_color = self.theme.text_primary
            r = RECT(cursor, bar.y, cursor + w, bar.y + bar.height)
            self._draw_text(dc, menu.title, r, text_color, "button", DT_CENTER | DT_VCENTER)
            cursor += w

        # Open dropdown panel
        if bar.open_index >= 0:
            panel = self._menu_panel_rect(bar.open_index)
            if panel is not None:
                left, top, right, bottom = panel
                self._draw_round_rect(
                    dc, left, top, right, bottom, 10, self.theme.surface,
                    _blend(self.theme.border, self.theme.accent, 0.2),
                )
                items = bar.menus[bar.open_index].items
                for idx, item in enumerate(items):
                    row_top = top + 4 + idx * 30
                    label_rect = RECT(left + 14, row_top, right - 80, row_top + 30)
                    self._draw_text(dc, item.label, label_rect, self.theme.text_primary, "body", DT_LEFT | DT_VCENTER)
                    if item.shortcut:
                        sc_rect = RECT(right - 80, row_top, right - 12, row_top + 30)
                        self._draw_text(dc, item.shortcut, sc_rect, self.theme.text_secondary, "body", DT_RIGHT | DT_VCENTER)

    def _draw_tooltip(self, dc, tooltip, screen_w, screen_h):
        text = tooltip.text
        # Approximate tooltip width via measured text.
        font = self._get_font("body")
        old_font = gdi32.SelectObject(dc, font)
        size = SIZE()
        gdi32.GetTextExtentPoint32W(dc, text, len(text), ctypes.byref(size))
        gdi32.SelectObject(dc, old_font)
        pad_x, pad_y = 12, 8
        w = size.cx + pad_x * 2
        h = size.cy + pad_y * 2
        x = max(8, min(tooltip.x, screen_w - w - 8))
        y = max(8, min(tooltip.y, screen_h - h - 8))
        bg = _blend(self.theme.text_primary, "#000000", 0.05)
        self._draw_round_rect(dc, x, y, x + w, y + h, 6, bg, bg)
        rect = RECT(x + pad_x, y, x + w - pad_x, y + h)
        self._draw_text(dc, text, rect, "#ffffff", "body", DT_LEFT | DT_VCENTER)

    def _paint(self):
        paint_struct = PAINTSTRUCT()
        screen_dc = user32.BeginPaint(self.hwnd, ctypes.byref(paint_struct))
        client_rect = RECT()
        user32.GetClientRect(self.hwnd, ctypes.byref(client_rect))
        width = max(1, client_rect.right - client_rect.left)
        height = max(1, client_rect.bottom - client_rect.top)

        buffer_dc = gdi32.CreateCompatibleDC(screen_dc)
        buffer_bitmap = gdi32.CreateCompatibleBitmap(screen_dc, width, height)
        old_bitmap = gdi32.SelectObject(buffer_dc, buffer_bitmap)

        background_brush = gdi32.CreateSolidBrush(_rgb_to_colorref(self.theme.background))
        user32.FillRect(buffer_dc, ctypes.byref(client_rect), background_brush)
        gdi32.DeleteObject(background_brush)

        sidebar = self._primary_sidebar()

        if self.tab_bar is not None:
            self._draw_round_rect(buffer_dc, 14, 14, width - 14, height - 14, 18, self.theme.surface, self.theme.border)
            toolbar_fill = _blend(self.theme.surface_alt, self.theme.background, 0.45)
            self._draw_round_rect(buffer_dc, 26, 24, width - 26, 84, 12, toolbar_fill, self.theme.border)
            self._draw_round_rect(buffer_dc, 26, 82, width - 26, height - 28, 12, self.theme.surface, self.theme.border)
            self._fill_rect(buffer_dc, 38, 82, width - 38, 83, _blend(self.theme.border, self.theme.surface, 0.2))
        elif sidebar is None:
            self._draw_round_rect(buffer_dc, 14, 14, width - 14, height - 14, 18, self.theme.surface, self.theme.border)
            self._draw_round_rect(buffer_dc, 26, 24, width - 26, height - 28, 12, self.theme.surface, self.theme.border)

        if self.tab_bar is not None:
            for item in self.tab_bar.tabs:
                is_active = item.title == self.tab_bar.active_tab
                tab_top = self.tab_bar.y + (5 if is_active else 8)
                tab_bottom = self.tab_bar.y + self.tab_bar.height + (10 if is_active else 2)
                fill = self.theme.surface if is_active else _blend(toolbar_fill, self.theme.surface, 0.12 + item.hover_progress * 0.18)
                border = _blend(self.theme.border, self.theme.accent, 0.03 + item.hover_progress * 0.04)
                self._draw_round_rect(
                    buffer_dc,
                    item.x,
                    tab_top,
                    item.x + item.width,
                    tab_bottom,
                    9,
                    fill,
                    border,
                )

                if is_active:
                    self._fill_rect(buffer_dc, item.x + 1, tab_bottom - 6, item.x + item.width - 1, tab_bottom + 2, self.theme.surface)
                    self._draw_round_rect(
                        buffer_dc,
                        item.x + 14,
                        tab_top + 4,
                        item.x + item.width - 14,
                        tab_top + 7,
                        3,
                        _blend(self.theme.accent, "#ffffff", 0.08),
                        _blend(self.theme.accent, "#ffffff", 0.08),
                    )

                favicon_fill = self.theme.accent if is_active else _blend(self.theme.text_secondary, self.theme.accent, 0.1 + item.hover_progress * 0.12)
                self._draw_round_rect(buffer_dc, item.x + 14, tab_top + 11, item.x + 22, tab_top + 19, 6, favicon_fill, favicon_fill)
                if is_active:
                    self._draw_round_rect(buffer_dc, item.x + 16, tab_top + 13, item.x + 20, tab_top + 17, 4, "#ffffff", "#ffffff")

                tab_rect = RECT(item.x + 30, tab_top + 2, item.x + item.width - 26, tab_top + 28)
                tab_color = self.theme.text_primary if is_active else _blend(self.theme.text_secondary, self.theme.text_primary, 0.12 + item.hover_progress * 0.2)
                self._draw_text(buffer_dc, item.title, tab_rect, tab_color, "tab", DT_LEFT | DT_VCENTER)

                close_rect = RECT(item.x + item.width - 22, tab_top + 4, item.x + item.width - 8, tab_top + 24)
                close_color = _blend(self.theme.text_secondary, self.theme.text_primary, (0.22 if is_active else 0.05) + item.hover_progress * 0.1)
                self._draw_text(buffer_dc, "x", close_rect, close_color, "body", DT_CENTER | DT_VCENTER)

            indicator_left = int(self.tab_bar.indicator_x)
            indicator_top = self.tab_bar.y + self.tab_bar.height + 10
            indicator_right = int(self.tab_bar.indicator_x + self.tab_bar.indicator_width)
            self._draw_round_rect(buffer_dc, indicator_left, indicator_top, indicator_right, indicator_top + 3, 3, self.theme.accent, self.theme.accent)

        for nav_bar in self.collapsible_nav_bars:
            if self._is_control_visible(nav_bar):
                self._draw_collapsible_nav_bar(buffer_dc, nav_bar)

        for nav_bar in self.nav_bars:
            if self._is_control_visible(nav_bar):
                self._draw_nav_bar(buffer_dc, nav_bar)

        for panel in self.panels:
            if self._is_control_visible(panel):
                self._draw_panel(buffer_dc, panel)

        self._resolve_card_overlaps()
        for card in self.cards:
            if self._is_control_visible(card):
                self._draw_card(buffer_dc, card)

        for grid in self.grids:
            if self._is_control_visible(grid):
                self._draw_grid(buffer_dc, grid)

        for chart in self.charts:
            if self._is_control_visible(chart):
                self._draw_chart(buffer_dc, chart)

        for progress in self.progress_bars:
            if self._is_control_visible(progress):
                self._draw_progress(buffer_dc, progress)

        for radio_group in self.radio_groups:
            if self._is_control_visible(radio_group):
                self._draw_radio_group(buffer_dc, radio_group)

        for checkbox in self.checkboxes:
            if self._is_control_visible(checkbox):
                self._draw_checkbox(buffer_dc, checkbox)

        for switch in self.switches:
            if self._is_control_visible(switch):
                self._draw_switch(buffer_dc, switch)

        for slider in self.sliders:
            if self._is_control_visible(slider):
                self._draw_slider(buffer_dc, slider)

        for text_input in self.text_inputs:
            if self._is_control_visible(text_input):
                self._draw_text_input(buffer_dc, text_input)

        for label in self.labels:
            if not self._is_control_visible(label):
                continue
            label_rect = RECT(label.x, label.y, label.x + label.width, label.y + label.height)
            color = label.color or (self.theme.text_primary if label.style == "title" else self.theme.text_secondary)
            if label.style == "body":
                color = label.color or self.theme.text_primary
            self._draw_text(buffer_dc, label.text, label_rect, color, label.style, DT_LEFT | DT_VCENTER)

        for button in self.buttons:
            if not self._is_control_visible(button):
                continue
            is_primary = button.accent is not None and button.background is None
            if is_primary:
                fill = _blend(button.accent, "#ffffff", 0.08 - button.hover_progress * 0.05)
                border = _blend(button.accent, "#000000", 0.08)
                text_color = "#ffffff"
            else:
                fill = button.background or self.theme.button_face
                fill = _blend(fill, self.theme.button_hover, button.hover_progress * 0.85)
                border = _blend(button.border or self.theme.button_border, self.theme.text_secondary, button.hover_progress * 0.08)
                text_color = button.foreground or self.theme.button_text
            self._draw_round_rect(
                buffer_dc,
                button.x,
                button.y,
                button.x + button.width,
                button.y + button.height,
                8,
                fill,
                border,
            )
            text_rect = RECT(button.x + 12, button.y, button.x + button.width - 12, button.y + button.height)
            self._draw_text(buffer_dc, button.text, text_rect, text_color, "button", DT_CENTER | DT_VCENTER)

        # Dropdowns paint last so collapsed headers + expanded popups overlay everything else.
        for dropdown in self.dropdowns:
            if self._is_control_visible(dropdown):
                self._draw_dropdown(buffer_dc, dropdown)

        for lb in self.list_boxes:
            if self._is_control_visible(lb):
                self._draw_listbox(buffer_dc, lb)

        for tv in self.tree_views:
            if self._is_control_visible(tv):
                self._draw_treeview(buffer_dc, tv)

        if self.menu_bar is not None:
            self._draw_menubar(buffer_dc, width)

        if self._tooltip.visible and self._tooltip.text:
            self._draw_tooltip(buffer_dc, self._tooltip, width, height)

        gdi32.BitBlt(screen_dc, 0, 0, width, height, buffer_dc, 0, 0, SRCCOPY)
        gdi32.SelectObject(buffer_dc, old_bitmap)
        gdi32.DeleteObject(buffer_bitmap)
        gdi32.DeleteDC(buffer_dc)
        user32.EndPaint(self.hwnd, ctypes.byref(paint_struct))

    def add_label(self, text="Label", x=24, y=24, width=460, height=34, color=None, style="body", tab=None):
        label = Label(text=text, x=x, y=y, width=width, height=height, color=color, style=style, tab=tab)
        self.labels.append(label)
        self.invalidate()
        return label

    def add_nav_bar(self, title, x=24, y=96, width=640, height=54, subtitle=None, actions=None, tab=None):
        nav_actions = actions or []
        normalized_actions = [action if isinstance(action, NavAction) else NavAction(**action) if isinstance(action, dict) else NavAction(text=str(action)) for action in nav_actions]
        nav_bar = NavBar(title=title, x=x, y=y, width=width, height=height, subtitle=subtitle, actions=normalized_actions, tab=tab)
        self.nav_bars.append(nav_bar)
        self.invalidate()
        return nav_bar

    def add_collapsible_nav_bar(
        self,
        title,
        items,
        x=52,
        y=212,
        width=248,
        collapsed_width=76,
        height=440,
        selected_key=None,
        collapsed=False,
        tab=None,
    ):
        normalized_items = []
        for item in items:
            if isinstance(item, NavEntry):
                normalized_items.append(item)
            elif isinstance(item, dict):
                normalized_items.append(NavEntry(**item))
            else:
                normalized_items.append(NavEntry(key=str(item), title=str(item)))

        nav_bar = CollapsibleNavBar(
            title=title,
            x=x,
            y=y,
            width=width,
            collapsed_width=collapsed_width,
            height=height,
            items=normalized_items,
            selected_key=selected_key or (normalized_items[0].key if normalized_items else None),
            collapsed=collapsed,
            tab=tab,
        )
        self.collapsible_nav_bars.append(nav_bar)
        self.invalidate()
        return nav_bar

    def add_panel(self, title, x=24, y=160, width=320, height=220, subtitle=None, accent=None, tab=None):
        panel = Panel(title=title, x=x, y=y, width=width, height=height, subtitle=subtitle, accent=accent, tab=tab)
        self.panels.append(panel)
        self.invalidate()
        return panel

    def add_card(self, title, value, x=24, y=160, width=220, height=120, subtitle=None, accent=None, tab=None, collision_safety=True):
        card = Card(title=title, value=value, x=x, y=y, width=width, height=height, subtitle=subtitle, accent=accent, tab=tab, collision_safety=collision_safety)
        self.cards.append(card)
        self.invalidate()
        return card

    def set_card_collision_safety(self, enabled, card=None):
        """Enable or disable overlap protection for a specific card or all cards."""
        if card is not None:
            card.collision_safety = bool(enabled)
        else:
            for existing in self.cards:
                existing.collision_safety = bool(enabled)
        self.invalidate()

    def add_grid(self, columns, rows, x=24, y=160, width=520, row_height=34, tab=None):
        grid = Grid(columns=columns, rows=rows, x=x, y=y, width=width, row_height=row_height, tab=tab)
        self.grids.append(grid)
        self.invalidate()
        return grid

    def add_chart(self, title, points, x=24, y=160, width=360, height=240, accent=None, tab=None):
        chart = Chart(title=title, points=points, x=x, y=y, width=width, height=height, accent=accent, tab=tab)
        self.charts.append(chart)
        self.invalidate()
        return chart

    def add_button(
        self,
        text="Button",
        command=None,
        x=24,
        y=72,
        width=180,
        height=44,
        background=None,
        foreground=None,
        border=None,
        accent=None,
        tab=None,
        tooltip=None,
    ):
        button = Button(
            text=text,
            x=x,
            y=y,
            width=width,
            height=height,
            command=command,
            background=background,
            foreground=foreground,
            border=border,
            accent=accent,
            tab=tab,
            tooltip=tooltip,
        )
        self.buttons.append(button)
        self.invalidate()
        return button

    def add_tabs(self, tabs, x=24, y=24, width=420, height=46, on_change=None):
        items = [TabItem(title=title) for title in tabs]
        active = tabs[0] if tabs else None
        self.tab_bar = TabBar(tabs=items, x=x, y=y, width=width, height=height, active_tab=active, on_change=on_change)
        self._layout_tabs()
        self.invalidate()
        return self.tab_bar

    def add_text_input(self, value="", placeholder="", x=24, y=24, width=240, height=36, on_change=None, on_submit=None, password=False, max_length=None, tab=None):
        control = TextInput(
            value=value, placeholder=placeholder, x=x, y=y, width=width, height=height,
            on_change=on_change, on_submit=on_submit, password=password, max_length=max_length, tab=tab,
            caret=len(value),
        )
        self.text_inputs.append(control)
        self.invalidate()
        return control

    def add_checkbox(self, label="", checked=False, x=24, y=24, width=220, height=28, on_change=None, tab=None):
        control = Checkbox(label=label, checked=checked, x=x, y=y, width=width, height=height, on_change=on_change, tab=tab)
        self.checkboxes.append(control)
        self.invalidate()
        return control

    def add_switch(self, label="", on=False, x=24, y=24, width=220, height=28, on_change=None, tab=None):
        control = Switch(label=label, on=on, x=x, y=y, width=width, height=height, on_change=on_change, tab=tab)
        self.switches.append(control)
        self.invalidate()
        return control

    def add_radio_group(self, options, selected=None, x=24, y=24, width=240, item_height=28, on_change=None, tab=None):
        normalized = []
        for option in options:
            if isinstance(option, RadioOption):
                normalized.append(option)
            elif isinstance(option, dict):
                normalized.append(RadioOption(key=option.get("key", option.get("value", option.get("label", ""))), label=option.get("label", "")))
            elif isinstance(option, tuple) and len(option) == 2:
                normalized.append(RadioOption(key=option[0], label=option[1]))
            else:
                key = str(option)
                normalized.append(RadioOption(key=key, label=key))
        control = RadioGroup(options=normalized, selected=selected, x=x, y=y, width=width, item_height=item_height, on_change=on_change, tab=tab)
        self.radio_groups.append(control)
        self.invalidate()
        return control

    def add_slider(self, value=0.0, minimum=0.0, maximum=100.0, step=0.0, x=24, y=24, width=240, height=36, on_change=None, tab=None):
        control = Slider(
            value=max(minimum, min(maximum, value)),
            minimum=minimum, maximum=maximum, step=step,
            x=x, y=y, width=width, height=height, on_change=on_change, tab=tab,
        )
        self.sliders.append(control)
        self.invalidate()
        return control

    def add_dropdown(self, options, selected=None, placeholder="Select...", x=24, y=24, width=240, height=36, on_change=None, tab=None):
        control = Dropdown(
            options=list(options), selected=selected, placeholder=placeholder,
            x=x, y=y, width=width, height=height, on_change=on_change, tab=tab,
        )
        self.dropdowns.append(control)
        self.invalidate()
        return control

    def add_progress_bar(self, value=0.0, x=24, y=24, width=240, height=8, accent=None, show_label=False, tab=None):
        control = ProgressBar(value=value, x=x, y=y, width=width, height=height, accent=accent, show_label=show_label, tab=tab)
        self.progress_bars.append(control)
        self.invalidate()
        return control

    def add_list_box(self, items, selected_index=-1, x=24, y=24, width=280, height=220,
                     item_height=28, on_change=None, tab=None, tooltip=None):
        control = ListBox(
            items=list(items), selected_index=selected_index, x=x, y=y, width=width, height=height,
            item_height=item_height, on_change=on_change, tab=tab, tooltip=tooltip,
        )
        self.list_boxes.append(control)
        self.invalidate()
        return control

    def add_tree_view(self, nodes, selected_key=None, x=24, y=24, width=300, height=280,
                      row_height=26, on_select=None, tab=None, tooltip=None):
        normalized = [self._normalize_tree_node(n) for n in nodes]
        control = TreeView(
            nodes=normalized, selected_key=selected_key, x=x, y=y, width=width, height=height,
            row_height=row_height, on_select=on_select, tab=tab, tooltip=tooltip,
        )
        control.scroll_offset = 0
        self.tree_views.append(control)
        self.invalidate()
        return control

    def _normalize_tree_node(self, node):
        if isinstance(node, TreeNode):
            node.children = [self._normalize_tree_node(c) for c in node.children]
            return node
        if isinstance(node, dict):
            return TreeNode(
                label=node.get("label", ""),
                key=node.get("key"),
                children=[self._normalize_tree_node(c) for c in node.get("children", [])],
                expanded=node.get("expanded", True),
            )
        if isinstance(node, str):
            return TreeNode(label=node, key=node)
        if isinstance(node, tuple):
            label = node[0]
            children = node[1] if len(node) > 1 else []
            return TreeNode(label=label, key=label,
                            children=[self._normalize_tree_node(c) for c in children])
        raise TypeError(f"Unsupported tree node type: {type(node)!r}")

    def add_menu_bar(self, menus, x=0, y=0, height=36):
        norm_menus = []
        for entry in menus:
            if isinstance(entry, Menu):
                norm_menus.append(entry)
                continue
            if isinstance(entry, tuple):
                title, items = entry[0], entry[1]
            elif isinstance(entry, dict):
                title, items = entry.get("title", ""), entry.get("items", [])
            else:
                raise TypeError(f"Unsupported menu entry type: {type(entry)!r}")
            norm_items = []
            for item in items:
                if isinstance(item, MenuItem):
                    norm_items.append(item)
                elif isinstance(item, dict):
                    norm_items.append(MenuItem(
                        label=item.get("label", ""),
                        command=item.get("command"),
                        shortcut=item.get("shortcut"),
                    ))
                elif isinstance(item, tuple):
                    norm_items.append(MenuItem(
                        label=item[0],
                        command=item[1] if len(item) > 1 else None,
                        shortcut=item[2] if len(item) > 2 else None,
                    ))
                elif isinstance(item, str):
                    norm_items.append(MenuItem(label=item))
                else:
                    raise TypeError(f"Unsupported menu item: {type(item)!r}")
            norm_menus.append(Menu(title=title, items=norm_items))
        self.menu_bar = MenuBar(menus=norm_menus, x=x, y=y, height=height)
        self.invalidate()
        return self.menu_bar

    def add_accelerator(self, key, callback, ctrl=False, shift=False, alt=False, description=None):
        """Register a keyboard shortcut. ``key`` is a virtual-key code or a single character."""
        if isinstance(key, str) and len(key) == 1:
            vk = ord(key.upper())
        else:
            vk = int(key)
        modifiers = (MOD_CTRL if ctrl else 0) | (MOD_SHIFT if shift else 0) | (MOD_ALT if alt else 0)
        acc = Accelerator(vk=vk, modifiers=modifiers, callback=callback, description=description)
        self._accelerators.append(acc)
        return acc

    def message_box(self, text, title="Message", style="info", buttons="ok"):
        """Show a Win32 native modal message box. Returns the clicked button id."""
        flag = {
            "info": MB_ICONINFORMATION,
            "warning": MB_ICONWARNING,
            "error": MB_ICONERROR,
            "question": MB_ICONQUESTION,
            "none": 0,
        }.get(style, MB_ICONINFORMATION)
        flag |= {
            "ok": MB_OK,
            "okcancel": MB_OKCANCEL,
            "yesno": MB_YESNO,
            "yesnocancel": MB_YESNOCANCEL,
        }.get(buttons, MB_OK)
        return user32.MessageBoxW(self.hwnd, str(text), str(title), flag)

    def set_active_tab(self, tab_name):
        if self.tab_bar is None or tab_name == self.tab_bar.active_tab:
            return

        self.tab_bar.active_tab = tab_name
        self._layout_tabs()
        if self.tab_bar.on_change is not None:
            self.tab_bar.on_change(tab_name)
        self.invalidate()

    def set_theme(
        self,
        background="#f3f3f3",
        surface="#ffffff",
        accent="#005fb8",
        text_primary="#1f1f1f",
        text_secondary="#616161",
    ):
        self.theme = Theme(
            background=background,
            surface=surface,
            surface_alt=_blend(surface, background, 0.58),
            accent=accent,
            accent_soft=_blend(accent, "#ffffff", 0.84),
            text_primary=text_primary,
            text_secondary=text_secondary,
            border=_blend(background, text_secondary, 0.16),
            button_face=_blend(surface, background, 0.24),
            button_hover=_blend(background, surface, 0.2),
            button_border=_blend(background, text_secondary, 0.22),
            button_text=text_primary,
        )
        self.invalidate()
        return self

    def invalidate(self):
        if getattr(self, "hwnd", None):
            user32.InvalidateRect(self.hwnd, None, True)

    def destroy(self):
        hwnd = getattr(self, "hwnd", None)
        if hwnd and user32.IsWindow(hwnd):
            user32.DestroyWindow(hwnd)

    def mainloop(self):
        message = MSG()
        while user32.GetMessageW(ctypes.byref(message), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(message))
            user32.DispatchMessageW(ctypes.byref(message))
        return int(message.wParam)


def create_window(title="GUIpi26 Window", width=800, height=600):
    """Create and return a Windows-native application window."""

    return Window(title=title, width=width, height=height)


def create_label(root, text="Label", x=24, y=24, width=460, height=34, color=None, style="body", tab=None):
    """Create a custom-rendered label on the given GUIpi26 window."""

    return root.add_label(text=text, x=x, y=y, width=width, height=height, color=color, style=style, tab=tab)


def create_button(
    root,
    text="Button",
    command=None,
    x=24,
    y=72,
    width=180,
    height=44,
    background=None,
    foreground=None,
    border=None,
    accent=None,
    tab=None,
    tooltip=None,
):
    """Create a custom-rendered button on the given GUIpi26 window."""

    return root.add_button(
        text=text,
        command=command,
        x=x,
        y=y,
        width=width,
        height=height,
        background=background,
        foreground=foreground,
        border=border,
        accent=accent,
        tab=tab,
        tooltip=tooltip,
    )


def create_nav_bar(root, title, x=24, y=96, width=640, height=54, subtitle=None, actions=None, tab=None):
    """Create a custom-rendered navigation bar on the given GUIpi26 window."""

    return root.add_nav_bar(title=title, x=x, y=y, width=width, height=height, subtitle=subtitle, actions=actions, tab=tab)


def create_panel(root, title, x=24, y=160, width=320, height=220, subtitle=None, accent=None, tab=None):
    """Create a custom-rendered panel on the given GUIpi26 window."""

    return root.add_panel(title=title, x=x, y=y, width=width, height=height, subtitle=subtitle, accent=accent, tab=tab)


def create_card(root, title, value, x=24, y=160, width=220, height=120, subtitle=None, accent=None, tab=None, collision_safety=True):
    """Create a custom-rendered card on the given GUIpi26 window."""

    return root.add_card(title=title, value=value, x=x, y=y, width=width, height=height, subtitle=subtitle, accent=accent, tab=tab, collision_safety=collision_safety)


def create_grid(root, columns, rows, x=24, y=160, width=520, row_height=34, tab=None):
    """Create a custom-rendered data grid on the given GUIpi26 window."""

    return root.add_grid(columns=columns, rows=rows, x=x, y=y, width=width, row_height=row_height, tab=tab)


def create_chart(root, title, points, x=24, y=160, width=360, height=240, accent=None, tab=None):
    """Create a custom-rendered chart on the given GUIpi26 window."""

    return root.add_chart(title=title, points=points, x=x, y=y, width=width, height=height, accent=accent, tab=tab)


def create_collapsible_nav_bar(
    root,
    title,
    items,
    x=52,
    y=212,
    width=248,
    collapsed_width=76,
    height=440,
    selected_key=None,
    collapsed=False,
    tab=None,
):
    """Create a collapsible side navigation bar on the given GUIpi26 window."""

    return root.add_collapsible_nav_bar(
        title=title,
        items=items,
        x=x,
        y=y,
        width=width,
        collapsed_width=collapsed_width,
        height=height,
        selected_key=selected_key,
        collapsed=collapsed,
        tab=tab,
    )


def create_horizontal_grid(x, y, width, columns, height, gap=16):
    """Create a horizontal layout grid and return its calculated cells."""

    if columns <= 0:
        raise ValueError("columns must be greater than 0")

    cell_width = int((width - gap * (columns - 1)) / columns)
    cells = []
    for index in range(columns):
        cell_x = x + index * (cell_width + gap)
        cells.append(LayoutCell(cell_x, y, cell_width, height))
    return HorizontalGrid(x=x, y=y, width=width, item_width=cell_width, height=height, gap=gap, cells=cells)


def create_vertical_grid(x, y, width, rows, item_height, gap=16):
    """Create a vertical layout grid and return its calculated cells."""

    if rows <= 0:
        raise ValueError("rows must be greater than 0")

    cells = []
    for index in range(rows):
        cell_y = y + index * (item_height + gap)
        cells.append(LayoutCell(x, cell_y, width, item_height))
    return VerticalGrid(x=x, y=y, width=width, item_height=item_height, gap=gap, cells=cells)


def create_tabs(root, tabs, x=24, y=24, width=420, height=46, on_change=None):
    """Create a custom tab strip for the given GUIpi26 window."""

    return root.add_tabs(tabs=tabs, x=x, y=y, width=width, height=height, on_change=on_change)


def set_theme(
    root,
    background="#f3f3f3",
    surface="#ffffff",
    accent="#005fb8",
    text_primary="#1f1f1f",
    text_secondary="#616161",
):
    """Apply a modern theme to the GUIpi26 window."""

    return root.set_theme(
        background=background,
        surface=surface,
        accent=accent,
        text_primary=text_primary,
        text_secondary=text_secondary,
    )


def create_text_input(root, value="", placeholder="", x=24, y=24, width=240, height=36, on_change=None, on_submit=None, password=False, max_length=None, tab=None):
    """Create a single-line text input."""
    return root.add_text_input(value=value, placeholder=placeholder, x=x, y=y, width=width, height=height, on_change=on_change, on_submit=on_submit, password=password, max_length=max_length, tab=tab)


def create_checkbox(root, label="", checked=False, x=24, y=24, width=220, height=28, on_change=None, tab=None):
    """Create a checkbox toggle."""
    return root.add_checkbox(label=label, checked=checked, x=x, y=y, width=width, height=height, on_change=on_change, tab=tab)


def create_switch(root, label="", on=False, x=24, y=24, width=220, height=28, on_change=None, tab=None):
    """Create a modern on/off switch."""
    return root.add_switch(label=label, on=on, x=x, y=y, width=width, height=height, on_change=on_change, tab=tab)


def create_radio_group(root, options, selected=None, x=24, y=24, width=240, item_height=28, on_change=None, tab=None):
    """Create a radio button group with mutually-exclusive options."""
    return root.add_radio_group(options=options, selected=selected, x=x, y=y, width=width, item_height=item_height, on_change=on_change, tab=tab)


def create_slider(root, value=0.0, minimum=0.0, maximum=100.0, step=0.0, x=24, y=24, width=240, height=36, on_change=None, tab=None):
    """Create a draggable numeric slider."""
    return root.add_slider(value=value, minimum=minimum, maximum=maximum, step=step, x=x, y=y, width=width, height=height, on_change=on_change, tab=tab)


def create_dropdown(root, options, selected=None, placeholder="Select...", x=24, y=24, width=240, height=36, on_change=None, tab=None):
    """Create a dropdown / select control with a popup option list."""
    return root.add_dropdown(options=options, selected=selected, placeholder=placeholder, x=x, y=y, width=width, height=height, on_change=on_change, tab=tab)


def create_progress_bar(root, value=0.0, x=24, y=24, width=240, height=8, accent=None, show_label=False, tab=None):
    """Create a non-interactive progress bar (value range 0.0 .. 1.0)."""
    return root.add_progress_bar(value=value, x=x, y=y, width=width, height=height, accent=accent, show_label=show_label, tab=tab)


def create_list_box(root, items, selected_index=-1, x=24, y=24, width=280, height=220,
                    item_height=28, on_change=None, tab=None, tooltip=None):
    """Create a vertically scrolling list box with single-row selection."""
    return root.add_list_box(items=items, selected_index=selected_index, x=x, y=y,
                             width=width, height=height, item_height=item_height,
                             on_change=on_change, tab=tab, tooltip=tooltip)


def create_tree_view(root, nodes, selected_key=None, x=24, y=24, width=300, height=280,
                     row_height=26, on_select=None, tab=None, tooltip=None):
    """Create a hierarchical tree view with collapsible nodes."""
    return root.add_tree_view(nodes=nodes, selected_key=selected_key, x=x, y=y,
                              width=width, height=height, row_height=row_height,
                              on_select=on_select, tab=tab, tooltip=tooltip)


def create_menu_bar(root, menus, x=0, y=0, height=36):
    """Create a top horizontal menu bar with cascading dropdown panels."""
    return root.add_menu_bar(menus=menus, x=x, y=y, height=height)


def create_accelerator(root, key, callback, ctrl=False, shift=False, alt=False, description=None):
    """Register a keyboard shortcut on the window."""
    return root.add_accelerator(key=key, callback=callback, ctrl=ctrl, shift=shift, alt=alt, description=description)


def show_message_box(root, text, title="Message", style="info", buttons="ok"):
    """Show a Win32 native modal message box. Returns the clicked button id."""
    return root.message_box(text=text, title=title, style=style, buttons=buttons)