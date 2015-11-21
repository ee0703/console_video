# -*- coding: utf-8 -*-
import sys
import pipeffmpeg
import BmpImagePlugin
import cStringIO as StringIO
import curses
import time
from PIL import Image


# gray scale of chars in 70 grades
gray_scale = '''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''


def color2char(color):
    """convert glay color value from 0 to 255 to char"""
    index = color/3
    if index >= 69:
        index = 69
    return gray_scale[69-index]


def play(file_path):
    """play a video file"""
    iv = pipeffmpeg.InputVideoStream()
    iv.open(file_path)
    stdscr = curses.initscr()
    max_h, max_w =  stdscr.getmaxyx()

    start_time = time.time()
    for i, bmp in enumerate(iv.readframe()):
        # resize each frame to proper size, and covert to gray
        image = Image.open(StringIO.StringIO(bmp))\
                    .resize((max_w, max_h), Image.ANTIALIAS)\
                    .convert('L')

        stdscr.clear()
        for h in range(max_h-1):
            for w in range(max_w):
                pix = image.getpixel((w, h))
                stdscr.addch(h, w, color2char(pix))

        time_eclipsed = time.time() - start_time
        minutes, seconds = time_eclipsed/60, time_eclipsed % 60
        stdscr.addstr(max_h-1, 0, 'Resolution:[%d*%d] Frame:%d Time:[%d:%d]' % (max_w, max_h, i, minutes, seconds))
        stdscr.refresh()

    curses.endwin()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '[usage] python player.py [video_path]\n\texample: python player.py video.mp4'
        sys.exit(1)
    play(sys.argv[1])
