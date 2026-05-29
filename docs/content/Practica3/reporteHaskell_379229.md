+++
date = '2026-05-01T15:41:53-08:00'
draft = false
title = 'Practica 3'
+++
# Haskell
**Mextli Citlali Perez Aguirre - 379229**

---

## 1. Introducción

Haskell es un lenguaje de programación **funcional puro**, de tipado estático y evaluación perezosa (*lazy evaluation*). A diferencia de lenguajes imperativos como C o Python, los programas en Haskell se construyen mediante composición de funciones matemáticas puras, sin efectos secundarios ni estado mutable. Esto lo hace un caso de estudio ideal para el paradigma funcional.

Los archivos fuente de Haskell utilizan la extensión `.hs`.

---

## 2. Instalación del Entorno de Desarrollo (Sesión 1)

### 2.1 GHCup

El punto de partida es la página oficial [haskell.org](https://www.haskell.org), en la sección **Downloads**. Ahí se indica que la forma recomendada de instalar el ecosistema completo es mediante **GHCup**, el instalador universal de Haskell.

Al dar clic en el hipervínculo de GHCup se llega a su página oficial, donde se copia el comando de instalación y se pega en una ventana de **PowerShell** (sin modo administrador):

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force;
[System.Net.ServicePointManager]::SecurityProtocol = ...;
& ([ScriptBlock]::Create((Invoke-WebRequest https://www.haskell.org/ghcup/sh/bootstrap-haskell.ps1 -UseBasicParsing))) -Interactive -DisableCurl
```

Este comando descarga y ejecuta el instalador que configura automáticamente todo el entorno.

### 2.2 Componentes que se instalan

| Herramienta | Rol |
|-------------|-----|
| **GHCup** | Instalador y gestor del entorno. Permite instalar, actualizar y cambiar versiones de GHC, HLS, Stack y Cabal. |
| **GHC** | *Glasgow Haskell Compiler* — compilador principal que transforma archivos `.hs` en binarios ejecutables. |
| **GHCi** | Intérprete interactivo incluido con GHC. Permite evaluar expresiones Haskell en tiempo real, útil para aprender y probar funciones. |
| **HLS** | *Haskell Language Server* — provee funciones de IDE (autocompletado, verificación de tipos, errores en tiempo de edición). Usado internamente por extensiones de VS Code. No se usa directamente. |
| **Stack** | Manejador de paquetes y proyectos. Similar a `pip` (Python) o `apt` (Ubuntu). Resuelve dependencias usando snapshots de Stackage para garantizar reproducibilidad. |
| **Cabal** | Herramienta de empaquetado (*build tool*). Define la estructura del proyecto en el archivo `.cabal`, invoca a GHC para compilar y usa Stack para descargar dependencias, todo en un solo comando. |

### 2.3 Verificación de la instalación

Una vez instalado, se puede verificar desde la terminal:

```bash
ghc --version
stack --version
ghci
```

Al ejecutar `ghci` se accede al intérprete interactivo. Un ejemplo básico para confirmar que funciona:

```
Prelude> 2 + 2
4
Prelude> putStrLn "Hola Haskell"
Hola Haskell
Prelude> :quit
```

La guía oficial **Get Started** de `haskell.org` lleva al usuario a través de este proceso y sirve como introducción breve al lenguaje.

---

## 3. Preparación previa a la Sesión 2

Antes de la segunda sesión se recomienda revisar el tutorial:

- **Haskell Tutorial for C Programmers** — introduce las diferencias de sintaxis y paradigma entre C y Haskell.
- Incluye un enlace a un **tour de sintaxis** del departamento CSE de Chalmers, muy condensado y útil para entender la gramática del lenguaje rápidamente.

El objetivo no es volverse experto en Haskell, sino adquirir suficiente noción del lenguaje y el paradigma funcional para entender la aplicación de ejemplo.

---

## 4. La Aplicación TODO en Haskell (Sesión 2)

La aplicación es una lista de tareas en línea de comandos, tomada del blog [Haskell/examples/blog/todo](https://github.com/steadylearner/Haskell/tree/main/examples) e implementada desde cero siguiendo el artículo **"How to use Haskell to build a todo app with Stack"**.

### 4.1 Creación del proyecto con Stack

Se crea el proyecto con:

```bash
stack new todo
```

Stack descarga la plantilla `new-template` y genera la siguiente estructura:

```
todo/
├── app/
│   └── Main.hs          ← Punto de entrada del ejecutable
├── src/
│   └── Lib.hs           ← Lógica de la aplicación (librería)
├── test/
│   └── Spec.hs          ← Suite de pruebas
├── todo.cabal           ← Definición del paquete (generado por hpack)
├── package.yaml         ← Configuración de dependencias
├── stack.yaml           ← Resolver y configuración de Stack
├── stack.yaml.lock      ← Bloqueo de versiones (no editar)
├── LICENSE
├── README.md
└── ChangeLog.md
```

### 4.2 El archivo `todo.cabal`

Generado automáticamente por **hpack** a partir de `package.yaml`, define los tres componentes del proyecto:

**Librería (`library`):**  
Expone el módulo `Lib` ubicado en `src/`. Sus dependencias son:
- `base >= 4.7 && < 5` — librería estándar de Haskell
- `dotenv` — carga variables de entorno desde un archivo `.env`
- `open-browser` — abre URLs en el navegador del sistema

**Ejecutable (`executable todo-exe`):**  
Punto de entrada en `app/Main.hs`. Depende de la librería `todo` y los mismos paquetes externos. Se compila con soporte para multi-threading (`-threaded`, `-rtsopts`).

**Suite de pruebas (`test-suite todo-test`):**  
Pruebas en `test/Spec.hs`, con modo `exitcode-stdio-1.0` (el resultado se comunica por el código de salida del proceso).

### 4.3 El archivo `stack.yaml.lock`

Generado automáticamente por Stack; **nunca debe editarse a mano**. Registra la URL exacta y el hash SHA256 del snapshot de Stackage:

```
lts/17/15.yaml  →  sha256: 72e87841a0ab5b72f6f018e8ee692fd972b7bb32a944990f028e10d6eb528e63
```

El snapshot **LTS 17.15** (Long Term Support, GHC 8.10.x) garantiza que todas las dependencias sean compatibles entre sí y el build sea reproducible en cualquier máquina.

### 4.4 Configuración de dependencias — `package.yaml`

Se edita `package.yaml` para agregar los paquetes externos necesarios:

```yaml
dependencies:
  - base >= 4.7 && < 5
  - dotenv
  - open-browser
```

Estos cambios son lo que produce las entradas `dotenv` y `open-browser` en el archivo `todo.cabal`.

### 4.5 Comandos básicos de Stack

```bash
stack test    # Compila y ejecuta la suite de pruebas
stack run     # Compila y ejecuta el ejecutable principal
stack build   # Solo compila, sin ejecutar
stack repl    # Abre GHCi en el contexto del proyecto (para probar funciones)
stack install # Instala el ejecutable en el PATH del sistema
```

Al ejecutar `stack test` por primera vez con la plantilla base:

```
todo> test (suite: todo-test)
Test suite not yet implemented
todo> Test suite todo-test passed
```

Al ejecutar `stack run` con la plantilla base muestra `someFunc`, confirmando que el proyecto compila correctamente.

---

## 5. Código Fuente de la Aplicación

### 5.1 `app/Main.hs` — Punto de entrada

```haskell
module Main where

import Lib (prompt)

main :: IO ()
main = do
    putStrLn "Commands:"
    putStrLn "+ <String> - Add a TODO entry"
    putStrLn "- <Int>    - Delete the numbered entry"
    putStrLn "s <Int>    - Show the numbered entry"
    putStrLn "e <Int>    - Edit the numbered entry"
    putStrLn "l          - List todo"
    putStrLn "r          - Reverse todo"
    putStrLn "c          - Clear todo"
    putStrLn "q          - Quit"
    prompt []  -- Inicia con la lista vacía
```

`main` es la función de entrada de todo programa Haskell. Su tipo `IO ()` indica que realiza operaciones de entrada/salida y devuelve unit (equivalente a `void`). La notación `do` permite secuenciar acciones de IO de forma legible. La llamada `prompt []` inicia la aplicación con una lista vacía.

### 5.2 `src/Lib.hs` — Lógica principal

El módulo `Lib` exporta las funciones `prompt` y `editIndex`, que contienen toda la lógica de la aplicación.

#### Función `prompt`

```haskell
prompt :: [String] -> IO ()
prompt todos = do
  putStrLn ""
  putStrLn "Usa +(crear), -(borrar), s(mostrar), e(ditar), l(istar), r(evertir), c(limpiar), q(salir)."
  command <- getLine
  if "e" `isPrefixOf` command
    then do
      print "¿Cuál es el nuevo texto para esa tarea?"
      newTodo <- getLine
      editTodo command todos newTodo
    else interpret command todos
```

`prompt` recibe la lista actual de tareas y espera un comando del usuario. Si el comando empieza con `"e"` (editar), pide el nuevo texto antes de procesar. En caso contrario delega a `interpret`.

#### Función `interpret` — despacho de comandos

```haskell
interpret :: String -> [String] -> IO ()
interpret ('+' : ' ' : todo) todos = prompt (todo : todos)
interpret ('-' : ' ' : num) todos =
  case deleteOne (read num) todos of
    Nothing    -> putStrLn "No existe esa entrada" >> prompt todos
    Just todos' -> prompt todos'
interpret ('s' : ' ' : num) todos =
  case showOne (read num) todos of
    Nothing   -> putStrLn "No existe esa entrada" >> prompt todos
    Just todo -> print (num ++ ". " ++ todo) >> prompt todos
interpret "l" todos = do
  mapM_ putTodo (zip [0..] todos)
  prompt todos
interpret "r" todos = do
  mapM_ putTodo (zip [0..] (reverseTodos todos))
  prompt todos
interpret "c" _     = prompt []
interpret "q" _     = return ()
interpret cmd todos  = putStrLn ("Comando inválido: " ++ cmd) >> prompt todos
```

El despacho usa **pattern matching** sobre el primer carácter del comando, un mecanismo central de Haskell que reemplaza a las cadenas `if/else` o `switch/case` de los lenguajes imperativos.

#### Funciones auxiliares

```haskell
-- Elimina el elemento en el índice n de la lista
deleteOne :: Int -> [a] -> Maybe [a]
deleteOne 0 (_ : as) = Just as
deleteOne n (a : as) = do
  as' <- deleteOne (n - 1) as
  return (a : as')
deleteOne _ [] = Nothing

-- Obtiene el elemento en el índice n
showOne :: Int -> [a] -> Maybe a
showOne n todos
  | n < 0 || n >= length todos = Nothing
  | otherwise                  = Just (todos !! n)

-- Reemplaza el elemento en el índice i por x
editIndex :: Int -> a -> [a] -> [a]
editIndex i x xs = take i xs ++ [x] ++ drop (i + 1) xs

-- Invierte la lista sin usar la función reverse de Prelude
reverseTodos :: [a] -> [a]
reverseTodos xs = go xs []
  where
    go []     ys = ys
    go (x:xs) ys = go xs (x : ys)
```

El tipo `Maybe a` es fundamental en Haskell: representa un valor que puede existir (`Just a`) o no existir (`Nothing`), sin necesidad de nulos ni excepciones. Es el equivalente funcional a un manejo seguro de errores.

#### Uso de `dotenv` y `open-browser` en `Main.hs`

Para demostrar el uso de paquetes externos, se puede extender `Main.hs`:

```haskell
module Main where

import Configuration.Dotenv (defaultConfig, loadFile)
import Lib (prompt)
import System.Environment (lookupEnv)
import Web.Browser (openBrowser)

main :: IO ()
main = do
    loadFile defaultConfig          -- Carga variables del archivo .env
    maybeUrl <- lookupEnv "MY_URL"  -- Lee la variable MY_URL
    case maybeUrl of
      Just url -> openBrowser url   -- Abre la URL en el navegador
      Nothing  -> return ()
    putStrLn "Commands:"
    -- ... resto de mensajes ...
    prompt []
```

El archivo `.env` en la raíz del proyecto tendría el formato:

```
MY_URL=https://github.com
```

### 5.3 `test/Spec.hs` — Pruebas

```haskell
import Lib (editIndex)

main :: IO ()
main = do
  -- Prueba básica de editIndex
  let result = editIndex 1 "nueva tarea" ["tarea 0", "tarea 1", "tarea 2"]
  print result
  -- Esperado: ["tarea 0","nueva tarea","tarea 2"]
```

Se puede probar cada función desde el REPL sin necesidad de compilar el proyecto completo:

```bash
stack repl
> deleteOne 1 ["a","b","c"]
Just ["a","c"]
> editIndex 0 "nueva" ["vieja","b"]
["nueva","b"]
```

---

## 6. Flujo de Ejecución

```
stack run
    │
    ▼
main (app/Main.hs)
    │   Muestra el menú de comandos
    ▼
prompt [] ──────────────────────────────────────────────────────┐
    │                                                           │
    │  Lee un comando con getLine                               │
    ▼                                                           │
interpret comando todos                                         │
    │                                                           │
    ├── "+ texto"  → agrega a la lista → prompt (texto:todos) ─┤
    ├── "- N"      → elimina índice N  → prompt todos'  ────────┤
    ├── "s N"      → muestra ítem N    → prompt todos   ────────┤
    ├── "e N"      → edita ítem N      → prompt newTodos ───────┤
    ├── "l"        → lista todo        → prompt todos   ────────┤
    ├── "r"        → lista invertida   → prompt todos   ────────┤
    ├── "c"        → limpia lista      → prompt []      ────────┘
    └── "q"        → return () ── FIN
```

La recursión es el mecanismo que mantiene el "bucle" de la aplicación: `prompt` se llama a sí misma con el estado actualizado en lugar de usar un `while` o `for`.

---

## 7. Conceptos Clave del Paradigma Funcional Observados

| Concepto | Descripción | Ejemplo en el código |
|----------|-------------|----------------------|
| **Funciones puras** | Sin efectos secundarios; mismo input = mismo output | `deleteOne`, `editIndex`, `reverseTodos` |
| **Inmutabilidad** | Las listas no se modifican; se crean versiones nuevas | `prompt (todo : todos)` crea una nueva lista |
| **Pattern matching** | Despacho basado en la estructura del dato | `interpret ('+':' ':todo) todos` |
| **Tipos algebraicos** | `Maybe a` para representar falla sin excepciones | `deleteOne` y `showOne` devuelven `Maybe` |
| **Recursión** | Reemplaza los bucles imperativos | `prompt` se llama a sí misma; `reverseTodos` usa `go` |
| **Tipos `IO`** | Separación explícita de código puro y con efectos | `main :: IO ()`, `prompt :: [String] -> IO ()` |
| **Operador `:`** | Agrega un elemento al frente de una lista | `todo : todos` |
| **Operador `++`** | Concatena dos listas | `take i xs ++ [x] ++ drop (i+1) xs` |

---

## 8. Conclusión

A través de estas dos sesiones se logró:

1. Instalar el entorno de desarrollo completo de Haskell (GHCup, GHC, GHCi, HLS, Stack, Cabal) en Windows usando PowerShell.
2. Crear un proyecto Haskell desde cero con `stack new` y comprender la estructura de archivos generada.
3. Analizar los archivos de configuración `todo.cabal` y `stack.yaml.lock` que definen las dependencias y garantizan la reproducibilidad del build.


La mayor diferencia con el paradigma imperativo es que el "estado" de la aplicación (la lista de tareas) no muta: cada operación genera una nueva versión de la lista que se pasa recursivamente a la siguiente iteración de `prompt`. Esto elimina una clase completa de errores relacionados con el estado compartido y los efectos secundarios.