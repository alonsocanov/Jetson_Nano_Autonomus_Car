/*  Arduino DC Motor Control - PWM | H-Bridge | L298N */
#include "motor.hpp"

// left motor
#define enA 9
#define inA1 6
#define inA2 7

// right motor
#define enB 10
#define inB1 12
#define inB2 11

Motor motor_l = Motor(enA, inA1, inA2);
Motor motor_r = Motor(enB, inB1, inB2);

void setup()
{
    //I2C COmunication
    // initialize serial:
    Serial.begin(9600);
    Serial.println('Motor Control')
}

void loop()
{
    if (Serial.available())
    {
        char c = Serial.read();
        if (c == '*')
        {
            Serial.print("Captured String is :");
            Serial.println(data);
            // Clear data
            data = "";
        }
        else
        {
            data += c;
        }
    }

    // motor_l.forward(100);
    // motor_r.forward(100);
    // delay(900);

    // motor_l.stop();
    // motor_r.stop();
    // delay(900);

    // motor_l.backward(100);
    // motor_r.backward(100);
    // delay(900);
}
