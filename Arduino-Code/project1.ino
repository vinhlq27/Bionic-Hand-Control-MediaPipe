#include <Servo.h>
#define numOfValsRec 5
#define digitsPerValRec 1

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; // $00000
int counter = 0;
bool counterStart = false;
String recString;


void setup() 
{
  Serial.begin(9600);
  servoThumb.attach(7);     // 7 is the port number in Arduino board for the thumb servo
  servoIndex.attach(9);     // 9 is the port number in Arduino board for the index servo
  servoMiddle.attach(11);   // 11 is the port number in Arduino board for the middle servo
  servoRing.attach(8);      // 8 is the port number in Arduino board for the ring servo
  servoPinky.attach(10);    // 10 is the port number in Arduino board for the pinky servo

}

void recData() 
{
  while(Serial.available())
  {
    char c = Serial.read();

    if(c =='$')
    {
      counterStart = true;
    }
    if(counterStart)
    {
      if(counter < stringLength)
      {
        recString = String(recString + c);
        counter++;
      }
      if(counter >= stringLength)
      {
        for(int i = 0; i < numOfValsRec; i++)
        {
          int num = (i*digitsPerValRec)+1;
          valsRec[i] = recString.substring(num,num + digitsPerValRec).toInt();
        }
        recString = "";
        counter = 0;
        counterStart = false;
      }
    }
  }
}

void loop() {
  recData();
  if (valsRec[0] == 1) {servoThumb.write(0);} else {servoThumb.write(180);}
  if (valsRec[1] == 1) {servoIndex.write(0);} else {servoIndex.write(180);}
  if (valsRec[2] == 1) {servoMiddle.write(0);} else {servoMiddle.write(180);}
  if (valsRec[3] == 1) {servoRing.write(0);} else {servoRing.write(180);}
  if (valsRec[4] == 1) {servoPinky.write(0);} else {servoPinky.write(180);}  
}
