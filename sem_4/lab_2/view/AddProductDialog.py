from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, 
                             QSpinBox, QDialogButtonBox, QVBoxLayout)

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить новый товар")
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Поля ввода 
        self.name_input = QLineEdit()
        self.manufacturer_input = QLineEdit()
        self.unp_input = QSpinBox()
        self.unp_input.setRange(0, 999999999)
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Число или 'нет на складе'")
        
        self.address_input = QLineEdit()

        # Добавляем на форму
        form_layout.addRow("Название товара:", self.name_input)
        form_layout.addRow("Производитель:", self.manufacturer_input)
        form_layout.addRow("УНП:", self.unp_input)
        form_layout.addRow("Количество:", self.quantity_input)
        form_layout.addRow("Адрес склада:", self.address_input)

        # Кнопки ОК и Отмена
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_data(self):
        """Возвращает введенные данные в виде словаря"""
        return {
            "name": self.name_input.text(),
            "manufacturer": self.manufacturer_input.text(),
            "unp": self.unp_input.value(),
            "quantity": self.quantity_input.text(),
            "address": self.address_input.text()
        }