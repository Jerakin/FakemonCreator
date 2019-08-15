import html
import platform
import traceback
from io import StringIO
from urllib.parse import urlencode

NEW_ISSUE_URL = 'https://github.com/Jerakin/FakemonCreator/issues/new'

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from creator import __version__ as version

class ExceptionWindow(QtWidgets.QWidget):
    def __init__(self, app, extype, value, tb):
        super(ExceptionWindow, self).__init__()

        self.app = app

        layout = QtWidgets.QGridLayout()

        information_label = QtWidgets.QLabel()
        information_label.setText('The Fakemon Creator just crashed. An '
            'unhandled exception was raised. Here are the details.')
        layout.addWidget(information_label, 0, 0)
        self.information_label = information_label

        tb_io = StringIO()
        traceback.print_tb(tb, file=tb_io)
        traceback_content = html.escape(tb_io.getvalue()).replace('\n', '<br>')

        text_content = QtWidgets.QTextBrowser()
        text_content.setReadOnly(True)
        text_content.setOpenExternalLinks(True)
        text_content.setHtml('''
<p>Version: {version}</p>
<p>OS: {os} </p>
<p>Type: {extype}</p>
<p>Value: {value}</p>
<p>Traceback:</p>
<code>{traceback}</code>
'''.format(version=html.escape(version), extype=html.escape(str(extype)),
    value=html.escape(str(value)), os=html.escape(platform.platform()),
    traceback=traceback_content))

        layout.addWidget(text_content, 1, 0)
        self.text_content = text_content

        report_url = NEW_ISSUE_URL + '?' + urlencode({
            'title': 'Unhandled exception: [Enter a title]',
            'body': '''* Description: [Enter what you did and what happened]
* Version: {version}
* OS: {os}
* Type: `{extype}`
* Value: {value}
* Traceback:
```
{traceback}
```
'''.format(version=version, extype=str(extype), value=str(value),
    traceback=tb_io.getvalue(), os=platform.platform())
        })

        report_label = QtWidgets.QLabel()
        report_label.setOpenExternalLinks(True)
        report_label.setText('Please help me by reporting this '
            '<a href="{url}">by reporting this issue on GitHub</a>.'
                             ' If are not on github send the error to Jerakin'.format(
                url=html.escape(report_url)))
        layout.addWidget(report_label, 2, 0)
        self.report_label = report_label

        exit_button = QtWidgets.QPushButton()
        exit_button.setText('Exit')
        exit_button.clicked.connect(lambda: self.app.exit(-100))
        layout.addWidget(exit_button, 3, 0, Qt.AlignRight)
        self.exit_button = exit_button

        self.setLayout(layout)
        self.setWindowTitle('Something went wrong')
        self.setMinimumSize(350, 0)