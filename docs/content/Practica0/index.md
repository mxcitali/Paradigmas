+++
date = '2026-02-18T15:41:53-08:00'
draft = false
title = 'Practica 0: Uso de Repositorios'
+++

# Primera sesión: Markdown
## ¿Qué es Markdown?

Markdown es un lenguaje de marcado ligero creado por John Gruber en 2004.  
Permite dar formato a texto usando una sintaxis simple y fácil de leer.

Se utiliza principalmente para:

- Documentación técnica  
- Archivos README en GitHub  
- Blogs  
- Páginas web estáticas  
- Notas profesionales  

---

## ¿Cómo se utiliza Markdown?

Los archivos Markdown tienen la extensión: .md


Ejemplo
README.md

Se escribe texto utilizando símbolos especiales para aplicar formato.

---

## Sintaxis básica de Markdown

<!-- Esto es un comentario (._.)-->
# Esto es un encabezado H1
## Esto es un encabezado H2 
### Esto es un encabezado H3
#### Esto es un encabezado H4
##### Esto es un encabezado H5

Esto es un texto en _italicas_
Esto es un texto en *italicas*

Esto es un texto en **negritas**
Esto es un texto en __negritas__

# (>.<)

Este `es un texto` especial

Este es un texto ~~tachado~~

* Elemento 1
* Elemento 2
* Elemento 3
  * Elemento 3.1
  * Elemento 3.2
    * Elemento 3.2.1
* Elemento 4
  
- Elemento 1
- Elemento 2
- Elemento 3
  - Elemento 3.1
  - Elemento 3.2
    - Elemento 3.2.1
- Elemento 4
  
1. Elemento 1
1. Elemento 2
1. Elemento 3
    1. Elemento 3.1
    2. Elemento 3.2
    3. Elemento 3.2.1
1. Elemento 4

[texto de enlace](https://elcodigoascii.com "Textp del tooltip")

![Texto alternativo](https://tse4.mm.bing.net/th/id/OIP.E2WdC_LjFMAxvmJGswml4wHaE-?rs=1&pid=ImgDetMain&o=7&rm=3)

```txt
this is code block
```

| Productos | Precio | Cantidad |
| - | - | - |
| Laptop | 3.3 | 2 |

> Esto es una nota

* [ ] Primera tarea
* [X] Segunda tarea
* [ ] Tercera tarea

<!-- Division horizontal -->
***

<!-- Emojis -->
@darthrookie :+1: :smile:

# Segunda Sesión: Uso de Git y GitHub

---

## ¿Qué es Git?

Git es un sistema de control de versiones distribuido creado por Linus Torvalds en 2005.

Permite:

- Llevar control de cambios en un proyecto
- Guardar el historial de versiones
- Trabajar en equipo sin perder información
- Recuperar versiones anteriores del código

Git funciona de manera local en tu computadora.

---

## ¿Qué es GitHub?

GitHub es una plataforma en la nube que permite almacenar repositorios Git en internet.

Permite:

- Subir proyectos a la nube
- Compartir código con otras personas
- Colaborar en equipo
- Crear un portafolio profesional
- Publicar proyectos

GitHub funciona como el servidor remoto donde se guarda el proyecto.

---

## ¿Cómo se utiliza Git?

El flujo básico de trabajo es:

1. Crear un proyecto en tu computadora
2. Inicializar Git
3. Agregar los archivos
4. Crear un commit
5. Conectar el repositorio con GitHub
6. Subir los archivos a la nube

---

## Comandos esenciales de Git

## Comandos esenciales de Git

- `git init` = Inicializa un repositorio Git en la carpeta actual.

- `git status` = Muestra el estado del proyecto y los archivos modificados.

- `git add .` = Agrega todos los archivos al área de preparación.

- `git add nombre_archivo` = Agrega un archivo específico.

- `git commit -m "Mensaje"` = Guarda los cambios con un mensaje descriptivo.

- `git branch -M main` = Define la rama principal como "main".

- `git remote add origin URL_DEL_REPOSITORIO` = Conecta el repositorio local con GitHub.

- `git push` = Sube cambios posteriores.

---

## ¿Cómo crear un repositorio en GitHub?

1. Iniciar sesión en GitHub.
2. Hacer clic en **New Repository**.
3. Escribir el nombre del repositorio.
4. Elegir si será público o privado.
5. Hacer clic en **Create Repository**.
6. Copiar la URL del repositorio.

---

# Tercera Sesión: Hugo y GitHub Actions

---

## ¿Qué es Hugo?

Hugo es un generador de sitios web estáticos escrito en Go.  
Permite crear sitios web rápidos sin utilizar bases de datos.  
Convierte archivos Markdown en páginas HTML listas para publicarse en internet.

Se utiliza para:

- Blogs  
- Portafolios  
- Documentación  
- Sitios personales  

---

## ¿Qué es GitHub Actions?

GitHub Actions es una herramienta de automatización integrada en GitHub.  
Permite ejecutar procesos automáticamente cuando se realiza un `push` al repositorio.

Se utiliza para:

- Automatizar procesos  
- Construir proyectos automáticamente  
- Publicar sitios web  
- Implementar integración continua (CI/CD)  

---

# Crear un sitio estático con Hugo

## 1. Instalar Hugo

Verificar instalación:

```bash
hugo version
```

---

## 2. Crear un nuevo sitio

```bash
hugo new site mi-sitio
```

---

## 3. Entrar al proyecto

```bash
cd mi-sitio
```

---

## 4. Inicializar Git

```bash
git init
```

---

## 5. Agregar un tema

```bash
git submodule add URL_DEL_TEMA themes/tema
```

Configurar el tema en el archivo `hugo.toml`:

```toml
theme = "tema"
```

---

## 6. Crear contenido

```bash
hugo new posts/primer-post.md
```

Editar el archivo dentro de la carpeta `content`.

---

## 7. Ejecutar servidor local

```bash
hugo server
```

El sitio estará disponible en:

```
http://localhost:1313
```

---

# Subir el sitio a GitHub

## 1. Agregar archivos

```bash
git add .
```

---

## 2. Crear commit

```bash
git commit -m "Primer sitio con Hugo"
```

---

## 3. Crear repositorio en GitHub

1. Iniciar sesión en GitHub.  
2. Hacer clic en **New Repository**.  
3. Asignar nombre al repositorio.  
4. Crear el repositorio.  
5. Copiar la URL proporcionada.  

---

## 4. Conectar repositorio local con GitHub

```bash
git remote add origin https://github.com/usuario/repositorio.git
```

---

## 5. Subir el proyecto a la nube

```bash
git branch -M main
git push -u origin main
```

Ahora el proyecto ya está almacenado en GitHub.

---

# Configurar GitHub Actions para publicar en GitHub Pages

## 1. Crear carpeta de workflows

```bash
mkdir -p .github/workflows
```

---

## 2. Crear archivo de configuración

Crear archivo:

```
.github/workflows/deploy.yml
```

## 3. Activar GitHub Pages

1. Ir al repositorio en GitHub.  
2. Entrar a **Settings**.  
3. Ir a **Pages**.  
4. Seleccionar la rama generada por GitHub Actions.  
5. Guardar cambios.  

Cada vez que se haga `git push`, el sitio se publicará automáticamente.

---

# Enlaces del Proyecto

## Portafolio en GitHub

```
https://github.com/mxcitali/Paradigmas
```

---

## Página estática en GitHub Pages

```
https://mxcitali.github.io/Paradigmas/
```
