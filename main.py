import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyMuPDF PDF Viewer")
        self.resize(800, 1000)

        self.label = QLabel("Open a PDF file to display the first page.", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.open_button = QPushButton("Open PDF")
        self.open_button.clicked.connect(self.open_pdf)

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                doc = fitz.open(file_path)
                page = doc.load_page(0)
                pix = page.get_pixmap(dpi=150)
                img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(img)
                self.label.setPixmap(pixmap)
                self.label.setScaledContents(True)
            except Exception as e:
                self.label.setText(f"Failed to load PDF: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())