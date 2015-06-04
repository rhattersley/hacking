#include <stdio.h>
#include <stdlib.h>

#include <string.h>

#define NXY 1100000
#define NZ 70
#define NRZ 30
#define NT 3

void work(float *x, float *fx, float *rfx)
{
    size_t z;
    size_t x_stride = sizeof(float) * NXY;
    printf("Stride: %ld\n", x_stride);
    float dummy;

    for(z=0; z<NZ; z++) {
        printf("z: %ld\n", z);
        printf("z*: %ld\n", z * x_stride);
        dummy = x[z * x_stride];
    }
}

int main() {
    float *x = malloc(sizeof(float) * NT * NZ * NXY);
    float *fx = malloc(sizeof(float) * NT * NZ * NXY);
    float *rx = malloc(sizeof(float) * NRZ);
    float *rfx = malloc(sizeof(float) * NT * NRZ * NXY);
    int xy;

    if (1) {
        memset(x, 0,sizeof(float) * NT * NZ * NXY);
        memset(fx, 0,sizeof(float) * NT * NZ * NXY);
        memset(rx, 0,sizeof(float) * NRZ);
        memset(rfx, 0,sizeof(float) * NT * NRZ * NXY);
    }

    for(xy=0; xy<NXY; xy++) {
        work(x, fx + xy, rfx + xy);
        break;
    }
}
