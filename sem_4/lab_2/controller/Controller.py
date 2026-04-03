from PyQt6.QtWidgets import QFileDialog, QMessageBox

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Настройки пагинации
        self.current_page = 0
        self.records_per_page = 10 

        # Связываем сигналы интерфейса с методами контроллера
        self._connect_signals()
        
        # Отображаем начальные данные
        self.refresh_main_table()

    def _connect_signals(self):
        """Подключение всех кнопок и действий к логике"""
        self.view.add_requested.connect(self.handle_add) 
        self.view.search_requested.connect(self.handle_search) 
        self.view.delete_requested.connect(self.handle_delete) 
        self.view.save_requested.connect(self.handle_save) 
        self.view.load_requested.connect(self.handle_load) 
        
        # Навигация 
        self.view.prev_page_requested.connect(self.prev_page)
        self.view.next_page_requested.connect(self.next_page)
        self.view.first_page_requested.connect(self.first_page)
        self.view.last_page_requested.connect(self.last_page)

    def refresh_main_table(self):
        """Обновление главной таблицы с учетом текущей страницы"""
        all_products = self.model.get_all() 
        total_records = len(all_products)
        
        # Расчет количества страниц
        total_pages = max(1, (total_records + self.records_per_page - 1) // self.records_per_page) 
        
        # Ограничение текущей страницы
        if self.current_page >= total_pages:
            self.current_page = total_pages - 1
        if self.current_page < 0:
            self.current_page = 0

        # Срез данных для текущей страницы
        start = self.current_page * self.records_per_page
        end = start + self.records_per_page
        page_data = all_products[start:end]

        # Передача данных во View для отрисовки
        self.view.update_table(page_data)
        self.view.update_pagination_info(self.current_page + 1, total_pages, total_records)

    def next_page(self):
        all_count = len(self.model.get_all())
        if (self.current_page + 1) * self.records_per_page < all_count:
            self.current_page += 1
            self.refresh_main_table()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh_main_table()

    def first_page(self):
        if self.current_page != 0:
            self.current_page = 0
            self.refresh_main_table()

    def last_page(self):
        all_products = self.model.get_all()
        total_records = len(all_products)
        total_pages = max(1, (total_records + self.records_per_page - 1) // self.records_per_page)
        
        if self.current_page != total_pages - 1:
            self.current_page = total_pages - 1
            self.refresh_main_table()

    def handle_add(self):
        """Логика добавления новой записи"""
        from view.AddProductDialog import AddProductDialog 
        dialog = AddProductDialog(self.view)
        
        if dialog.exec():
            data = dialog.get_data()
            from model.Product import Product
            new_product = Product(**data)
            self.model.add_product(new_product)
            self.refresh_main_table()

    def handle_delete(self):
        """Логика удаления записей по условиям"""
        from view.DeleteProductDialog import DeleteProductDialog
        dialog = DeleteProductDialog(self.view)
        
        if dialog.exec():
            criteria = dialog.get_filter_criteria() 
            removed_count = self.model.remove_products_by_criteria(**criteria) 
            if removed_count > 0:
                QMessageBox.information(self.view, "Успех", f"Удалено записей: {removed_count}")
            else:
                QMessageBox.warning(self.view, "Результат", "Записи по данным критериям не найдены")
            
            self.refresh_main_table()

    def handle_search(self):
        """Логика поиска с полноценной пагинацией по 10 записей"""
        from view.SearchProductDialog import SearchProductDialog
        dialog = SearchProductDialog(self.view)
        
        # Локальные переменные для хранения состояния поиска
        search_state = {
            "results": [],
            "current_page": 1,
            "items_per_page": 10
        }

        def update_dialog_view():
            """Вспомогательная функция для обновления таблицы в диалоге"""
            res = search_state["results"]
            page = search_state["current_page"]
            step = search_state["items_per_page"]
            
            total_pages = max(1, (len(res) + step - 1) // step)
            
            # Срез списка для текущей страницы
            start_idx = (page - 1) * step
            end_idx = start_idx + step
            products_to_show = res[start_idx:end_idx]
            
            # Обновляем таблицу и надпись страницы в диалоге
            dialog.update_results(products_to_show, page, total_pages)
            dialog.page_label.setText(f"Страница: {page} / {total_pages}")
            
            # Блокировка кнопок навигации
            dialog.prev_btn.setEnabled(page > 1)
            dialog.next_btn.setEnabled(page < total_pages)

        def perform_search():
            """Выполняется при нажатии кнопки 'Найти'"""
            criteria = dialog.get_search_criteria()
            # Получаем ВСЕ подходящие результаты из модели
            search_state["results"] = self.model.search_products(**criteria)
            search_state["current_page"] = 1 # Сброс на первую страницу при новом поиске
            update_dialog_view()

        def go_next():
            search_state["current_page"] += 1
            update_dialog_view()

        def go_prev():
            search_state["current_page"] -= 1
            update_dialog_view()

        # Привязываем события
        dialog.search_btn.clicked.connect(perform_search)
        dialog.next_btn.clicked.connect(go_next)
        dialog.prev_btn.clicked.connect(go_prev)
        
        # Инициализируем кнопки (выключаем их до первого поиска)
        dialog.prev_btn.setEnabled(False)
        dialog.next_btn.setEnabled(False)

        dialog.exec()

    def handle_save(self):
        """Сохранение в XML через DOM"""
        file_path, _ = QFileDialog.getSaveFileName(self.view, "Сохранить файл", "", "XML Files (*.xml)") 
        if file_path:
            if self.model.save_to_xml(file_path): 
                QMessageBox.information(self.view, "Сохранение", "Файл успешно сохранен (DOM)")
            else:
                QMessageBox.critical(self.view, "Ошибка", "Не удалось сохранить файл")

    def handle_load(self):
        """Загрузка из XML через SAX"""
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Открыть файл", "", "XML Files (*.xml)") 
        if file_path:
            self.model.file_path = file_path
            self.model.load_from_xml() # Вызывает SAX парсер [cite: 11]
            self.current_page = 0
            self.refresh_main_table()