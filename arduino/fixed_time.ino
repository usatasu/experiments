const int REWARDPIN = 7;
const int REWARDTSPIN = 11;

const int USDURATION = 15;
const int FIXITI = 0;
const int IRI = 10000;
const int MAXTRIALS = 300;

int trialNum = 1;
unsigned long usOn = 0;
unsigned long trial = 0;

void setup() {
  pinMode(REWARDPIN, OUTPUT);
  pinMode(REWARDTSPIN, OUTPUT);
}

void loop() {
  trial = millis();
  while (millis() - trial <= IRI) {}

  usOn = millis();
  digitalWrite(REWARDPIN, HIGH);
  digitalWrite(REWARDTSPIN, HIGH);
  while (millis() - usOn <= USDURATION) {}
  digitalWrite(REWARDPIN, LOW);
  digitalWrite(REWARDTSPIN, LOW);

  trialNum++;

  while(millis() - usOn < FIXITI) {}

  while(trialNum >= MAXTRIALS) {}
}
