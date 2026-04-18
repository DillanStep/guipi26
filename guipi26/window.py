# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 2026

@author: dillan stephenson
"""

from dataclasses import dataclass
import ctypes
from ctypes import wintypes
from typing import List, Optional, Tuple


user32 = ctypes.WinDLL("user32", use_last_error=True)
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

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
WM_LBUTTONUP = 0x0202
WM_MOUSELEAVE = 0x02A3
WM_MOUSEMOVE = 0x0200
WM_PAINT = 0x000F
WM_SIZE = 0x0005
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_VISIBLE = 0x10000000


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
        self.tab_bar = None
        self._font_cache = {}
        self._tracking_mouse = False
        self._hovered_button = None
        self._hovered_tab = None
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
            self._update_hover_state(_get_x_lparam(l_param), _get_y_lparam(l_param))
            return 0

        if message == WM_MOUSELEAVE:
            self._tracking_mouse = False
            self._update_hover_state(-1, -1)
            return 0

        if message == WM_LBUTTONUP:
            self._handle_click(_get_x_lparam(l_param), _get_y_lparam(l_param))
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

        for button in self.buttons:
            if self._is_control_visible(button) and button.contains(x_pos, y_pos):
                hovered_button = button
            button.hover_target = 1.0 if button is hovered_button else 0.0
            button.hover_progress = button.hover_target

        if self.tab_bar is not None:
            for item in self.tab_bar.tabs:
                if item.contains(self.tab_bar, x_pos, y_pos):
                    hovered_tab = item
                item.hover_target = 1.0 if item is hovered_tab else 0.0
                item.hover_progress = item.hover_target

        if hovered_button is not self._hovered_button or hovered_tab is not self._hovered_tab:
            self._hovered_button = hovered_button
            self._hovered_tab = hovered_tab
            self.invalidate()

    def _handle_click(self, x_pos, y_pos):
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

        for button in reversed(self.buttons):
            if self._is_control_visible(button) and button.contains(x_pos, y_pos):
                if button.command is not None:
                    button.command()
                self.invalidate()
                return

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