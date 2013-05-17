# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE
import gobject

from locale import gettext as _

import pygtk
pygtk.require('2.0')
from gi.repository import Gtk# pylint: disable=E0611
from gi.repository.GdkPixbuf import Pixbuf
import logging
import urllib2
import os

logger = logging.getLogger('searchgui')

from searchgui_lib import Window
from searchgui.AboutSearchguiDialog import AboutSearchguiDialog
from searchgui.PreferencesSearchguiDialog import PreferencesSearchguiDialog
from Search import Search


DEFAULT_IMAGE_WIDTH = 200

# See searchgui_lib.Window.py for more details about how this class works
class SearchguiWindow(Window):
    __gtype_name__ = "SearchguiWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(SearchguiWindow, self).finish_initializing(builder)
        self.builder = builder
        self.AboutDialog = AboutSearchguiDialog
        self.PreferencesDialog = PreferencesSearchguiDialog

        # Code for other initialization actions should be added here.
    def perform_search(self, sender):
        s = Search()
        view = self.ui.image_result_grid
        query = self.ui.query_input.get_text()
        self.results = s.search(query)
        model = Gtk.ListStore(Pixbuf, str)
        view.set_model(model)
        view.set_pixbuf_column(0)
        # view.set_text_column(1)
        # view.set_selection_mode(Gtk.SELECTION_MULTIPLE)
        view.set_columns(-1)
        #  view.set_item_width(150)
        print len(self.results)
        self.index = 0
        while self.index<10 and self.index<len(self.results):
            result = self.results[self.index]
            pixbuf = self.get_image_from_url(result)
            pix_w = pixbuf.get_width()
            pix_h = pixbuf.get_height()
            new_h = (pix_h * DEFAULT_IMAGE_WIDTH) / pix_w # Calculate the scaled height before resizing image
            scaled_pix = pixbuf.scale_simple(DEFAULT_IMAGE_WIDTH, new_h, 0)
            model.append([scaled_pix, ''])
            logger.debug('ADDED %s', result)
            self.index += 1


    def get_image_from_url(self, url):
        response = urllib2.urlopen(url)
        fname = url.split("/")[-1]
        f = open(fname, "wb")
        f.write(response.read())
        f.close()
        response.close()
        image = Gtk.Image()
        buf = Pixbuf.new_from_file(fname)
        os.remove(fname)
        return buf

    def get_next_ten(self, sender):
        view = self.ui.image_result_grid
        model = Gtk.ListStore(Pixbuf, str)
        view.set_model(model)
        view.set_pixbuf_column(0)
        view.set_columns(-1)
        print len(self.results)
        limit = self.index + 10
        while self.index<limit and self.index<len(self.results):
            result = self.results[self.index]
            pixbuf = self.get_image_from_url(result)
            pix_w = pixbuf.get_width()
            pix_h = pixbuf.get_height()
            new_h = (pix_h * DEFAULT_IMAGE_WIDTH) / pix_w # Calculate the scaled height before resizing image
            scaled_pix = pixbuf.scale_simple(DEFAULT_IMAGE_WIDTH, new_h, 0)
            model.append([scaled_pix, ''])
            logger.debug('ADDED %s', result)
            self.index += 1



