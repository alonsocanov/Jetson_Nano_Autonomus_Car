// #ifndef MOTOR_HPP
// #define MOTOR_HPP

class Motor
{
    byte en;
    byte in1;
    byte in2;

private:
    int velocity(float value, float lim_max = 100, float lim_min = -100)
    {
        if (value > lim_max)
        {
            value = lim_max;
        }
        else if (value < lim_min)
        {
            value = lim_min;
        }

        // Map the potentiometer value from 0 to 255 from percentaje o to 100
        int pwmOutput = map(abs(value), 0, 100, 0, 255);
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

    void move(float vel)
    {
        int pwm = velocity(vel);
        analogWrite(en, pwm);
        if (vel < 0)
        {
            digitalWrite(in1, HIGH);
            digitalWrite(in2, LOW);
        }
        else
        {
            digitalWrite(in1, LOW);
            digitalWrite(in2, HIGH);
        }
    };

    // void backward(float vel)
    // {
    //     int pwm = velocity(vel);
    //     analogWrite(en, pwm);
    //
    // };

    void stop()
    {
        analogWrite(en, LOW);
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
    };
};

// #endif