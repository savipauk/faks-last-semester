#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#define PAYLOAD_SIZE 16

typedef enum { HELLO, SIT, ARISE, LEFT, BYE } Message;

typedef struct {
  long type;
  Message msg;
} msg_buf;

long msg_type_visitor = 1;
long msg_type_wheel = 2;

void ringispil(int queue_id) {
  int unfinished = 8;

  while (unfinished != 0) {
    for (int i = 0; i < 4;) {
      msg_buf msg_rcv;
      msgrcv(queue_id, &msg_rcv, sizeof(msg_rcv) - sizeof(long),
             msg_type_visitor, 0);

      switch (msg_rcv.msg) {
      case HELLO: {
        // visitor says hello, we need 4 visitors to start a ride
        printf("dobio hello\n");
        i++;
        break;
      }
      case LEFT: {
        // visitor finished a ride
        break;
      }
      case BYE: {
        // visitor is over
        unfinished--;
        break;
      }
      default:
        printf("unexpected message...panik!!!\n");
      }
    }

    msg_buf msg_snd = {msg_type_wheel, SIT};
    msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);
    printf("unfinished %d\n", unfinished);
  }
  printf("GOTOV\n");
}

void visitor(int id, int queue_id) {
  // man 3 time: "The time() function returns the value of time in seconds ..."
  // => child procesi vjerojatno dobe isti seed jer se sve pozove unutar iste
  // sekunde. xor s getpid pa je mala sansa da je isti seed
  srand(time(NULL) ^ getpid());

  for (size_t i = 0; i < 2; ++i) {
    int r = 100 + (rand() % 1900);
    usleep(r * 1000);
    printf("dobio hello\n");
    msg_buf msg_snd = {msg_type_visitor, HELLO};
    msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);

    msg_buf msg_rcv;
    msgrcv(queue_id, &msg_rcv, sizeof(msg_rcv) - sizeof(long), msg_type_wheel,
           0);

    if (msg_rcv.msg == SIT) {
      printf("Sjeo posjetitelj %d\n", id);
    }

    msgrcv(queue_id, &msg_rcv, sizeof(msg_rcv) - sizeof(long), msg_type_wheel,
           0);
    if (msg_rcv.msg == ARISE) {
      printf("Ustao posjetitelj %d\n", id);
      msg_buf msg_snd = {msg_type_visitor, LEFT};
      msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);
    }
  }

  msg_buf msg_snd = {msg_type_visitor, BYE};
  msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);
  printf("Posjetitelj %d zavrsio\n", id);
}

int main() {
  // 0666 su permissions
  int queue_id = msgget(IPC_PRIVATE, IPC_CREAT | 0666);

  int id = 0;

  for (size_t i = 0; i < 8; ++i) {
    pid_t pid = fork();

    if (pid < 0) {
      return 1;
    }

    if (pid == 0) {
      id = i + 1;
      break;
    }
  }

  if (id == 0) {
    // usleep(5000 * 1000);
    ringispil(queue_id);
  } else {
    visitor(id, queue_id);
  }

  return 0;
}
