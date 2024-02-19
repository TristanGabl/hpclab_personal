#include <iostream>
#include <unistd.h>
#include <limits.h>

char hostname[HOST_NAME_MAX];
char username[LOGIN_NAME_MAX];
gethostname(hostname, HOST_NAME_MAX);
getlogin_r(username, LOGIN_NAME_MAX);

int main()
{
    std::cout << "Hello, World!" << std::endl;
    // print host
    std::cout << "Host: " << hostname << std::endl;
    return 0;
}
