# Catbot-
<img width="247" height="277" alt="front view" src="https://github.com/user-attachments/assets/26344b46-2cf3-4420-837c-9a58104cda23" />
The cat bot is an ai desk assistant that is
-Compact
-Aesthehic
-Serves the added function of setting study hrs and replying to texts recieved during the study hours
using Macrodroid.

##AI model
It uses a local ai model through Ollama (Gemma) in my current backend, however it can use any other ai model
provided that it is installed and the backend is set up accordingly.

##Hardware
The hardware includes an ESP-32-S3-zero wifi module as wifi connectivity is essential for input to be send to the ai
and output to be displayed). Additionally, it also includes a microphone module (INMP441) that records audio input,
two Buttons that serve different functions, a removable back for easy access in case any issues were to arise and a 
passive buzzer that beeps on receiving a notification. The electrical wiring diagram and schematic and pcb are shown below, however my design works by using a perfboard (refer electrical wiring diagram).


<img width="237" height="418" alt="wiring d" src="https://github.com/user-attachments/assets/fba0a400-0e88-40d1-8dff-4f39507a1286" />

<img width="486" height="320" alt="final sch" src="https://github.com/user-attachments/assets/b107937d-55bc-4214-89b7-66b8655ee65f" />

<img width="289" height="312" alt="pcb" src="https://github.com/user-attachments/assets/4671020f-b70a-4239-8632-30ed04d22751" />

The buttons are to be connected through wires, glued in place

##Backend 
The backend consists of several different files, that all come together to handle most of the ai functions of the device.
It has been written in Python by yours truly *bows dramatically and compiled on VS Code
(note:- once again while individual aspects have been tested the whole backend has not been tested together yet
also emv files have been removed, personality.txt can be edited)
#TO DO EXPLAIN MORE

##Credits
This project has been made as a part of the Half Life Program in hack club, all the code has been written by me
I take inspo from several online guides and yt vids




