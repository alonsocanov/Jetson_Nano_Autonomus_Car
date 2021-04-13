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

String data;
String test;

int ind1;
float val_1;
char av = 'a';

Motor motor_l = Motor(enA, inA1, inA2);
Motor motor_r = Motor(enB, inB1, inB2);

void setup()
{
    //I2C COmunication
    // initialize serial:
    Serial.begin(9600);

    motor_l.stop();
    motor_r.stop();
}

void loop()
{
    if (Serial.available())
    {
<<<<<<< Updated upstream

        data = Serial.readStringUntil('\n');
        Serial.print("Arduino: ");

        Serial.println(data);
        //finds location of first comma (,)
        ind1 = data.indexOf(',');
        test = data.substring(0, ind1);
        val_1 = test.toFloat();

        if (val_1 == 10.0)
        {
            motor_l.forward(100);
            motor_r.forward(100);
            delay(900)
        }
    }
    else
    {
        motor_l.stop();
        motor_r.stop();
    }

    // motor_l.backward(100);
    // motor_r.backward(100);
    // delay(900);
}
