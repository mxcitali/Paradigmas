"""
app.py — Controller (Flask MVC).
Ejecutar: python app.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, request, redirect, url_for, flash
from models import ParkingLot, create_vehicle, HourlyRatePolicy

app = Flask(__name__)
app.secret_key = "parksys-secret-2024"

# Instancia global del modelo (estado en memoria)
lot = ParkingLot(policy=HourlyRatePolicy())


def _common_ctx() -> dict:
    """Contexto compartido para todas las vistas."""
    return {"policy_desc": lot.get_policy().description()}


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    ctx = _common_ctx()
    ctx.update({
        "spots": lot.get_spots(),
        "active_tickets": lot.get_active_tickets(),
        "occ": lot.get_occupancy_dict(),
        "revenue": lot.get_total_revenue(),
    })
    return render_template("dashboard.html", **ctx)


@app.route("/entry", methods=["GET"])
def entry_get():
    ctx = _common_ctx()
    ctx["spots"] = lot.get_spots()
    return render_template("entry.html", **ctx)


@app.route("/entry", methods=["POST"])
def entry_post():
    plate = request.form.get("plate", "").strip()
    vtype = request.form.get("vehicle_type", "").strip()

    # Validación de campos
    if not plate:
        flash("Las placas no pueden estar vacías.", "error")
        return redirect(url_for("entry_get"))
    if not vtype:
        flash("Selecciona un tipo de vehículo.", "error")
        return redirect(url_for("entry_get"))

    try:
        vehicle = create_vehicle(plate, vtype)
        ticket = lot.enter(vehicle)
        flash(
            f"✓ Entrada registrada — Ticket #{ticket.get_id()} | "
            f"{vehicle} → Spot {ticket.get_spot().get_id()}",
            "success"
        )
    except ValueError as e:
        flash(f"✗ {e}", "error")
        return redirect(url_for("entry_get"))

    return redirect(url_for("dashboard"))


@app.route("/exit", methods=["GET"])
def exit_get():
    ctx = _common_ctx()
    ctx["active_tickets"] = lot.get_active_tickets()
    return render_template("exit.html", **ctx)


@app.route("/exit", methods=["POST"])
def exit_post():
    raw = request.form.get("ticket_id", "").strip()

    if not raw.isdigit():
        flash("ID de ticket inválido — debe ser un número.", "error")
        return redirect(url_for("exit_get"))

    ticket_id = int(raw)
    try:
        ticket, cost = lot.exit(ticket_id)
        hours = ticket.get_duration_hours()
        flash(
            f"✓ Salida registrada — Ticket #{ticket_id} | "
            f"{ticket.get_vehicle()} | {hours:.2f}h | Costo: ${cost:.2f} | "
            f"Spot {ticket.get_spot().get_id()} liberado",
            "success"
        )
    except (ValueError, RuntimeError) as e:
        flash(f"✗ {e}", "error")
        return redirect(url_for("exit_get"))

    return redirect(url_for("dashboard"))


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)
