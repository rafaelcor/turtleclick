#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Andrés Aguirre Dorelo<aaguirre@fing.edu.uy>
# Rafael Carlos Cordano Ottati<rafael.cordano@gmail.com>
# MINA/INCO/UDELAR
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys

from gettext import gettext as _

from plugins.plugin import Plugin

from TurtleArt.tapalette import make_palette
from TurtleArt.tautils import debug_output
from TurtleArt.taprimitive import Primitive, ArgSlot, ConstantArg
from TurtleArt.tatype import TYPE_INT, TYPE_FLOAT, TYPE_STRING, TYPE_NUMBER, TYPE_COLOR
import logging
_logger = logging.getLogger('turtleart-activity x11 events plugin')
from TurtleArt.taconstants import MACROS
sys.path.append(os.path.abspath('./plugins/x_events'))
import lib_event
import Xlib
import Xlib.ext.xtest
import Xlib.ext.record
import Xlib.ext.shape
import Xlib.ext.xinerama


class X_events(Plugin):

    def __init__(self, parent):
        Plugin.__init__(self)
        self._parent = parent
        self.running_sugar = self._parent.running_sugar
        self._status = True

    def setup(self):
        # set up X11 events specific blocks
        palette = make_palette('xlib-bots',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Palette of X11 event blocks'))

        palette.add_block('setX11mouse',
                              style='basic-style-2arg',
                              label=_('setXY'),
                              value_block=True,
                              default=[0,0],
                              help_string=\
                                  _('set the mouse pointer to x y coordinates'),
                              prim_name='setX11mouse')

        palette.add_block('getX11mouseX',
                              style='box-style',
                              label=_('getMouseX'),
                              value_block=True,
                              help_string=\
                                  _('get the mouse pointer x coordinate'),
                              prim_name='getX11mouseX')

        palette.add_block('getX11mouseY',
                              style='box-style',
                              label=_('getMouseY'),
                              value_block=True,
                              help_string=\
                                  _('get the mouse pointer y coordinate'),
                              prim_name='getX11mouseY')
                              
        palette.add_block('leftClick',
                              style='box-style',
                              label=_('leftClick'),
                              value_block=True,
                              help_string=\
                                  _('click left click'),
                              prim_name='leftClick')
                              
        
        palette.add_block('rightClick',
                              style='box-style',
                              label=_('rightClick'),
                              value_block=True,
                              help_string=\
                                  _('click right click'),
                              prim_name='rightClick')

        palette.add_block('click',
                              style='basic-style-1arg',
                              label=_('click'),
                              value_block=True,
                              default=[1],
                              help_string=\
                                  _('simulate a mouse click'),
                              prim_name='click')

        palette.add_block('getScreenWidth',
                              style='box-style',
                              label=_('getScreenWidth'),
                              value_block=True,
                              help_string=\
                                  _('get the screen width'),
                              prim_name='getScreenWidth')

        palette.add_block('getScreenHeight',
                              style='box-style',
                              label=_('getScreenHeight'),
                              value_block=True,
                              help_string=\
                                  _('get the screen height'),
                              prim_name='getScreenHeight')

        palette.add_block('pressButton',
                              style='basic-style-1arg',
                              label=_('pressButton'),
                              value_block=True,
                              default=[0],
                              help_string=\
                                  _('keeps button pressed'),
                              prim_name='pressButton')

        palette.add_block('releaseButton',
                              style='basic-style-1arg',
                              label=_('releaseButton'),
                              value_block=True,
                              default=[0],
                              help_string=\
                                  _('releases button'),
                              prim_name='releaseButton')

        palette.add_block('setLineColorRGB',
                              style='basic-style-3arg',
                              label=_('setLineColorRGB'),
                              value_block=True,
                              default=[0,0,0],
                              help_string=\
                                  _('set line color from rgb value'),
                              prim_name='setLineColorRGB')
        palette.add_block('setLineColor',
                              style='basic-style-1arg',
                              label=_('setLineColor'),
                              value_block=True,
                              default=MACROS,
                              help_string=\
                                  _('set line color'),
                              prim_name='setLineColor')


        palette.add_block('setLineOpacity',
                              style='basic-style-1arg',
                              label=_('setLineOpacity'),
                              value_block=True,
                              default=[1],
                              help_string=\
                                  _('set line opacity'),
                              prim_name='setLineOpacity')

        palette.add_block('showLine',
                              style='basic-style-1arg',
                              label=_('showLine'),
                              value_block=True,
                              default=[1],
                              help_string=\
                                  _('show vertical line over mouse'),
                              prim_name='showLine')

        palette.add_block('setLineWidth',
                              style='basic-style-1arg',
                              label=_('setLineWidth'),
                              value_block=True,
                              default=[0],
                              help_string=\
                                  _('width of vertical line over mouse'),
                              prim_name='setLineWidth')

        palette.add_block('setLineHeight',
                              style='basic-style-1arg',
                              label=_('setLineHeight'),
                              value_block=True,
                              default=[0],
                              help_string=\
                                  _('height of vertical line over mouse'),
                              prim_name='setLineHeight')
                              
        palette.add_block('setLineWidthAndHeigth',
                              style='basic-style-2arg',
                              label=_('setLineWidthAndHeigth'),
                              value_block=True,
                              default=[0, 0],
                              help_string=\
                                  _('set width and height of line over mouse'),
                              prim_name='setLineWidthAndHeigth')


        self._parent.lc.def_prim(
            'setX11mouse', 2,
            Primitive(self.setX11mouse, arg_descs=[ArgSlot(TYPE_NUMBER),
                                                   ArgSlot(TYPE_NUMBER)]))
        self._parent.lc.def_prim(
            'getX11mouseX', 0,
            Primitive(self.getX11mouseX, TYPE_INT))
        self._parent.lc.def_prim(
            'getX11mouseY', 0,
            Primitive(self.getX11mouseY, TYPE_INT))
        self._parent.lc.def_prim(
            'leftClick', 0,
            Primitive(self.leftClick, TYPE_INT))
        self._parent.lc.def_prim(
            'rightClick', 0,
            Primitive(self.rightClick, TYPE_INT))
        self._parent.lc.def_prim(
            'click', 1,
            Primitive(self.click, arg_descs=[ArgSlot(TYPE_NUMBER)]))
        self._parent.lc.def_prim(
            'getScreenWidth', 0,
            Primitive(self.getScreenWidth, TYPE_INT))
        self._parent.lc.def_prim(
            'getScreenHeight', 0,
            Primitive(self.getScreenHeight, TYPE_INT))
        self._parent.lc.def_prim(
            'pressButton', 1,
            Primitive(self.pressButton, arg_descs=[ArgSlot(TYPE_NUMBER)]))
        self._parent.lc.def_prim(
            'releaseButton', 1,
            Primitive(self.releaseButton, arg_descs=[ArgSlot(TYPE_NUMBER)]))
        self._parent.lc.def_prim(
            'setLineColor', 1,
            Primitive(self.setLineColor, arg_descs=[ArgSlot(TYPE_COLOR)]))
            
        self._parent.lc.def_prim(
            'setLineColorRGB', 3,
            Primitive(self.setLineColorRGB, arg_descs=[ArgSlot(TYPE_INT),
                                                    ArgSlot(TYPE_INT),
                                                    ArgSlot(TYPE_INT)]))
            
            
        self._parent.lc.def_prim(
            'showLine', 1,
            Primitive(self.showLine, arg_descs=[ArgSlot(TYPE_NUMBER)]))
        self._parent.lc.def_prim(
            'setLineWidth', 1,
            Primitive(self.setLineWidth, arg_descs=[ArgSlot(TYPE_NUMBER)]))


        self._parent.lc.def_prim(
            'setLineHeight', 1,
            Primitive(self.setLineHeight, arg_descs=[ArgSlot(TYPE_NUMBER)]))
            
        self._parent.lc.def_prim(
            'setLineWidthAndHeigth', 2,
            Primitive(self.setLineWidthAndHeigth, arg_descs=[ArgSlot(TYPE_NUMBER),
													 ArgSlot(TYPE_NUMBER)]))
        
        self._parent.lc.def_prim(
            'setLineOpacity', 1,
            Primitive(self.setLineOpacity, arg_descs=[ArgSlot(TYPE_NUMBER)]))

    # Block primitives

    def setX11mouse(self,x, y):
        lib_event.createAbsoluteMouseEvent(int(x),int(y))

    def getX11mouseX(self):
        x,y = lib_event.getMousePosition()
        return x

    def getX11mouseY(self):
        x,y = lib_event.getMousePosition()
        return y

    def getScreenWidth(self):
        x,y = lib_event.getScreenResolution()
        return x

    def getScreenHeight(self):
        x,y = lib_event.getScreenResolution()
        return y
        
    def leftClick(self):
        return 1
    
    def rightClick(self):
        return 2

    def click(self,button):
        lib_event.clickButton(button)

    def pressButton(self,button):
        lib_event.pressButton(button)

    def releaseButton(self,button):
        lib_event.releaseButton(button)
        
    def setLineColor(self, colorName):
        lib_event.setLineColor(colorName)

    def setLineColorRGB(self,red,green,blue):
        lib_event.setLineColorRGB(red,green,blue)

    def showLine(self,active):
        lib_event.showLine(active)

    def setLineWidth(self,width):
        lib_event.setLineWidth(width)

    def setLineHeight(self,height):
        lib_event.setLineHeight(height)
    
    def setLineWidthAndHeigth(self, width, height):
		lib_event.setLineWidthAndHeigth(width, height)
    
    def setLineOpacity(self, opacity):
        lib_event.setLineOpacity(opacity)
