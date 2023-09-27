import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from pytube import YouTube
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio


class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YouTube MP3 Downloader')
        self.setGeometry(100, 100, 500, 250)
        self.setWindowIcon(QIcon('youtube_logo.png'))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Créez un widget QLabel pour l'image
        youtube_logo = QLabel(self)
        pixmap = QPixmap('youtube_logo.png')

        youtube_logo.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        youtube_logo.setAlignment(Qt.AlignCenter)
        youtube_logo.setScaledContents(True)

        # Créez un conteneur QHBoxLayout pour l'image centrée
        image_layout = QHBoxLayout()
        image_layout.addWidget(youtube_logo)
        image_layout.addStretch(1)  # Ajoutez de l'espace flexible pour centrer l'image

        self.layout.addLayout(image_layout)  # Ajoutez le layout de l'image

        self.url_label = QLabel('Enter YouTube URL:', self)
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Paste URL here')

        self.filename_label = QLabel('Custom Filename:', self)
        self.filename_input = QLineEdit(self)
        self.filename_input.setPlaceholderText('Enter custom filename (optional)')

        self.download_button = QPushButton('Download MP3', self)
        self.choose_path_button = QPushButton('Choose Download Path', self)

        self.download_button.clicked.connect(self.download_mp3)
        self.choose_path_button.clicked.connect(self.choose_download_path)

        # Appliquez le style pour les boutons et le QLineEdit
        self.download_button.setStyleSheet(
            """
            QPushButton {
                background-color: #FF5733;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E64A2D;
            }
            """
        )
        self.choose_path_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            """
        )
        self.url_input.setStyleSheet(
            """
            QLineEdit {
                padding: 5px;
                border: 2px solid #3498DB;
                border-radius: 5px;
            }
            """
        )

        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.filename_label)
        self.layout.addWidget(self.filename_input)
        self.layout.addWidget(self.choose_path_button)
        self.layout.addWidget(self.download_button)

        self.central_widget.setLayout(self.layout)

        self.download_path = os.path.expanduser("~")

    def download_mp3(self):
        url = self.url_input.text()
        custom_filename = self.filename_input.text()

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            video_path = stream.download(output_path=self.download_path)
        except Exception as e:
            error_message = f"An error occurred while downloading the video: {str(e)}"
            print(error_message)
            self.show_error_message(error_message)
            return

        if not custom_filename:
            custom_filename = yt.title  # Utilisez le titre de la vidéo comme nom de fichier par défaut

        mp3_filename = f"{custom_filename}.mp3"
        mp3_path = os.path.join(self.download_path, mp3_filename)

        try:
            ffmpeg_extract_audio(video_path, mp3_path)
            os.remove(video_path)
            success_message = f"The file '{mp3_filename}' was successfully downloaded as MP3 in {self.download_path}."
            print(success_message)
            self.show_success_message(success_message)
        except Exception as e:
            error_message = f"An error occurred while converting the video to MP3: {str(e)}"
            print(error_message)
            self.show_error_message(error_message)
            return

        self.url_input.clear()
        self.filename_input.clear()

    def choose_download_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        download_path = QFileDialog.getExistingDirectory(self, "Choose Download Path", self.download_path, options=options)

        if download_path:
            self.download_path = download_path

    def show_success_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Download Successful")
        msg.setText(message)
        msg.exec_()

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()


def main():
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
