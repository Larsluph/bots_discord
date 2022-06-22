class MapParameter:
    DEFAULT_VALUES = (
        ("min_delay", "20m"),
        ("max_delay", "12h")
    )
    
    @staticmethod
    def create_table():
        return 'CREATE TABLE "parameter" ("id" INTEGER, "name" TEXT NOT NULL UNIQUE, "value" TEXT NOT NULL,	PRIMARY KEY("id" AUTOINCREMENT));'
    
    @staticmethod
    def fill_table():
        return 'INSERT INTO "parameter" ("name", "value") VALUES (?, ?);'
    
    @staticmethod
    def select():
        pass

    @staticmethod
    def insert():
        pass

    @staticmethod
    def update():
        pass

    @staticmethod
    def delete():
        pass
