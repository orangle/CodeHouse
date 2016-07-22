/*结构体
 *
 */

#include<stdio.h>

void main(void){
    struct num {
        double x, y;
    } z;

    double x = 3.0;
    z.x = x;
    z.y = 4;
    if (z.y < 0){
        printf("z=%f%fi\n", z.x, z.y);
    }else{
        printf("z=%f+%fi\n", z.x, z.y);
    }
    return ;
}
