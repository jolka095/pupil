import collections
import typing as T

from glfw import (
    glfwGetMonitors,
    glfwGetMonitorName,
    glfwGetPrimaryMonitor,
    glfwGetVideoMode,
)

try:
    from typing import OrderedDict as T_OrderedDict  # Python 3.7.2
except ImportError:

    class T_OrderedDict(collections.OrderedDict, T.MutableMapping[T.KT, T.VT]):
        pass


class GUIMonitor:
    """
    Wrapper class for monitor related GLFW API.
    """

    VideoMode = T.NamedTuple(
        "VideoMode",
        [
            ("width", int),
            ("height", int),
            ("red_bits", int),
            ("green_bits", int),
            ("blue_bits", int),
            ("refresh_rate", int),
        ],
    )

    __slots__ = ("__gl_handle", "__name", "__index")

    def __init__(self, index, gl_handle):
        self.__gl_handle = gl_handle
        self.__name = glfwGetMonitorName(gl_handle).decode("utf-8")
        self.__index = index

    @property
    def unsafe_handle(self):
        return self.__gl_handle

    @property
    def name(self) -> str:
        tag = "PRIMARY" if self.__index == 0 else str(self.__index)
        return f"{self.__name} [{tag}]"

    @property
    def size(self) -> T.Tuple[int, int]:
        mode = self.current_video_mode
        return (mode.width, mode.height)

    @property
    def refresh_rate(self) -> int:
        mode = self.current_video_mode
        return mode.refresh_rate

    @property
    def current_video_mode(self) -> "GUIMonitor.VideoMode":
        gl_video_mode = glfwGetVideoMode(self.__gl_handle)
        return GUIMonitor.VideoMode(*gl_video_mode)

    @property
    def is_available(self) -> bool:
        return GUIMonitor.find_monitor_by_name(self.name) is not None

    @staticmethod
    def currently_connected_monitors() -> T.List["GUIMonitor"]:
        return [GUIMonitor(i, h) for i, h in enumerate(glfwGetMonitors())]

    @staticmethod
    def currently_connected_monitors_by_name() -> T_OrderedDict[str, "GUIMonitor"]:
        return collections.OrderedDict(
            (m.name, m) for m in GUIMonitor.currently_connected_monitors()
        )

    @staticmethod
    def primary_monitor() -> "GUIMonitor":
        gl_handle = glfwGetPrimaryMonitor()
        return GUIMonitor(0, gl_handle)

    @staticmethod
    def find_monitor_by_name(name: str) -> T.Optional["GUIMonitor"]:
        monitors = GUIMonitor.currently_connected_monitors_by_name()
        return monitors.get(name, None)
