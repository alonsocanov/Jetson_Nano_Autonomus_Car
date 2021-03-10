/*  Arduino DC Motor Control - PWM | H-Bridge | L298N */

#define enA 9
#define inA1 6
#define inA2 7
#define button 4

int rotDirection = 0;
int pressed = false;

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
        pinMode(enA, OUTPUT);
        pinMode(in1, OUTPUT);
        pinMode(in2, OUTPUT);
        pinMode(button, INPUT);
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

    void time(float t)
    {
        delay(t);
    };
};

void setup()
{
    //I2C COmunication
    // initialize serial:
    Serial.begin(9600);
}

Motor motor_l = Motor(enA, inA1, inA2);

void loop()
{

    motor_l.time(900);

    motor_l.stop();
    motor_l.time(900);

    motor_l.backward(100);
    motor_l.time(900);

    // I2C Comunication
    // if (count % 10 == 0)
    // {
    //     Serial.println("Hello, Serial communication works");
    // }
    // else
    // {
    //     Serial.println(count);
    // }
    // count++;
}
