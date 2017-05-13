#include<stdio.h>

struct test
{
	unsigned int I;
	float f;
	char *c;
	unsigned long L;
};


int run1(struct test t1)
{
	printf("I:%d\tf:%f\tc:%s\tL:%ld\t\n",t1.I,t1.f,t1.c,t1.L);

return 0;
}

int run2(struct test *t1)
{
	printf("I:%d\tf:%f\tc:%s\tL:%ld\t\n",t1->I,t1->f,t1->c,t1->L);
	t1->f=5.5;
return 0;
}
