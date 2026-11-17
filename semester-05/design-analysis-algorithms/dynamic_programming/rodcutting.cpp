#include <iostream>
#include <cassert>
using namespace std;

int rodCutting(const int price[], int n) {
    return 0;
}

int main() {
    int price[] = {1, 5, 8, 9, 17, 10, 16, 18, 20};
    int result = rodCutting(price, 8);
    cout << result << endl;
    assert(result == 21);

    return 0;
}