float ang_lata = 0;
bool flag_mar = false;
bool flag_contenedor = false;
float ang_cont = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial); // Espera si es necesario
  Serial.println("Esperando datos...");
}

void loop() {
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