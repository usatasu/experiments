const int LICKPIN = 11;
const int REWARDPIN = 12;

const uint8_t LICKON = 101;
const uint8_t LICKOFF = 100;
const uint8_t REWARDON = 255;

int currLickState;
int prevLickState;
int currRewardState;
int prevRewardState;

unsigned long time;

void setup() {
  pinMode(LICKPIN, INPUT_PULLUP);
  pinMode(REWARDPIN, INPUT);
  Serial.begin(115200);
}

void loop() {
  currLickState = digitalRead(LICKPIN);
  currRewardState = digitalRead(REWARDPIN);

  if (prevLickState && !currLickState) {
    Serial.print(LICKON);
    Serial.print(" ");
    Serial.println(millis());
  }

  if (!prevLickState && currLickState) {
    Serial.print(LICKOFF);
    Serial.print(" ");
    Serial.println(millis());
  }

  if (prevRewardState && !currRewardState) {
    Serial.print(REWARDON);
    Serial.print(" ");
    Serial.println(millis());
  }

  prevLickState = currLickState;
  prevRewardState = currRewardState;
}
