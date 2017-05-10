# -- coding: utf-8 --

from ..data import icon


def notify(title, message, timeout=5, icon_path=icon.ico, retcode=None):
    """
    Optional parameters:
        * ``icon`` - path to an ICO file to display instead of the ntfy icon
    """
    import win32api
    import win32gui
    import win32con
    import os
    import time

    class WindowsBalloonTip:
        """
        http://stackoverflow.com/a/17262942
        """

        def __init__(self, title, msg, timeout, icon_path):
            message_map = {win32con.WM_DESTROY: self.OnDestroy, }

            # Register the window class.
            wc = win32gui.WNDCLASS()
            hinst = wc.hInstance = win32api.GetModuleHandle(None)
            wc.lpszClassName = 'PythonTaskbar'
            wc.lpfnWndProc = message_map  # could also specify a wndproc.
            class_atom = win32gui.RegisterClass(wc)

            # Create the window.
            style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
            self.hwnd = win32gui.CreateWindow(class_atom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT,
                                              win32con.CW_USEDEFAULT,
                                              0, 0, hinst, None)
            win32gui.UpdateWindow(self.hwnd)

            # Icons management
            icon_path_name = os.path.abspath(icon_path)
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            try:
                hicon = win32gui.LoadImage(hinst, icon_path_name, win32con.IMAGE_ICON, 0, 0, icon_flags)
            except Exception as e:
                print(str(e))
                hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
            flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
            nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, 'Tooltip')

            # Notify
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
            win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY,
                                      (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER + 20, hicon, 'Balloon Tooltip',
                                       msg, 200, title))
            time.sleep(timeout)

            # Destroy
            win32gui.DestroyWindow(self.hwnd)
            win32gui.UnregisterClass(class_atom, hinst)

        def OnDestroy(self, hwnd, msg, wparam, lparam):
            # nid = (self.hwnd, 0)
            # win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
            win32gui.PostQuitMessage(0)  # Terminate the app.

    WindowsBalloonTip(title, message, timeout, icon_path)
