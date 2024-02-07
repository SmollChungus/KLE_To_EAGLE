# KLE to Eagle PCB converter

Python based tool to directly generate the scaffold for an EAGLE schematic + board

To generate the .scr EAGLE script file, download your keyboard.json from KLE.

run main.py in terminal, follow command line.

set keyswitch type:            (MX, MXHS, HE, ALPS*, ALPSMX*)

set diode | capacitor size:    (323*, 123*, BAV70* | 0402, 0603, 0804)

set connector type:            (USB, JST, EZMATE)


Make sure to import the Keyboard_Analog.lbr library and activate it inside EAGLE before running the .scr file.
Hit run script in the EAGLE schematic editor and select keyboard_schematic_script.scr
Open up EAGLE board editor, hit run script, and select keyboard_board_script.scr

Happy routing!


![%.sch%](https://i.imgur.com/ZOlMPaJ.png)
![%.brd%](https://i.imgur.com/HAYMNlP.png)





## To Do:
- [ ] refactor
EAGLE schematic.sch:

- [x] user config inputs 
- [x] switches
- [x] capacitors
- [ ] multiplexer components
- [ ] multiplexer nets
- [ ] multiplexer nets++
- [ ] chip + components
- [ ] chip + nets
- [ ] chip + nets++
- [ ] connector/usb
- [ ] label spacebar with size

EAGLE board.brd:

- [ ] switch placement
- [ ] capacitor placement
- [ ] diode placement
- [ ] chip + components placement

 BOM generation/cleaner:
- [ ] beep

bugs:
- [x] remove spaces from keyboard.key.label for EAGLE script syntax
- [x] fix '&' and '*' label collision with eagle scripting syntax
- [x] fix bracket label collision zzz
- [x] numpad double labels collision
- [x] schematic y drift