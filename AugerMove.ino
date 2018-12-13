boolean go = false;

void setup()
{
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop()
{
  if (go == true)
  {
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
  }
}
void serialEvent()
{
  if (Serial.available())
  {
    go = !go;
    while (Serial.available())
    {
      Serial.read(); // Clear the buffer
    }
  }
}

