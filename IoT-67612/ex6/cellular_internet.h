#ifndef EX5_CELLULAR_INTERNET_H
#define EX5_CELLULAR_INTERNET_H

int SetupInternetConnectionProfileConnType(char *cmd_buf);

int SetupInternetConnectionProfileApn(char *cmd_buf);

int SetupInternetConnectionProfileInactTimeout(char *cmd_buf, int inact_time_sec);

int SetupInternetServiceProfileSrvType(char *cmd_buf);

int SetupInternetServiceProfileConId(char *cmd_buf);

int SetupInternetServiceProfileAddr(char *cmd_buf, char *IP, int port, int keepintvl_sec);

int OpenInternetConnection();

int CloseInternetConnection();

int WaitUntilServiceProfileIsUp();

int OpenTransparentSocket();

int ExitTransparentSocket();

#endif //EX5_CELLULAR_INTERNET_H
