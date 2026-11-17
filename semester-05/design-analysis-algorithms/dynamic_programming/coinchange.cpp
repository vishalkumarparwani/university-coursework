#include <iostream>
#include <cassert>
using namespace std;

int coin_change_ways(const int coins[], int n, int amount) {
    long ways[101] = {0};
    ways[0] = 1;

    for (int i = 0; i < n; ++i) {
        for (int j = coins[i]; j <= amount; ++j) {
            ways[j] += ways[j - coins[i]];
        }
        for (int j = 0; j <= amount; ++j) {
            cout << ways[j] << "  ";
        }
        cout << endl;
    }

    return ways[amount];
}

int main() {
    int S[] = {1, 5, 6, 8};
    int result = coin_change_ways(S, 4, 13);
    cout << "Number of ways to make change for 13: " << result << endl;

    return 0;
}