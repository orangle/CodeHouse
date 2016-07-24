#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define TNUM 2

typedef struct _thread_data_t {
    int tid;
    double stuff;
} thread_data_t;

void *thr_func(void *arg){
    pid_t pid;
    pthread_t tid;
    thread_data_t *data = (thread_data_t *)arg;

    pid = getpid();
    tid = pthread_self();
    
    printf("Thread: pid %u, tid %u, tid %d\n", (unsigned int)pid,
            (unsigned int) tid, data->tid);

    pthread_exit(NULL);
}

int main(){
    pthread_t thr[TNUM];
    int i, rc;
    thread_data_t thr_data[TNUM];

    for(i = 0; i < TNUM; ++i){
        thr_data[i].tid = i;
        if ((rc = pthread_create(&thr[i], NULL, thr_func, &thr_data[i]))){
            fprintf(stderr, "error: pthread_create, rc: %d\n", rc);
            return EXIT_FAILURE;
        }
    }

    for (i = 0; i < TNUM; ++i) {
        pthread_join(thr[i], NULL);
    }

    return 0;
}
