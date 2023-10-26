#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>

using namespace std;

const char *ltmPath = "vis.ltm";

#pragma clang diagnostic push
#pragma ide diagnostic ignored "bugprone-sizeof-container"
#pragma ide diagnostic ignored "cppcoreguidelines-narrowing-conversions"
#pragma ide diagnostic ignored "ConstantFunctionResult"

unsigned long long write() {
    map<uint8_t, map<uint8_t, map<uint8_t, uint32_t>>> ltm;
    ltm[0][0][0] = 66;
    ltm[255][255][255] = 99;
    ofstream f(ltmPath, ios::binary);
    unsigned long long size = sizeof(ltm);
    f.write((char *) &ltm, size);
    f.close();
    return size;
}

map<uint8_t, map<uint8_t, map<uint8_t, uint32_t>>> read(unsigned long long size) {
    map<uint8_t, map<uint8_t, map<uint8_t, uint32_t>>> ltm;
    ifstream f(ltmPath, ios::binary);
    f.read((char *) &ltm, size);
    f.close();
    return ltm;
}

#pragma clang diagnostic pop

int main() {
    auto ltm = read(write());
    cout << ltm[0][0][0] << " - " << ltm[255][255][255] << endl; // std::cout , std::endl
    return 0;
}
