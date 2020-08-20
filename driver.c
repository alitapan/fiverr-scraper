#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(){

	pid_t pid;
	pid = fork();

	if(pid == 0) {

		pid_t p;
		p = fork();
		if(p == 0) {
			printf("Running process: process id is %d\n", getpid());
			execlp("python", "python", "crawler/spider.py", "1", "2", NULL);
		}
		else if(p>0) {
			printf("Running process: process id is %d\n", getpid());
			execlp("python", "python", "crawler/spider.py", "1", "3", NULL);
			waitpid(p, NULL, 0);

		}
	}
	else if(pid>0) {

		pid_t d;
		d = fork();
		if(d == 0) {
			printf("Running process: process id is %d\n", getpid());
			execlp("python", "python", "crawler/spider.py", "1", "4", NULL);

		}
		else if(d>0) {
			printf("Running process: process id is %d\n", getpid());
			execlp("python", "python", "crawler/spider.py", "1", "5", NULL);
			waitpid(d , NULL, 0);

		}
		waitpid(pid, NULL, 0);
	}
	return 0;

}
