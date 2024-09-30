import unittest
import os
from unittest.mock import MagicMock, patch, mock_open
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from docx import Document
from main import MainWindow
    
class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.root = MagicMock()
        self.main_window = MainWindow(self.root)

    def tearDown(self):
        return

    @patch('main.filedialog.askopenfile')
    def test_open_file_txt(self, mock_askopenfile):
        file = open("src\\test_files\\plaintxtexample.txt", 'r')
        mock_askopenfile.return_value = file
        result = self.main_window.open_file()

        self.assertTrue(result, "File cannot be read")
        file.close()

    @patch('main.filedialog.askopenfile')
    def test_open_file_empty(self, mock_askopenfile):
        # todo
        return


    @patch('main.filedialog.askopenfile')
    def test_open_file_docx(self, mock_askopenfile):
        # todo
        return
    
    @patch('main.filedialog.askopenfile')
    def test_open_file_pdf(self, mock_askopenfile):
        # todo
        return

if __name__ == '__main__':
    unittest.main()