import pyautogui as pg
import os
import datetime
from PIL import ImageGrab
from time import sleep as t
import time

INTERVAL = 0.02
CONFIDENCE = 0.7
TARGET_CONTACT = 'romain'

def locate_move_click(image: str):
    target = pg.locateOnScreen(image, confidence=CONFIDENCE)
    if target:
        pg.moveTo(x=target.left / 2 + target.width / 4, y=target.top / 2 + target.height / 4, duration=0.2)
        t(0.1)
        pg.click()
        t(0.1)
    else:
        print('Target icon not found: {}'.format(image))
        exit(1)
    pass

def open_wechat():
    pg.hotkey('command', 'space', interval=INTERVAL)
    pg.typewrite('wechat\n\n', interval=INTERVAL)

def find_wechat_contact(contact: str):
    pg.hotkey('command', 'f', interval=INTERVAL)
    pg.typewrite(contact, interval=INTERVAL)
    t(2)
    pg.press('enter')
    emoji = pg.locateOnScreen('icons/emoji.png', confidence=0.9)
    pg.moveTo(emoji.left / 2 + 20, emoji.top / 2 + 50, duration=2 * INTERVAL)
    pg.click()

def take_window_screenshot_to_clipboard(save_name: str):
    pg.hotkey('command', 'shift', '5', interval=INTERVAL)
    t(INTERVAL)
    pg.keyDown('ctrl')
    t(INTERVAL)
    pg.click()
    t(INTERVAL)
    pg.keyUp('ctrl')
    if save_name:
        image = ImageGrab.grabclipboard()
        image.save(f'output/{save_name}-{datetime.datetime.now().strftime("%y%m%d%H%M%S")}.png')

def main():
    start = time.time()
    print('Started to get codes...')
    os.makedirs('output', exist_ok=True)
    open_wechat()
    locate_move_click('icons/mini-programs.png')
    locate_move_click('icons/suishenban.png')
    t(3)
    locate_move_click('icons/health-code.png')
    t(1.5)
    # Take screenshots
    take_window_screenshot_to_clipboard(save_name='health-code')

    # Find contacts and send
    open_wechat()
    find_wechat_contact(TARGET_CONTACT)

    pg.hotkey('command', 'v', interval=INTERVAL)
    pg.press('enter')

    # locate_move_click('icons/mini-programs.png')
    locate_move_click('icons/suishenban.png')
    locate_move_click('icons/travel-history.png')
    t(1)
    locate_move_click('icons/text-allow.png')
    t(5)
    locate_move_click('icons/agree-permission.png')
    locate_move_click('icons/query.png')
    t(1)
    take_window_screenshot_to_clipboard(save_name='travel-history')
    open_wechat()
    # find_wechat_contact(TARGET_CONTACT)
    pg.hotkey('command', 'v', interval=INTERVAL)
    pg.press('enter')

    locate_move_click('icons/suishenban.png')
    locate_move_click('icons/nucleic-acid.png')
    t(2)
    take_window_screenshot_to_clipboard(save_name='nucleic-acid')

    open_wechat()
    # find_wechat_contact(TARGET_CONTACT)
    pg.hotkey('command', 'v', interval=INTERVAL)
    pg.press('enter')
    print(f'Finished. Time usage: {time.time() - start:2f}s.')

if __name__ == '__main__':
    main()