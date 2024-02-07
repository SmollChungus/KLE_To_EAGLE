# KLE to Eagle PCB converter

Python based tool to directly generate the scaffold for an EAGLE schematic + board


## To Do:
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