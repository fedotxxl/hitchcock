#!/usr/bin/env python
import npyscreen
import curses


class TypingFieldBase(npyscreen.wgtextbox.TextfieldBase):
    def __init__(self, *args, **keywords):
        super(TypingFieldBase, self).__init__(*args, **keywords)
        self.syntax_highlighting = True
        self._highlightingdata = [curses.A_NORMAL] * len(self.value)
        self.current_cursor_position = 0

    def edit(self):
        self.cursor_position = self.current_cursor_position
        self.editing = 1
        if self.cursor_position is False:
            self.cursor_position = len(self.value or '')
        self.parent.curses_pad.keypad(1)

        self.old_value = self.value

        self.how_exited = False

        while self.editing:
            self.display()
            self.get_and_use_key_press()

        self.begin_at = 0
        self.display()
        self.cursor_position = False
        return self.how_exited, self.value

    def t_input_isprint(self, inp):
        if self._last_get_ch_was_unicode and inp not in '\n\t\r':
            return True
        if curses.ascii.isprint(inp) and \
        (chr(inp) not in '\n\t\r'):
            return True
        else:
            return False


class TypingFieldColor(TypingFieldBase):
    """
    Type the text that appears in the field; color changes indicate
        whether each character was entered correctly. Backspace moves
        cursor backwards and undoes effect of entered text.
    """
    def set_up_handlers(self):
        super(TypingFieldBase, self).set_up_handlers()

        # For OS X
        del_key = curses.ascii.alt('~')

        self.handlers.update({
            curses.KEY_BACKSPACE:   self.h_undo_left,
            curses.ascii.DEL:       self.h_undo_left,
            curses.ascii.BS:        self.h_undo_left,
            })

        self.complex_handlers.extend((
            (self.t_input_isprint, self.h_move_right_color),
            ))

    def h_undo_left(self, inp):
        if self.cursor_position > 0:
            self.cursor_position -= 1
            self.current_cursor_position -= 1
            self._highlightingdata[self.cursor_position] = curses.A_NORMAL

    def h_move_right_color(self, inp):
        if self.cursor_position < len(self.value):
            if inp == ord(self.value[self.cursor_position]):
                hl_color = self.parent.theme_manager.findPair(self, 'IMPORTANT')
                self._highlightingdata[self.cursor_position] = hl_color
            else:
                curses.beep()
                hl_color = self.parent.theme_manager.findPair(self, 'CRITICAL')
                self._highlightingdata[self.cursor_position] = hl_color
            self.cursor_position += 1
            self.current_cursor_position += 1


# class TypingFieldColorTitle(npyscreen.wgmultiline.TitleMultiLine):
#     _entry_type = TypingFieldColor


# class TypingFieldColorBoxed(npyscreen.wgboxwidget.BoxTitle):
#     _contained_widget = TypingFieldColor


# class TypingFieldNoMistakes(TypingFieldBase):
#     """
#     Type the text that appears in the field; color change indicates
#         when each character is entered correctly. Cursor only moves
#         forward on correctly entered characters. Backspace has no effect.
#     """
#     def set_up_handlers(self):
#         super(TypingFieldBase, self).set_up_handlers()
#
#         self.complex_handlers.extend((
#             (self.t_input_isprint, self.h_move_right_if_correct),
#             ))
#
#     def h_move_right_if_correct(self, inp):
#         if self.cursor_position < len(self.value):
#             if inp == ord(self.value[self.cursor_position]):
#                 hl_color = self.parent.theme_manager.findPair(self, 'IMPORTANT')
#                 self._highlightingdata[self.cursor_position] = hl_color
#                 self.cursor_position += 1
#                 self.current_cursor_position += 1
#             else:
#                 curses.beep()
#
#
# class TypingFieldNoMistakesTitle(npyscreen.wgmultiline.TitleMultiLine):
#     _entry_type = TypingFieldNoMistakes
#
#
# class TypingFieldNoMistakesBoxed(npyscreen.wgboxwidget.BoxTitle):
#     _contained_widget = TypingFieldNoMistakes


if __name__ == '__main__':
    class TypingForm(npyscreen.Form):
        def afterEditing(self):
            self.parentApp.setNextForm(None)

        def create(self):
            # This field seems to work
            self.typingfieldcolor = self.add(TypingFieldColor,
                name='Typing Field Color',
                value="Here's some text for you to type! Backspace undoes errors!")
            # This field does NOT seem to work
            # self.typingfieldnomistakes = self.add(TypingFieldNoMistakesBoxed,
            #     name='Typing Field No Mistakes',
            #     value="Here's some more text to type! No errors allowed!")

    class Application(npyscreen.NPSAppManaged):
        def onStart(self):
          form = self.addForm('MAIN', TypingForm, name='Little Typing Form')

    App = Application()
    App.run()