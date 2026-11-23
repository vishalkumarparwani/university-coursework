
#include <iostream>
using namespace std;

void quickSort(int a[], int low, int high) {
    if (low >= high)
        return;

    int pivot = a[low];

    int i = low;
    int j = high;

    while (i < j) {

        while (a[i] <= pivot && i < high)
            i++;

        while (a[j] > pivot)
            j--;

        if (i < j) {
            int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }
    }

    int temp = a[low];
    a[low] = a[j];
    a[j] = temp;

    quickSort(a, low, j - 1);
    quickSort(a, j + 1, high);
}

int main() {
    int a[] = {8, 3, 1, 7, 0, 10, 2};

    int n = 7;

    quickSort(a, 0, n - 1);

    cout << "Sorted array: ";

    for (int i = 0; i < n; i++)
        cout << a[i] << " ";

    return 0;
}
