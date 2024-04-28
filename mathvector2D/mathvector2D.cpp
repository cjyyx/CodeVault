#include <iostream>
using namespace std;

class MathVector
{
private:
    /* data */
public:
    double x;
    double y;
    MathVector(double x, double y)
    {
        this->x = x;
        this->y = y;
    }
    MathVector operator+(const MathVector &v)
    {
        MathVector v_result(this->x + v.x, this->y + v.y);
        return v_result;
    }
    MathVector operator-(const MathVector &v)
    {
        MathVector v_result(this->x - v.x, this->y - v.y);
        return v_result;
    }
    MathVector operator*(const MathVector &v)
    {
        MathVector v_result(this->x * v.x, this->y * v.y);
        return v_result;
    }
};

double norm(MathVector v)
{
    double result;
}

int main(int argc, char const *argv[])
{

    MathVector v1(1, 2);
    MathVector v2(2, 1);
    MathVector v3 = v1 * v2;
    cout << v3.x << "\n"
         << v3.y << endl;
    return 0;
}
