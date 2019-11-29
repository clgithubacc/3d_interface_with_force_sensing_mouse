//Positions are from top view of the mouse
bool debugMode=false;

int fsrul = 0; //Analog 0
int fsrur = 1; //Analog 1
int fsrbl = 2; //Analog 2
int fsrbr = 3; //Analog 3
int fsrReadings[4];
int forces[4];

//Pattern related parameters
//Minimum amount of force difference between two sensors to be considered as in different patterns
int forceDiffThreshold=200;
int uniformPressingThreshold;
void setup(void) {
  Serial.begin(9600);
}

void loop(void) {
//  Serial.println(analogRead(fsrul));
  
  fsrReadings[0]=analogRead(fsrul);
  fsrReadings[1]=analogRead(fsrur);
  fsrReadings[2]=analogRead(fsrbl);
  fsrReadings[3]=analogRead(fsrbr);
  for(int i=0;i<4;i++){
    forces[i]=map(fsrReadings[i],0,900,0,2000);
  }
  getReadings();
  delay(100);
}
void getReadings(){
  int forceDiffs[3];
  bool exceedThreshold[3];
  int pattern=5;
  for(int i=0;i<3;i++){
    forceDiffs[i]=forces[i]-forces[3];
    exceedThreshold[i]=abs(forceDiffs[i])>forceDiffThreshold;
  }
//  if (!(exceedThreshold[0]||exceedThreshold[1]||exceedThreshold[2])){
//    pattern=0; //Uniform
  if (!(exceedThreshold[0]||exceedThreshold[1]||exceedThreshold[2])&&forces[0]>uniformPressingThreshold){
    pattern=0; //Uniform
  }else if(exceedThreshold[0]&&!(exceedThreshold[1]||exceedThreshold[2])){
    pattern=1; //Upper Left
  }else if(exceedThreshold[1]&&!(exceedThreshold[0]||exceedThreshold[2])){
    pattern=2; //Upper Right
  }else if(exceedThreshold[2]&&!(exceedThreshold[0]||exceedThreshold[1])){
    pattern=3; //Bottom Left
  }else if(exceedThreshold[0]&&exceedThreshold[1]&&exceedThreshold[2]){
    pattern=4; //Bottom Right
  }
  Serial.println(String(pattern)+String(" ")+String(forces[0])+String(" ")+String(forces[1])+String(" ")+String(forces[2])+String(" ")+String(forces[3]));
}
