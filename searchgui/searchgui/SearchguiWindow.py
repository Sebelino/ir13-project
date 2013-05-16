# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

import pygtk
pygtk.require('2.0')
from gi.repository import Gtk # pylint: disable=E0611
from gi.repository.GdkPixbuf import Pixbuf
import logging
import urllib2
import gobject

logger = logging.getLogger('searchgui')

from searchgui_lib import Window
from searchgui.AboutSearchguiDialog import AboutSearchguiDialog
from searchgui.PreferencesSearchguiDialog import PreferencesSearchguiDialog
from Search import Search

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
    def perform_search(self,sender):
        s = Search()
        view = self.ui.image_result_grid
        query = self.ui.query_input.get_text()
        results = s.search(query)
        model = Gtk.ListStore(Pixbuf,  gobject.TYPE_STRING)
        view = Gtk.IconView(model)  # Pass the model stored in a ListStore to the GtkIconView
        view.set_pixbuf_column(0)
        view.set_text_column(1)
        view.set_selection_mode(Gtk.SELECTION_MULTIPLE)
        view.set_columns(0)
        view.set_item_width(150)
        for result in results:

            print result

    def get_image_from_url(self, url):
        response = urllib2.urlopen(url)
        fname = url.split("/")[-1]
        f = open(fname, "wb")
        f.write(response.read())
        f.close()
        response.close()
        image = Gtk.Image()
        image.set_from_pixbuf(Pixbuf.new_from_file(fname))
        return image


