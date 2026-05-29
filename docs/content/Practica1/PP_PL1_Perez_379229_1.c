// Mextli Citlali Perez Aguirre
// 379229
// Paradigmas de la Programcion


/*
notas de laboratorio:
    - Uso de memoria estatica(arrays)
    - No usar malloc/free
    - Capacidad fija de 10 trabajos

    - Funciones:
        q_init
        q_is_empty
        _q_is_full
        q_enqueue
        q_dequeue
        q_peek
        q_print
    - Si llena -> no agrega
    - Si vacia -> no peek/dequeue


Estructura de "Trabajo"
id:int 
usuario:char[32] <-- nombre del usuario
documento:chat[32] <-- nombre del documento
total_pgs:int <-- numero total de paginas
restante_pgs: paginas restantes por imprimir
copias:int <-- copias por imprimir
prioriad:enum <-- [NORMAL,URGENTE]
estado:enum <-- [EN_COLA, IMPRIMIENDO, COMPLETADO, CANCELADO]
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TAM_MAX 10

typedef enum {
    NORMAL = 0,
    URGENTE = 1
} Prioridad;

typedef enum {
    EN_COLA = 0,
    IMPRIMIENDO = 1,
    COMPLETADO = 2,
    CANCELADO = 3
} Estado;

/********** ESTRUCTURA **********/

typedef struct {
    int id;
    char usuario[32];
    char documento[32];
    int total_pgs;
    int restante_pgs;
    int copias;
    Prioridad prioridad;
    Estado estado;
} Tarea;

typedef struct {
    Tarea datos[TAM_MAX];
    int size;
} ColaLineal;

/********** PROTOTIPOS **********/

void q_init(ColaLineal *cola);
int q_is_empty(const ColaLineal *cola);
int q_is_full(const ColaLineal *cola);

int q_enqueue(ColaLineal *cola, Tarea t);
int q_peek(const ColaLineal *cola, Tarea *t);
int q_dequeue(ColaLineal *cola, Tarea *t);

void q_print(const ColaLineal *cola);

int menu();
void ejecutar(ColaLineal *cola);

/********** MAIN **********/

int main()
{
    ColaLineal cola;

    q_init(&cola);
    ejecutar(&cola);

    return 0;
}

/********** MENU **********/

int menu()
{
    int op;

    printf("\n---- COLA DE IMPRESION ----\n");
    printf("1. Agregar tarea\n");
    printf("2. Ver siguiente tarea\n");
    printf("3. Procesar tarea\n");
    printf("4. Mostrar cola\n");
    printf("5. Salir\n");

    printf("Opcion: ");
    scanf("%d", &op);

    return op;
}

void ejecutar(ColaLineal *cola)
{
    int op;
    int id_counter = 1;

    do
    {
        op = menu();

        switch(op)
        {
            case 1:
            {
                Tarea t;

                t.id = id_counter++;

                printf("Usuario: ");
                scanf("%s", t.usuario);

                printf("Documento: ");
                scanf("%s", t.documento);

                printf("Paginas: ");
                scanf("%d", &t.total_pgs);

                printf("Copias: ");
                scanf("%d", &t.copias);

                printf("Prioridad (0=Normal 1=Urgente): ");
                scanf("%d", (int*)&t.prioridad);

                t.restante_pgs = t.total_pgs;
                t.estado = EN_COLA;

                if(q_enqueue(cola, t))
                    printf("Tarea agregada (id=%d)\n", t.id);
                else
                    printf("Cola llena\n");

                break;
            }

            case 2:
            {
                Tarea t;

                if(q_peek(cola, &t))
                {
                    printf("\nSiguiente tarea:\n");
                    printf("ID: %d\n", t.id);
                    printf("Usuario: %s\n", t.usuario);
                    printf("Documento: %s\n", t.documento);
                    printf("Paginas: %d\n", t.total_pgs);
                }
                else
                    printf("Cola vacia\n");

                break;
            }

            case 3:
            {
                Tarea t;

                if(q_dequeue(cola, &t))
                {
                    printf("Procesando tarea ID %d...\n", t.id);
                    printf("Documento %s completado\n", t.documento);
                }
                else
                    printf("Cola vacia\n");

                break;
            }

            case 4:
                q_print(cola);
                break;

            case 5:
                printf("Saliendo...\n");
                break;

            default:
                printf("Opcion invalida\n");
        }

    } while(op != 5);
}

/********** FUNCIONES DE COLA **********/

void q_init(ColaLineal *cola)
{
    cola->size = 0;
}

int q_is_empty(const ColaLineal *cola)
{
    return cola->size == 0;
}

int q_is_full(const ColaLineal *cola)
{
    return cola->size == TAM_MAX;
}

int q_enqueue(ColaLineal *cola, Tarea t)
{
    if(q_is_full(cola))
        return 0;

    cola->datos[cola->size] = t;
    cola->size++;

    return 1;
}

int q_peek(const ColaLineal *cola, Tarea *t)
{
    if(q_is_empty(cola))
        return 0;

    *t = cola->datos[0];
    return 1;
}

int q_dequeue(ColaLineal *cola, Tarea *t)
{
    if(q_is_empty(cola))
        return 0;

    *t = cola->datos[0];

    for(int i = 1; i < cola->size; i++)
    {
        cola->datos[i-1] = cola->datos[i];
    }

    cola->size--;

    return 1;
}

void q_print(const ColaLineal *cola)
{
    if(q_is_empty(cola))
    {
        printf("Cola vacia\n");
        return;
    }

    printf("\n--- COLA DE IMPRESION ---\n");

    for(int i = 0; i < cola->size; i++)
    {
        printf("ID:%d  Usuario:%s  Doc:%s  Paginas:%d\n",
               cola->datos[i].id,
               cola->datos[i].usuario,
               cola->datos[i].documento,
               cola->datos[i].total_pgs);
    }
}