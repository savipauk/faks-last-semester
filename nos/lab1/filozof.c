#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define MAX_N 10

typedef enum { REQUEST = 1, REPLY, DONE } Message;

typedef struct {
  Message msg;
  int sender;
  int clock;
} msg_buf;

int local_clock = 0;
int n = 3;
int my_id = 0;
int pipes[MAX_N + 1][2];       // [i][0] = read, [i][1] = write, i = 0 is main
int waiting_queue[MAX_N + 1];  // [i = 0] = main
int replies = 0;
int done = 0;

void enter_critical();
void exit_critical();
void send_msg(int to, Message msg);
void read_one_message();

void enter_critical() {
  local_clock++;

  for (int i = 1; i <= n; i++) {
    if (i == my_id) {
      continue;
    }

    send_msg(i, REQUEST);
  }

  waiting_queue[my_id] = local_clock;

  while (replies < n - 1) {
    read_one_message();
  }
}

void exit_critical() {
  waiting_queue[my_id] = -1;

  for (int i = 1; i <= n; i++) {
    if (i == my_id) {
      continue;
    }

    // funkcionira iako izgleda cudno imati done prije reply
    send_msg(i, DONE);

    if (waiting_queue[i] == -1) {
      continue;
    }

    send_msg(i, REPLY);
  }
}

void send_msg(int to, Message msg) {
  msg_buf msg_snd = {.sender = my_id, .msg = msg, .clock = local_clock};

  printf("filozof %d -> %d: %d %d\n", my_id, to, msg, local_clock);

  ssize_t w;
  do {
    w = write(pipes[to][1], &msg_snd, sizeof(msg_snd));
  } while (w == -1);
}

void read_one_message() {
  msg_buf msg_rcv;
  ssize_t r;

  do {
    r = read(pipes[my_id][0], &msg_rcv, sizeof(msg_rcv));
  } while (r == -1);

  if (msg_rcv.clock > local_clock) {
    local_clock = msg_rcv.clock;
  }
  local_clock++;

  printf("filozof %d <- %d: %d %d\n", my_id, msg_rcv.sender, msg_rcv.msg,
         msg_rcv.clock);

  switch (msg_rcv.msg) {
    case REQUEST: {
      if (waiting_queue[my_id] == -1 || waiting_queue[my_id] > msg_rcv.clock ||
          (waiting_queue[my_id] == msg_rcv.clock && my_id > msg_rcv.sender)) {
        send_msg(msg_rcv.sender, REPLY);
      } else {
        waiting_queue[msg_rcv.sender] = msg_rcv.clock;
      }
      break;
    }

    case REPLY: {
      replies++;
      break;
    }

    case DONE: {
      done++;
      break;
    }

    default: {
      printf("unknown message\n");
      break;
    }
  }
}

void think() {
  srand(time(NULL) ^ getpid());

  // sudjeluj na konferenciji
  int r = 100 + (rand() % 1900);
  usleep(r * 1000);

  // cs
  {
    enter_critical();

    // pristupi stolu, jedi ispisi
    printf("filozof %d za stolom\n", my_id);
    sleep(3);

    exit_critical();
  }
  // cs

  // sudjeluj na konferenciji
  r = 100 + (rand() % 1900);
  usleep(r * 1000);

  while (done < n - 1) {
    read_one_message();
  }
}

int main(int argc, char* argv[]) {
  if (argc != 2) {
    printf("argc != 2. defaulting to n = 3.\n");
  } else {
    n = atoi(argv[1]);
    if (n > MAX_N) {
      n = MAX_N;
    }
    printf("setting n = %d\n", n);
  }

  fflush(stdout);

  for (int i = 1; i <= n; i++) {
    if (pipe(pipes[i]) == -1) {
      exit(1);
    }
  }

  for (int i = 0; i <= n; i++) {
    waiting_queue[i] = -1;
  }

  for (int i = 0; i < n; ++i) {
    pid_t pid = fork();

    if (pid < 0) {
      return 1;
    }

    if (pid == 0) {
      my_id = i + 1;

      for (int j = 1; j <= n; j++) {
        if (j == my_id) {
          close(pipes[j][1]);  // no writing to yourself
        } else {
          close(pipes[j][0]);  // no reading from others
        }
      }

      break;
    }
  }

  if (my_id == 0) {
    for (int i = 1; i <= n; i++) {
      close(pipes[i][0]);
      close(pipes[i][1]);
    }

    for (int i = 0; i < n; i++) {
      wait(NULL);
    }
  } else {
    think();
  }

  return 0;
}
