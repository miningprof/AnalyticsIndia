import os
import markdown
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QDialogButtonBox, QMessageBox

DOCS_USER_MANUAL_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'user_manual.md'))

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help Documentation")
        self.setMinimumSize(700, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        
        html_content = ""
        try:
            if os.path.exists(DOCS_USER_MANUAL_FILE):
                with open(DOCS_USER_MANUAL_FILE, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            else:
                html_content = f"<p>Error: User manual file not found at '{DOCS_USER_MANUAL_FILE}'.</p>"
        except Exception as e:
            html_content = f"<p>Error loading help content: {str(e)}</p>"
            QMessageBox.warning(self, "Error", f"Could not load help content: {e}")

        self.text_browser.setHtml(html_content)
        layout.addWidget(self.text_browser)

        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
