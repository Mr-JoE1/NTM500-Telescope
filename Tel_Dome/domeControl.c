
/*
 * dome_control.c file to control telescope dome in manual/Remote modes 
 * Author : Mohamed Maher 
 * Date : 10/01/2021 
 * www.infinitytech.ltd 
 * NOTE :  you have to link your source to -lpigpio -lrt -lpthread
 */
 


#include "domeControl.h"
unsigned int OP_MODE = 0 ;
unsigned int SAFE_LOCK =0 ; 




/*----- function to get the current  system time and date for logging ---------*/
 
const char* timestamp(){

	time_t ltime ;
	ltime=time(NULL);
	return asctime(localtime(&ltime));
}

/*--------- function to log Error to Console and log file ----------*/

void log_error(const char* err){

	FILE *flog = fopen("log.txt","w"); 
	if(flog== NULL){
		printf("%sError Opening log file: %s%s\n",RED,YELL,strerror(errno));
		gpioTerminate();
		exit(EXIT_FAILURE);
	}
	else{
		printf("%s%s : %s%s\n",RED, err ,YELL,strerror(errno)); 
		fprintf(flog,"%s >> %s : %s\n",timestamp(), err, strerror(errno));
		gpioTerminate();
		exit(EXIT_FAILURE);
	}
}

unsigned int system_safe_lock(){
	
	if(gpioRead(SYS_SOS_SW)==0 || gpioRead(SENSOR_INT)==0 || gpioRead(BRAKE_SW)==0)
		return SAFE_LOCK = 1; 
	else
		return SAFE_LOCK = 0;
}


unsigned int check_mode(){
	unsigned int MODE_FLAG = 0; 
	if(gpioRead(MODE_SW)==1 && OP_MODE==1){
		printf("%sControl Mode switched to %sRemote\n\n",GREEN,MAG);
		MODE_FLAG=2;
	}
	if(gpioRead(MODE_SW)==0 && OP_MODE==2){
		printf("%sControl Mode switched to %sManual\n\n",GREEN,MAG);
		MODE_FLAG=1;
	}
	if(MODE_FLAG != OP_MODE && MODE_FLAG > 0){
		//printf("Contol Mode is switched \n",RED);
		OP_MODE = MODE_FLAG; 
		return OP_MODE ; 
	}
}

/*-------  SYSTEM BRAKING FUNCTION -----------*/

void system_brake(int gpio , int level, uint32_t tick, void *userdata){
	//printf("%sWARNING : %s%s \n",GREEN,YELL, *(char*) userdata);
	if (level == 1) {
		
		 printf("%sWARNING : %s%s \n",GREEN,YELL, userdata);
		 system_safe_lock();
	}

}

/*-------- function to init Dome Control System ---------*/

void system_init(){
	if( gpioInitialise() < 0 ){
		
		log_error("ERROR Initializing GPIO"); 
	}
	// setting GPIO MODES 
	gpioSetMode(DOOR_INV, PI_OUTPUT);
	gpioSetMode(DOME_INV, PI_OUTPUT);
	gpioSetMode(AIR_PUMB, PI_OUTPUT);
	gpioSetMode(DOOR_INV_ON, PI_OUTPUT);
	gpioSetMode(DOOR_INV_REV, PI_OUTPUT);
	gpioSetMode(DOME_INV_ON, PI_OUTPUT);
	gpioSetMode(DOME_INV_REV, PI_OUTPUT);
	gpioSetMode(DOME_BRAKE, PI_OUTPUT);
	gpioSetMode(DOOR_BRAKE, PI_OUTPUT);
	gpioSetMode(SYS_BUZZER, PI_OUTPUT);


	gpioSetMode(DOOR_UP_SW, PI_INPUT);
	gpioSetMode(DOOR_DOWN_SW, PI_INPUT);
	gpioSetMode(DOME_LEFT_SW, PI_INPUT);
	gpioSetMode(DOME_RIGHT_SW, PI_INPUT);
	gpioSetMode(BRAKE_SW, PI_INPUT);
	gpioSetMode(SYS_SOS_SW, PI_INPUT);
	gpioSetMode(MODE_SW, PI_INPUT);
	gpioSetMode(SENSOR_INT, PI_INPUT);
	gpioSetMode(UP_LIMIT_SW, PI_INPUT);
	gpioSetMode(DOWN_LIMIT_SW, PI_INPUT);
	gpioSetMode(DOME_HOME_SW, PI_INPUT);
	
	gpioSetPullUpDown(DOOR_UP_SW,PI_PUD_UP);
	gpioSetPullUpDown(DOOR_DOWN_SW,PI_PUD_UP);
	gpioSetPullUpDown(DOME_LEFT_SW,PI_PUD_UP);
	gpioSetPullUpDown(DOME_RIGHT_SW,PI_PUD_UP);
	gpioSetPullUpDown(BRAKE_SW,PI_PUD_UP);
	gpioSetPullUpDown(SYS_SOS_SW,PI_PUD_UP);
	gpioSetPullUpDown(MODE_SW,PI_PUD_UP);
	gpioSetPullUpDown(SENSOR_INT,PI_PUD_UP);
	gpioSetPullUpDown(UP_LIMIT_SW,PI_PUD_UP);
	gpioSetPullUpDown(DOWN_LIMIT_SW,PI_PUD_UP);
	gpioSetPullUpDown(DOME_HOME_SW,PI_PUD_UP);
	
	// Starting System 
	printf("%s###########################################\n",GREEN); 
	printf("%s## Staring System Processes,loading .... ##\n",YELL);
	printf("%s###########################################\n\n",GREEN);
	
	gpioWrite(SYS_BUZZER ,0);
	gpioWrite(DOME_BRAKE ,0);
	gpioWrite(DOOR_BRAKE ,0); 
	gpioWrite(DOOR_INV ,0);
	gpioWrite(DOOR_INV_ON,1);
	gpioWrite(DOOR_INV_REV,1);
	printf("Door Inverter is powered %s ON \n",GREEN);
	gpioWrite(DOME_INV ,0);
	gpioWrite(DOME_INV_ON,1);
	gpioWrite(DOME_INV_REV,1);
	printf("Dome Inverter is powered %s ON \n",GREEN); 
	gpioWrite(AIR_PUMB ,0);
	printf("AIR PUMB is powered %s ON \n",GREEN);
	sleep(2); 
	gpioWrite(SYS_BUZZER,1);
	if(gpioRead(DOWN_LIMIT_SW)==0){
		printf("%sDoor Status : Closed\n\n",GREEN); 
	}
	else{
		printf("%sWARNING: %sDOOR Is Opened in Initial State !!\n\n",RED,YELL); 
	}

	if(gpioRead(DOME_HOME_SW)==0){
		printf("%sDome Status : HOME\n\n",GREEN); 
	}
	else{
		printf("%sWARNING: %sDome is not Home in Initial State !!\n\n",RED,YELL); 
	}

	if(gpioRead(MODE_SW)==0){
		printf("%sControl Mode set to %sManual\n\n",GREEN,MAG);
		OP_MODE=1; 
	}
	else{
		printf("%sControl Mode set to %sRemote\n\n",GREEN,MAG);
		OP_MODE=2; 
	}
	printf("%s### System is READY ###\n\n",MAG); 

}

/*-------- function to TO RECEIVE DATA FROM TCP SERVER------*/

void tcp_rec(int sockfd)
{
	char buff[MAX];
	int n;
	for (;;) {

		bzero(buff, sizeof(buff));
		if( read( sockfd, buff, sizeof(buff) ) > 0){

			// Put function to Move to angle with timer and  Open Door Here
			// Add Safety ISR HERE TOOOOOO !

			printf("%sFrom Server : Going to %s", buff);
			if ((strncmp(buff, "exit", 4)) == 0) {
				printf("%sDome TCP Client Exit...\n", RED);
				break;
			}
		}
	}
}

/*-------- function to init TCP SOCKET CONNECTION  ---------*/
int connect_to_ser()
{
	int sockfd, connfd;
	unsigned int  err_count = 0 ;
	struct sockaddr_in servaddr, cli;

	// socket create and varification
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd == -1) {
		log_error("TCP Connection failed... !");
	
	}
	else
		printf("%sTCP Connection created\n", GREEN);

	bzero(&servaddr, sizeof(servaddr));

	// assign IP, PORT
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = inet_addr("192.168.1.4");
	servaddr.sin_port = htons(PORT);

	// connect the client socket to server socket
	server_connect:

	if ( connect(sockfd, (SA*)&servaddr, sizeof(servaddr) ) != 0) {
		printf("%sConnecting to Server Faild, Tring again...\n", RED);
		err_count= err_count + 1 ;
		sleep(1); 
 
		if( err_count == 5){
			printf("%sFATAL ERROR: %sConnection Failed, Check Network Connection ",RED,YELL);
			log_error("System EXIT with TCP Failer, Restart DOME SYSTEM ! ");
		}
		goto server_connect;
	}
	else
		printf("%sconnected to the server..\n", GREEN);

	// function for chat
	tcp_rec(sockfd);

	// close the socket
	close(sockfd);
}
