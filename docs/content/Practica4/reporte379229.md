+++
date = '2026-05-23T15:41:53-08:00'
draft = false
title = 'Practica 4'
+++
# Paradigma Lógico
**Mextli Citlali Perez Aguirre - 379229**

---

## 1. Introducción

El **paradigma lógico** es un estilo de programación declarativa basado en la lógica matemática de primer orden. En lugar de describir *cómo* computar una solución paso a paso, el programador declara *qué* es verdadero mediante hechos y reglas, y el motor de inferencia del lenguaje deduce las respuestas automáticamente mediante **unificación** y **búsqueda con backtracking**.

**Prolog** (PROgramming in LOGic) es el lenguaje lógico más utilizado. Su ciclo de trabajo fundamental es:

1. Definir una *base de conocimientos* con hechos y reglas.
2. Formular *consultas* que el motor resuelve automáticamente.

### Diferencia clave con otros paradigmas

| Paradigma | Descripción |
|-----------|-------------|
| Imperativo / Funcional | El programador describe *cómo* ejecutar pasos (`procedure1()`, `procedure2()`…) |
| Lógico | El programador declara *qué* es verdadero; el motor infiere la respuesta |

---

## Sesión 1 — Instalación e Introducción a Prolog

## 2. Instalación del Entorno

Se utilizó **SWI-Prolog**, disponible en https://www.swi-prolog.org.  
Instalación en Linux:

```bash
sudo apt install swi-prolog
```

Acceder al intérprete interactivo:

```bash
swipl
```

Cargar un archivo `.pl`:

```prolog
?- [archivo].
% o bien:
?- consult('archivo.pl').
```

---

## 3. Hechos en Prolog

Un **hecho** declara que algo es verdadero de forma incondicional.

**Sintaxis:**

```prolog
relacion(objeto1, objeto2, ...).
```

**Reglas de escritura:**
- Los nombres de relaciones y objetos comienzan con **minúscula**.
- La relación es siempre el **primer término**.
- Los objetos van separados por comas y entre paréntesis.
- Todo hecho termina con un **punto** (`.`).

**Base de conocimientos kb1.pl:**

```prolog
% kb1.pl
girl(priya).
girl(natasha).
girl(jasmin).
can_cook(priya).
```

**Base de conocimientos kb2.pl:**

```prolog
% kb2.pl
sing_a_song(ana).
listens_to_music(rodrigo).
listens_to_music(ana)     :- sing_a_song(ana).
happy(ana)                :- sing_a_song(ana).
happy(rodrigo)            :- listens_to_music(rodrigo).
plays_guitar(rodrigo)     :- listens_to_music(rodrigo).
```

**Base de conocimientos kb3.pl:**

```prolog
% kb3.pl
can_cook(priya).
can_cook(jasmin).
can_cook(timoteo).
likes(priya, jasmin)  :- can_cook(jasmin).
likes(priya, timoteo) :- can_cook(timoteo).
```

---

## 4. Reglas en Prolog

Una **regla** define condiciones bajo las cuales una relación se cumple. El operador `:-` se lee como «si»:

```prolog
cabeza :- cuerpo1, cuerpo2.   % conjunción (Y)
cabeza :- cuerpo1 ; cuerpo2.  % disyunción (O)
```

**Ejemplos:**

```prolog
happy(lili)         :- dances(lili).
hungry(tom)         :- search_for_food(tom).
friends(jack, bili) :- lovesCricket(jack), lovesCricket(bili).
goToPlay(ryan)      :- isClosed(school), free(ryan).
```

---

## 5. Consultas

Las consultas se formulan en el prompt `?-`. Prolog responde `true`/`false` o devuelve instanciaciones de variables:

```prolog
?- cat(tom).
true.

?- lazy(juan).
true.

?- girl(X).
X = priya ;
X = natasha ;
X = jasmin.
```

---

## 6. Relaciones en Prolog

Las relaciones modelan vínculos entre objetos y pueden derivarse mediante reglas.

### Relaciones de fraternidad (kb4.pl)

```prolog
% kb4.pl
parent(simon, pedro).
parent(simon, raj).
male(pedro).
male(raj).

brother(X, Y) :- parent(Z, X), parent(Z, Y), male(X), male(Y), X \== Y.
```

> **Nota:** `X \== Y` evita que un individuo sea considerado hermano de sí mismo.

### Base de conocimientos familiar — family.pl

```prolog
% family.pl
female(pam). female(liz). female(pat). female(ann).
male(jim).   male(bob).   male(tom).   male(pete).

parent(pam, bob).  parent(tom, bob).  parent(tom, liz).
parent(bob, ann).  parent(bob, pat).  parent(pat, jim).
parent(pete, jim).

mother(X, Y)  :- parent(X, Y), female(X).
father(X, Y)  :- parent(X, Y), male(X).
haschild(X)   :- parent(X, _).
sister(X, Y)  :- parent(Z, X), parent(Z, Y), female(X), X \== Y.
brother(X, Y) :- parent(Z, X), parent(Z, Y), male(X),   X \== Y.
```

### Extensión familiar — family_ext.pl

```prolog
% family_ext.pl — copiar contenido de family.pl y agregar:
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandmother(X, Z) :- mother(X, Y), parent(Y, Z).
grandfather(X, Z) :- father(X, Y), parent(Y, Z).
wife(X, Y)        :- parent(X, Z), parent(Y, Z), female(X), male(Y).
uncle(X, Z)       :- brother(X, Y), parent(Y, Z).
```

### Recursión — family_rec.pl

La relación `predecessor` (antepasado) se define recursivamente:

```prolog
% family_rec.pl — copiar contenido de family.pl y agregar:
predecessor(X, Z) :- parent(X, Z).
predecessor(X, Z) :- parent(X, Y), predecessor(Y, Z).
```

- **Caso base:** X es padre directo de Z.
- **Caso recursivo:** X es padre de Y, y Y es predecesor de Z.

---

## 7. Seguimiento de Ejecución

SWI-Prolog incluye modo traza para depurar:

```prolog
?- trace.
true.

[trace] ?- mother(pam, X).
   Call: (10) mother(pam,_G123) ? creep
   Call: (11) parent(pam,_G123) ? creep
   Exit: (11) parent(pam,bob) ? creep
   Call: (11) female(pam) ? creep
   Exit: (11) female(pam) ? creep
   Exit: (10) mother(pam,bob) ? creep
X = bob.

?- notrace.
```

---

## Sesión 2 — Objetos, Operadores y Listas

## 8. Objetos de Datos en Prolog

| Tipo | Descripción | Ejemplos |
|------|-------------|---------|
| Átomos | Constantes simbólicas | `tom`, `pat`, `x100` |
| Números | Enteros y reales | `100`, `2000.45` |
| Variables | Empiezan con mayúscula o `_` | `X`, `Y`, `Xval`, `_` |
| Estructuras | Término compuesto | `dia(9,jun,2026)`, `punto(10,25)` |
| Cadenas | Entre comillas simples | `'Hello, World!'` |

---

## 9. Operadores

### Comparación

| Operador | Significado |
|----------|-------------|
| `X > Y`   | X mayor que Y |
| `X < Y`   | X menor que Y |
| `X >= Y`  | X mayor o igual que Y |
| `X =< Y`  | X menor o igual que Y |
| `X =:= Y` | Valores iguales |
| `X =\= Y` | Valores diferentes |

### Aritméticos

| Operador | Función |
|----------|---------|
| `+`   | Suma |
| `-`   | Resta |
| `*`   | Multiplicación |
| `/`   | División real |
| `//`  | División entera |
| `**`  | Potencia |
| `mod` | Módulo |

### Programa operadores.pl

```prolog
% operadores.pl
calc :-
    X is 100 + 200, write('100 + 200 = '), write(X), nl,
    Y is 400 - 150, write('400 - 150 = '), write(Y), nl,
    Z is 10  * 300, write('10 * 300  = '), write(Z), nl,
    A is 100 / 30,  write('100 / 30  = '), write(A), nl,
    B is 100 // 30, write('100 // 30 = '), write(B), nl,
    C is 100 ** 2,  write('100 ** 2  = '), write(C), nl,
    D is 100 mod 30,write('100 mod 30= '), write(D), nl.
```

---

## 10. Control de Flujo

### Bucles — loop.pl

Prolog no tiene bucles nativos; se simulan con recursión:

```prolog
% loop.pl
count_to_10(10) :- write(10), nl.
count_to_10(X)  :-
    write(X), nl,
    Y is X + 1,
    count_to_10(Y).

count_down(L, H) :- between(L, H, Y), Z is H - Y, write(Z), nl.
count_up(L, H)   :- between(L, H, Y), Z is L + Y, write(Z), nl.
```

### Toma de decisiones — option.pl

```prolog
% option.pl
gt(X, Y)  :- X >= Y, write('X es mayor o igual').
gt(X, Y)  :- X < Y,  write('X es menor').

gte(X, Y) :- X > Y,    write('X es mayor').
gte(X, Y) :- X =:= Y,  write('X e Y son iguales').
gte(X, Y) :- X < Y,    write('X es menor').
```

### Conjunciones y Disyunciones — conj_disj.pl

```prolog
% conj_disj.pl
parent(jhon, bob).  parent(lili, bob).
male(jhon).         female(lili).

father(X, Y)   :- parent(X, Y), male(X).
mother(X, Y)   :- parent(X, Y), female(X).
child_of(X, Y) :- father(X, Y) ; mother(X, Y).   % disyunción
```

---

## 11. Listas en Prolog

Las listas se representan entre corchetes. La notación `[H|T]` separa la **cabeza** del resto:

```prolog
[a, b, c]  =  [a | [b, c]]
[a, b, c]  =  [a, b | [c]]
[a, b, c]  =  [a, b, c | []]
```

### Operaciones básicas — list_basics.pl

```prolog
% list_basics.pl
list_member(X, [X|_]).
list_member(X, [_|T]) :- list_member(X, T).

list_length([], 0).
list_length([_|T], N) :- list_length(T, N1), N is N1 + 1.

list_concat([], L, L).
list_concat([X|L1], L2, [X|L3]) :- list_concat(L1, L2, L3).

list_append(A, T, T)     :- list_member(A, T), !.
list_append(A, T, [A|T]).

list_delete(X, [X], []).
list_delete(X, [X|L1], L1).
list_delete(X, [Y|L2], [Y|L1]) :- list_delete(X, L2, L1).

list_insert(X, L, R) :- list_delete(X, R, L).
```

### Reposicionamiento — list_repos.pl

```prolog
% list_repos.pl
list_perm([], []).
list_perm(L, [X|P]) :- list_delete(X, L, L1), list_perm(L1, P).

list_rev([], []).
list_rev([H|T], R) :- list_rev(T, RT), list_concat(RT, [H], R).

list_shift([H|T], S) :- list_concat(T, [H], S).

list_order([X, Y|T]) :- X =< Y, list_order([Y|T]).
list_order([_]).

list_union([X|Y], Z, W)     :- list_member(X, Z), list_union(Y, Z, W).
list_union([X|Y], Z, [X|W]) :- \+ list_member(X, Z), list_union(Y, Z, W).
list_union([], Z, Z).

list_intersect([X|Y], Z, [X|W]) :- list_member(X, Z), list_intersect(Y, Z, W).
list_intersect([X|Y], Z, W)     :- \+ list_member(X, Z), list_intersect(Y, Z, W).
list_intersect([], _, []).
```

### Misceláneos — list_misc.pl

```prolog
% list_misc.pl
list_even_len([]).
list_even_len([_|T]) :- list_odd_len(T).
list_odd_len([_]).
list_odd_len([_|T])  :- list_even_len(T).

list_divide([], [], []).
list_divide([X], [X], []).
list_divide([X,Y|T], [X|L1], [Y|L2]) :- list_divide(T, L1, L2).

max_of_two(X, Y, X) :- X >= Y.
max_of_two(X, Y, Y) :- X < Y.
list_max_elem([X], X).
list_max_elem([X,Y|R], Max) :- list_max_elem([Y|R], MR), max_of_two(X, MR, Max).

list_sum([], 0).
list_sum([H|T], Sum) :- list_sum(T, ST), Sum is H + ST.
```

---

## Sesión 3 — Aplicaciones: Torres de Hanoi y El Mono y el Plátano

## 12. Torres de Hanoi

Las **Torres de Hanoi** es un problema clásico de recursión: mover *N* discos desde una clavija origen a una destino usando una auxiliar, sin colocar jamás un disco mayor sobre uno menor.

### Definición recursiva

- **Caso base:** mover 1 disco directamente de origen a destino.
- **Caso recursivo:**
  1. Mover N-1 discos de origen → auxiliar.
  2. Mover el disco N de origen → destino.
  3. Mover N-1 discos de auxiliar → destino.

Para N discos se requieren exactamente **2ᴺ − 1** movimientos.

### Ejecución con 3 discos

```prolog
?- hanoi(3, izquierda, centro, derecha).
Mover disco 1 de izquierda a derecha
Mover disco 2 de izquierda a centro
Mover disco 1 de derecha a centro
Mover disco 3 de izquierda a derecha
Mover disco 1 de centro a izquierda
Mover disco 2 de centro a derecha
Mover disco 1 de izquierda a derecha
true.
```

El código fuente está en `hanoi.pl` (adjunto).

---

## 13. El Mono y el Plátano

El **problema del mono y el plátano** es un clásico de planificación en IA. Un mono en una habitación debe obtener un plátano colgado del techo. Dispone de una caja que puede empujar y sobre la que puede subir.

### Representación del estado

```
estado(PosMonkey, PosBox, OnBox, HasBanana)
```

| Campo | Valores posibles |
|-------|-----------------|
| `PosMonkey` | `atdoor`, `middle`, `atwindow` |
| `PosBox`    | `atdoor`, `middle`, `atwindow` |
| `OnBox`     | `onbox`, `offbox` |
| `HasBanana` | `has`, `hasnot` |

### Consulta de solución

```prolog
?- solucion(estado(atdoor, atwindow, offbox, hasnot), Acciones).
Acciones = [
    caminar_a(atwindow),
    empujar_caja(atwindow, middle),
    subir_caja,
    agarrar_platano
].
```

El código fuente está en `monkey.pl` (adjunto).

---

## 14. Conclusiones

- **Declaratividad:** Prolog permite concentrarse en *qué* es verdadero sin gestionar el flujo de ejecución explícitamente.
- **Backtracking automático:** el motor explora todas las alternativas de forma transparente, simplificando problemas de búsqueda.
- **Recursión como iteración:** la ausencia de bucles obliga a pensar en casos base y reducción, profundizando la comprensión de la recursión.
- **Unificación:** la igualdad de patrones complejos simplifica la representación de estados y transiciones (problema del mono).
- **Torres de Hanoi:** la solución en Prolog es sorprendentemente compacta —2 cláusulas— comparada con implementaciones iterativas.

---

## 15. Referencias

- SWI-Prolog: https://www.swi-prolog.org
- Material de clase: ISyTE — Paradigmas de la Programación, M.I. José Carlos Gallegos Mariscal.
- Clocksin, W. F. & Mellish, C. S. (2003). *Programming in Prolog*. Springer.
- Bratko, I. (2001). *Prolog Programming for Artificial Intelligence*. Addison-Wesley.