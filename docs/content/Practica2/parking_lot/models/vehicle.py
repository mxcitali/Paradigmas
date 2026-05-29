from dataclasses import dataclass
from enum import Enum


class VehicleType(Enum):
    CAR = "Car"
    MOTORCYCLE = "Motorcycle"


@dataclass
class Vehicle:
    """Abstracción base de un vehículo."""
    _plate: str
    _type: VehicleType

    def get_plate(self) -> str:
        return self._plate

    def get_type(self) -> VehicleType:
        return self._type

    def __str__(self) -> str:
        return f"{self._type.value}({self._plate})"


class Car(Vehicle):
    """Subtipo: automóvil."""
    def __init__(self, plate: str):
        super().__init__(plate, VehicleType.CAR)


class Motorcycle(Vehicle):
    """Subtipo: motocicleta."""
    def __init__(self, plate: str):
        super().__init__(plate, VehicleType.MOTORCYCLE)


def create_vehicle(plate: str, vehicle_type: str) -> Vehicle:
    """Factory: crea el subtipo correcto según el tipo recibido."""
    plate = plate.strip().upper()
    vtype = vehicle_type.strip().lower()
    if vtype == "car":
        return Car(plate)
    elif vtype in ("motorcycle", "moto"):
        return Motorcycle(plate)
    else:
        raise ValueError(f"Tipo de vehículo desconocido: '{vehicle_type}'")
