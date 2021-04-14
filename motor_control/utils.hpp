
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
