float ang_lata = 0;
bool flag_lata_cerca = false;
bool flag_mar = false;
bool flag_contenedor = false;
float ang_cont = 0;
bool flag_cont_cerca = false;


void setup() {
  Serial.begin(115200);
  Serial.println("Esperando datos...");
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // leer línea completa
    data.trim(); // elimina espacios y saltos extra

    // Separar por comas
    int index = 0;
    String partes[6];
    while (data.length() > 0 && index < 6) {
      int comaIndex = data.indexOf(',');
      if (comaIndex == -1) {
        partes[index++] = data;
        break;
      } else {
        partes[index++] = data.substring(0, comaIndex);
        data = data.substring(comaIndex + 1);
      }
    }

    // Convertir a variables
    ang_lata = partes[0].toFloat();
    flag_lata_cerca = partes[1].toInt();
    flag_mar = partes[2].toInt();
    flag_cont = partes[3].toInt();
    ang_cont = partes[4].toFloat();
    flag_cont_cerca = partes[5].toInt();

    // Mostrar los valores
    Serial.println("---- Datos recibidos ----");
    Serial.print("ang_lata: "); Serial.println(ang_lata);
    Serial.print("flag_lata_cerca: "); Serial.println(flag_lata_cerca);
    Serial.print("flag_mar: "); Serial.println(flag_mar);
    Serial.print("flag_cont: "); Serial.println(flag_cont);
    Serial.print("ang_cont: "); Serial.println(ang_cont);
    Serial.print("flag_cont_cerca: "); Serial.println(flag_cont_cerca);
  }
}
