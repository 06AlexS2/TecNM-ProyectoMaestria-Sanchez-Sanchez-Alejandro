#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
//#include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library. 

//inicializar pin analogico del pulsimetro y su umbral de deteccion
const int PulseWire = A3;
int Threshold = 520;

//inicializar variables del joystick
const int pinJoyX = A0;
const int pinJoyY = A1;
const int pinButton1 = 2;
const int pinButton2 = 3;
const int pinButton3 = 4;

//inicializar variables del sensor de GSR
const int GSR=A2; 
int sensorValue=0;
int gsr_average=0;
float human_res;

//inicializar estado de los botones en cero (sin presionar)
int button1State = 0;
int button2State = 0;
int button3State = 0;


void setup() {
  Serial.begin(9600);

  //declarar modo de pines de los botones
  pinMode(pinButton1, INPUT);
  pinMode(pinButton2, INPUT);
  pinMode(pinButton3, INPUT);

}

void loop() {

  //seccion de cronometro
  unsigned long currentMillis = millis();
  unsigned long seconds = currentMillis / 1000;
  unsigned long minutes = seconds / 60;
  unsigned long hours = minutes / 60;
  currentMillis %= 1000;
  seconds %= 60;
  minutes %= 60;
  hours %= 24;
  
  //APARTADO DE GAMEPAD
  //botones
  button1State = digitalRead(pinButton1);
  button2State = digitalRead(pinButton2);
  button3State = digitalRead(pinButton3);

  //joystick
  int Xvalue = 0;
  int Yvalue = 0;
  Xvalue = analogRead(pinJoyX);
  Yvalue = analogRead(pinJoyY);

  //APARTADO DE SENSORES
  //seccion de pulsimetro
  int myBPM = analogRead(PulseWire);

  //sección de GSR
  long sum=0;
  for(int i=0;i<10;i++)
  { 
    sensorValue=analogRead(GSR); 
    sum += sensorValue; 
  }
  gsr_average = sum/10;

  //APARTADO DE IMPRESION EN EL PUERTO SERIAL

  //seccion del gamepad (izquierda,derecha)
  if(Xvalue >= 1000){
    Serial.print("a,");
  }else{
    Serial.print("0,");
  }
  if(Xvalue == 0){
    Serial.print("d,");
  }else{
    Serial.print("0,");
  }

  //seccion de botones (salto, disparo, granada)
  if(button1State == HIGH){
    Serial.print("w,");
  }else{
    Serial.print("0,");
  }

  if(button2State == HIGH){
    Serial.print("e,");
  }else{
    Serial.print("0,");
  }

  if(button3State == HIGH){
    Serial.print("q,");
  }else{
    Serial.print("0,");
  }

  //seccion de GSR
  Serial.print(gsr_average);
  Serial.print(",");
  
  Serial.println(myBPM);                        // Print the value inside of myBPM. 
  //Serial.print(",");

//  //imprimir cronometro
//  Serial.print(hours);
//  Serial.print(':');
//  Serial.print(minutes);
//  Serial.print(':');
//  Serial.print(seconds);
//  Serial.print(':');
//  Serial.println(currentMillis);
  delay(20);
}
