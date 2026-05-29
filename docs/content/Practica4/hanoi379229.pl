% hanoi379229.pl
% Torres de Hanoi — Paradigmas de la Programación
%
% Uso:
%   ?- hanoi(3, izquierda, centro, derecha).
%   ?- hanoi(4, a, b, c).

% Caso base: un solo disco, moverlo directamente.
hanoi(1, Source, _, Dest) :-
    format('Mover disco 1 de ~w a ~w~n', [Source, Dest]).

% Caso recursivo: N discos.
%   1. Mover N-1 discos de Source a Aux (usando Dest como auxiliar).
%   2. Mover el disco N de Source a Dest.
%   3. Mover N-1 discos de Aux a Dest (usando Source como auxiliar).
hanoi(N, Source, Aux, Dest) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, Source, Dest, Aux),
    format('Mover disco ~w de ~w a ~w~n', [N, Source, Dest]),
    hanoi(N1, Aux, Source, Dest).

% ── Versión con conteo de movimientos ────────────────────────────────────────
% Uso: ?- hanoi_count(3, izquierda, centro, derecha, 0, Total).

hanoi_count(1, Source, _, Dest, Acc, Total) :-
    format('Mover disco 1 de ~w a ~w~n', [Source, Dest]),
    Total is Acc + 1.

hanoi_count(N, Source, Aux, Dest, Acc, Total) :-
    N > 1,
    N1 is N - 1,
    hanoi_count(N1, Source, Dest, Aux, Acc, Acc1),
    format('Mover disco ~w de ~w a ~w~n', [N, Source, Dest]),
    Acc2 is Acc1 + 1,
    hanoi_count(N1, Aux, Source, Dest, Acc2, Total).
