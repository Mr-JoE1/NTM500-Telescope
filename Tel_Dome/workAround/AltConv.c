#include <stdio.h>
#include <stdlib.h>
#include<math.h>

int Conversion ()
{
double 	DEC_degree;
double  HA_degree;
double  LAT_degree;
double  ALT_degree;
double 	A_degree;


printf("Enter DEC value in degree : ");
printf("Enter HA value in degree : ");
printf("Enter LAT value in degree : ");

scanf("%f",&DEC_degree);
scanf("%f",&HA_degree);
scanf("%f",&LAT_degree);

/*double DEC_radian = DEC_degree * (M_PI/180);
double HA_radian = HA_degree * (M_PI/180);*/

double S_HA = sin(HA_degree);
double S_DEC = sin(DEC_degree);
double S_LAT = sin(LAT_degree);

double C_HA = cos(HA_degree);
double C_DEC = cos(DEC_degree);
double C_LAT = cos(LAT_degree);
double S_ALT ;// =sin(ALT_degree);
S_ALT =((S_DEC*S_LAT)+(C_DEC*C_LAT*C_HA));
ALT_degree=asin(S_ALT);
double C_ALT = cos(ALT_degree);
double C_A = ((S_DEC -(S_ALT*S_LAT))/(C_ALT*C_LAT));
A_degree=asin(C_A);
double AZ_degree =360-A_degree;
printf("AZ_degree value is %f \n",AZ_degree);
printf("ALT_degree value is %f \n",ALT_degree);

double AZ_radian  = AZ_degree * (M_PI/180);
double ALT_radian = ALT_degree * (M_PI/180);

printf("AZ_radian  value is %f \n",AZ_radian );
printf("ALT_radian  value is %f \n",ALT_radian);
return 0;
}

int main()
{
	/* code */
	Conversion();
	return 0;
}