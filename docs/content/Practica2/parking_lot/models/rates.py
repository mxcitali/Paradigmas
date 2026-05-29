from typing import Protocol, runtime_checkable
from models.vehicle import Vehicle, VehicleType


@runtime_checkable
class RatePolicy(Protocol):
    """Interfaz común (abstracción) para cualquier política de cobro."""
    def calculate(self, hours: float, vehicle: Vehicle) -> float:
        ...

    def description(self) -> str:
        ...


class HourlyRatePolicy:
    """Cobra por hora según el tipo de vehículo (polimorfismo en tarifa)."""

    def __init__(self, car_rate: float = 20.0, moto_rate: float = 10.0):
        self._car_rate = car_rate
        self._moto_rate = moto_rate

    def calculate(self, hours: float, vehicle: Vehicle) -> float:
        rate = self._car_rate if vehicle.get_type() == VehicleType.CAR else self._moto_rate
        return round(hours * rate, 2)

    def description(self) -> str:
        return f"Por hora (Auto: ${self._car_rate}/h, Moto: ${self._moto_rate}/h)"


class FlatRatePolicy:
    """Cobra una tarifa fija sin importar el tiempo ni el tipo."""

    def __init__(self, flat_amount: float = 50.0):
        self._flat_amount = flat_amount

    def calculate(self, hours: float, vehicle: Vehicle) -> float:
        return self._flat_amount

    def description(self) -> str:
        return f"Tarifa plana: ${self._flat_amount}"


class TieredRatePolicy:
    """Primeras N horas a tarifa base; horas extra a tarifa mayor."""

    def __init__(self, base_rate: float = 15.0, extra_rate: float = 25.0, threshold_hours: float = 3.0):
        self._base_rate = base_rate
        self._extra_rate = extra_rate
        self._threshold = threshold_hours

    def calculate(self, hours: float, vehicle: Vehicle) -> float:
        if hours <= self._threshold:
            return round(hours * self._base_rate, 2)
        base = self._threshold * self._base_rate
        extra = (hours - self._threshold) * self._extra_rate
        return round(base + extra, 2)

    def description(self) -> str:
        return (f"Escalonada: primeras {self._threshold}h a ${self._base_rate}/h, "
                f"resto a ${self._extra_rate}/h")
