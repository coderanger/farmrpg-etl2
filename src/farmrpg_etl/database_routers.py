class GameRouter:
    """
    A router to send unmanaged models to game_prod by default.
    """

    def db_for_read(self, model, **hints):
        return "default" if model._meta.managed else "game_prod"

    def db_for_write(self, model, **hints):
        if model._meta.managed:
            return "default"
        raise Exception("Writing not allowed")

    def allow_relation(self, obj1, obj2, **hints):
        return obj1._meta.managed and obj2._meta.managed

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"
