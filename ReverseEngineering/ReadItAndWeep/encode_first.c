#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void encode_first(long param_1)
{
    char bVar1;
    void *__s;
    unsigned int local_14;

    __s = malloc(0x10);
    memset(__s, 0, 0x10);
    local_14 = 0;
    while (local_14 < 0x10)
    {
        bVar1 = *(char *)(param_1 + (unsigned long)local_14) ^ 0x17;
        *(char *)((unsigned long)local_14 + (long)__s) =
            bVar1 + (((char)((unsigned int)(unsigned short)(short)(char)bVar1 * 0x41 >> 8) >> 5) - ((char)bVar1 >> 7)) * -0x7f;
        if (*(char *)((long)__s + (unsigned long)local_14) < ' ')
        {
            *(char *)((long)__s + (unsigned long)local_14) = *(char *)((long)__s + (unsigned long)local_14) + ' ';
        }
        local_14 = local_14 + 1;
    }
    //printf("%d", local_14);
}

int main()
{
    // printf() displays the string inside quotation
    printf("Hello, World!");
    encode_first(0);
    return 0;
}
