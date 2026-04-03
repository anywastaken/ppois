import xml.dom.minidom
from model.ProductHandler import ProductHandler
import os

class Database:
    def __init__(self, file_path="data.xml"):
        self.file_path = file_path
        self._products = []
        if os.path.exists(self.file_path):
            self.load_from_xml()
        else:
            print(f"Файл {self.file_path} не найден. Создана пустая база.")

    def load_from_xml(self):
        """Чтение файла с использованием SAX парсера """
        try:
            handler = ProductHandler()
            parser = xml.sax.make_parser()
            parser.setContentHandler(handler)
            parser.parse(self.file_path)
            
            self._products = handler.products
            print(f"Загружено записей: {len(self._products)}")
        except Exception as e:
            print(f"Ошибка при чтении XML: {e}")
            self._products = []

    def add_product(self, product):
        self._products.append(product)

    def remove_products_by_criteria(self, name=None, quantity=None, manufacturer=None, unp=None, address=None):

        if all(v is None for v in [name, quantity, manufacturer, unp, address]):
            return 0
        initial_count = len(self._products)
        
        self._products = [
            p for p in self._products if not (
                (name is None or p.name == name) and
                (quantity is None or p.quantity == quantity) and
                (manufacturer is None or p.manufacturer == manufacturer) and
                (unp is None or p.unp == unp) and
                (address is None or p.address == address)
            )
        ]
        
        removed_count = initial_count - len(self._products)
        return removed_count
    
    def search_products(self, name=None, quantity=None, manufacturer=None, unp=None, address=None):

        if all(v is None for v in [name, quantity, manufacturer, unp, address]):
            return []

        results = [
            p for p in self._products if (
                (name is None or name.lower() in p.name.lower()) and
                (quantity is None or p.quantity == quantity) and
                (manufacturer is None or manufacturer.lower() in p.manufacturer.lower()) and
                (unp is None or p.unp == unp) and
                (address is None or address.lower() in p.address.lower())
            )
        ]
        
        return results

    def save_to_xml(self, file_path):
        
        doc = xml.dom.minidom.Document()
        
        root = doc.createElement('inventory')
        doc.appendChild(root)

        for product in self._products:
            product_node = doc.createElement('product')
            root.appendChild(product_node)

            # Вспомогательная функция для создания вложенных текстовых узлов
            def create_element(name, value):
                element = doc.createElement(name)
                text = doc.createTextNode(str(value))
                element.appendChild(text)
                product_node.appendChild(element)

            # Создаем структуру
            create_element('name', product.name)
            create_element('manufacturer', product.manufacturer)
            create_element('unp', product.unp)
            create_element('quantity', product.quantity)
            create_element('address', product.address)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc.toprettyxml(indent="    ", encoding="utf-8").decode('utf-8'))
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False

    def get_all(self):
        """Возвращает весь текущий массив записей[cite: 9]."""
        return self._products

    def get_count(self):
        """Возвращает общее число доступных записей."""
        return len(self._products)