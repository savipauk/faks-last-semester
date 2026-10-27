#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define PAYLOAD_SIZE 16

typedef enum { HELLO = 1, SIT, ARISE, LEFT, BYE, REQUEST, REPLY, EXIT } Message;

typedef struct {
  long type;  // receiver: id + 1, mtype > 0
  Message msg;
  int sender;
  int clock;
} msg_buf;

// global
int queue_id;
int my_id;  // mtype = my_id + 1
            // tu on dobiva svoje poruke
int local_clock = 0;

int waiting_queue[9];
int replied[9];
int done[9];

// visitor
int got_sit = 0;
int got_arise = 0;

// ringispil
int bye_count = 0;

void enter_critical();
void exit_critical();
void send_message(int to, Message msg, int clock);
void send_to_all(Message msg, int clock);
void read_one_message();
int can_enter();

void enter_critical() {
  local_clock++;
  waiting_queue[my_id] = local_clock;

  for (int i = 0; i < 9; i++) {
    replied[i] = 0;
  }

  send_to_all(REQUEST, local_clock);

  while (!can_enter()) {
    read_one_message();
  }
}

void exit_critical() {
  send_to_all(EXIT, waiting_queue[my_id]);
  waiting_queue[my_id] = -1;
}

// moj zahtjev je prvi, svi ostali su odgovorili
int can_enter() {
  int smallest = waiting_queue[my_id];
  int id = my_id;

  for (int i = 0; i < 9; i++) {
    if (i == my_id) {
      continue;
    }

    if (replied[i] == 0) {
      return 0;
    }

    int other_clock = waiting_queue[i];
    if (waiting_queue[i] != -1 && (smallest == -1 || other_clock < smallest)) {
      smallest = other_clock;
      id = i;
    }
  }

  if (id == my_id) {
    return 1;
  }

  return 0;
}

void send_message(int to, Message msg, int clock) {
  msg_buf msg_snd = {to + 1, msg, my_id, clock};
  msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);
}

void send_to_all(Message msg, int clock) {
  for (int i = 0; i < 9; i++) {
    if (i == my_id || done[i]) {
      continue;
    }

    send_message(i, msg, local_clock);
  }
}

void read_one_message() {
  msg_buf msg_rcv;
  msgrcv(queue_id, &msg_rcv, sizeof(msg_rcv) - sizeof(long), my_id + 1, 0);

  if (msg_rcv.clock > local_clock) {
    local_clock = msg_rcv.clock;
  }
  local_clock++;

  switch (msg_rcv.msg) {
    case HELLO:
    case SIT: {
      if (msg_rcv.sender == 0) {
        got_sit = 1;
      } else {
        printf("%d was told to sit by %d\n", my_id, msg_rcv.sender);
      }
      break;
    }

    case ARISE: {
      if (msg_rcv.sender == 0) {
        got_arise = 1;
      } else {
        printf("%d was told to arise by %d\n", my_id, msg_rcv.sender);
      }
      break;
    }

    case BYE: {
      break;
    }

    case REQUEST: {
      waiting_queue[msg_rcv.sender] = msg_rcv.clock;
      send_message(msg_rcv.sender, REPLY, local_clock);
      break;
    }

    case REPLY:
      replied[msg_rcv.sender] = 1;
      break;

    case EXIT: {
      waiting_queue[msg_rcv.sender] = -1;
      break;
    }

    default:
      printf("unknown message: %d\n", msg_rcv.msg);
      break;
  }
}

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

    // critical section
    {
      enter_critical();
      got_sit = 0;
      send_message(0, HELLO, local_clock);
      while (!got_sit) {
        read_one_message();
      }
      printf("sjeo posjetitelj %d\n", my_id);
      exit_critical();
    }
    // critical section

    got_arise = 0;
    while (!got_arise) {
      read_one_message();
    }

    printf("ustao posjetitelj %d\n", my_id);

    send_message(0, LEFT, local_clock);
  }

  send_to_all(BYE, local_clock);
  printf("posjetitelj %d zavrsio\n", my_id);
}

int main() {
  // 0666 su permissions
  queue_id = msgget(IPC_PRIVATE, IPC_CREAT | 0666);
  my_id = 0;

  for (int i = 0; i < 9; i++) {
    waiting_queue[i] = -1;
  }

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
