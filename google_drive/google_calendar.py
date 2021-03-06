# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import pkg_resources
#import logging
import textwrap
#import json
#import webob
#from lxml import etree
#from xml.etree import ElementTree as ET

from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblock.fragment import Fragment

# from StringIO import StringIO

from .utils import render_template, AttrDict, load_resource


# Globals ###########################################################

#log = logging.getLogger(__name__)


# Classes ###########################################################

class GoogleCalendarBlock(XBlock):
    """
    XBlock providing a google calendar view for a specific calendar
    """
    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="Example Google Calendar"
    )

    calendar_id = String(
        display_name="Public Calendar ID",
        help="This is the Calendar ID for the publically available Google calendar you would like to embed. To find this ID, go to your Calendar Settings and copy the ID found in the Calendar Address section.",
        scope=Scope.settings,
        default="edx.org_vme83q0j2v52mbhjncvfd5uqs8@group.calendar.google.com"
    )

    # 0=Week, 1=Month, 2=Agenda
    default_view = Integer(
        display_name="Default View",
        help="The view of the calendar initially presented to students.",
        scope=Scope.settings,
        default=1
    )

    views = ["Week", "Month", "Agenda"]

    def student_view(self, context={}):
        """
        Player view, displayed to the student
        """

        fragment = Fragment()

        view = "Week" if self.default_view==0 else "Month" if self.default_view==1 else "Agenda"

        iframe = "<iframe src=\"https://www.google.com/calendar/embed?mode={}&amp;src={}\"></iframe>".format(view, self.calendar_id)

        context.update({
            "self": self,
            "iframe": iframe
        })
        fragment.add_content(render_template('/templates/html/google_calendar.html', context))
        fragment.add_css(load_resource('public/css/google_calendar.css'))
        fragment.add_javascript(load_resource('public/js/google_calendar.js'))

        fragment.initialize_js('GoogleCalendarBlock')

        return fragment

    def studio_view(self, context):
        """
        Editing view in Studio
        """
        fragment = Fragment()
        fragment.add_content(render_template('/templates/html/google_calendar_edit.html', {
            'self': self
        }))
        fragment.add_javascript(load_resource('public/js/google_calendar_edit.js'))

        fragment.initialize_js('GoogleCalendarEditBlock')

        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):

        self.display_name = submissions['display_name']
        self.calendar_id = submissions['calendar_id']
        self.default_view = submissions['default_view']

        return {
            'result': 'success',
        }
