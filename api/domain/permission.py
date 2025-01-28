class Permission:
    def __init__(self, code: str, name: str, id: int | None = None):
        self.id = id
        self.set_code(code)
        self.set_name(name)

    def set_code(self, code: str):
        if len(code) != 3:
            raise ValueError(
                "El código del permiso debe contener exactamente 3 caracteres"
            )
        self.code = code

    def set_name(self, name: str):
        if len(name) < 10:
            raise ValueError(
                "El nombre del permiso debe tener por lo menos 10 caracteres."
            )
        self.name = name
