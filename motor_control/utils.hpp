#define PI 3.1415926535897932384626433832795
#define HALF_PI 1.5707963267948966192313216916398
#define TWO_PI 6.283185307179586476925286766559
#define DEG_TO_RAD 0.017453292519943295769236907684886
#define RAD_TO_DEG 57.295779513082320876798154814105

float check_negative(String str)
{
    float value;
    if (str[0] == '-')
    {
        value = str.substring(1, str.length()).toFloat() * -1;
    }
    else
    {
        value = str.toFloat();
    }

    return value;
}

float deg_to_rad(float value)
{
    float rad;
    rad = value * DEG_TO_RAD;
    return rad;
}

float y_speed(float value)
{
    float speed;
    speed = cos(value);

    return speed;
}

float x_speed(float value)
{
    float speed;
    speed = sin(value);

    return speed;
}