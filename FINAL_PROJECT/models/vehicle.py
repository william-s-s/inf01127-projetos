class Vehicle:
    def __init__(self, plate, color, model):
        self.plate = plate
        self.color = color
        self.model = model

    def __str__(self):
        return f"{self.model} ({self.color}) - Plate: {self.plate}"
