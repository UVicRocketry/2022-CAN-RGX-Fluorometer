/*
This code is modified from the supporting document of 
"Open-source fluorescence spectrometer for noncontact scientific research and education"
doi: https://doi.org/10.1021/acs.jchemed.1c00560
*/


#define SPEC_TRG A0
#define SPEC_ST A1
#define SPEC_CLK A2
#define SPEC_VIDEO A3
#define SPEC_CHANNELS 288 // New Spec Channel
uint16_t data[SPEC_CHANNELS];
#define N 3 // MAF N
uint16_t filteredData[SPEC_CHANNELS];
#define INT_TIME 32 //Integration Time
const int delay_time = 1000;
int led_pin=10;
int value=255; //0~255

void setup()
{
    //Set desired pins to OUTPUT
    pinMode(SPEC_CLK, OUTPUT);
    pinMode(SPEC_ST, OUTPUT);
    //pinMode(LASER_404, OUTPUT);
    //pinMode(WHITE_LED, OUTPUT);
    pinMode(led_pin, OUTPUT);
    digitalWrite(SPEC_CLK, HIGH); // Set SPEC_CLK High
    digitalWrite(SPEC_ST, LOW); // Set SPEC_ST Low
    Serial.begin(115200); // Baud Rate set to 115200
}
/*
This function reads spectrometer data from SPEC_VIDEO
See the Timing Chart in the Datasheet for more info
*/
void readSpectrometer()
{
    int delayTime = 1;
    // Start clock cycle and set start pulse to signal start
    digitalWrite(SPEC_CLK, LOW);
    delayMicroseconds(delayTime); //10000us = 0.01s
    digitalWrite(SPEC_CLK, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(SPEC_CLK, LOW);
    digitalWrite(SPEC_ST, HIGH);
    delayMicroseconds(delayTime);
    
    //Sample for a period of time
    for (int i = 0; i < 10; i++) {
        digitalWrite(SPEC_CLK, HIGH);
        delayMicroseconds(delayTime);
        digitalWrite(SPEC_CLK, LOW);
        delayMicroseconds(delayTime);
    }
    //Clock cycles for integration time //1
    for (int i = 0; i < INT_TIME; i++)
    {
        digitalWrite(SPEC_CLK, HIGH);
        digitalWrite(SPEC_CLK, LOW);
    }
    //Clock cycles for integration time //2
    for (int i = 0; i < INT_TIME; i++)
    {
        digitalWrite(SPEC_CLK, HIGH);
        digitalWrite(SPEC_CLK, LOW);
    }
    //Clock cycles for integration time //3
    for (int i = 0; i < INT_TIME; i++)
    {
        digitalWrite(SPEC_CLK, HIGH);
        digitalWrite(SPEC_CLK, LOW);
    }
    //Clock cycles for integration time //4
    for (int i = 0; i < INT_TIME; i++)
    {
        digitalWrite(SPEC_CLK, HIGH);
        digitalWrite(SPEC_CLK, LOW);
    }
    //Set SPEC_ST to low
    digitalWrite(SPEC_ST, LOW);
    //Sample for a period of time
    for (int i = 0; i < 87; i++)
    {
        digitalWrite(SPEC_CLK, HIGH);
        delayMicroseconds(delayTime);
        digitalWrite(SPEC_CLK, LOW);
        delayMicroseconds(delayTime);
    }
    //One more clock pulse before the actual read
    digitalWrite(SPEC_CLK, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(SPEC_CLK, LOW);
    delayMicroseconds(delayTime);
    //Read from SPEC_VIDEO
    for (int i = 0; i < SPEC_CHANNELS; i++)
    {
        data[i] = analogRead(SPEC_VIDEO);
        filteredData[i] = 0;
        if (i < N) {
            filteredData[i] = data[i];
        }
        
        if (i >= N) {
            for (int k = 0; k < N; k++) {
                filteredData[i - 1] += data[i - k];
            }
            filteredData[i - 1] = filteredData[i - 1] / N;
            
            if (i >= SPEC_CHANNELS - 1) {
                filteredData[i] = data[i];
            }
        }
        digitalWrite(SPEC_CLK, HIGH);
        delayMicroseconds(delayTime);
        digitalWrite(SPEC_CLK, LOW);
        delayMicroseconds(delayTime);
    }
    //Set SPEC_ST to high
    digitalWrite(SPEC_ST, HIGH);
    //Sample for a small amount of time
    for (int i = 0; i < 7; i++)
    {
        digitalWrite(SPEC_CLK, HIGH);
        delayMicroseconds(delayTime);
        digitalWrite(SPEC_CLK, LOW);
        delayMicroseconds(delayTime);
    }
    digitalWrite(SPEC_CLK, HIGH);
    delayMicroseconds(delayTime);
}
/*
The function below prints out data to the terminal or
processing plot
*/

void printData()
{
    for (int i = 0; i < SPEC_CHANNELS; i++)
    {
        Serial.print(i+1);
        Serial.print(",");
        Serial.print(filteredData[i]);
        Serial.print("\n");
    }
}

void loop()
{
    analogWrite(led_pin, value);
    readSpectrometer();
    printData();
    delay(delay_time);
}