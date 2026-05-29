from datetime import datetime
from models.vehicle import Vehicle
from models.spot import ParkingSpot, SpotType
from models.ticket import Ticket, TicketStatus
from models.rates import RatePolicy, HourlyRatePolicy


def _build_default_spots() -> list[ParkingSpot]:
    """Crea el conjunto inicial de spots: 6 para autos, 4 para motos."""
    spots = []
    for i in range(1, 7):
        spots.append(ParkingSpot(f"A{i}", SpotType.CAR))
    for i in range(1, 5):
        spots.append(ParkingSpot(f"M{i}", SpotType.MOTORCYCLE))
    return spots


class ParkingLot:
    """
    Administra spots, tickets activos y recaudación.
    Composición: contiene ParkingSpot y Ticket.
    Abstracción: la política de cobro se inyecta (RatePolicy).
    """

    def __init__(self, spots: list[ParkingSpot] | None = None, policy: RatePolicy | None = None):
        self._spots: list[ParkingSpot] = spots if spots is not None else _build_default_spots()
        self._policy: RatePolicy = policy if policy is not None else HourlyRatePolicy()
        self._active_tickets: dict[int, Ticket] = {}
        self._next_ticket_id: int = 1
        self._total_revenue: float = 0.0

    # ── Consultas ──────────────────────────────────────────────────────────────

    def get_spots(self) -> list[ParkingSpot]:
        return list(self._spots)

    def get_policy(self) -> RatePolicy:
        return self._policy

    def set_policy(self, policy: RatePolicy) -> None:
        self._policy = policy

    def get_active_tickets(self) -> list[Ticket]:
        return list(self._active_tickets.values())

    def get_total_revenue(self) -> float:
        return self._total_revenue

    def get_occupancy(self) -> str:
        total = len(self._spots)
        occupied = sum(1 for s in self._spots if s.is_occupied())
        free = total - occupied
        return f"libres={free} ocupados={occupied} total={total}"

    def get_occupancy_dict(self) -> dict:
        total = len(self._spots)
        occupied = sum(1 for s in self._spots if s.is_occupied())
        return {"total": total, "occupied": occupied, "free": total - occupied}

    # ── Lógica de negocio ──────────────────────────────────────────────────────

    def _find_available_spot(self, vehicle: Vehicle) -> ParkingSpot | None:
        """Busca el primer spot compatible disponible."""
        for spot in self._spots:
            if spot.is_available_for(vehicle):
                return spot
        return None

    def enter(self, vehicle: Vehicle, now: datetime | None = None) -> Ticket:
        """
        Registra la entrada de un vehículo.
        Invariante: no puede haber dos vehículos en el mismo spot.
        """
        now = now or datetime.now()
        spot = self._find_available_spot(vehicle)
        if spot is None:
            raise ValueError("No hay lugares disponibles compatibles para este vehículo.")

        spot.park(vehicle)                           # puede lanzar RuntimeError si invariante falla
        ticket = Ticket(self._next_ticket_id, vehicle, spot, now)
        self._active_tickets[self._next_ticket_id] = ticket
        self._next_ticket_id += 1
        return ticket

    def exit(self, ticket_id: int, now: datetime | None = None) -> tuple[Ticket, float]:
        """
        Registra la salida: cierra ticket, libera spot, calcula costo.
        Retorna (ticket, costo).
        """
        now = now or datetime.now()

        if ticket_id not in self._active_tickets:
            raise ValueError(f"Ticket #{ticket_id} no encontrado o ya fue cerrado.")

        ticket = self._active_tickets[ticket_id]
        ticket.close(now)

        hours = ticket.get_duration_hours()
        cost = self._policy.calculate(hours, ticket.get_vehicle())   # polimorfismo aquí

        ticket.get_spot().release()
        self._total_revenue += cost
        del self._active_tickets[ticket_id]

        return ticket, cost
