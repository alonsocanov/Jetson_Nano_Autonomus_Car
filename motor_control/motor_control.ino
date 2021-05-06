/*  Arduino DC Motor Control - PWM | H-Bridge | L298N */
#include "motor.hpp"
#include "utils.hpp"

// left motor
#define enA 11
#define inA1 12
#define inA2 13

// right motor
#define enB 11
#define inB1 13
#define inB2 12

String data;

int ind1, ind2, ind3;
float speed, angle, y, x, time;
String speed_str, angle_str, time_str;

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

        data = Serial.readStringUntil('\n');
        //finds location of first comma (,)
        ind1 = data.indexOf(',', 0);
        ind2 = data.indexOf(',', ind1 + 1);

        speed_str = data.substring(0, ind1);
        angle_str = data.substring(ind1 + 1, ind2);
        time_str = data.substring(ind2 + 1, data.length());

        speed = check_negative(speed_str) * 100.0;
        angle = check_negative(angle_str);
        time = check_negative(time_str);

        if (angle > 0)
        {
            y = y_speed(deg_to_rad(angle)) * speed;
            motor_l.move(speed);
            motor_r.move(y);
        }
        else if (angle)
        {
            y = y_speed(deg_to_rad(angle)) * speed;
            motor_l.move(y);
            motor_r.move(speed);
        }
        else
        {
            motor_l.move(speed);
            motor_r.move(speed);
        }

        delay(time);
        Serial.println(data);
    }
    else
    {
        motor_l.stop();
        motor_r.stop();
    }
}
