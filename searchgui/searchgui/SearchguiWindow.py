# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('searchgui')

from searchgui_lib import Window
from searchgui.AboutSearchguiDialog import AboutSearchguiDialog
from searchgui.PreferencesSearchguiDialog import PreferencesSearchguiDialog

# See searchgui_lib.Window.py for more details about how this class works
class SearchguiWindow(Window):
    __gtype_name__ = "SearchguiWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(SearchguiWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutSearchguiDialog
        self.PreferencesDialog = PreferencesSearchguiDialog

        # Code for other initialization actions should be added here.
    def perform_search(self, sender):
        print "Hello, World!"

