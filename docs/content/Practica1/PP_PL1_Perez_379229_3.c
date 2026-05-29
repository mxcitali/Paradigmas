
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**********ESTTRUCTURA************/

typedef enum {
    NORMAL = 0, 
    URGENTE = 1
} Prioridad_t;

typedef enum{
    EN_COLA = 0,
    IMPRIMIENDO = 1,
    COMPLETADO = 2,
    CANCELADO = 3
} Estado_t;

typedef struct Tarea{
    int id;
    char usuario[32];
    char documento[48];
    int total_pgs;
    int restante_pgs;
    int copias;
    Prioridad_t prioridad;
    Estado_t estado;
} Tarea;


typedef struct Node_t{
    Tarea job;
    struct Node_t* next;
} Node_t;

typedef struct{
    Node_t* head;  // frente
    Node_t* tail;  // final
    int size;
} QueueDynamic_t;

/**********PROTOTIPOS************/
int menu();
void qd_init(QueueDynamic_t* q);
void elegir(QueueDynamic_t *cola);
int qd_is_empty(const QueueDynamic_t* q);
int qd_enqueue(QueueDynamic_t* q, Tarea job);
int qd_peek(const QueueDynamic_t* q, Tarea* out);
int qd_dequeue(QueueDynamic_t* q, Tarea* out);
void qd_destroy(QueueDynamic_t* q);
void simular_impresion(QueueDynamic_t *cola);
int qd_cancel(QueueDynamic_t* q, int id_buscar);

/**********MAIN************/
int main()
{
    QueueDynamic_t cola;

    qd_init(&cola);

    elegir(&cola);

    qd_destroy(&cola);

    return 0;
}

/**********FUNCIONES************/
int menu()
{
    int op;

    printf("\n--- COLA DE IMPRESION ---\n");
    printf("1. Agregar tarea\n");
    printf("2. Ver siguiente tarea\n");
    printf("3. Procesar una tarea\n");
    printf("4. Mostrar cola\n");
    printf("5. Simular impresion completa\n");
    printf("6. Cancelar\n");
    printf("7. Salir\n");

    printf("Opcion: ");
    scanf("%d",&op);

    return op;
}

void elegir(QueueDynamic_t *cola)
{
    int op;
    int id = 1;

    do
    {
        op = menu();

        switch(op)
        {
            case 1:
                Tarea t;

                t.id = id++;

                printf("Usuario: ");
                scanf("%s",t.usuario);

                printf("Documento: ");
                scanf("%s",t.documento);

                printf("Paginas: ");
                scanf("%d",&t.total_pgs);

                printf("Copias: ");
                scanf("%d",&t.copias);

                printf("Prioridad (0 normal, 1 urgente): ");
                scanf("%d",(int*)&t.prioridad);

                t.restante_pgs = t.total_pgs;
                t.estado = EN_COLA;

                qd_enqueue(cola,t);

                break;

            case 2:
                Tarea t;

                if(qd_peek(cola,&t))
                    printf("Siguiente: %s\n",t.documento);
                else
                    printf("Cola vacia\n");

                break;

            case 3:
                Tarea t;

                if(qd_dequeue(cola,&t))
                    printf("Imprimiendo %s\n",t.documento);
                else
                    printf("Cola vacia\n");

                break;

            case 4:
                if(qd_is_empty(cola))
                {
                    printf("Cola vacia\n");
                    break;
                }

                Node_t* aux = cola->head;

                while(aux != NULL)
                {
                    printf("ID:%d Usuario:%s Doc:%s\n",
                        aux->job.id,
                        aux->job.usuario,
                        aux->job.documento);

                    aux = aux->next;
                }

                break;

               
            case 5:
                simular_impresion(cola);
                break;

            case 6:
                int id_canc;
                printf("Ingrese el ID de la tarea a cancelar: ");
                scanf("%d", &id_canc);
                if(qd_cancel(cola, id_canc))
                    printf("Tarea %d cancelada exitosamente.\n", id_canc);
                else
                    printf("No se encontro la tarea o la cola esta vacia.\n");
                break;

            case 7:
                printf("Saliendo y liberando memoria...\n");
                break;
            
        }

    }while(op != 7);
}


void simular_impresion(QueueDynamic_t *cola)
{
    Tarea t;

    if(qd_is_empty(cola))
    {
        printf("No hay trabajos en la cola\n");
        return;
    }

    printf("\n--- INICIANDO SIMULACION ---\n");

    while(!qd_is_empty(cola))
    {
        qd_dequeue(cola,&t);

        t.estado = IMPRIMIENDO;

        printf("\nImprimiendo documento: %s\n",t.documento);

        while(t.restante_pgs > 0)
        {
            printf("Pagina %d de %d\n",
                   t.total_pgs - t.restante_pgs + 1,
                   t.total_pgs);

            t.restante_pgs--;

            sleep(1);   
        }

        t.estado = COMPLETADO;

        printf("Documento %s COMPLETADO\n",t.documento);
    }

    printf("\n--- COLA TERMINADA ---\n");
}

void qd_init(QueueDynamic_t* q)
{
    q->head = NULL;
    q->tail = NULL;
    q->size = 0;
}

int qd_is_empty(const QueueDynamic_t* q)
{
    return q->size == 0;
}

int qd_cancel(QueueDynamic_t* q, int id_buscar) {
    if(qd_is_empty(q)) return 0;

    Node_t* actual = q->head;
    Node_t* anterior = NULL;

    while(actual != NULL) {
        if(actual->job.id == id_buscar) {
            if(anterior == NULL) {
                q->head = actual->next;
                if(q->head == NULL) q->tail = NULL;
            } else {
                anterior->next = actual->next;
                if(actual == q->tail) q->tail = anterior;
            }
            free(actual);
            q->size--;
            return 1; 
        }
        anterior = actual;
        actual = actual->next;
    }
    return 0;
}

int qd_enqueue(QueueDynamic_t* q, Tarea job)
{
    Node_t* nuevo = (Node_t*)malloc(sizeof(Node_t));
    if(nuevo == NULL) return 0;

    nuevo->job = job;
    nuevo->next = NULL;

    if(qd_is_empty(q)) {
        q->head = nuevo;
        q->tail = nuevo;
    } 
    else if(job.prioridad == URGENTE) {
        nuevo->next = q->head;
        q->head = nuevo;
    } 
    else {
        q->tail->next = nuevo;
        q->tail = nuevo;
    }

    q->size++;
    return 1;
}

int qd_peek(const QueueDynamic_t* q, Tarea* out)
{
    if(qd_is_empty(q))
        return 0;

    *out = q->head->job;

    return 1;
}

int qd_dequeue(QueueDynamic_t* q, Tarea* out)
{
    if(qd_is_empty(q))
        return 0;

    Node_t* temp = q->head;

    *out = temp->job;

    q->head = temp->next;

    if(q->head == NULL)
        q->tail = NULL;

    free(temp);

    q->size--;

    return 1;
}

void qd_destroy(QueueDynamic_t* q)
{
    Node_t* actual = q->head;

    while(actual != NULL)
    {
        Node_t* temp = actual;
        actual = actual->next;
        free(temp);
    }

    q->head = NULL;
    q->tail = NULL;
    q->size = 0;
}