#include <iostream>
#include <string>
#include <cassert>
using namespace std;

int editDistance(const string& s1, const string& s2) {
    return 0;
}

int main() {
    int result = editDistance("KITTEN", "SITTING");
    cout << result << endl;
    assert(result == 3);
    return 0;
}