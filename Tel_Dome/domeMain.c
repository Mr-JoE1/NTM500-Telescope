#include "domeControl.h"

//unsigned int OP_MODE = 0 ;
//unsigned int SAFE_LOCK =0 ; 



int main(){
	unsigned int current_mode = 0; 
	system_init(); 
	

	// CHECK OPERATION MODE
	while(1){	 
		
		safe_lock:
		while(SAFE_LOCK==1){
			if (gpioRead(BRAKE_SW)==0){
				printf("system brake \n");
				gpioWrite(SYS_BUZZER,0);
		 		gpioWrite(DOME_INV_ON,1);
				gpioWrite(DOME_INV_REV,1);
		 		gpioWrite(DOOR_INV_ON,1);
		 		gpioWrite(DOOR_INV_REV,1);
		 		gpioWrite(DOME_BRAKE,0);
				gpioWrite(DOOR_BRAKE,0);
		 		
				//sleep(0.5);
				gpioWrite(SYS_BUZZER,1);
				//sleep(0.25);
			}
			else if(gpioRead(SYS_SOS_SW)==0 || gpioRead(SENSOR_INT) == 0){
				printf("--------- safe stop \n");
				gpioWrite(SYS_BUZZER,0);
		 		gpioWrite(DOME_INV_ON,1);
		 		gpioWrite(DOME_INV_REV,1);
		 		gpioWrite(DOOR_INV_ON,1);
		 		gpioWrite(DOOR_INV_REV,1);
		 		gpioWrite(DOME_BRAKE,0);
		 		gpioWrite(DOOR_BRAKE,0);
				sleep(0.5);
				gpioWrite(SYS_BUZZER,1);
				sleep(0.2);

			}
			else SAFE_LOCK = 0; 
		}


		//MANUAL MODE ROUTINES

		while(OP_MODE==1){
 
			current_mode = 1; 
			if(gpioRead(DOOR_UP_SW)==0)
			{	//printf("door opening\n");
				gpioWrite(DOOR_INV_ON,0);
				sleep(2);
				gpioWrite(DOOR_BRAKE,1);
			} 
			else if(gpioRead(DOOR_DOWN_SW)==0){
				gpioWrite(DOOR_INV_ON,0);
				gpioWrite(DOOR_INV_REV,0);
				sleep(2);
				gpioWrite(DOOR_BRAKE,1);
			}
			else{
				gpioWrite(DOOR_INV_ON,1);
				gpioWrite(DOOR_INV_REV,1);
				gpioWrite(DOOR_BRAKE,0);
			}


			if(gpioRead(DOME_RIGHT_SW)==0){
				gpioWrite(DOME_INV_ON,0);
				gpioWrite(DOME_BRAKE,1);
			}
			else if(gpioRead(DOME_LEFT_SW)==0){

				gpioWrite(DOME_BRAKE,1);
				gpioWrite(DOME_INV_ON,0);
				gpioWrite(DOME_INV_REV,0);
			}
			else{
				gpioWrite(DOME_BRAKE,0);
				gpioWrite(DOME_INV_ON,1);
				gpioWrite(DOME_INV_REV,1);
			}
			//gpioSetISRFuncEx(SYS_SOS_SW,FALLING_EDGE, 500, system_brake,"System Emrgency Stop By User , Release Emergency Switch !");
			//gpioSetISRFuncEx(SENSOR_INT,FALLING_EDGE, 500, system_brake,"Something in Door way, Safety System Lock !!!!");
			//gpioSetISRFuncEx(BRAKE_SW,FALLING_EDGE, 500, system_brake,"System Mechanical Braking Enabled");
			//if(current_mode != check_mode()) break;
			//if(system_safe_lock() == 1) goto safe_lock; 
		}

		while(OP_MODE==2){

			current_mode = 2 ;
			//STARTING TCP COMMUNICATION
			//connect_to_ser();
			gpioSetISRFuncEx(SYS_SOS_SW,FALLING_EDGE, 500, system_brake,"System Emrgency Stop By User , Release Emergency Switch !");
			gpioSetISRFuncEx(SENSOR_INT,FALLING_EDGE, 500, system_brake,"Something in Door way, Safety System Lock !!!!");
			gpioSetISRFuncEx(BRAKE_SW,FALLING_EDGE, 500, system_brake,"System Mechanical Braking Enabled");
			if(current_mode != check_mode()) break;
			if(system_safe_lock() == 1) goto safe_lock;
	
		}





	}
	gpioTerminate(); 
	return 0; 


}
