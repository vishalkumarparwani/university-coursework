#include <stdio.h>
using namespace std;

int cross(int ax, int ay, int bx, int by, int cx, int cy) {
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax);
}

int main() {
    int result = cross(0, 0, 1, 0, 0, 1);
    printf("Cross product: %d\n", result);

    if (result > 0) {
        printf("Counter-clockwise\n");
    } else if (result < 0) {
        printf("Clockwise\n");
    } else {
        printf("Collinear\n");
    }
    
    return 0;
}