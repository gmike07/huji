#ifndef GPS_H
#define GPS_H

#include "minmea.h"

void initGPS();

void deInitGPS();

void getGPS(struct minmea_sentence_gga* gga, char* gga_msg);

#endif  // GPS_H
