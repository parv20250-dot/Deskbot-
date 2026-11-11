# Catbot-

<img width="247" height="277" alt="front view" src="https://github.com/user-attachments/assets/26344b46-2cf3-4420-837c-9a58104cda23" />

The cat bot is an ai desk assistant that is
-Compact
-Aesthehic
-Serves the added function of setting study hrs and replying to texts recieved during the study hours
using Macrodroid.
## Button guide
I wanted to add cuz its lowk confusing even to me, it has only two buttons (I did not want to have too many buttons as I wanted a smooth sleek look) I try to do a lot with it which led to wel.....
This 
|Button|Input        |Function                        |
|------|-------------|--------------------------------|
|A     | Single press| Approve reply                  |
|A     | Double press| Reject reply                   |
|A     | Long press  | Change study mode              |
|B     | Single press| Change cat expression          |
|B     | Long press  | Starts recording audio         |
|B     | Release     | Stops recording and upload audio|


## AI model
The catbot deskbot uses a local ai model Gemma through Ollama in my current backend, however it can use any other ai model
provided that it is installed and the backend is set up accordingly to communicate with them.

I opted to use a local ai as it was easier for testing and also for privacy reasons, since it has access to my texts and my devices. All the AI processing happens locally on my laptop instead of using a cloud hosted AI.

## Hardware
The hardware includes an ESP-32-S3-zero wifi dev module as wifi connectivity is essential for input to be send to the ai
and output to be displayed). Additionally, it also includes a microphone module (INMP441) that records audio input,
two Buttons that serve different functions, a removable back for easy access in case any issues were to arise and a 
passive buzzer that beeps on receiving a notification. The electrical wiring diagram and schematic and pcb are shown below, however my design works by using a perfboard (refer electrical wiring diagram).


<img width="237" height="418" alt="wiring d" src="https://github.com/user-attachments/assets/fba0a400-0e88-40d1-8dff-4f39507a1286" />



<img width="486" height="320" alt="final sch" src="https://github.com/user-attachments/assets/b107937d-55bc-4214-89b7-66b8655ee65f" />



<img width="289" height="312" alt="pcb" src="https://github.com/user-attachments/assets/4671020f-b70a-4239-8632-30ed04d22751" />

The buttons are to be connected through wires, glued in place.

## Backend 
The backend consists of several different files, that all come together to handle most of the ai related functions of the device.
It has been written in Python by yours truly *bows dramatically and compiled on VS Code

#### Tools-
Search, browse and weather are the tools the ai model currently has access to.
Search returns only the ddgs results, while browse allows the ai model to access a browser through playwright and then search links. 
The browser used in the browse function is firfox and the search engine used is duckduckgo. 
Unless you specifically mention the word "search" in the input the ai model cannot access the browse tool, this decision was made as I did not want to give an ai model unrestrained access over a browser, it can however use the search tool at any time.
The tools are all written in their indiv files (cuz I wanted to text em individuallY) and then brought together and called in the tools part of the code.

#### Personality (note)
The file persona.txt contains the personality sketch for the ai model to follow, it is based off of my own patterns and habits, which I found by analysing my own texts, asking people and LOTS of overthinking. I also lay out some ground rules for the ai model in it.

<ins> note <ins> The example texts at the end of the file have been removed before uploading to GitHub for privacy reasons, if necessary add your own examples. 

#### Server
The server or the api that allows for the ESP and the hardware components to be connected to the backend and the ai model is started each time on running the backend using FAST API. In order to create a server simply open up an integrated terminal on backend and write "uvicorn main:app --host 0.0.0.0 --port 8000" to start up the server. Use ctrl+c to close the server.

The api is secured through an api key, each request is send to the server alongside the api key. It doesn't work without api key.

#### env files
This has NOT been added into the upload (cuz yk the drill by now privacy) but in the backend files a .env file must be created with api_key and if you want to use the weather function which city you're based in


(note:- once again while individual aspects have been tested the whole backend has not been tested together yet
also env files have been removed, personality.txt can be edited)


## Firmware
The firmware file contains the code for the hardware components of the deskbot. It is written in Arduino C++ and compiled on Arduino.

<img width="806" height="98" alt="FINALLY" src="https://github.com/user-attachments/assets/b9932b0f-4a56-4344-aebc-317139411a0e" />

NOTE- like backend while it has been debugged as much as I can it is untested and might require tweaking.
It runs on the ESP32. The firmware:-
Controls the OLED display and is responsible for showing if study mode on or off, displaying texts, also shows random expressions when idle.

#### expressions 
Expressions are 


<img width="605" height="203" alt="image" src="https://github.com/user-attachments/assets/3ae4dbb3-36c5-435d-b6f6-ce595e8c31b8" />


These basically but stored as bmp arrays, they are randomly selcted and displayed.

The firmware also handles button inputs and detects single presses, double presses and long presses, it also connects to wifi and handles audio recording and formatting before uploading it to backend.

When you get a notification, the passive buzzer plays a beep.
<img width="658" height="138" alt="image" src="https://github.com/user-attachments/assets/5eb2c848-ecbf-4e84-9882-122c2809cfde" />
Add info here on firmware



## BOM
The below table showcases the components that are used and their costs.

|Item                                  |Qty|Supplier   |Cost/item|Total Cost|link                                                                                                                                                |
|--------------------------------------|---|-----------|---------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------|
|ESP-32-S3-ZERO                        |1  |electro:kit|$9.90    |$9.90     |https://www.electrokit.com/en/esp32-s3-dev-board-mini-4mb-psram-2mb-with-headers                                                                    |
|MEMS microphone on board I2S - INMP441|1  |electro:kit|$4.90    |$4.90     |https://www.electrokit.com/mems-mikrofon-pa-kort-i2s-inmp441                                                                                        |
|Perfboard                             |1  |electro:kit|$1.60    |$1.60     |https://www.electrokit.com/en/experimentkort-1-hal-30x70mm-genomplaterade-hal                                                                       |
|Hookup wire                           |1  |electro:kit|$2.20    |$2.20     |https://www.electrokit.com/en/kopplingstrad-0.14mm2-rod-10m                                                                                         |
|Resistor                              |1  |electro:kit|$1.20    |$1.20     |https://www.electrokit.com/en/motstand-3w-100ohm-5100r                                                                                              |
|Passive buzzer                        |1  |electro:kit|$1.00    |$1.00     |https://www.electrokit.com/en/passive-piezo-buzzer-80db-12nf-12.5x7mm                                                                               |
|OLED display                          |1  |jmux       |$6.50    |$6.50     |https://jmux.se/products/oled-display-0-96-inch-i2c-128x64-pixlar-for-rpi-arduino-atmega?_pos=1&_psq=0.96%22+OLED+128x64px+I2C&_psid=8185eb917&_ss=e|
|Tactile switches                      |2  |electro:kit|$0.13    |$0.26     |https://www.electrokit.com/tryckknapp-pcb-6x6x4.3mm-svart                                                                                           |
|Estimated total shipping              |1  |           |         |$4.90     |                                                                                                                                                    |
NOTE- For text features to work Macrodroid is also necessary, it is a paid application.

## Credits
This project has been made as a part of the Half Life Program in hack club, all the code has been written by me
I take inspo from several online guides and yt vids




