# SRSV: communication between two separate programs (IPC)

Lab requirement: the input simulator and the controller simulator must be
separate programs that communicate with each other (e.g. over shared memory,
as in the template).

**Choice for the lab:** POSIX shared memory (`shm_open` + `mmap`) with a shared
header and C11 atomics. It is what the template does, it is still the standard
way, and it fits the problem: the simulator changes an input's state, the
controller polls it and writes a response.

## Shared header

`shared.h`, included by both programs:

```c
#include <stdatomic.h>

#define SHM_NAME   "/srsv_lab1"
#define MAX_INPUTS 32

struct input_slot {
    atomic_int state;     // simulator bumps this on each new event
    atomic_int response;  // controller copies state here when processed
};

struct shared {
    struct input_slot in[MAX_INPUTS];
};
```

## Opening the segment

The same code goes in both programs, so whichever starts first creates it:

```c
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

int fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0600);
ftruncate(fd, sizeof(struct shared));   // new segment is zero-filled
struct shared *sh = mmap(NULL, sizeof *sh, PROT_READ | PROT_WRITE,
                         MAP_SHARED, fd, 0);
close(fd);                              // mapping stays valid
```

## Using it

After mapping it is ordinary memory:

- **Simulator:** each period it does `atomic_fetch_add(&sh->in[i].state, 1)`,
  then watches for `response == state` and measures the reaction time.
- **Controller:** it sees `state != response`, simulates the processing for
  `C`, then stores `response = state`.
- **Cleanup:** on exit call `munmap`, and have one side call
  `shm_unlink(SHM_NAME)`.

Atomics are enough because each field has exactly one writer; no mutex or
semaphore is needed.

## Portability traps (macOS for development, Linux for grading)

- **`-std=c11` on Linux:** glibc hides `shm_open` and `ftruncate` under strict
  C11. Use `-std=gnu11` or add `-D_POSIX_C_SOURCE=200809L` to the compiler
  flags. macOS does not complain either way.
- **`-lrt`:** older glibc needs it for `shm_open`; on newer glibc it is
  harmless, and macOS does not need it.
- **`ftruncate` on macOS:** it only works once per shared-memory object and
  fails with `EINVAL` if the segment already exists from a previous run. Either
  ignore that error, or call `shm_unlink` at startup in the program that is
  always launched first.
- **Missing on macOS:** POSIX message queues (`mq_open`), unnamed semaphores
  (`sem_init`), `clock_nanosleep`, and real `SCHED_FIFO` do not exist or do not
  work. If later labs need them, develop in a Linux VM or container.

## Alternatives

| Mechanism | When it fits | Drawback for this lab |
|---|---|---|
| Named pipe (`mkfifo`) or Unix domain socket | Event/message style: "input 3 fired" | Syscall on every event; blocking and partial reads must be handled |
| POSIX message queue (`mq_send`/`mq_receive`) | Messages with priorities, common in real-time courses | Not available on macOS |
| `mmap` of a regular file | Same as shared memory, with a visible file | No real advantage over `shm_open` |
