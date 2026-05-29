from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from models.vehicle import Vehicle
from models.spot import ParkingSpot


class TicketStatus(Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


@dataclass
class Ticket:
    """Representa el registro de una estancia en el estacionamiento."""
    _ticket_id: int
    _vehicle: Vehicle
    _spot: ParkingSpot
    _entry_time: datetime
    _exit_time: datetime | None = field(default=None, init=False)
    _status: TicketStatus = field(default=TicketStatus.ACTIVE, init=False)

    def get_id(self) -> int:
        return self._ticket_id

    def get_vehicle(self) -> Vehicle:
        return self._vehicle

    def get_spot(self) -> ParkingSpot:
        return self._spot

    def get_entry_time(self) -> datetime:
        return self._entry_time

    def get_exit_time(self) -> datetime | None:
        return self._exit_time

    def get_status(self) -> TicketStatus:
        return self._status

    def get_duration_hours(self) -> float:
        """Calcula duración en horas. Requiere que el ticket esté cerrado."""
        if self._exit_time is None:
            raise RuntimeError("El ticket aún está activo.")
        delta = self._exit_time - self._entry_time
        return max(delta.total_seconds() / 3600, 0.0)

    def close(self, exit_time: datetime) -> None:
        """Cierra el ticket registrando la hora de salida."""
        if self._status == TicketStatus.CLOSED:
            raise RuntimeError(f"El ticket #{self._ticket_id} ya está cerrado.")
        self._exit_time = exit_time
        self._status = TicketStatus.CLOSED

    def to_dict(self) -> dict:
        return {
            "ticket_id": self._ticket_id,
            "plate": self._vehicle.get_plate(),
            "vehicle_type": self._vehicle.get_type().value,
            "spot_id": self._spot.get_id(),
            "entry_time": self._entry_time.strftime("%Y-%m-%d %H:%M:%S"),
            "exit_time": self._exit_time.strftime("%Y-%m-%d %H:%M:%S") if self._exit_time else None,
            "status": self._status.value,
        }
