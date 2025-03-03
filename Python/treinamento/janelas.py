from pywinauto import Desktop

def list_open_windows():
    """Lista todas as janelas abertas no Windows."""
    windows = Desktop(backend="uia").windows()
    for win in windows:
        print(f"🔹 {win.window_text()}")

if __name__ == "__main__":
    list_open_windows()
