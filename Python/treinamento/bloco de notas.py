import pyautogui
import time
import os

def open_notepad_and_write():
    os.system("notepad.exe")
    time.sleep(2)
    pyautogui.write("Olá, este é um teste de automação!", interval=0.1)
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)
    pyautogui.write("teste.txt")
    pyautogui.press("enter")

if __name__ == "__main__":
    open_notepad_and_write()
