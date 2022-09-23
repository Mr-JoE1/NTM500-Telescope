#include <stdio.h>
#include <time.h>


int main(int argc, char const *argv[])
{
	
	clock_t start = clock(); 
	printf("started at: %ld \n",start); 
	sleep(10); 
	clock_t end = clock(); 
	printf("ended at: %ld \n",clock());
	printf("ticks/sec %ld \n", CLOCKS_PER_SEC); 
	double total = (end - start)/CLOCKS_PER_SEC; 
	printf("Total time in Sec: %f \n", total); 

	return 0;
}