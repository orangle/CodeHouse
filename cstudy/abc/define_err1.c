/*理解define 宏定义中的一个错误
 *在预处理阶段，宏是怎样替换代码块中的内容的
 * N:   a= 2+2*2+2
 * M:   b= (2+2)*(2+2)
 * 使用宏定义的原则：先替换在计算
 * */

#define N 2+2
#define M (2+2)

void main(){
    int a = N*N;
    int b = M*M;
    printf("N 2+2,  N*N=%d \n", a);
    printf("M (2+2), M*M=%d \n", b);
}
