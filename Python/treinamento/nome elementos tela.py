import pygetwindow as gw

def list_open_windows():
    return [win.title for win in gw.getAllWindows() if win.title]

if __name__ == "__main__":
    print(list_open_windows())
