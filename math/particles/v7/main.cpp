#include <stdlib.h>
#include <stdio.h>
#include <time.h>


using namespace std;

float randomNum(float max) {
    int r = rand();
    int mod = max * 100;
    float n = r % mod;
    return n / 100;
} 

float randomCoef() {
    float n = randomNum(3);
    float choices[4] = { n, -1*n, 0, 0 };
    int r = rand();
    int idx = r % 4;
    return choices[idx];
}

float delta(float coefs[10], float x, float y, float z) {
    return coefs[0] * x * x 
        + coefs[1] * y * y 
        + coefs[2] * z * z 
        + coefs[3] * x * y 
        + coefs[4] * y * z 
        + coefs[5] * x * z 
        + coefs[6] * x 
        + coefs[7] * y 
        + coefs[8] * z 
        + coefs[9];
}

int main(int argc, char *argv[]) {
    int particles = 3;
    int dt = 1;
    int t = 2;
    float states[particles][t*dt+dt][3];

    srand(time(NULL));

    // generate coefficients
    float xcoefs[10];
    float ycoefs[10];
    float zcoefs[10];
    for (int i=0; i<10; i++) {
        xcoefs[i] = randomCoef();
        ycoefs[i] = randomCoef();
        zcoefs[i] = randomCoef();
    }

    // initialize states
    for (int i=0; i<particles; i++) {
        float x0 = randomNum(1.5);
        float y0 = randomNum(1.5);
        float z0 = randomNum(1.5);
        float x1 = delta(xcoefs, x0, y0, z0);
        float y1 = delta(ycoefs, x0, y0, z0);
        float z1 = delta(zcoefs, x0, y0, z0);

        float dx = (x1 - x0) / dt;
        float dy = (y1 - y0) / dt;
        float dz = (z1 - z0) / dt;

        for (int j=0; j<dt; j++) {
            states[i][j][0] = x0 + j * dx;
            states[i][j][1] = y0 + j * dy;
            states[i][j][2] = z0 + j * dz;
        }
    }

    for (int j=dt; j<t*dt+dt; j++) {
        for (int i=0; i<particles; i++) {
            float x = states[i][j-dt][0];
            float y = states[i][j-dt][1];
            float z = states[i][j-dt][2];
            states[i][j][0] = delta(xcoefs, x, y, z);
            states[i][j][1] = delta(ycoefs, x, y, z);
            states[i][j][2] = delta(zcoefs, x, y, z);
        }
    }


    for (int i=0; i<particles; i++) {
        printf("vvvvvvvvvvvvvvvvv\n");
        for (int j=0; j<t*dt+dt; j++) {
            float x = states[i][j][0];
            float y = states[i][j][1];
            float z = states[i][j][2];
            printf("%.2f %.2f %.2f\n", x, y, z);
        }
        printf("^^^^^^^^^^^^^^^^^\n");
    }


    return 0;
}