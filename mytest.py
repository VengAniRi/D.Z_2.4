import unittest
from unittest.mock import patch
import app
from io import StringIO


class AppTests(unittest.TestCase):
    def setUp(self):
        app.documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]

        app.directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': []
        }

    @patch('builtins.input', lambda *args: '2207 876234')
    def test_get_doc_owner_name_good(self):
        self.assertEqual(app.get_doc_owner_name(), "Василий Гупкин")

    @patch('builtins.input', lambda *args: '123')
    def test_get_doc_owner_name_bad(self):
        self.assertEqual(app.get_doc_owner_name(), None)

    @patch('builtins.input', lambda *args: '2207 876234')
    def test_get_doc_shelf_good(self):
        self.assertEqual(app.get_doc_shelf(), '1')

    @patch('builtins.input', lambda *args: '123')
    def test_get_doc_shelf_bad(self):
        self.assertEqual(app.get_doc_shelf(), None)

    def test_show_all_docs_info(self):
        correct_answer = 'Список всех документов:\n\n' \
                       'passport "2207 876234" "Василий Гупкин"\n' \
                       'invoice "11-2" "Геннадий Покемонов"\n' \
                       'insurance "10006" "Аристарх Павлов"\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            app.show_all_docs_info()
            self.assertEqual(fake_out.getvalue(), correct_answer)

    @patch('builtins.input', side_effect=['123', 'passport', 'Ivanov', '2'])
    def test_add_new_doc_old_shelf(self, mock_inputs):
        documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
            {"type": "passport", "number": "123", "name": "Ivanov"}
        ]
        directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006', '123'],
            '3': []
        }
        self.assertEqual(app.add_new_doc(), '2')
        self.assertEqual(app.documents, documents)
        self.assertEqual(app.directories, directories)

    @patch('builtins.input', side_effect=['123', 'passport', 'Ivanov', '5'])
    def test_add_new_doc_bad_new_self(self, mock_inputs):
        documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
            {"type": "passport", "number": "123", "name": "Ivanov"}
        ]
        directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': [],
            '5': ['123']
        }
        self.assertEqual(app.add_new_doc(), '5')
        self.assertEqual(app.documents, documents)
        self.assertEqual(app.directories, directories)

    @patch('builtins.input', lambda *args: '11-2')
    def test_delete_doc_good(self):
        documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
        ]
        directories = {
            '1': ['2207 876234', '5455 028765'],
            '2': ['10006'],
            '3': []
        }
        self.assertEqual(app.delete_doc(), ('11-2', True))
        self.assertEqual(app.documents, documents)
        self.assertEqual(app.directories, directories)

    @patch('builtins.input', lambda *args: '11-3')
    def test_delete_doc_bad(self):
        documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]

        directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': []
        }
        self.assertEqual(app.delete_doc(), None)
        self.assertEqual(app.documents, documents)
        self.assertEqual(app.directories, directories)

if __name__ == '__main__':
    unittest.main()
