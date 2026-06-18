import ctypes
import ctypes.wintypes
import win32process
import win32api
import win32con
import win32ui
import psutil
import time

PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_NAME = "RobloxPlayerBeta.exe"

class Memory:
    def __init__(self):
        self.pid = None
        self.handle = None
        self._find_process()

    def _find_process(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == PROCESS_NAME.lower():
                self.pid = proc.info['pid']
                break
        if not self.pid:
            raise Exception(f"Process {PROCESS_NAME} not found")
        self.handle = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)

    def read_memory(self, address, size=4):
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        if not ctypes.windll.kernel32.ReadProcessMemory(self.handle, address, buffer, size, ctypes.byref(bytes_read)):
            raise Exception("ReadProcessMemory failed")
        return buffer.raw

    def write_memory(self, address, value, size=4):
        buffer = ctypes.c_void_p(value)
        bytes_written = ctypes.c_size_t()
        if not ctypes.windll.kernel32.WriteProcessMemory(self.handle, address, buffer, size, ctypes.byref(bytes_written)):
            raise Exception("WriteProcessMemory failed")

    def read_int(self, address):
        return int.from_bytes(self.read_memory(address, 4), byteorder='little')

    def write_int(self, address, value):
        self.write_memory(address, value, 4)

    def read_float(self, address):
        return ctypes.c_float.from_buffer_copy(self.read_memory(address, 4)).value

    def write_float(self, address, value):
        self.write_memory(address, ctypes.c_float(value).value, 4)
