// #ifndef MOTOR_HPP
// #define MOTOR_HPP

class Motor
{
    byte en;
    byte in1;
    byte in2;

private:
    int velocity(float value, float lim_max = 100.0, float lim_min = 0.0)
    {
        float abs_val = abs(value);
        if (abs_val > lim_max)
        {
            abs_val = lim_max;
        }
        else if (abs_val < lim_min)
        {
            abs_val = lim_min;
        }

        // Map the potentiometer value from 0 to 255 from 0 to 100
        int pwm = map(abs_val, 0, 100, 0, 255);
        return pwm;
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
    }

    void move(float vel)
    {
        int pwm = velocity(vel);

        if (vel < 0)
        {
            analogWrite(en, pwm);
            digitalWrite(in1, HIGH);
            digitalWrite(in2, LOW);
        }
        else if (vel > 0)
        {
            analogWrite(en, pwm);
            digitalWrite(in1, LOW);
            digitalWrite(in2, HIGH);
        }
        else
        {
            analogWrite(en, LOW);
            digitalWrite(in1, LOW);
            digitalWrite(in2, LOW);
        }
    };

    void stop()
    {
        analogWrite(en, LOW);
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
    };
};

// #endif