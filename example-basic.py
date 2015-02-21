import curses
import npyscreen

# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm())

# This form class defines the display that will be presented to the user.

class MainForm(npyscreen.Form):
    BLANK_LINES_BASE     = 0
    BLANK_COLUMNS_RIGHT  = 0
    DEFAULT_X_OFFSET = 2
    FRAMED = False
    MAIN_WIDGET_CLASS_START_LINE = 1
    STATUS_WIDGET_CLASS = npyscreen.Textfield
    STATUS_WIDGET_X_OFFSET = 2
    COMMAND_WIDGET_CLASS= npyscreen.Textfield
    COMMAND_WIDGET_NAME = None
    COMMAND_WIDGET_BEGIN_ENTRY_AT = None
    COMMAND_ALLOW_OVERRIDE_BEGIN_ENTRY_AT = True

    def draw_form(self):
        MAXY, MAXX = self.lines, self.columns #self.curses_pad.getmaxyx()
        self.curses_pad.hline(0, 0, curses.ACS_HLINE, MAXX-1)
        self.curses_pad.hline(2, 0, curses.ACS_HLINE, MAXX-1)

    def create(self):
        self.wStatus1 = self.add(self.__class__.STATUS_WIDGET_CLASS,  rely=0,
                                        relx=self.__class__.STATUS_WIDGET_X_OFFSET,
                                        editable=False,
                                        )
        self.wStatus1.value = "Request:"
        self.wStatus1.important = True

        self.filter = self.add(npyscreen.Textfield,  rely=1,
                                        relx=self.__class__.STATUS_WIDGET_X_OFFSET,
                                        editable=True,
                                        )

        self.wStatus2 = self.add(self.__class__.STATUS_WIDGET_CLASS,  rely=2,
                                        relx=self.__class__.STATUS_WIDGET_X_OFFSET,
                                        editable=False,
                                        )
        self.wStatus2.value = "Suggestions:"
        self.wStatus2.important = True

        self.s1 = self.add(npyscreen.Textfield,  rely=3,
                                        relx=self.__class__.STATUS_WIDGET_X_OFFSET,
                                        editable=False,
                                        )
        self.s1.value = "1:Trololo"

        self.s11 = self.add(npyscreen.Textfield,  rely=3,
                                        editable=False,
                                        )
        self.s11.value = "zz!"
        self.s11.relx= self.__class__.STATUS_WIDGET_X_OFFSET + self.s1.value.__len__()
        self.s11.show_bold = True

    def afterEditing(self):
        self.parentApp.setNextForm(None)

if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()