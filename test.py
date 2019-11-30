import pywinauto
dsk = pywinauto.Desktop(backend='uia')
explorer = pywinauto.Application().connect(path='explorer.exe')


# import pywinauto
# from pywinauto import Application
# app = Application().connect(title_re=".*Notepad", class_name="Notepad")

import win32gui


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


if __name__ == "__main__":
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    # for i in top_windows:
    #     if "notepad" in i[1].lower():
    #         print
    #         i
    #         win32gui.ShowWindow(i[0], 5)
    #         win32gui.SetForegroundWindow(i[0])
    #         break


dsk = pywinauto.Desktop(backend='uia')
explorer = pywinauto.Application().Connect(path='explorer.exe')

# chain actions: set focus and right click after that
explorer.Video.MyHomeVideos.set_focus().click_input(button='right')