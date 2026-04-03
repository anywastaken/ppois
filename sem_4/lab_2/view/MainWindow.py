from PyQt6.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, 
                             QVBoxLayout, QHBoxLayout, QPushButton, 
                             QWidget, QToolBar, QLabel, QHeaderView)
from PyQt6.QtCore import pyqtSignal

class MainWindow(QMainWindow):
    # Сигналы для контроллера
    add_requested = pyqtSignal()
    search_requested = pyqtSignal()
    delete_requested = pyqtSignal()
    save_requested = pyqtSignal()
    load_requested = pyqtSignal()
    next_page_requested = pyqtSignal()
    prev_page_requested = pyqtSignal()
    first_page_requested = pyqtSignal()
    last_page_requested = pyqtSignal()
    

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Складской учет товаров — Вариант 6")
        self.resize(1000, 600)
        
        # Панель инструментов
        self._create_toolbar()

        # Таблица для отображения данных
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Название товара", "Производитель", "УНП", "Количество", "Адрес склада"
        ])
        # Растягиваем колонки по ширине окна
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Элементы навигации
        self.page_info_label = QLabel("Страница: 1 / 1")
        self.total_records_label = QLabel("Всего записей: 0")
        self.prev_btn = QPushButton(" < Назад ")
        self.next_btn = QPushButton(" Вперед > ")
        self.first_btn = QPushButton(" << ")
        self.last_btn = QPushButton(" >> ")
        
        # Связываем кнопки с нашими сигналами
        self.prev_btn.clicked.connect(self.prev_page_requested.emit)
        self.next_btn.clicked.connect(self.next_page_requested.emit)
        self.first_btn.clicked.connect(self.first_page_requested.emit)
        self.last_btn.clicked.connect(self.last_page_requested.emit)

        # Компоновка интерфейса
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)

        # Панель пагинации внизу
        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(self.total_records_label)
        pagination_layout.addStretch() # Пружина, чтобы кнопки были по центру
        pagination_layout.addWidget(self.first_btn)
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_info_label)
        pagination_layout.addWidget(self.next_btn)
        pagination_layout.addWidget(self.last_btn)
        pagination_layout.addStretch()

        main_layout.addLayout(pagination_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _create_toolbar(self):
        """Создание панели инструментов с кнопками """
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Добавляем действия (Actions)
        btn_load = toolbar.addAction("Открыть")
        btn_load.triggered.connect(self.load_requested.emit)

        btn_save = toolbar.addAction("Сохранить")
        btn_save.triggered.connect(self.save_requested.emit)

        toolbar.addSeparator()

        btn_add = toolbar.addAction("Добавить")
        btn_add.triggered.connect(self.add_requested.emit)

        btn_search = toolbar.addAction("Поиск")
        btn_search.triggered.connect(self.search_requested.emit)

        btn_delete = toolbar.addAction("Удалить")
        btn_delete.triggered.connect(self.delete_requested.emit)

    def update_table(self, products):
        """Метод для заполнения таблицы данными из Модели """
        self.table.setRowCount(0)
        for row, product in enumerate(products):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(product.name))
            self.table.setItem(row, 1, QTableWidgetItem(product.manufacturer))
            self.table.setItem(row, 2, QTableWidgetItem(str(product.unp)))
            self.table.setItem(row, 3, QTableWidgetItem(str(product.quantity)))
            self.table.setItem(row, 4, QTableWidgetItem(product.address))

    def update_pagination_info(self, current, total_pages, total_records):
        """Обновление текстовых счетчиков страниц """
        self.page_info_label.setText(f"Страница: {current} / {total_pages}")
        self.total_records_label.setText(f"Всего записей: {total_records}")