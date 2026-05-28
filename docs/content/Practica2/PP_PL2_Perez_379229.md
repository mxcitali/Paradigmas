+++
date = '2026-02-18T15:41:53-08:00'
draft = false
title = 'Practica 2: Uso de Repositorios'
+++
# Práctica 02: Simulador de Estacionamiento
## MEXTLI CITLALI PEREZ AGUIRRE - 379229
**Universidad Autónoma de Baja California — Facultad de Ingeniería, Arquitectura y Diseño**

| Campo | Valor |
|---|---|
| Materia | 40032 — Paradigmas de la Programación |
| Docente | M.I. José Carlos Gallegos Mariscal |
| Grupo | 941 |

---

## 1. Introducción

El proyecto implementa un sistema de administración de estacionamiento aplicando POO en tres iteraciones: modelo de dominio con consola, extensión con polimorfismo y subtipos, e interfaz web con Flask bajo el patrón MVC.

El sistema administra lugares (spots), vehículos y tickets; registra entradas/salidas, calcula cobros según distintas políticas de tarifa y muestra la ocupación en tiempo real.

**Objetivos:** modelar entidades como clases, aplicar encapsulación con atributos privados, separar políticas de cobro mediante abstracción, usar composición en `ParkingLot`, implementar herencia con `Car`/`Motorcycle`, aplicar polimorfismo con `RatePolicy` e integrar todo en Flask MVC.

---

## 2. Modelo del Dominio

| Clase | Responsabilidad |
|---|---|
| `Vehicle` (abstracta) | Base de todos los vehículos: placa y tipo. |
| `Car` / `Motorcycle` | Subtipos concretos de `Vehicle`. |
| `ParkingSpot` | Lugar físico: id, tipo permitido, estado de ocupación. |
| `Ticket` | Registro de estancia: vehículo, spot, tiempos. |
| `ParkingLot` | Administra spots, tickets activos y recaudación. |
| `RatePolicy` | Interfaz (Protocol) para cualquier política de cobro. |
| `HourlyRatePolicy` | Cobra por hora según el tipo de vehículo. |
| `FlatRatePolicy` | Tarifa fija independiente del tiempo. |
| `TieredRatePolicy` | Tarifa escalonada: precio base las primeras horas, mayor el resto. |

**Relaciones:** `ParkingLot` *compone* `List[ParkingSpot]` y `Dict[int, Ticket]`; `Car` y `Motorcycle` *heredan* de `Vehicle`; `ParkingLot` *usa* `RatePolicy` inyectada.

---

## 3. Evidencia de Conceptos POO

### 3.1 Encapsulación

Los atributos usan prefijo `_`. El método `park()` valida invariantes antes de modificar el estado, impidiendo acceso directo desde el exterior:

```python
# models/spot.py
def park(self, vehicle: Vehicle) -> None:
    if self._occupied:
        raise RuntimeError(f"El spot {self._spot_id} ya está ocupado.")
    if not self.is_available_for(vehicle):
        raise ValueError(f"Vehículo incompatible con el spot {self._spot_id}.")
    self._current_vehicle = vehicle
    self._occupied = True
```

### 3.2 Abstracción

`RatePolicy` (Protocol) actúa como contrato. `ParkingLot` solo llama `calculate(hours, vehicle)` sin conocer los detalles de ninguna implementación:

```python
# models/rates.py
@runtime_checkable
class RatePolicy(Protocol):
    def calculate(self, hours: float, vehicle: Vehicle) -> float: ...
    def description(self) -> str: ...

class HourlyRatePolicy:
    def calculate(self, hours: float, vehicle: Vehicle) -> float:
        rate = self._car_rate if vehicle.get_type() == VehicleType.CAR else self._moto_rate
        return round(hours * rate, 2)

class FlatRatePolicy:
    def calculate(self, hours: float, vehicle: Vehicle) -> float:
        return self._flat_amount
```

### 3.3 Composición

`ParkingLot` **tiene** spots y tickets; la política se inyecta como dependencia:

```python
# models/parking_lot.py
class ParkingLot:
    def __init__(self, spots=None, policy=None):
        self._spots: list[ParkingSpot] = spots or _build_default_spots()
        self._policy: RatePolicy = policy or HourlyRatePolicy()
        self._active_tickets: dict[int, Ticket] = {}
        self._total_revenue: float = 0.0
```

### 3.4 Herencia y Subtipos

`Car` y `Motorcycle` heredan de `Vehicle` y fijan su tipo al llamar al constructor padre. Una factory crea el subtipo correcto:

```python
# models/vehicle.py
class Car(Vehicle):
    def __init__(self, plate: str):
        super().__init__(plate, VehicleType.CAR)

class Motorcycle(Vehicle):
    def __init__(self, plate: str):
        super().__init__(plate, VehicleType.MOTORCYCLE)

def create_vehicle(plate: str, vehicle_type: str) -> Vehicle:
    if vehicle_type == "car": return Car(plate)
    elif vehicle_type in ("motorcycle", "moto"): return Motorcycle(plate)
    else: raise ValueError(f"Tipo desconocido: '{vehicle_type}'")
```

### 3.5 Polimorfismo

`exit()` llama `self._policy.calculate()` sin importar qué implementación está activa. La política se puede cambiar en tiempo de ejecución con `set_policy()`:

```python
# models/parking_lot.py  (fragmento de exit)
cost = self._policy.calculate(hours, ticket.get_vehicle())  # polimorfismo
```

**Resultado con 4.5 h, un Auto:**

| Política | Costo | Lógica |
|---|---|---|
| `HourlyRatePolicy` | $90.00 | 4.5 × $20/h |
| `FlatRatePolicy` | $50.00 | Tarifa fija |
| `TieredRatePolicy` | $82.50 | 3h×$15 + 1.5h×$25 |

---

## 4. MVC con Flask

| Capa | Archivos | Responsabilidad |
|---|---|---|
| **Model** | `models/*.py` | Lógica de negocio: clases, validaciones, cálculos. |
| **View** | `templates/*.html` | Dashboard, formulario de entrada, formulario de salida. |
| **Controller** | `app.py` | Recibe peticiones HTTP, llama al modelo y renderiza vistas. |

**Rutas:** `GET/POST /` (dashboard), `GET/POST /entry` (registrar entrada), `GET/POST /exit` (registrar salida).

El Controller únicamente orquesta; la lógica permanece en el Model:

```python
# app.py — POST /entry
@app.route("/entry", methods=["POST"])
def entry_post():
    plate = request.form.get("plate", "").strip()
    vtype = request.form.get("vehicle_type", "").strip()
    try:
        vehicle = create_vehicle(plate, vtype)
        ticket = lot.enter(vehicle)
        flash(f"✓ Ticket #{ticket.get_id()} | {vehicle} → Spot {ticket.get_spot().get_id()}", "success")
    except ValueError as e:
        flash(f"✗ {e}", "error")
        return redirect(url_for("entry_get"))
    return redirect(url_for("dashboard"))
```

> _(Insertar capturas de pantalla del dashboard, formulario de entrada y salida aquí)_

---

## 5. Pruebas Manuales

### Flujo 1 — Entrada y salida con HourlyRatePolicy

| Paso | Acción | Resultado esperado |
|---|---|---|
| 1 | Entrada: `ABC-123`, tipo `car` | Ticket #1, Spot A1 asignado |
| 2 | Ver ocupación | `libres=9, ocupados=1` |
| 3 | Salida: ticket=1, 2 horas simuladas | Costo=$40.00, Spot A1 liberado |
| 4 | Ver ocupación | `libres=10, ocupados=0` |

### Flujo 2 — Polimorfismo: HourlyRate vs FlatRate

| Paso | Acción | Resultado esperado |
|---|---|---|
| 1 | Entrada: `ABC-123` (auto) | Ticket #1, HourlyRate activa |
| 2 | Entrada: `XYZ-777` (moto) | Ticket #2, HourlyRate activa |
| 3 | Salida ticket #1, 2 h | Costo=**$40.00** (2h × $20/h) |
| 4 | Cambiar a FlatRatePolicy | Tarifa plana: $50 activa |
| 5 | Salida ticket #2, 2 h | Costo=**$50.00** (tarifa fija) |
| 6 | Comparar pasos 3 y 5 | Mismo tiempo, costo diferente = **polimorfismo** ✓ |

> _(Insertar capturas de pantalla de CLI y web aquí)_

---

## 6. Conclusiones

La práctica aplicó los cuatro pilares de POO de forma integrada. La **encapsulación** garantizó consistencia interna; la **abstracción** con `RatePolicy` desacopló completamente la lógica de cobro. La **composición** resultó más flexible que la herencia para modelar `ParkingLot`. El **polimorfismo** fue el concepto más valioso: agregar una nueva política solo requiere una clase con `calculate()`, sin tocar código existente (principio Abierto/Cerrado). La integración con Flask demostró que un modelo bien diseñado se conecta naturalmente a cualquier capa de presentación.

---

## 7. Referencias

[1] Pallets Projects. (2026). *Welcome to Flask — Flask Documentation (3.1.x)*. https://flask.palletsprojects.com/

[2] Python Software Foundation. (2026). *dataclasses — Data Classes*. https://docs.python.org/3/library/dataclasses.html

[3] Fowler, M. (2004). *Inversion of Control Containers and the Dependency Injection pattern*. https://martinfowler.com/articles/injection.html

[4] Python Typing Team. (2026). *Protocols — typing specification*. https://typing.python.org/en/latest/spec/protocol.html
