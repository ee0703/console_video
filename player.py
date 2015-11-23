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

    # Getting the frame rate of the video
    # Got this from the source code of pipeffmpeg (Can be replaced by Popen)
    file_info = pipeffmpeg.get_info(file_path)

    try:
        f_rate = file_info["streams"][0]["r_frame_rate"]
        # Getting the number of seconds for a frame
        delay = 1.0 / int(f_rate.split("/")[0])
    except (KeyError, IndexError):
        # Setting a default delay if frame rate not obtained
        delay = 0.02

    stdscr = curses.initscr()
    max_h, max_w =  stdscr.getmaxyx()

    start_time = time.time()
    for i, bmp in enumerate(iv.readframe()):
        # timestap when frame start
        frame_start_time = time.time()
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

        # Adding a delay if needed
        real_delay = delay - (time.time() - frame_start_time)
        if real_delay > 0:
            time.sleep(real_delay)

    curses.endwin()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '[usage] python player.py [video_path]\n\texample: python player.py video.mp4'
        sys.exit(1)
    play(sys.argv[1])
