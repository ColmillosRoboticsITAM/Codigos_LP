#include <Wire.h>
#include <LSM6.h>
#include <Math.h>

#define m_right  16
#define m_left  2
#define dm_right  15 
#define dm_left  4
const int Frecuencia = 115200;
const int Resolucion = 8;
double val = 0;

LSM6 imu;

float biasZ = 0;
float anguloZ = 0;
unsigned long lastTime = 0;

float ang_lata = 0;
bool flag_mar = false;
bool flag_contenedor = false;
float ang_cont = 0;
unsigned long now = 0;

// Constantes PID
float Kp = 4.5;
float Ki = 0.0;
float Kd = 0.0;

// Variables PID
float output = 0.0;

float error = 0.0;
float lastError = 0.0;
float integral = 0.0;
float derivative = 0.0;

int latas_dentro = 0;

void calibrarGyroZ() {
  const int N = 1000;
  long suma = 0;

  Serial.println("Calibrando giroscopio (mantener quieto)...");
  for (int i = 0; i < N; i++) {
    imu.read();
    suma += imu.g.z;
    delay(1);
  }

  biasZ = suma / float(N);
  Serial.print("Bias Z calculado: ");
  Serial.println(biasZ);
}

enum EstadoRobot {
  INICIO,
  BUSCAR_LATA,
  GIRAR_A_LATA,
  IR_A_LATA,
  RECOGER_LATA,
  IR_A_CONTENEDOR,
  ENTREGAR_LATA,
  FINALIZAR
};
EstadoRobot estadoActual = INICIO;

void setup() {
  Serial.begin(115200);
  // Pines motores
    pinMode(m_right, OUTPUT);
    pinMode(m_left, OUTPUT);
    pinMode(dm_right, OUTPUT);
    pinMode(dm_left, OUTPUT);

    // PWM
    ledcAttach(m_right, Frecuencia, Resolucion);
    ledcAttach(m_left, Frecuencia, Resolucion);

  Wire.begin();

  if (!imu.init()) {
    Serial.println("IMU no detectada");
    while (1);
  }

  imu.enableDefault();
  delay(1000);
  calibrarGyroZ();
  lastTime = millis();
  while (!Serial); // Espera si es necesario
  Serial.println("Esperando datos...");
  lastTime = millis();
}


void loop() {
  now = millis();
  read_heading();
  calc_pid(-anguloZ, 90);
  turn_robot(output);
  switch (estadoActual) {
    case INICIO:
      Serial.println("Estado: INICIO");
      // Inicializar sistemas
      delay(1000); // Simula espera de inicio
      estadoActual = BUSCAR_LATA;
      break;

    case BUSCAR_LATA:
      Serial.println("Estado: BUSCAR_LATA");
      if (!flag_mar) {
        estadoActual = GIRAR_A_LATA;
      }
      else{
        //Rotar
      }
      break;
    
    case GIRAR_A_LATA:
      Serial.println("Estado: IR_A_LATA");
      if (moverseALata()) {
        estadoActual = RECOGER_LATA;
      }
      break;

    case IR_A_LATA:
      Serial.println("Estado: IR_A_LATA");
      if(flag_mar){
        //Rotar 180
        calc_pid(-anguloZ,135);
        turn_robot(output);
      }
      else if(!flag_mar){
        //Avanzar
      }
      if (Flag_Lata_dentro) {
        estadoActual = RECOGER_LATA;
      }
      break;

    case RECOGER_LATA:
      Serial.println("Estado: RECOGER_LATA");
      if (!Flag_Lata_dentro) {
        latas_dentro += 1;
        if (latas_dentro>=3) {
        estadoActual = IR_A_CONTENEDOR;
        }
        else{
        estadoActual = BUSCAR_LATA;  
        }
      else{
        //Avanzar por 3s
        }
      }
      break;

    case IR_A_CONTENEDOR:
      Serial.println("Estado: IR_A_CONTENEDOR");
      if (irAContenedor()) {
        estadoActual = ENTREGAR_LATA;
      }
      break;

    case ENTREGAR_LATA:
      Serial.println("Estado: ENTREGAR_LATA");
      if (entregarLata()) {
        if (hayMasLatas()) {
          estadoActual = BUSCAR_LATA;
        } else {
          estadoActual = FINALIZAR;
        }
      }
      break;

    case FINALIZAR:
      Serial.println("Estado: FINALIZAR");
      detenerRobot();
      while (true); // Detiene el loop
      break;
  }
  delay(100);
}




void Serial_msg (){
  static String inputString = "";
  if (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') { // Mensaje completo recibido
      // Parsear la cadena
      int p1 = inputString.indexOf(',');
      int p2 = inputString.indexOf(',', p1 + 1);
      int p3 = inputString.indexOf(',', p2 + 1);

      if (p1 > 0 && p2 > p1 && p3 > p2) {
        ang_lata = inputString.substring(0, p1).toFloat();
        flag_mar = inputString.substring(p1 + 1, p2).toInt();
        flag_contenedor = inputString.substring(p2 + 1, p3).toInt();
        ang_cont = inputString.substring(p3 + 1).toFloat();

        Serial.print("ang_lata: "); Serial.println(ang_lata);
        Serial.print("flag_mar: "); Serial.println(flag_mar);
        Serial.print("flag_contenedor: "); Serial.println(flag_contenedor);
        Serial.print("ang_cont: "); Serial.println(ang_cont);
      } else {
        Serial.println("Error de formato");
      }

      inputString = ""; // limpiar para el siguiente mensaje
    } else {
      inputString += c;
    }
  }
}

void read_heading(){
  imu.read();
  float dt = (now - lastTime) / 1000.0;
  lastTime = now;

  float velocidadZ = imu.g.z - biasZ;
  if (abs(velocidadZ) > 300) {
    anguloZ += velocidadZ * dt/122.5;
  }
  // Serial.print("Vel Z: ");
  // Serial.print(velocidadZ, 2);
  //Serial.print("|\tÁngulo Z: ");
  //Serial.println(-anguloZ, 2);
  delay(10);
}

void calc_pid(double input, double setpoint){
  // Cálculo de PID
  unsigned long now = millis();
  float dt = (now - lastTime) / 1000.0;
  lastTime = now;

  error = (setpoint - input)/180;
  integral += error * dt;
  derivative = (error - lastError) / dt;
  lastError = error;

  output = Kp * error + Ki * integral + Kd * derivative;
  Serial.print("actual: ");Serial.print(input);
  Serial.print("\terror: ");Serial.print(error);
  Serial.print("\tsalida: ");Serial.print(output);Serial.println("\t|");
}

void turn_robot(double power){
  //input comes between -1% to 1%
  //127 is 0 power    0 full reverse    255 is full forward
  double consPow = constrain(power, -1.0, 1.0);
  int throttle = (int)((consPow + 1) * 127.5);
  int inv_throttle = abs(255 - throttle);
  Serial.print("Th: ");Serial.print(throttle);Serial.print("\t");Serial.println(inv_throttle);
  int m_stall = (throttle == 127 || throttle == 128) ? 0 : 1;
  digitalWrite(dm_right, m_stall);
  digitalWrite(dm_left, m_stall);
  ledcWrite(m_left, throttle);
  ledcWrite(m_right, inv_throttle);
}