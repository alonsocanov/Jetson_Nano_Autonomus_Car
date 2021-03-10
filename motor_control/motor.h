class Motor
{
    byte en;
    byte in1;
    byte in2;

private:
    int velocity(float value)
    {
        // Map the potentiometer value from 0 to 255 from percentaje o to 100
        int pwmOutput = map(value, 0, 100, 0, 255);
        return pwmOutput;
    };

public:
    Motor(int enable, int input1, int input2)
    {
        en = enable;
        in1 = input1;
        in2 = input2;
        pinMode(en, OUTPUT);
        pinMode(in1, OUTPUT);
        pinMode(in2, OUTPUT);
        // Set initial rotation direction
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
    };

    void forward(float vel)
    {
        int pwm = velocity(vel);
        analogWrite(en, pwm);
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
    };

    void backward(float vel)
    {
        int pwm = velocity(vel);
        analogWrite(en, pwm);
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
    };

    void stop()
    {
        analogWrite(en, LOW);
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
    };
};