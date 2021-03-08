/*  Arduino DC Motor Control - PWM | H-Bridge | L298N  -  Example 01

    by Dejan Nedelkovski, www.HowToMechatronics.com
*/

#define enA 9
#define inA1 6
#define inA2 7
#define button 4


int rotDirection = 0;
int pressed = false;

class Motor{
  int en;
  int in1;
  int in2;

  private:
    int velocity(float value){
    // Map the potentiometer value from 0 to 255
    int pwmOutput = map(value, 0, 1023, 0 , 255);
    return pwmOutput
    }
  
  public:
    Motor(int enable, int input1, int, input2){
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

    void forward(float vel, float t){
      int pwm = velocity(vel)
      analogWrite(en, pwm);
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      delay(t);  
    };

    void backward(float vel, float t){
      int pwm = velocity(vel)
      analogWrite(en, pwm);
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      delay(t);  
    };

    void stopMotor(float t){
      analogWrite(en, LOW);
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
      delay(t);
    };
  
  
};

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(button, INPUT);
  // Set initial rotation direction
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
}

void loop() {
  // Read potentiometer value
  int potValue = analogRead(A0);
  // Map the potentiometer value from 0 to 255
  int pwmOutput = map(potValue, 0, 1023, 0 , 255);
  // Send PWM signal to L298N Enable pin 
  analogWrite(enA, pwmOutput); 

  // Read button - Debounce
  if (digitalRead(button) == true) {
    pressed = !pressed;
  }
  while (digitalRead(button) == true);
  delay(20);

  // If button is pressed - change rotation direction
  if (pressed == true  & rotDirection == 0) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    rotDirection = 1;
    delay(20);
  }
  // If button is pressed - change rotation direction
  if (pressed == false & rotDirection == 1) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    rotDirection = 0;
    delay(20);
  }
}
