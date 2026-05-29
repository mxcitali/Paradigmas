from dataclasses import dataclass, field
from enum import Enum
from models.vehicle import Vehicle, VehicleType


class SpotType(Enum):
    CAR = "Car"
    MOTORCYCLE = "Motorcycle"
    ANY = "Any"


@dataclass
class ParkingSpot:
    """Representa un lugar físico del estacionamiento."""
    _spot_id: str
    _allowed: SpotType
    _occupied: bool = field(default=False, init=False)
    _current_vehicle: Vehicle | None = field(default=None, init=False)

    def get_id(self) -> str:
        return self._spot_id

    def get_allowed(self) -> SpotType:
        return self._allowed

    def is_occupied(self) -> bool:
        return self._occupied

    def get_current_vehicle(self) -> Vehicle | None:
        return self._current_vehicle

    def is_available_for(self, vehicle: Vehicle) -> bool:
        """Verifica compatibilidad del vehículo con este spot."""
        if self._occupied:
            return False
        if self._allowed == SpotType.ANY:
            return True
        if self._allowed == SpotType.CAR and vehicle.get_type() == VehicleType.CAR:
            return True
        if self._allowed == SpotType.MOTORCYCLE and vehicle.get_type() == VehicleType.MOTORCYCLE:
            return True
        return False

    def park(self, vehicle: Vehicle) -> None:
        """Ocupa el lugar con el vehículo dado. Valida invariante."""
        if self._occupied:
            raise RuntimeError(f"El spot {self._spot_id} ya está ocupado.")
        if not self.is_available_for(vehicle):
            raise ValueError(f"El vehículo {vehicle} no es compatible con el spot {self._spot_id}.")
        self._current_vehicle = vehicle
        self._occupied = True

    def release(self) -> None:
        """Libera el lugar."""
        self._current_vehicle = None
        self._occupied = False

    def to_dict(self) -> dict:
        return {
            "spot_id": self._spot_id,
            "allowed": self._allowed.value,
            "occupied": self._occupied,
            "vehicle": str(self._current_vehicle) if self._current_vehicle else None,
        }
