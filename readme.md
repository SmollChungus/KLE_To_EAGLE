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
- [ ] remove spaces from keyboard.key.label for EAGLE script syntax
- [ ] fix '&' label collision with eagle syntax