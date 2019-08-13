//Author: Andrew Collins
//Sensor: Client 111004
//Board: Adafruit M0

#include <SPI.h>
#include <WiFi101.h>


#define HOST_IP_ADDR "---"//Add your host IP
#define PORT 8090
#define CLIENT_ID "111001" //change
#define SECRET_SSID "----"//Add your network ID
#define SECRET_PASS "----"//Add your network Password
#define DELAYTIME_SEC 15 //delay time in seconds
const char* ssid = SECRET_SSID;
const char* password = SECRET_PASS;

const char* host = HOST_IP_ADDR;

long randNumber;
const int analog_ip = A0; //Naming analog input pin

void setup()
{
		WiFi.setPins(8,7,4,2);
		Serial.begin(9600);
  	Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
  randomSeed(analogRead(analog_ip));
}


void loop()
{
 ServerCommunication(CLIENT_ID, "Number:,14,Number:,17");
  Serial.println();

  delay(DELAYTIME_SEC*1000);//wait x seconds till next connection
}

/*-----------------Start: Server Communication-----------------*/
void ServerCommunication(String ID, String msg){
  Serial.print(ID);
  Serial.print("Attempting to connect to Server/Host:");
  Serial.print(host);
  Serial.print(" : ");
  Serial.print("Port");
  Serial.println(PORT);

  WiFiClient client;

  if(!client.connect(HOST_IP_ADDR,PORT)){
    Serial.println("Connection failed");
    delay(5000);
    return;
  }

//  Serial.println("Connected to server successful!");

String message= String(ID+","+msg);
  //sending data to server
//  Serial.print("Sending Data to server:");
//  Serial.println("msg");
  if(client.connected()){
    //client.println("This is my data sent by client");
   client.println(message);
  }

  //wait for server to sent message
  //timeout after 6 seconds
  unsigned long timeout = millis();
  while (client.available() == 0){ //while no bytes recived
    if(millis() - timeout > 60000){
     Serial.println("-----Done waiting-----");
      client.stop();
      delay(5000);
      return;
    }
  }

  //Server message received
  while(client.available()){
    char ch = static_cast<char>(client.read());
    Serial.print(ch);
  }



  //End Connection
 Serial.println("---Ending connection with Server---");
  client.stop();
Serial.println();


//  Serial.println();
  return;
}
/*-----------------End: Server Communication-----------------*/