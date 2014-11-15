#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Andrés Aguirre Dorelo
# MINA/INCO/UDELAR
# basic ax12 actuator control
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

#Andres Aguirre <aaguirre@fing.edu.uy>
#Rafael Cordano <rafael.cordano@gmail.com>

from Xlib import X, display, ext, xobject
from Xlib.ext import record, xtest, shape, xinerama
from Xlib.xobject import colormap, drawable
import time
import gtk

dis = display.Display()
scr = dis.screen()
win = scr.root
xb, yb = False, False
wwin = gtk.Window(gtk.WINDOW_POPUP)
wwin.set_keep_above(True);
color = gtk.gdk.color_parse("#234fdb")
wwin.modify_bg(gtk.STATE_NORMAL, color)
wwin.set_decorated(False)
wwin.add_events(gtk.gdk.KEY_PRESS_MASK |
               gtk.gdk.POINTER_MOTION_MASK |
               gtk.gdk.BUTTON_PRESS_MASK |
               gtk.gdk.SCROLL_MASK
               )

def setLineWidth(width):
    w, h = wwin.get_size()
	#global lineWidth
	#lineWidth = width
    print width
    wwin.set_size_request(int(width), wwin.get_screen().get_height())
    print wwin.get_size_request()
def showLine(active):
    if active:
        wwin.show()
    else:
        wwin.hide()


def setLineColor(red, green, blue):
    global color
    r = hex(red)
    rh = "%s" % r.split("x")[1]
    g = hex(green)
    gh = "%s" % g.split("x")[1]
    b = hex(blue)
    bh = "%s" % b.split("x")[1]
    chex = "#%s%s%s"%(rh, gh, bh)
    color = gtk.gdk.color_parse(chex)


def createRelativeMouseEvent(deltaX, deltaY):
	d = display.Display()
	#move pointer to set relative location
	d.warp_pointer(deltaX,deltaY)
	d.sync()

def createAbsoluteMouseEvent(x,y):
    (xx, yy) = wwin.get_position()
    data = win.get_geometry()
    height = data.height
    win.warp_pointer(x, y)
    wwin.move(x, yy)
    wwin.set_keep_above(True);
    dis.sync()

def getMousePosition():
	d = display.Display()
	data = d.screen().root.query_pointer()._data
	return data['root_x'], data['root_y']

def getScreenResolution():
	d = display.Display()
	resolution = d.screen().root.get_geometry()
	return resolution.width, resolution.height

def buttonPress(button):
	d = display.Display()
	ext.xtest.fake_input(d,X.ButtonPress,button)
	d.sync()

def buttonRelease(button):
	d = display.Display()
	ext.xtest.fake_input(d,X.ButtonRelease,button)
	d.sync()

def clickButton(button):
    
    x,y = getMousePosition()
    win.warp_pointer(x - 20, y)
    wwin.set_keep_above(False)
    wwin.set_keep_below(True)

    d = display.Display()
	#press button 1, for middle mouse button use 2, for opposite button use 3
    wwin.destroy()
    ext.xtest.fake_input(d,X.ButtonPress,button)
    d.sync()
    #to make click we need to release the same button
    ext.xtest.fake_input(d, X.ButtonRelease,button)
    d.sync()

    ext.xtest.fake_input(d,X.ButtonPress,button)
    d.sync()

    ext.xtest.fake_input(d,X.ButtonRelease,button)
    d.sync()
    

def pressButton(button):
	#wwin.destroy()
	print "hello"
	d = display.Display()
	#press button 1, for middle mouse button use 2, for opposite button use 3
	ext.xtest.fake_input(d,X.ButtonPress,button)
	d.sync()

def releaseButton(button):
	d = display.Display()
	#to make click we need to release the same button
	ext.xtest.fake_input(d, X.ButtonRelease,button)
	d.sync()

