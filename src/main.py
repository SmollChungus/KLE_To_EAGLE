import json
from util.serial import deserialize
from util.format import replace_special_chars_in_label

# KLE JSON parsing
with open('test.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)  

keyboard = deserialize(json_data)
print('Deserialization done, list of keys imported: ')

# Iterate over the keys and update labels
for key in keyboard.keys:
    if hasattr(key, 'labels') and key.labels:  
        key.labels = [replace_special_chars_in_label(label) if label else label for label in key.labels]
    

## Debug
for key in keyboard.keys:
    print(f'{key}\n')


# User Input Setup
print("enter keyboard name:")
keyboard_name = 'test'  
switch_type = "HE"
connector_type = "JST"
capacitor_size = "0402"

print('MX | MXHS | HE')
while switch_type not in ['HE', 'MX', 'MXHS']:
    print("Please enter a valid switch type (MX | MXHS | HE)")
    switch_type = input().upper()
print(f' Switch type set to: {switch_type}')

print('Capacitor size: 0402 | 0603 | 0804')
while capacitor_size not in ['0402', '0603', '0804']:
    print('please enter a valid capacitor size (0402 | 0603 | 0804)')
    capacitor_size = input()

print('USB | JST | EZMATE')
while connector_type not in ['USB', 'JST', 'EZMATE']:
    print("Please enter a valid switch type (USB | JST | EZMATE)")
    connector_type = input().upper()
print(f' Switch type set to: {connector_type}')



# Beep boop - mostly setup for eagle to find the right footprint, needs work
if switch_type in ['MX', 'MXHS']:
    switch_name = "KEYSWITCH-PLAIN-MXHSPCB-1U"  
    diode_name = "DIODE-SOD-323"  
    diode_offset = [0.10, 0.70] 
    net_offset = [0.10, 0.40]  

if switch_type == 'HE':
    switch_name = 'KEYSWITCH-HE'
    capacitor_name = (f"CAPACITOR-{capacitor_size}")
    capacitor_vcc_offset = [-0.4, -0.3]
    capacitor_out_offset = [0.5, -0.3]
    net_vcc_offset = [-0.4, -0.1]
    net_out_offset = [0.5, 0]
    c_vcc_value = "1nF"
    c_out_value = '10nF'
    multiplexer_amount = 1 + ( 40 // 16)
    print(multiplexer_amount)

# File to write the script to
file_name = (f'{keyboard_name}_schematic_script.scr')

with open(file_name, 'w', encoding='utf-8') as file:
    # Write header information
    file.write("GRID ON;\n")
    file.write("GRID IN 0.1 1;\n")
    file.write("GRID ALT IN 0.01;\n")
    file.write("SET WIRE_BEND 2;\n\n")

    # Iterate over keys and write component placement and net commands
    for i, key in enumerate(keyboard.keys):
        x_pos = key.x + 0.1 * i
        y_pos = key.y * -1.1  
        label = key.labels[0].upper() if key.labels else f"SW{i+1}"  # Use the first label or a default

        # Write the switch and capacitor placement commands
        file.write(f"ADD {switch_name} '{label}' ({x_pos:.2f} {y_pos:.2f});\n")
        file.write(f"ADD {capacitor_name} C_VCC_{label} R90 ({x_pos + capacitor_vcc_offset[0]:.2f} {y_pos + capacitor_vcc_offset[1]:.2f});\n")
        file.write(f"ADD {capacitor_name} C_OUT_{label} R90 ({x_pos + capacitor_out_offset[0]:.2f} {y_pos + capacitor_out_offset[1]:.2f});\n")
        file.write(f"VALUE C_VCC_{label} {c_vcc_value};\n")
        file.write(f"VALUE C_OUT_{label} {c_out_value};\n\n")
        
        # Write the net commands
        # cap to vcc
        file.write(f"NET VCC ({x_pos + net_vcc_offset[0]:.2f} {y_pos + net_vcc_offset[1]:.2f}) ({x_pos + net_vcc_offset[0]:.2f} {y_pos + 0.6 + net_vcc_offset[1]:.2f});\n\n")
        file.write(f"NET VCC ({x_pos + net_vcc_offset[0]:.2f} {y_pos + 0.6 + net_vcc_offset[1]:.2f}) ({x_pos:.2f} {y_pos + 0.5:.2f});\n\n")
        # cap to analog out
        file.write(f"NET {label} ({x_pos + net_out_offset[0]:.2f} {y_pos + net_out_offset[1]:.2f}) ({x_pos + net_out_offset[0]} {y_pos -0.1});\n\n")
        # caps and sensor to ground
        file.write(f"NET GND ({x_pos } {y_pos - 0.5}) ({x_pos - 0.4} {y_pos - 0.5});\n")
        file.write(f"NET GND ({x_pos } {y_pos - 0.5}) ({x_pos + 0.5} {y_pos - 0.5});\n\n")


    # Write footer information if needed
    # file.write("WINDOW FIT;\n")

print(f"Eagle script written to {file_name}")


