/*  Arduino DC Motor Control - PWM | H-Bridge | L298N */

#define enA 9
#define inA1 6
#define inA2 7
#define button 4

int rotDirection = 0;
int pressed = false;

class Motor
{
  int en;
  int in1;
  int in2;

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
    input1 = in1;
    input2 = in2;
    pinMode(enA, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(button, INPUT);
    // Set initial rotation direction
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  };

  void forward(float vel, float t)
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

  void stopMotor()
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

  pinMode(enA, OUTPUT);
  pinMode(inA1, OUTPUT);
  pinMode(inA2, OUTPUT);
  // pinMode(button, INPUT);
  // Set initial rotation direction
  digitalWrite(inA1, LOW);
  digitalWrite(inA2, LOW);
}

void loop()
{
  // Read potentiometer value
  // int potValue = analogRead(A0);
  // Map the potentiometer value from 0 to 255
  // int pwmOutput = map(potValue, 0, 1023, 0, 255);
  // Send PWM signal to L298N Enable pin
  analogWrite(enA, 255);

  // Read button - Debounce
  // if (digitalRead(button) == true)
  // {
  //   pressed = !pressed;
  // }
  // while (digitalRead(button) == true)
  //   ;
  // delay(20);

  // If button is pressed - change rotation direction
  // if (pressed == true & rotDirection == 0)
  // {
  digitalWrite(inA1, HIGH);
  digitalWrite(inA2, LOW);
  delay(20);
  // }
  // If button is pressed - change rotation direction
  // if (pressed == false & rotDirection == 1)
  // {
  //   digitalWrite(in1, LOW);
  //   digitalWrite(in2, HIGH);
  //   rotDirection = 0;
  //   delay(20);
  // }

  // I2C Comunication
  if (count % 10 == 0)
  {
    Serial.println("Hello, Serial communication works");
  }
  else
  {
    Serial.println(count);
  }
  count++;
}
