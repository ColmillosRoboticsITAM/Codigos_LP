#include <Wire.h>
#include <LSM6.h>
#include <Math.h>

LSM6 imu;

float biasZ = 0;
float anguloZ = 0;
unsigned long lastTime = 0;

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

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!imu.init()) {
    Serial.println("IMU no detectada");
    while (1)
      ;
  }

  imu.enableDefault();
  delay(1000);
  calibrarGyroZ();
  lastTime = millis();
}

void loop() {
  imu.read();

  unsigned long now = millis();
  float dt = (now - lastTime) / 1000.0;
  lastTime = now;

  float velocidadZ = imu.g.z - biasZ;
  if (abs(velocidadZ) > 300) {
    anguloZ += velocidadZ * dt / 100;
  }
  // Serial.print("Vel Z: ");
  // Serial.print(velocidadZ, 2);
  Serial.print("|\tÁngulo Z: ");
  Serial.println(-anguloZ, 2);

  delay(10);
}
