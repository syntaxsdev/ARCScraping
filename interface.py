import sys, os, threading, asyncio, time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
from ARCScraping import ARCScraping

class WebScraperGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Virginia Tech Applied Research Corporation: Web Scraper'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 250
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('data/VTARClogo.png'))
        
        self.input_label = QLabel(self)
        self.input_label.setText('Input File:')
        self.input_label.move(20, 20)

        self.input_entry = QLineEdit(self)
        self.input_entry.move(100, 20)
        self.input_entry.resize(280, 25)

        self.input_button = QPushButton('Select File', self)
        self.input_button.move(385, 20)
        self.input_button.clicked.connect(self.select_input_file)

        self.process_button = QPushButton('Process', self)
        self.process_button.move(200, 100)
        self.process_button.clicked.connect(self.process_csv)
        
        self.process_label = QLabel(self)
        self.process_label.move(200, 150)
        self.process_label.resize(200, 25)

        self.stat1 = QLabel(self)
        self.stat1.move(50, 175)
        self.stat1.resize(200, 25)

        self.stat2 = QLabel(self)
        self.stat2.move(50, 200)
        self.stat2.resize(200, 25)

        self.stat3 = QLabel(self)
        self.stat3.move(50, 225)
        self.stat3.resize(200, 25)


    def select_input_file(self):
        input_path, _ = QFileDialog.getOpenFileName(self, 'Select File', '', 'CSV Files (*.csv)')
        if input_path:
            self.input_path = input_path
            self.input_entry.setText(self.input_path)
    
    def process_csv(self):
        input_path = self.input_path
        self.process_button.setEnabled(False)
        self.process_label.setText('Processing...')

        # Work around for async methods
        process = threading.Thread(target=self.async_process_handler)
        process.start()


    def async_process_handler(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task = loop.create_task(self.process_csv_thread(self.input_path))
        loop.run_until_complete(task)
        loop.close()

    async def process_csv_thread(self, input_path):
        self.start_time = time.time()

        arc = ARCScraping(input_path)
        researcher_count = len(arc.researchers_scraped)
        self.stat1.setText(f"Total Researchers: {researcher_count}")
        self.stat2.setText(f"Est Time: {researcher_count * 40} - {researcher_count * 80} secs")
        self
        elapsed_timer = threading.Thread(target=self.thread_elapsed_time)
        elapsed_timer.start()
        await arc.run()
        self.process_label.setText('Done.')
        self.process_button.setEnabled(True)

    def thread_elapsed_time(self):
        while (self.process_button.isEnabled() == False):
            time.sleep(1)
            self.stat3.setText(f"Running Time: {(time.time() - self.start_time):.0f} secs")
        self.stat3.setText(f"Complete Time: {(time.time() - self.start_time):.0f)} secs")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WebScraperGUI()
    ex.show()
    sys.exit(app.exec_())
