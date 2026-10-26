#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define PAYLOAD_SIZE 16

typedef enum { HELLO = 1, SIT, ARISE, BYE } Message;

typedef struct {
  long type;
  Message msg;
} msg_buf;

// global
int queue_id;
int my_id;
int locaL_clock = 0;

int waiting_queue[9];

// visitor
int sitting = 0;

// ringispil


void enter_critical() {

}

void exit_critical();
void send_hello_to_ringispil();
void read_one_message();

void ringispil() {
  srand(time(NULL) ^ getpid());
  int total_visitors = 0;

  while (total_visitors < 16) {
    for (int i = 0; i < 4; i++) {
      msg_buf msg_rcv;
      msgrcv(queue_id, &msg_rcv, sizeof(msg_rcv) - sizeof(long), (long)HELLO,
             0);
      printf("dobio hello\n");

      msg_buf msg_snd = {(long)SIT, SIT};
      msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);
    }

    printf("pokrenuo ringispil\n");
    total_visitors += 4;

    int r = 1000 + (rand() % 2000);
    usleep(r * 1000);

    printf("zavrsio ringispil\n");
    for (int i = 0; i < 4; i++) {
      msg_buf msg_snd = {(long)ARISE, ARISE};
      msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);
    }
  }
  printf("GOTOV\n");
}

void visitor() {
  // man 3 time: "The time() function returns the value of time in seconds ..."
  // => child procesi vjerojatno dobe isti seed jer se sve pozove unutar iste
  // sekunde. xor s getpid pa je mala sansa da je isti seed
  srand(time(NULL) ^ getpid());

  for (size_t i = 0; i < 2; ++i) {
    int r = 100 + (rand() % 1900);
    usleep(r * 1000);
    printf("zelim se voziti\n");

    // cs
    enter_critical();
    sitting = 0;
    send_hello_to_ringispil();
    while (!sitting) {
      read_one_message();
    }
    printf("sjeo posjetitelj %d\n", my_id);
    exit_critical();
    // cs

    msg_buf msg_snd = {(long)HELLO, HELLO};
    msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);

    msg_buf msg_rcv;
    msgrcv(queue_id, &msg_rcv, sizeof(msg_rcv) - sizeof(long), (long)SIT, 0);
    printf("sjeo posjetitelj %d\n", my_id);

    msgrcv(queue_id, &msg_rcv, sizeof(msg_rcv) - sizeof(long), (long)ARISE, 0);

    printf("ustao posjetitelj %d\n", my_id);
  }

  msg_buf msg_snd = {(long)BYE, BYE};
  msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);
  printf("posjetitelj %d zavrsio\n", my_id);
}

int main() {
  // 0666 su permissions
  queue_id = msgget(IPC_PRIVATE, IPC_CREAT | 0666);
  my_id = 0;

  for (size_t i = 0; i < 8; ++i) {
    pid_t pid = fork();

    if (pid < 0) {
      return 1;
    }

    if (pid == 0) {
      my_id = i + 1;
      break;
    }
  }

  if (my_id == 0) {
    ringispil();

    for (int i = 0; i < 8; i++) {
      wait(NULL);
    }

    msgctl(queue_id, IPC_RMID, NULL);
  } else {
    visitor();
  }

  return 0;
}
