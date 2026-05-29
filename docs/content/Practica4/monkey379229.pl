% monkey379299.pl
% El Mono y el Plátano — Paradigmas de la Programación
%
% Estado: estado(PosMonkey, PosBox, OnBox, HasBanana)
%   PosMonkey : atdoor | middle | atwindow
%   PosBox    : atdoor | middle | atwindow
%   OnBox     : onbox  | offbox
%   HasBanana : has    | hasnot
%
% Uso:
%   ?- solucion(estado(atdoor, atwindow, offbox, hasnot), Acciones).

% ── Acciones (transiciones de estado) ────────────────────────────────────────

% Agarrar el plátano: el mono debe estar en el centro, sobre la caja.
move(estado(middle, middle, onbox, hasnot),
     agarrar_platano,
     estado(middle, middle, onbox, has)).

% Subir a la caja: el mono debe estar en la misma posición que la caja.
move(estado(P, P, offbox, H),
     subir_caja,
     estado(P, P, onbox, H)).

% Empujar la caja de P1 a P2 (el mono baja automáticamente).
move(estado(P1, P1, offbox, H),
     empujar_caja(P1, P2),
     estado(P2, P2, offbox, H)) :-
    P1 \== P2.

% Caminar a una nueva posición (sin la caja).
move(estado(_, Box, offbox, H),
     caminar_a(P2),
     estado(P2, Box, offbox, H)).

% ── Planificador (búsqueda con backtracking) ──────────────────────────────────

% Caso final: el mono ya tiene el plátano.
solucion(estado(_, _, _, has), []).

% Caso recursivo: ejecutar una acción y continuar.
solucion(Estado, [Accion | Resto]) :-
    move(Estado, Accion, NuevoEstado),
    solucion(NuevoEstado, Resto).

% ── Versión con impresión de pasos ───────────────────────────────────────────
% Uso: ?- resolver(estado(atdoor, atwindow, offbox, hasnot)).

resolver(Estado) :-
    solucion(Estado, Acciones),
    write('Secuencia de acciones:'), nl,
    imprimir_acciones(Acciones, 1).

imprimir_acciones([], _).
imprimir_acciones([A | R], N) :-
    format('  ~w. ~w~n', [N, A]),
    N1 is N + 1,
    imprimir_acciones(R, N1).
