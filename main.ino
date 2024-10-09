int pwmLedPin = 9;  // Pin untuk LED PWM (gunakan pin yang mendukung PWM)

void setup() {
  Serial.begin(115200);  // Mulai komunikasi serial
  pinMode(LED_BUILTIN, OUTPUT);  // Tetapkan pin LED built-in sebagai output
  pinMode(pwmLedPin, OUTPUT);  // Tetapkan pin LED PWM sebagai output
  digitalWrite(LED_BUILTIN, LOW);  // Awalnya lampu built-in dalam kondisi mati
  analogWrite(pwmLedPin, 0);  // Awalnya LED PWM dalam kondisi mati
}

void loop() {
  if (Serial.available() > 0) {
    // Baca perintah dari serial
    String command = Serial.readStringUntil('\n');
    
    // Cek apakah perintahnya "ON", "OFF", atau intensitas angka (0-255)
    command.trim();  // Hapus spasi atau newline dari string
    
    if (command == "ON") {
      // Nyalakan LED built-in
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("LED Built-in Turned ON");
    }
    else if (command == "OFF") {
      // Matikan LED built-in
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("LED Built-in Turned OFF");
    }
    else {
      // Coba konversi perintah menjadi angka untuk intensitas LED PWM (0-255)
      int intensity = command.toInt();
      if (intensity >= 0 && intensity <= 255) {
        analogWrite(pwmLedPin, intensity);  // Atur intensitas LED PWM
        Serial.print("PWM LED Intensity set to ");
        Serial.println(intensity);
      }
    }
  }
}
