#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

void ringispil() {
  printf("ringispil\n");
}

void ringispil_p() {
  while (1) {
  }
}

void visitor(int id) {
  srand(time(NULL));

  for (size_t i = 0; i < 2; ++i) {
    int r = 100 + (rand() % 1900);
    usleep(r * 1000);
    // send_msg("zelim se voziti")
    if (/*reply is Sjedni*/ 1) {
      printf("Sjeo posjetitelj %d\n", id);
    }

    if (/*reply is Ustani*/ 1) {
      printf("Ustao posjetitelj %d\n", id);
    }
  }
  // send_msg("posjetitelj id zavrsio")
  printf("Posjetitelj %d zavrsio\n", id);
}

int main() {
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
    usleep(5000 * 1000);
    ringispil();
  } else {
    visitor(id);
  }

  return 0;
}
