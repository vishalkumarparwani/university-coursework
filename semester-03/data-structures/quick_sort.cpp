#include <iostream>
using namespace std;

int comparisons = 0;

void quickSort(int a[], int low, int high, bool bestCase) {
    if (low >= high)
        return;

    if (bestCase) {
        int mid = (low + high) / 2;
        int t = a[low];
        a[low] = a[mid];
        a[mid] = t;
    }

    int pivot = a[low];
    int i = low;
    int j = high;

    while (i < j) {
        while (a[i] <= pivot && i < high) {
            comparisons++;
            i++;
        }
        comparisons++;

        while (a[j] > pivot) {
            comparisons++;
            j--;
        }
        comparisons++;

        if (i < j) {
            int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }
    }

    int temp = a[low];
    a[low] = a[j];
    a[j] = temp;

    quickSort(a, low, j - 1, bestCase);
    quickSort(a, j + 1, high, bestCase);
}

bool isSorted(int a[], int n) {
    for (int i = 1; i < n; i++) {
        if (a[i] < a[i - 1])
            return false;
    }
    return true;
}

int main() {
    int n;
    cout << "Enter array size (minimum 10): ";
    cin >> n;
    while (n < 10 || n > 1000) {
        cout << "Enter a size between 10 and 1000: ";
        cin >> n;
    }

    int a[1000], b[1000];
    for (int i = 0; i < n; i++) {
        a[i] = i + 1;
        b[i] = i + 1;
    }

    comparisons = 0;
    quickSort(a, 0, n - 1, false);
    cout << "\nWorst Case Comparisons: " << comparisons << endl;
    cout << "Array sorted: " << (isSorted(a, n) ? "Yes" : "No") << endl;

    comparisons = 0;
    quickSort(b, 0, n - 1, true);
    cout << "\nBest Case Comparisons: " << comparisons << endl;
    cout << "Array sorted: " << (isSorted(b, n) ? "Yes" : "No") << endl;

    return 0;
}