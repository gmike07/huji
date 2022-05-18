#ifndef EX4_CELLULAR_PARSE_PHYSICAL_H
#define EX4_CELLULAR_PARSE_PHYSICAL_H

int ParseICCID(unsigned char *buf, char *iccid, int maxlen);

int ParseIMEI(unsigned char *buf, char *imei, int maxlen);

int ParseSignalQuality(unsigned char *buf, int *signal);

#endif //EX4_CELLULAR_PARSE_PHYSICAL_H
