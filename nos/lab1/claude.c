#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

// proces 0 je vrtuljak, procesi 1..8 su posjetitelji
#define N 9

typedef enum { HELLO = 1, SIT, ARISE, LEFT, BYE, REQEUST, REPLY, EXIT } Message;

typedef struct {
  long type;  // primatelj: id + 1 (mtype mora biti > 0)
  Message msg;
  int sender;
  int clock;
} msg_buffer;

// nakon fork() svaki proces ima svoju kopiju ovoga
int queue_id;
int my_id;
int lclock = 0;

int req_ts[N];   // vremenska oznaka zahtjeva procesa j, -1 ako ga nema
int replied[N];  // je li proces j odgovorio na moj zahtjev
int done[N];     // je li proces j zavrsio (ne odgovara vise)

int hello_from = -1;  // vrtuljak: tko je poslao HELLO
int left_count = 0;   // vrtuljak: koliko ih je sislo
int bye_count = 0;    // vrtuljak: koliko ih je zavrsilo
int got_sit = 0;      // posjetitelj
int got_arise = 0;    // posjetitelj

void send_to(int to, Message msg, int clock) {
  msg_buffer msg_snd = {to + 1, msg, my_id, clock};
  msgsnd(queue_id, &msg_snd, sizeof(msg_snd) - sizeof(long), 0);
}

void send_to_all(Message msg, int clock) {
  for (int j = 0; j < N; j++) {
    if (j != my_id && !done[j]) {
      send_to(j, msg, clock);
    }
  }
}

// primi jednu poruku iz svog sanducica i obradi je
void receive_one() {
  msg_buffer msg_rcv;
  msgrcv(queue_id, &msg_rcv, sizeof(msg_rcv) - sizeof(long), my_id + 1, 0);

  // uskladi lokalni sat
  if (msg_rcv.clock > lclock) {
    lclock = msg_rcv.clock;
  }
  lclock++;

  switch (msg_rcv.msg) {
    case REQEUST:
      req_ts[msg_rcv.sender] = msg_rcv.clock;
      send_to(msg_rcv.sender, REPLY, lclock);
      break;
    case REPLY:
      replied[msg_rcv.sender] = 1;
      break;
    case EXIT:
      req_ts[msg_rcv.sender] = -1;
      break;
    case HELLO:
      hello_from = msg_rcv.sender;
      break;
    case SIT:
      got_sit = 1;
      break;
    case ARISE:
      got_arise = 1;
      break;
    case LEFT:
      left_count++;
      break;
    case BYE:
      done[msg_rcv.sender] = 1;
      bye_count++;
      break;
  }
}

// moj zahtjev je prvi u redu i svi ostali su odgovorili
int can_enter() {
  for (int j = 0; j < N; j++) {
    if (j == my_id) {
      continue;
    }
    if (!replied[j] && !done[j]) {
      return 0;
    }
    if (req_ts[j] != -1 && (req_ts[j] < req_ts[my_id] ||
                            (req_ts[j] == req_ts[my_id] && j < my_id))) {
      return 0;
    }
  }
  return 1;
}

void lamport_enter() {
  lclock++;
  req_ts[my_id] = lclock;
  for (int j = 0; j < N; j++) {
    replied[j] = 0;
  }
  send_to_all(REQEUST, req_ts[my_id]);

  while (!can_enter()) {
    receive_one();
  }
}

void lamport_exit() {
  int t = req_ts[my_id];
  req_ts[my_id] = -1;
  send_to_all(EXIT, t);
}

void ringispil() {
  srand(time(NULL) ^ getpid());
  int total_visitors = 0;

  while (total_visitors < 16) {
    int seated[4];

    for (int i = 0; i < 4; i++) {
      while (hello_from == -1) {
        receive_one();
      }
      printf("dobio hello od %d\n", hello_from);
      seated[i] = hello_from;
      hello_from = -1;
      send_to(seated[i], SIT, lclock);
    }

    // zadnji posjetitelj salje EXIT tek nakon sto je sjeo
    while (req_ts[seated[3]] != -1) {
      receive_one();
    }

    printf("pokrenuo ringispil\n");
    total_visitors += 4;

    int r = 1000 + (rand() % 2000);
    usleep(r * 1000);

    printf("zavrsio ringispil\n");
    left_count = 0;
    for (int i = 0; i < 4; i++) {
      send_to(seated[i], ARISE, lclock);
    }

    // nitko ne smije sjesti prije nego svi prethodni sidu
    while (left_count < 4) {
      receive_one();
    }
  }

  while (bye_count < 8) {
    receive_one();
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
    printf("zelim se voziti %d\n", my_id);

    lamport_enter();
    got_sit = 0;
    send_to(0, HELLO, lclock);
    while (!got_sit) {
      receive_one();
    }
    printf("sjeo posjetitelj %d\n", my_id);
    lamport_exit();

    got_arise = 0;
    while (!got_arise) {
      receive_one();
    }
    printf("ustao posjetitelj %d\n", my_id);
    send_to(0, LEFT, lclock);
  }

  send_to_all(BYE, lclock);
  printf("posjetitelj %d zavrsio\n", my_id);
}

int main() {
  // 0666 su permissions
  queue_id = msgget(IPC_PRIVATE, IPC_CREAT | 0666);

  for (int j = 0; j < N; j++) {
    req_ts[j] = -1;
  }

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
