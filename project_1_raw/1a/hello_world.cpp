#include <iostream>
#include <unistd.h>
#include <limits.h>

int main()
{
    std::cout << "Hello, World!" << std::endl;
    // print host
    char hostname[HOST_NAME_MAX];
    gethostname(hostname, HOST_NAME_MAX);
    std::cout << "Host: " << hostname << std::endl;
    return 0;
}
