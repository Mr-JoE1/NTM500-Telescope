#ifndef DOMECONTROL_H_
#define DOMECONTROL_H_

#include <stdio.h>
#include <pigpio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h>

// needed for TCP functions 
#define MAX 80
#define PORT 10080
#define SA struct sockaddr

// define all gpio pins names
// ALL OUPUTS CONNECTED TO RELAY/SSR MODULES 3.3V:24V  
#define  DOOR_INV 2
#define  DOME_INV 3
#define  AIR_PUMB 4
#define  DOOR_INV_ON 17
#define  DOOR_INV_REV 27
#define  DOME_INV_ON  22
#define  DOME_INV_REV 10
#define  DOME_BRAKE 26
#define  DOOR_BRAKE 19
#define  SYS_BUZZER 5

// ALL INPUTS CONNECTED TO ISOLATED OPT MODULE 24:3.3 --- PULLUD UP 
#define DOOR_UP_SW 14
#define DOOR_DOWN_SW 15
#define DOME_LEFT_SW 18
#define DOME_RIGHT_SW 23
#define BRAKE_SW 24    // ASSIGNED TO ISR FUNC 
#define SYS_SOS_SW 25  // ASSIGNED TO ISR FUNC 
#define MODE_SW 8
#define SENSOR_INT 7   // ASSIGNED TO ISR FUNC 
#define UP_LIMIT_SW 12
#define DOWN_LIMIT_SW 16
#define DOME_HOME_SW 20
#define DOOR_MID_SW 21

// Define some colors marcos 
#define RED "\033[1;31m"  //bold red color
#define BLUE "\033[1;34m"  //bold BLUE color
#define GREEN "\033[1;32m"  //bold red color
#define MAG "\033[1;35m"  //bold red color
#define YELL "\033[1;33m"  //bold yellow color

extern unsigned int OP_MODE; 
extern unsigned int SAFE_LOCK; 

const char* timestamp(); 
void log_error(const char* err);
unsigned int system_safe_lock(); 
unsigned int check_mode();
void system_brake(int gpio , int level, uint32_t tick, void *userdata); 
void system_init();
void tcp_rec(int sockfd);
int connect_to_ser(); 


#endif
