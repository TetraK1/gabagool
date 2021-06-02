const uint8_t ADDRESS_MASK = 0b01111111;
const uint8_t VALUE_MASK = 0b10000000;

const uint8_t SSR1 = 0b00000001;
const uint8_t SSR2 = 0b00000010;

void setup() {
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    Serial.begin(9600);
}

uint8_t b_in;

void loop() {
    if (Serial.available() > 0) {
        b_in = Serial.read();
        Serial.print("Received: ");
        Serial.println(int(b_in));
        
        if((b_in & ADDRESS_MASK) == SSR1){
            Serial.println("Writing to SSR1");
            digitalWrite(2, b_in & VALUE_MASK);
        } else if( (b_in & ADDRESS_MASK) == SSR2){
            Serial.println("Writing to SSR2");
            digitalWrite(3, b_in & VALUE_MASK);
        } 
    }
}
