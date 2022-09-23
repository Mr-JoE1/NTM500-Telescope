/*
 * etne_sample.c
 *
 * Copyright (c) 1997-2021 ETEL SA. All Rights Reserved.
 *
 * This software is the confidential and proprietary information of ETEL SA
 * ("Confidential Information"). You shall not disclose such Confidential
 * Information and shall use it only in accordance with the terms of the
 * license agreement you entered into with ETEL.
 *
 * This software is provided "AS IS" without a warranty or representations of any kind.
 * ALL EXPRESS OR IMPLIED CONDITIONS, REPRESENTATIONS AND WARRANTIES, INCLUDING ANY IMPLIED WARRANTY
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT ARE HEREBY EXCLUDED. ETEL AND ITS
 * LICENSORS SHALL NOT BE LIABLE FOR ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
 * THE SOFTWARE OR ITS DERIVATIVES. IN NO EVENT WILL ETEL OR ITS LICENSORS BE LIABLE FOR ANY LOST REVENUE, PROFIT OR
 * DATA, OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE DAMAGES, HOWEVER CAUSED AND REGARDLESS
 * OF THE THEORY OF LIABILITY, ARISING OUT OF THE USE OF OR INABILITY TO USE SOFTWARE, EVEN IF ETEL HAS BEEN ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGES. THE ENTIRE RISK ARISING OUT OF USE, PERFORMANCE OR NON-PERFORMANCE OF THE SOFTWARE
 * REMAINS WITH THE LICENSEE. IF ETEL SHOULD NEVERTHELESS BE FOUND LIABLE, WHETER DIRECTLY OR INDRECTLY, FOR ANY LOSS,
 * DAMAGE OR INJURY ARISING UNDER THIS AGREEMENT OR OTHERWISE, REGARDLESS OF CAUSE OR ORIGIN, ON ANY BASIS WHATSOEVER,
 * ITS TOTAL MAXIMUM LIABILITY IS LIMITED TO CHF 100.000 WHICH WILL BE THE COMPLETE AND EXCLUSIVE REMEDY AGAINST ETEL.

 * This software is in particular not designed or intended .for use in on-line control of aircraft, air traffic, aircraft
 * navigation or aircraft communications; or in the design, construction, Operation or maintenance of any nuclear facility.
 * Licensee represents and warrants that it will not use or redistribute the Software for such purposes.
 */

/***************************************************************************************
 * This software is an example which show the way to implement the following things:
 *		1)	The way to open several connection on an UltimET PCI using ETNE server
 *		2)	How to use the new DSA_EXT_DIAG for extended diagnostic in case of error
 *
 *	Remark: The EDI package must be greater or equal to 4.00A !!!

***************************************************************************************/

#include <Windows.h>
#include <conio.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

#include "dsa40.h"
#include "etne40.h"


// SOME MARCOS DEFINITIONS 
// enmuarating axes numbersU
#define AXIS_NB_X 0
#define AXIS_NB_Y 1

// TEST CONFIG 

//note: all etel errors codes are negative values
int err = 1;						 // means no errors

int main(int argc, char* argv[]) {

	DSA_DRIVE* axisX = NULL;
	DSA_DRIVE* axisY = NULL;


	/* Create the drive and UltimET objects. */
	if (err = dsa_create_drive(&axisX)) {
		DSA_DIAG(err, axisX);
		goto _error;
	}
	if (err = dsa_create_drive(&axisY)) {
		DSA_DIAG(err, axisY);
		goto _error;
	}
	/*
	 * Establish communcation to the  postion driver Driver 
	 * Refer to EDI maunual page 32
	 * example:
	 *		err = dsa_open_u(axisX, "etb:usb:0");
	 */
	if (err = dsa_open_u(axisX, "etb:USB:0")) { /* Motor axis X is on drive number 0 */
		DSA_DIAG(err, axisX);
		printf("frist conn failed \n");
		goto _error;
	}
	printf("frist conn done \n");
	if (err = dsa_open_u(axisY, "etb:USB:1")) { /* Motor axis Y is on drive number 0 */
		DSA_DIAG(err, axisY);
		goto _error;
	}
	/*
	 * Driver Powering on , PDF page :33
	 * powering each axis indevidually
	 * power on timout set to 10 secounds before returning error 
	 */

	if (err = dsa_power_on_s(axisX, 10000)) {
		DSA_DIAG(err, axisX);
		goto _error;
	}
	if (err = dsa_power_on_s(axisY, 10000)) {
		DSA_DIAG(err, axisY);
		goto _error;
	}
	_error:
	/* Print the first error that occured. */
		printf("error code  =  (%d)\n", err);
}