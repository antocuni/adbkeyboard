import os
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

#################################################################### 
def main(): 
    app = QApplication(sys.argv) 
    w = MyWindow() 
    w.show() 
    sys.exit(app.exec_()) 

####################################################################
class MyWindow(QWidget): 
    def __init__(self, *args): 
        QWidget.__init__(self, *args)

        # create objects
        self.label = QLabel("Android Keyboard")
        self.edit = AndroidKeyboardEdit()

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)


####################################################################
class AndroidKeyboardEdit(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
        self.monkey = Monkey()
        
    def event(self, event):
        if event.type() in (QEvent.KeyPress, QEvent.KeyRelease):
            self._handle_key_event(event)
            return False    
        return QLineEdit.event(self, event)

    def _handle_key_event(self, event):
        keycode = KEYCODE_MAP.get(event.key(), None)
        if keycode is None:
            if 33 <= event.key() <= 255:
                # try with type
                self.monkey.send('type %s' % chr(event.key()))
                return
            else:
                print 'Unknown key: ', qt_key_name(event.key())
                return
        #
        if event.type() == QEvent.KeyPress:
            action = 'down'
        else:
            action = 'up'

        cmd = 'key %s %s' % (action, keycode)
        self.monkey.send(cmd)

def qt_key_name(num):
    for name, value in Qt.__dict__.iteritems():
        if name.startswith('Key_') and value == num:
            return name
    return 'unknown: %d' % num
    

import telnetlib
class Monkey(object):

    def __init__(self, verbose=False):
        self.verbose = verbose
        print "adb forward"
        os.system("adb forward tcp:54784 tcp:54784")
        print "adb shell monkey"
        os.system("adb shell monkey --port 54784")
        print "telnet"
        self.sock = telnetlib.Telnet('localhost', 54784)

    def send(self, command):
        if self.verbose:
            print command.strip(),
        self.sock.write(command + "\n")
        res = self.sock.read_until('\n').strip()
        if self.verbose:
            print res

    def close(self):
        self.send('quit')
        self.sock.close()
            
    def __del__(self):
        self.close()

def _keycode_map():
    keys = {

        ord("'"): "KEYCODE_APOSTROPHE",
        ord("@"): "KEYCODE_AT",
        ord("\\"): "KEYCODE_BACKSLASH",
        ord(' '): "KEYCODE_SPACE",
        ord('#'): "KEYCODE_POUND",
        ord('*'): "KEYCODE_STAR",
        ord('+'): "KEYCODE_PLUS",
        ord(','): "KEYCODE_COMMA",
        ord('-'): "KEYCODE_MINUS",
        ord('.'): "KEYCODE_PERIOD",
        ord('/'): "KEYCODE_SLASH",
        ord(';'): "KEYCODE_SEMICOLON",
        ord('='): "KEYCODE_EQUALS",
        ord('['): "KEYCODE_LEFT_BRACKET",
        ord(']'): "KEYCODE_RIGHT_BRACKET",
        ord('`'): "KEYCODE_GRAVE",
        ord('('): "KEYCODE_NUMPAD_LEFT_PAREN",
        ord(')'): "KEYCODE_NUMPAD_RIGHT_PAREN",

        Qt.Key_Alt: "KEYCODE_ALT_LEFT",
        Qt.Key_AltGr: "KEYCODE_ALT_RIGHT",
        Qt.Key_Backspace: "KEYCODE_DEL",
        Qt.Key_Calculator: "KEYCODE_CALCULATOR",
        Qt.Key_Calendar: "KEYCODE_CALENDAR",
        Qt.Key_CapsLock: "KEYCODE_CAPS_LOCK",
        Qt.Key_Control: "KEYCODE_CTRL_LEFT",
        Qt.Key_Down: "KEYCODE_DPAD_DOWN",
        Qt.Key_End: "KEYCODE_MOVE_END",
        Qt.Key_Enter: "KEYCODE_ENTER",
        Qt.Key_Return: "KEYCODE_ENTER",
        Qt.Key_Escape: "KEYCODE_BACK",
        Qt.Key_F1: "KEYCODE_POWER",
        Qt.Key_F2: "KEYCODE_HOME", 
        Qt.Key_F3: "KEYCODE_APP_SWITCH",
        Qt.Key_Home: "KEYCODE_MOVE_HOME",
        Qt.Key_Insert: "KEYCODE_INSERT",
        Qt.Key_Left: "KEYCODE_DPAD_LEFT",
        Qt.Key_MediaLast: "KEYCODE_MEDIA_FAST_FORWARD",
        Qt.Key_MediaNext: "KEYCODE_MEDIA_NEXT",
        Qt.Key_MediaPause: "KEYCODE_MEDIA_PAUSE",
        Qt.Key_MediaPlay: "KEYCODE_MEDIA_PLAY",
        Qt.Key_MediaPrevious: "KEYCODE_MEDIA_PREVIOUS",
        Qt.Key_MediaRecord: "KEYCODE_MEDIA_RECORD",
        Qt.Key_MediaTogglePlayPause: "KEYCODE_MEDIA_PLAY_PAUSE",
        Qt.Key_MediaStop: "KEYCODE_MEDIA_STOP",
        Qt.Key_Menu: "KEYCODE_MENU",
        Qt.Key_PageDown: "KEYCODE_PAGE_DOWN",
        Qt.Key_PageUp: "KEYCODE_PAGE_UP",
        Qt.Key_Pause: "KEYCODE_BREAK",
        Qt.Key_Right: "KEYCODE_DPAD_RIGHT",
        Qt.Key_ScrollLock: "KEYCODE_SCROLL_LOCK",
        Qt.Key_Search: "KEYCODE_SEARCH",
        Qt.Key_Tab: "KEYCODE_TAB",
        Qt.Key_Up: "KEYCODE_DPAD_UP",
        Qt.Key_VolumeDown: "KEYCODE_VOLUME_DOWN",
        Qt.Key_VolumeMute: "KEYCODE_VOLUME_MUTE",
        Qt.Key_VolumeUp: "KEYCODE_VOLUME_UP",
        Qt.Key_Shift: "KEYCODE_SHIFT_LEFT",
        Qt.Key_SysReq: "KEYCODE_SYSRQ",
        
        # KEYCODE_BUTTON_*: game pad buttons, unmmaped
        # unmmaped: "KEYCODE_CALL",
        # unmmaped: "KEYCODE_CAMERA",
        # unmmaped: "KEYCODE_CAPTIONS",
        # unmmaped: "KEYCODE_CONTACTS",
        # unmapped: "KEYCODE_ASSIST",
        # unmapped: "KEYCODE_AVR_INPUT",
        # unmapped: "KEYCODE_AVR_POWER",
        # unmapped: "KEYCODE_BOOKMARK",
        # unmapped: "KEYCODE_CHANNEL_DOWN",
        # unmapped: "KEYCODE_CHANNEL_UP",
        # unmapped: "KEYCODE_CLEAR",
        # unmapped: "KEYCODE_CTRL_RIGHT",
        # unmapped: "KEYCODE_DPAD_CENTER",
        # unmapped: "KEYCODE_DVR",
        # unmapped: "KEYCODE_EISU",
        # unmapped: "KEYCODE_ENDCALL",
        # unmapped: "KEYCODE_ENVELOPE",
        # unmapped: "KEYCODE_ESCAPE",
        # unmapped: "KEYCODE_EXPLORER",
        # unmapped: "KEYCODE_FOCUS",
        # unmapped: "KEYCODE_FORWARD",
        # unmapped: "KEYCODE_FORWARD_DEL",
        # unmapped: "KEYCODE_FUNCTION",
        # unmapped: "KEYCODE_GUIDE",
        # unmapped: "KEYCODE_HEADSETHOOK",
        # unmapped: "KEYCODE_HENKAN",
        # unmapped: "KEYCODE_INFO",
        # unmapped: "KEYCODE_KANA",
        # unmapped: "KEYCODE_KATAKANA_HIRAGANA",
        # unmapped: "KEYCODE_LANGUAGE_SWITCH",
        # unmapped: "KEYCODE_MANNER_MODE",
        # unmapped: "KEYCODE_MEDIA_CLOSE",
        # unmapped: "KEYCODE_MEDIA_EJECT",
        # unmapped: "KEYCODE_MEDIA_REWIND",
        # unmapped: "KEYCODE_META_LEFT",
        # unmapped: "KEYCODE_META_RIGHT",
        # unmapped: "KEYCODE_MUHENKAN",
        # unmapped: "KEYCODE_MUSIC",
        # unmapped: "KEYCODE_MUTE",
        # unmapped: "KEYCODE_NOTIFICATION",
        # unmapped: "KEYCODE_NUM",
        # unmapped: "KEYCODE_NUMPAD_0",
        # unmapped: "KEYCODE_NUMPAD_1",
        # unmapped: "KEYCODE_NUMPAD_2",
        # unmapped: "KEYCODE_NUMPAD_3",
        # unmapped: "KEYCODE_NUMPAD_4",
        # unmapped: "KEYCODE_NUMPAD_5",
        # unmapped: "KEYCODE_NUMPAD_6",
        # unmapped: "KEYCODE_NUMPAD_7",
        # unmapped: "KEYCODE_NUMPAD_8",
        # unmapped: "KEYCODE_NUMPAD_9",
        # unmapped: "KEYCODE_NUMPAD_ADD",
        # unmapped: "KEYCODE_NUMPAD_COMMA",
        # unmapped: "KEYCODE_NUMPAD_DIVIDE",
        # unmapped: "KEYCODE_NUMPAD_DOT",
        # unmapped: "KEYCODE_NUMPAD_ENTER",
        # unmapped: "KEYCODE_NUMPAD_EQUALS",
        # unmapped: "KEYCODE_NUMPAD_MULTIPLY",
        # unmapped: "KEYCODE_NUMPAD_SUBTRACT",
        # unmapped: "KEYCODE_NUM_LOCK",
        # unmapped: "KEYCODE_PICTSYMBOLS",
        # unmapped: "KEYCODE_PROG_BLUE",
        # unmapped: "KEYCODE_PROG_GREEN",
        # unmapped: "KEYCODE_PROG_RED",
        # unmapped: "KEYCODE_PROG_YELLOW",
        # unmapped: "KEYCODE_RO",
        # unmapped: "KEYCODE_SETTINGS",
        # unmapped: "KEYCODE_SHIFT_RIGHT",
        # unmapped: "KEYCODE_SOFT_LEFT",
        # unmapped: "KEYCODE_SOFT_RIGHT",
        # unmapped: "KEYCODE_STB_INPUT",
        # unmapped: "KEYCODE_STB_POWER",
        # unmapped: "KEYCODE_SWITCH_CHARSET",
        # unmapped: "KEYCODE_SYM",
        # unmapped: "KEYCODE_TV",
        # unmapped: "KEYCODE_TV_INPUT",
        # unmapped: "KEYCODE_TV_POWER",
        # unmapped: "KEYCODE_WINDOW",
        # unmapped: "KEYCODE_YEN",
        # unmapped: "KEYCODE_ZENKAKU_HANKAKU",
        # unmapped: "KEYCODE_ZOOM_IN",
        # unmapped: "KEYCODE_ZOOM_OUT",
        }
        
    for k in range(ord('0'), ord('9')+1):
        # Qt.Key_0 to Qt.Key_9
        keys[k] = "KEYCODE_%s" % chr(k)
    for k in range(ord('A'), ord('Z')+1):
        # Qt.Key_A to Qt.Key_Z
        keys[k] = "KEYCODE_%s" % chr(k)
    return keys

KEYCODE_MAP = _keycode_map()


####################################################################
if __name__ == "__main__": 
    main()
    ## m = Monkey(verbose=True)
    ## m.send('type ?')
    
