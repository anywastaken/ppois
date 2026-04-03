from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QSpinBox, 
                             QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QHeaderView)

class SearchProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск товаров")
        self.resize(900, 500)
        
        # 1. Поля ввода критериев (согласно варианту 6)
        self.name_input = QLineEdit()
        self.manufacturer_input = QLineEdit()
        self.unp_input = QSpinBox()
        self.unp_input.setRange(0, 999999999)
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Число или 'нет на складе'")
        self.address_input = QLineEdit()
        
        form_layout = QFormLayout()
        form_layout.addRow("Название товара:", self.name_input)
        form_layout.addRow("Производитель:", self.manufacturer_input)
        form_layout.addRow("УНП:", self.unp_input)
        form_layout.addRow("Количество на складе:", self.quantity_input)
        form_layout.addRow("Адрес склада:", self.address_input)
        
        self.search_btn = QPushButton("Найти")
        
        # 2. Таблица для вывода результатов поиска
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels([
            "Товар", "Производитель", "УНП", "Кол-во", "Адрес"
        ])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # 3. Навигация по страницам поиска 
        self.page_label = QLabel("Страница: 1 / 1")
        self.prev_btn = QPushButton("<")
        self.next_btn = QPushButton(">")
        
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.page_label)
        nav_layout.addWidget(self.next_btn)
        
        # Основная компоновка
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.search_btn)
        main_layout.addWidget(self.result_table)
        main_layout.addLayout(nav_layout)
        
        self.setLayout(main_layout)

    def get_search_criteria(self):
        """Возвращает данные для фильтрации в Model """
        invalid_input = False
        if self.quantity_input.text() != 'нет на складе':
            try:
                int(self.quantity_input.text())
            except ValueError:
                invalid_input=True
        return {
            "name": self.name_input.text() or None,
            "manufacturer": self.manufacturer_input.text() or None,
            "unp": self.unp_input.value() if self.unp_input.value() > 0 else None,
            "quantity": self.quantity_input.text() if self.quantity_input.text() == 'нет на складе' 
            else None if invalid_input 
            else int(self.quantity_input.text()) or None,
            "address": self.address_input.text() or None
        }

    def update_results(self, products, current_page, total_pages):
        """Отображает найденные записи постранично """
        self.result_table.setRowCount(0)
        for row, p in enumerate(products):
            self.result_table.insertRow(row)
            self.result_table.setItem(row, 0, QTableWidgetItem(p.name))
            self.result_table.setItem(row, 1, QTableWidgetItem(p.manufacturer))
            self.result_table.setItem(row, 2, QTableWidgetItem(str(p.unp)))
            self.result_table.setItem(row, 3, QTableWidgetItem(str(p.quantity)))
            self.result_table.setItem(row, 4, QTableWidgetItem(p.address))
        
        self.page_label.setText(f"Страница: {current_page} / {total_pages}")