class DbRouter:
    books_app_label = 'books'

    def db_for_read(self, model, **hints):
        """
        Для чтения моделей из 'books' → 'gutendex',
        все остальные модели читаются из 'default'.
        """
        if model._meta.app_label == self.books_app_label:
            return 'gutendex'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Для записи (создания/обновления) любых моделей используем 'default'.
        """
        if model._meta.app_label == self.books_app_label:
            return None
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешаем все связи. Если нужно жестче — можно проверять
        obj1._state.db и obj2._state.db и разрешать только внутри одной БД.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Миграции:
         - В БД 'gutendex' не выполняем НИКАКИХ миграций (чисто read-only).
         - В БД 'default' выполняем миграции для всех моделей,
           кроме app_label='books'.
        """
        if db == 'gutendex':
            return False
        return app_label != self.books_app_label
