class MySolution {
private:
    int a;
    int b;
public:
    MySolution(int a, int b) {
        this->a = a;
        this->b = b;
    }
    int add(int a, int b) {
        return a + b;
    }
    int subtract(int a, int b) {
        return a - b;
    }
};