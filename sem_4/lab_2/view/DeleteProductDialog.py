from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, 
                             QSpinBox, QDialogButtonBox, QVBoxLayout, QCheckBox)

class DeleteProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удаление записей")
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Поля для ввода условий удаления
        self.name_input = QLineEdit()
        self.manufacturer_input = QLineEdit()
        
        self.unp_input = QSpinBox()
        self.unp_input.setRange(0, 999999999)
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 999999999)
        self.address_input = QLineEdit()

        form_layout.addRow("Название товара:", self.name_input)
        form_layout.addRow("Производитель:", self.manufacturer_input)
        form_layout.addRow("УНП производителя:", self.unp_input)
        form_layout.addRow("Количество на складе:", self.quantity_input)
        form_layout.addRow("Адрес склада:", self.address_input)

        # Кнопки
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_filter_criteria(self):
        """
        Собирает только заполненные поля. 
        Если поле пустое, возвращаем None, чтобы Модель его игнорировала.
        """
        return {
            "name": self.name_input.text() if self.name_input.text() else None,
            "manufacturer": self.manufacturer_input.text() if self.manufacturer_input.text() else None,
            "unp": self.unp_input.value() if self.unp_input.value() > 0 else None,
            "quantity": self.quantity_input.value() if self.quantity_input.value() > 0 else None,
            "address": self.address_input.text() if self.address_input.text() else None
        }