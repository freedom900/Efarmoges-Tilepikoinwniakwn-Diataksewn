#include <SPI.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 102 // define my unique address
#define DESTINATION_ADDRESS_1 99 // define who I can talk to

// Singleton instance of the radio
RF22Router rf22(MY_ADDRESS); // initiate the class to talk to my radio with MY_ADDRESS
int number_of_bytes=0; // will be needed to measure bytes of message
bool successful_transmission = false; 
// named constant for the pin the sensor is connected to
unsigned long ALOHA_timer = 0;
unsigned long startTime = 0;
unsigned long endTime = 0;
unsigned long ALOHA_min_timer = 300;
unsigned long ALOHA_max_timer = 500;
int laser_din= 3;
int laser_din2 = 5;
int sensorVal = 0;
bool flag = false;
bool flag2 = false;
bool statusChange = false;

void setup() {
  Serial.begin(9600); // to be able to view the results in the computer's monitor
  if (!rf22.init()) // initialize my radio
    Serial.println("RF22 init failed");
  // Defaults after init are 434.0MHz, 0.05MHz AFC pull-in, modulation FSK_Rb2_4Fd36
  if (!rf22.setFrequency(444.0)) // set the desired frequency
    Serial.println("setFrequency Fail");
  rf22.setTxPower(RF22_TXPOW_20DBM); // set the desired power for my transmitter in dBm
  //1,2,5,8,11,14,17,20 DBM
  rf22.setModemConfig(RF22::OOK_Rb40Bw335  ); // set the desired modulation
  // Manually define the routes for this network
  rf22.addRouteTo(DESTINATION_ADDRESS_1, DESTINATION_ADDRESS_1); // tells my radio card that if I want to send data to DESTINATION_ADDRESS_1 then I will send them directly to DESTINATION_ADDRESS_1 and not to another radio who would act as a relay
  delay(1000); // delay for 1 s
  randomSeed(4);
  pinMode(laser_din,INPUT);
}

void loop() 
{
  successful_transmission = false;
  if(digitalRead(laser_din)==LOW && flag == false) {
    sensorVal++;
    Serial.println("ANEVAINEI!!");
    flag = true;
    statusChange = true;
  }
  else if(digitalRead(laser_din)==LOW && flag == true){
    //Serial.println("AKOMA EDO EINAI O XONTROS");
  }
  else{
    //Serial.println("Efyge o kyrios");
    flag = false;
  }
  /* if(digitalRead(laser_din2)==LOW && flag2 == false && sensorVal > 0) {
    sensorVal--;
    Serial.println("KATEVAINEI!!");
    flag2 = true;
    statusChange = true;
  }
  else if(digitalRead(laser_din)==LOW && flag2 == true){
    //Serial.println("AKOMA EDO EINAI O XONTROS");
  }
  else{
    //Serial.println("Efyge o kyrios");
    flag2 = false;
  } */
  delay(200);
// the following variables are used in order to transform my integer measured value into a uint8_t variable, which is proper for my radio
  char data_read[RF22_ROUTER_MAX_MESSAGE_LEN];
  uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
  memset(data_read, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);
  memset(data_send, '\0', RF22_ROUTER_MAX_MESSAGE_LEN);    
  sprintf(data_read, "%d", sensorVal); // I'm copying the measurement sensorVal into variable data_read
  data_read[RF22_ROUTER_MAX_MESSAGE_LEN - 1] = '\0'; 
  memcpy(data_send, data_read, RF22_ROUTER_MAX_MESSAGE_LEN); // now I'm copying data_read to data_send

  // just demonstrating that the string I will send, after those transformation from integer to char and back remains the same
  endTime = millis();
  if(statusChange && endTime - startTime >= ALOHA_timer){
    if (rf22.sendtoWait(data_send, sizeof(data_send), DESTINATION_ADDRESS_1) != RF22_ROUTER_ERROR_NONE) // I'm sending the data in variable data_send to DESTINATION_ADDRESS_1... cross fingers
    {
      Serial.println("sendtoWait failed"); // for some reason I have failed
      ALOHA_timer = random(ALOHA_min_timer, ALOHA_max_timer);
      //delay(ALOHA_timer);
      startTime = millis();
    }
    else
    {
      successful_transmission = true;
      Serial.println("sendtoWait Successful"); // I have received an acknowledgement from DESTINATION_ADDRESS_1. Data have been delivered!
      statusChange = false;
    }
    
  }
  Serial.println(sensorVal);
}
