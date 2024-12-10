
import sys
import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QDateEdit, QMessageBox, QListWidgetItem
from PyQt5.QtCore import QDate


# Диалог для добавления и редактирования заметок
class NoteDialog(QDialog):
    def init(self, title="", content="", date=None, parent=None):
        super().init(parent)
        self.setWindowTitle("Добавить заметку" if not title else "Редактировать заметку")
        self.layout = QVBoxLayout(self)

        # Поле для ввода названия заметки
        self.label_title = QLabel("Название заметки:")
        self.layout.addWidget(self.label_title)
        self.title_input = QLineEdit(self)
        self.title_input.setText(title)
        self.layout.addWidget(self.title_input)

        # Поле для ввода содержания заметки
        self.label_content = QLabel("Текст заметки:")
        self.layout.addWidget(self.label_content)
        self.content_input = QTextEdit(self)
        self.content_input.setFixedHeight(150)
        self.content_input.setText(content)
        self.layout.addWidget(self.content_input)

        # Поле для выбора даты заметки
        self.label_date = QLabel("Дата заметки:")
        self.layout.addWidget(self.label_date)
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(date if date else QDate.currentDate())
        self.layout.addWidget(self.date_input)

        # Кнопка сохранения
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.validate_input)  # Изменено: добавлен метод проверки
        self.layout.addWidget(self.save_button)

    # Метод для получения данных заметки
    def validate_input(self):
        if not self.title_input.text().strip() and not self.content_input.toPlainText().strip():
            QMessageBox.warning(self, "Ошибка", "Заполните хотя бы название или текст заметки.")
        else:
            self.accept()

    def get_data(self):
        return self.title_input.text(), self.content_input.toPlainText(), self.date_input.date().toString("yyyy-MM-dd")

# Основной интерфейс еженедельника
class Ui_Ezenedelnik(object):
    def setupUi(self, Ezenedelnik):
        Ezenedelnik.setObjectName("Ezenedelnik")
        Ezenedelnik.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Ezenedelnik)
        self.centralwidget.setObjectName("centralwidget")

        # Кнопка для удаления выбранной заметки
        self.Udalitzametky = QtWidgets.QPushButton(self.centralwidget)
        self.Udalitzametky.setGeometry(QtCore.QRect(385, 180, 360, 50))
        self.Udalitzametky.setStyleSheet(
            "QPushButton {border: 2px solid #FF0000; border-radius: 12px; background-color: #f0f0f0; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #FFCCCC;}"
        )
        self.Udalitzametky.setText("Удалить заметку")
        self.Udalitzametky.setObjectName("Udalitzametky")

        # Кнопка для отображения всех заметок
        self.show_all_notes_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_all_notes_button.setGeometry(QtCore.QRect(170, 18, 150, 40))
        self.show_all_notes_button.setText("Все заметки")
        self.show_all_notes_button.setStyleSheet("QPushButton {border: 2px solid #B0B0B0; border-radius: 12px; background-color: #E8E8E8; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #F0F0F0;}")

# Список заметок с оформлением
        self.ListZametok = QtWidgets.QListWidget(self.centralwidget)
        self.ListZametok.setGeometry(QtCore.QRect(40, 65, 281, 421))
        self.ListZametok.setObjectName("ListZametok")
        self.ListZametok.setStyleSheet("""
            QListWidget::item {
                border: 1px solid #B0B0B0;
                padding: 8px;
                margin: 5px 0;
                border-radius: 5px;
                background-color: #FFFFFF;
            }
            QListWidget::item:selected {
                background-color: #E0F7FA;
                color: #000000;
            }
        """)

        # Метка для списка заметок
        self.Moi_zametki = QtWidgets.QLabel(self.centralwidget)
        self.Moi_zametki.setGeometry(QtCore.QRect(40, 45, 121, 16))
        self.Moi_zametki.setObjectName("Moi_zametki")

        # Основные кнопки для добавления заметок по категориям
        self.add_urgent_note_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_urgent_note_button.setGeometry(QtCore.QRect(340, 30, 210, 60))
        self.add_urgent_note_button.setText("Срочное")
        self.add_urgent_note_button.setStyleSheet("QPushButton {border: 2px solid #4CAF50; border-radius: 12px; background-color: #f0f0f0; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #d0e4e8;}")

        self.add_important_note_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_important_note_button.setGeometry(QtCore.QRect(560, 30, 210, 60))
        self.add_important_note_button.setText("Важное")
        self.add_important_note_button.setStyleSheet("QPushButton {border: 2px solid #4CAF50; border-radius: 12px; background-color: #f0f0f0; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #d0e4e8;}")

        self.add_non_urgent_note_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_non_urgent_note_button.setGeometry(QtCore.QRect(340, 100, 210, 60))
        self.add_non_urgent_note_button.setText("Не срочное")
        self.add_non_urgent_note_button.setStyleSheet("QPushButton {border: 2px solid #4CAF50; border-radius: 12px; background-color: #f0f0f0; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #d0e4e8;}")

        self.add_non_important_note_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_non_important_note_button.setGeometry(QtCore.QRect(560, 100, 210, 60))
        self.add_non_important_note_button.setText("Не важное")
        self.add_non_important_note_button.setStyleSheet("QPushButton {border: 2px solid #4CAF50; border-radius: 12px; background-color: #f0f0f0; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #d0e4e8;}")

        # Кнопки для фильтрации заметок по категориям
        self.filter_urgent_button = QtWidgets.QPushButton(self.centralwidget)
        self.filter_urgent_button.setGeometry(QtCore.QRect(20, 500, 160, 40))
        self.filter_urgent_button.setText("Показать Срочное")
        self.filter_urgent_button.setStyleSheet("QPushButton {border: 2px solid #B0B0B0; border-radius: 12px; background-color: #E8E8E8; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #F0F0F0;}")

        self.filter_important_button = QtWidgets.QPushButton(self.centralwidget)
        self.filter_important_button.setGeometry(QtCore.QRect(185, 500, 160, 40))
        self.filter_important_button.setText("Показать Важное")
        self.filter_important_button.setStyleSheet("QPushButton {border: 2px solid #B0B0B0; border-radius: 12px; background-color: #E8E8E8; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #F0F0F0;}")

self.filter_non_urgent_button = QtWidgets.QPushButton(self.centralwidget)
        self.filter_non_urgent_button.setGeometry(QtCore.QRect(20, 550, 160, 40))
        self.filter_non_urgent_button.setText("Показать Не срочное")
        self.filter_non_urgent_button.setStyleSheet("QPushButton {border: 2px solid #B0B0B0; border-radius: 12px; background-color: #E8E8E8; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #F0F0F0;}")

        self.filter_non_important_button = QtWidgets.QPushButton(self.centralwidget)
        self.filter_non_important_button.setGeometry(QtCore.QRect(185, 550, 160, 40))
        self.filter_non_important_button.setText("Показать Не важное")
        self.filter_non_important_button.setStyleSheet("QPushButton {border: 2px solid #B0B0B0; border-radius: 12px; background-color: #E8E8E8; padding: 10px; font-size: 14px;} QPushButton:hover {background-color: #F0F0F0;}")

        # Календарь для выбора даты
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(350, 250, 430, 250))
        self.calendarWidget.setObjectName("calendarWidget")

        # Подключение кнопок к функциям
        self.add_urgent_note_button.clicked.connect(lambda: self.add_note_with_category("Срочное"))
        self.add_important_note_button.clicked.connect(lambda: self.add_note_with_category("Важное"))
        self.add_non_urgent_note_button.clicked.connect(lambda: self.add_note_with_category("Не срочное"))
        self.add_non_important_note_button.clicked.connect(lambda: self.add_note_with_category("Не важное"))

        # Подключение кнопок фильтрации к функциям
        self.filter_urgent_button.clicked.connect(lambda: self.show_notes_by_category("Срочное"))
        self.filter_important_button.clicked.connect(lambda: self.show_notes_by_category("Важное"))
        self.filter_non_urgent_button.clicked.connect(lambda: self.show_notes_by_category("Не срочное"))
        self.filter_non_important_button.clicked.connect(lambda: self.show_notes_by_category("Не важное"))

        # Подключение к удалению заметок, отображению всех заметок и выбору даты
        self.Udalitzametky.clicked.connect(self.remove_note)
        self.show_all_notes_button.clicked.connect(self.show_all_notes)
        self.calendarWidget.clicked.connect(self.show_notes_for_date)

        # Двойной клик для редактирования заметок
        self.ListZametok.itemDoubleClicked.connect(self.edit_note)

        Ezenedelnik.setCentralWidget(self.centralwidget)
        self.retranslateUi(Ezenedelnik)
        self.load_notes()
        self.show_all_notes()

    # Устанавливает тексты для элементов интерфейса, включая заголовок окна и текст для метки "Мои заметки".
    def retranslateUi(self, Ezenedelnik):
        _translate = QtCore.QCoreApplication.translate
        Ezenedelnik.setWindowTitle(_translate("Ezenedelnik", "Еженедельник"))
        self.Moi_zametki.setText(_translate("Ezenedelnik", "Мои заметки"))

    # Загрузка заметок из файла
    def load_notes(self):
        try:
            with open("notes.json", "r", encoding="utf-8") as f:
                self.notes = json.load(f)
        except FileNotFoundError:
            self.notes = []

    # Сохранение заметок в файл
    def save_notes(self):
        with open("notes.json", "w", encoding="utf-8") as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=4)

    # Добавление заметки в виджет списка
    def add_note_to_list(self, note):
        if isinstance(note, dict):
            display_content = note['content'][:40] + '...' if len(note['content']) > 40 else note['content']
            item_text = f"{note['date']} - {note['title']}: {display_content}"
            list_item = QListWidgetItem(item_text)
            list_item.setData(QtCore.Qt.UserRole, note)
            self.ListZametok.addItem(list_item)
        else:
            print("Неверный формат заметки:", note)

# Метод добавления заметки с категорией
    def edit_note(self, item):
        note = item.data(QtCore.Qt.UserRole)
        dialog = NoteDialog(note['title'], note['content'], QDate.fromString(note['date'], "yyyy-MM-dd"))
        if dialog.exec_() == QDialog.Accepted:
            title, content, date = dialog.get_data()
            note['title'] = title
            note['content'] = content
            note['date'] = date
            self.save_notes()
            self.show_all_notes()

    # Метод редактирования выбранной заметки
    def remove_note(self):
        selected_items = self.ListZametok.selectedItems()
        if not selected_items:
            return

        # Создаем диалоговое окно вручную
        reply = QMessageBox(self.centralwidget)
        reply.setWindowTitle("Подтверждение")
        reply.setText("Вы уверены, что хотите удалить выбранные заметки?")

        # Добавляем кнопки с нужными текстами
        yes_button = reply.addButton("Да", QMessageBox.YesRole)
        no_button = reply.addButton("Нет", QMessageBox.NoRole)

        # Показываем диалоговое окно
        reply.exec_()

        # Проверяем, какая кнопка была нажата
        if reply.clickedButton() == yes_button:
            for item in selected_items:
                self.ListZametok.takeItem(self.ListZametok.row(item))
                self.notes.remove(item.data(QtCore.Qt.UserRole))
            self.save_notes()

    # Отображение всех заметок в списке
    def show_all_notes(self):
        self.ListZametok.clear()
        for note in self.notes:
            self.add_note_to_list(note)

    # Фильтрация заметок по категории
    def show_notes_by_category(self, category):
        self.ListZametok.clear()
        for note in self.notes:
            if note.get("category") == category:
                self.add_note_to_list(note)

    # Показать заметки для выбранной даты из календаря
    def show_notes_for_date(self, date):
        self.ListZametok.clear()
        for note in self.notes:
            if note.get("date") == date.toString("yyyy-MM-dd"):
                self.add_note_to_list(note)

    # Сохраняет заметку в списке и обновляет отображение всех заметок.
    def add_note_with_category(self, category):
        dialog = NoteDialog()
        if dialog.exec_() == QDialog.Accepted:
            title, content, date = dialog.get_data()
            title = f"{category} - {title}"  # Добавляем категорию к названию
            new_note = {"title": title, "content": content, "date": date, "category": category}
            self.notes.append(new_note)
            self.save_notes()
            self.show_all_notes()

# Запуск приложения
if name == "main":
    app = QtWidgets.QApplication(sys.argv)
    Ezenedelnik = QtWidgets.QMainWindow()
    ui = Ui_Ezenedelnik()
    ui.setupUi(Ezenedelnik)
    Ezenedelnik.show()
    sys.exit(app.exec_())
