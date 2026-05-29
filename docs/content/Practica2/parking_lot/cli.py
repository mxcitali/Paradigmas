"""
cli.py — Menú de consola (Sesión 1 y 2).
Ejecutar: python cli.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime
from models import ParkingLot, create_vehicle, HourlyRatePolicy, FlatRatePolicy, TieredRatePolicy


def print_header(title: str) -> None:
    print(f"\n{'═' * 50}")
    print(f"  {title}")
    print(f"{'═' * 50}")


def print_menu() -> None:
    print_header("SIMULADOR DE ESTACIONAMIENTO")
    print("  1. Registrar entrada")
    print("  2. Registrar salida")
    print("  3. Ver ocupación")
    print("  4. Ver tickets activos")
    print("  5. Cambiar política de cobro")
    print("  6. Salir")
    print()


def registrar_entrada(lot: ParkingLot) -> None:
    print_header("REGISTRAR ENTRADA")
    plate = input("  Placas del vehículo: ").strip()
    if not plate:
        print("  ✗ Las placas no pueden estar vacías.")
        return
    vtype = input("  Tipo (car / motorcycle): ").strip()
    try:
        vehicle = create_vehicle(plate, vtype)
        ticket = lot.enter(vehicle)
        print(f"\n  ✓ Entrada registrada:")
        print(f"    Ticket #: {ticket.get_id()}")
        print(f"    Vehículo: {vehicle}")
        print(f"    Spot:     {ticket.get_spot().get_id()}")
        print(f"    Hora:     {ticket.get_entry_time().strftime('%H:%M:%S')}")
    except ValueError as e:
        print(f"  ✗ Error: {e}")


def registrar_salida(lot: ParkingLot) -> None:
    print_header("REGISTRAR SALIDA")
    raw = input("  Número de ticket: ").strip()
    if not raw.isdigit():
        print("  ✗ ID de ticket inválido.")
        return
    ticket_id = int(raw)

    # Para demostración: permitir ingresar horas manualmente (tiempo simulado)
    sim = input("  ¿Simular horas transcurridas? (Enter=tiempo real, o escribe número de horas): ").strip()
    try:
        if sim:
            hours = float(sim)
            # Calcular exit_time como entry_time + horas simuladas
            from datetime import timedelta
            active = lot.get_active_tickets()
            t = next((t for t in active if t.get_id() == ticket_id), None)
            if t is None:
                print(f"  ✗ Ticket #{ticket_id} no encontrado.")
                return
            exit_time = t.get_entry_time() + timedelta(hours=hours)
        else:
            exit_time = datetime.now()

        ticket, cost = lot.exit(ticket_id, exit_time)
        hours_real = ticket.get_duration_hours()
        print(f"\n  ✓ Salida registrada:")
        print(f"    Ticket #: {ticket.get_id()}")
        print(f"    Vehículo: {ticket.get_vehicle()}")
        print(f"    Spot:     {ticket.get_spot().get_id()} (liberado)")
        print(f"    Tiempo:   {hours_real:.2f} h")
        print(f"    Costo:    ${cost:.2f}")
        print(f"    Política: {lot.get_policy().description()}")
    except (ValueError, RuntimeError) as e:
        print(f"  ✗ Error: {e}")


def ver_ocupacion(lot: ParkingLot) -> None:
    print_header("ESTADO DE OCUPACIÓN")
    occ = lot.get_occupancy_dict()
    print(f"  Total:    {occ['total']}")
    print(f"  Ocupados: {occ['occupied']}")
    print(f"  Libres:   {occ['free']}")
    print()
    for spot in lot.get_spots():
        estado = "🔴 OCUPADO" if spot.is_occupied() else "🟢 LIBRE"
        veh = f" ← {spot.get_current_vehicle()}" if spot.is_occupied() else ""
        print(f"  [{spot.get_id()}] ({spot.get_allowed().value}) {estado}{veh}")


def ver_tickets_activos(lot: ParkingLot) -> None:
    print_header("TICKETS ACTIVOS")
    tickets = lot.get_active_tickets()
    if not tickets:
        print("  No hay tickets activos.")
        return
    for t in tickets:
        print(f"  Ticket #{t.get_id()} | {t.get_vehicle()} | Spot: {t.get_spot().get_id()} | "
              f"Entrada: {t.get_entry_time().strftime('%H:%M:%S')}")


def cambiar_politica(lot: ParkingLot) -> None:
    print_header("CAMBIAR POLÍTICA DE COBRO")
    print(f"  Política actual: {lot.get_policy().description()}")
    print("  1. Por hora (Auto $20/h, Moto $10/h)")
    print("  2. Tarifa plana ($50)")
    print("  3. Escalonada (primeras 3h $15/h, extra $25/h)")
    opt = input("  Selecciona: ").strip()
    if opt == "1":
        lot.set_policy(HourlyRatePolicy())
    elif opt == "2":
        lot.set_policy(FlatRatePolicy())
    elif opt == "3":
        lot.set_policy(TieredRatePolicy())
    else:
        print("  ✗ Opción inválida.")
        return
    print(f"  ✓ Nueva política: {lot.get_policy().description()}")


def main() -> None:
    lot = ParkingLot()
    print("\n  Bienvenido al Simulador de Estacionamiento")
    print(f"  Política inicial: {lot.get_policy().description()}")

    while True:
        print_menu()
        opcion = input("  Selecciona una opción: ").strip()
        if opcion == "1":
            registrar_entrada(lot)
        elif opcion == "2":
            registrar_salida(lot)
        elif opcion == "3":
            ver_ocupacion(lot)
        elif opcion == "4":
            ver_tickets_activos(lot)
        elif opcion == "5":
            cambiar_politica(lot)
        elif opcion == "6":
            print("\n  ¡Hasta luego!\n")
            break
        else:
            print("  ✗ Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
