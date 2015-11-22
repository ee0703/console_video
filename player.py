# -*- coding: utf-8 -*-
import sys
import pipeffmpeg
import BmpImagePlugin
import cStringIO as StringIO
import curses
import time
from PIL import Image


# gray scale of chars in 70 grades
gray_scale = ''' .'`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'''
gray_scale = ''.join(c*(256//len(gray_scale)) for c in gray_scale)
gray_scale += gray_scale[-1]*(256-len(gray_scale))


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
        data = ''.join(gray_scale[pix] for pix in image.getdata())
        for h in range(max_h-1):
            stdscr.addstr(h, 0, data[h*max_w:(h+1)*max_w])

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
