import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QDateEdit, QLineEdit
from PyQt5.QtCore import Qt, QDate
from scraper import Scraper

class DateSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KANPOU Auto App")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.start_date_label = QLabel("Select Date Range and Enter Search Word:")
        layout.addWidget(self.start_date_label)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        layout.addWidget(self.start_date)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        layout.addWidget(self.end_date)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search word")
        layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Start")
        self.search_button.clicked.connect(self.perform_search)
        layout.addWidget(self.search_button)
        self.setCentralWidget(self.search_button)
        
        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)

        self.setGeometry(100, 100, 600, 300)  # Set window size
        self.center()
    
    def center(self):
        qr = self.frameGeometry()  
        cp = QDesktopWidget().availableGeometry().center()  # Get screen center
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def perform_search(self):
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        search_word = self.search_input.text()
        Scraper().startProc(start, end, search_word)
        print(start, end, search_word)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DateSearchApp()
    window.show()
    # sys.exit(app.exec_())
    app.exec()
