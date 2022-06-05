#include<stdio.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<errno.h>
#include<fcntl.h>

int main(){
    if(mkfifo("dataFlow", 0777) == -1){
        if(errno != EEXIST){
            printf("Could not create fifo file\n");
            return 1;
        }
        else{
            printf("Fifo file already exists\n");
            return 1;
        }
    }
}