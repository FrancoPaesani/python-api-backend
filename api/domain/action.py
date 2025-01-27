class Action:
    def __init__(self, description: str, id: int = None):
        self.set_description(description)
        self.id = id

    def set_description(self, description: str):
        if len(description) <= 3:
            raise ValueError("La descripción debe ser mayor a 3 caracteres.")
        self.description = description
