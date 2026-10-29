main:
	mkdir -p build
	make filozof ringispil

filozof:
	cc filozof.c -Wall -Wextra -std=c11 -D_BSD_SOURCE -fsanitize=address,undefined -g -o build/filozof

ringispil:
	cc ringispil.c -Wall -Wextra -std=c11 -D_BSD_SOURCE -fsanitize=address,undefined -g -o build/ringispil
