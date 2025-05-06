#define A_pwm 17
#define A_dir 4
#define B_pwm 15
#define B_dir 2

const int frecuencia = 115200;
const int resolucion = 8;

void setup() {
  // put your setup code here, to run once:
  pinMode(A_pwm, OUTPUT);
  pinMode(A_dir, OUTPUT);  
  pinMode(B_pwm, OUTPUT);
  pinMode(B_dir, OUTPUT);
  
  ledcAttach(A_pwm, frecuencia, resolucion);
  ledcAttach(B_pwm, frecuencia, resolucion);

  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0){
    char c = Serial.read();
    if (c == 'B'){
      Serial.println("REVERSE");
      setPower(true, 1, 255);
      setPower(false, 1, 255);
    }
    else if (c == 'F'){
      Serial.println("FORWARD");
      setPower(true, 1, 0);
      setPower(false, 1, 0);
    }
    else if (c == 'R'){
      Serial.println("RIGHT");
      setPower(true, 1, 0);
      setPower(false, 1, 255);
    }
    else if (c== 'L'){
      Serial.println("LEFT");
      setPower(true, 1, 255);
      setPower(false, 1, 0);
    }
    else if (c== 'S'){
      Serial.println("STOP");
      setPower(true, 0, 255);
      setPower(false, 0, 255);
    }
  }
}

void setPower(bool isR, int isE, int vel){
  if (isR) {
    digitalWrite(A_dir, isE);
    ledcWrite(A_pwm, vel);
  }
  else if (!isR) {
    digitalWrite(B_dir, isE);
    ledcWrite(B_pwm, vel);
  }
}
