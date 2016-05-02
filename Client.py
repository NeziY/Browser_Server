from PyQt4 import QtGui, QtCore, uic
import socket
import sys  # We need sys so that we can pass argv to QApplication
import re

# -----------------BROWSER GUI----------------- #

class Browser(QtGui.QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.ui = uic.loadUi('testClientGui.ui')

        self.csi_thread = Client_Server_Interactive_Thread()
        self.connect(self.csi_thread, QtCore.SIGNAL("display_html(QString)"), self.display_html)

        self.connect(self.ui.txt_browser,
                     QtCore.SIGNAL('anchorClicked(const QUrl &)'),
                     self.anchorClickedHandler)

        self.csi_thread.start()

        self.ui.go_bttn.clicked.connect(self.get_url_txtbx)

    # -----------------CLICK EVENT FOR ANCHOR (HTML LINK)----------------- #

    def anchorClickedHandler(self):
        # self.ui.txt_browser.setSource(QtCore.QUrl("html_file.html"))
        send_msg(data_link_str)
    # -----------------GET TEXT FROM URL TEXT BOX----------------- #

    def get_url_txtbx(self):
        global url_txt
        url_txt = str(self.ui.url_txtbx.text())
        send_msg(url_txt)

    # -----------------DISPLAY HTML TO BROWSER----------------- #

    def display_html(self, data):
        #self.ui.viewer_txt_bx.setText(data)
        self.ui.txt_browser.setText(data)
        self.parse_document(data)

    # -----------------HIGHLIGHT FOR <MARK> TAG----------------- #
    def highlight(self, str_html):

        cursor = self.ui.txt_browser.textCursor()
        # Setup the desired format for matches
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor("red")))
        # Setup the regex engine
        pattern = str_html
        regex = QtCore.QRegExp(pattern)
        # Process the displayed document
        pos = 0
        index = regex.indexIn(self.ui.txt_browser.toPlainText(), pos)
        # Select the matched text and apply the desired
        if index != -1:
            cursor.setPosition(index)
            cursor.movePosition(QtGui.QTextCursor.EndOfLine, 1)
            cursor.mergeCharFormat(format)


    # -----------------PARSE HTML CODE----------------- #
    def parse_document(self, data):
        global data_link_str
        data_link_str = ''

        r_mark = re.compile('<mark>(.*?)</mark>')
        r_link = re.compile('<a href="(.*)">')
        r_marknlink = re.compile('>(.*?)</a>')

        for match in r_mark.finditer(data):
            data_str_mark = match.group(1)
            data_link = r_link.search(data_str_mark)
            data_mark_link = r_marknlink.search(data_str_mark)

            # if data_mark_link:
            #     str3 = data_mark_link.group(1)
            #     str3_list = str3.split()
            #     for pattern in str3_list:
            #         self.highlight(pattern)
            #
            #
            #     if data_link:
            #         str2 = data_link.group(1)
            #
            # else:
            #     data_str_mark_list = data_str_mark.split()
            #     for pattern in data_str_mark_list:
            #         self.highlight(pattern)

            if data_mark_link:
                str3 = data_mark_link.group(1)
                self.highlight(str3)
                if data_link:
                    data_link_str = data_link.group(1)

            elif data_str_mark:
                self.highlight(data_str_mark)





# -----------------QT THREAD TO SEND MSG FROM SERVER TO GUI----------------- #

class Client_Server_Interactive_Thread(QtCore.QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        socket_create()
        while True:
            msg = listen_for_msg()
            self.emit(QtCore.SIGNAL('display_html(QString)'), msg)

# -----------------CREATE SOCKET----------------- #


def socket_create():
    global host
    global port
    global s
    host = '192.168.204.99'
    port = 9977
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

# -----------------LISTENS TO INCOMING DATA FROM SERVER----------------- #

def listen_for_msg():
    data = s.recv(1024)
    data_str = str(data[:].decode("utf-8"))
    return data_str

# -----------------SEND REQUEST FROM USER TO SERVER----------------- #

def send_msg(msg):

        if msg == "server":
            s.send(str.encode(msg, "utf-8"))
        elif msg != "":
            s.send(str.encode(msg, "utf-8"))
        elif msg == "quit":
            s.close()

# -----------------GUI MAIN FUNCTION----------------- #

app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
form = Browser()  # We set the form to be our Browser
form.ui.show()    # Show the form
app.exec_()

