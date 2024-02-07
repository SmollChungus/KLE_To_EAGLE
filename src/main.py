import json
from util.serial import deserialize
from util.format import replace_special_chars_in_label

with open('test.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)  

keyboard = deserialize(json_data)
print('Deserialization done, list of keys imported: ')

label_counts = {}

for key in keyboard.keys:
    if hasattr(key, 'labels') and key.labels:
        key.labels = [replace_special_chars_in_label(label) if label else label for label in key.labels]
        if key.labels[0] in label_counts:
            label_counts[key.labels[0]] += 1
            key.labels[0] += str(label_counts[key.labels[0]])
        else:
            label_counts[key.labels[0]] = 0

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



# Beep boop - mostly setup for eagle to find the right footprint, needs work, make Classes
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


################# EAGLE SCHEMATIC #################
file_name = f'{keyboard_name}_schematic_script.scr'

with open(file_name, 'w', encoding='utf-8') as file:
    file.write("GRID ON;\n")
    file.write("GRID IN 0.1 1;\n")
    file.write("GRID ALT IN 0.01;\n")
    file.write("SET WIRE_BEND 2;\n\n")

    current_row_y = 0
    row_index = 0

    for i, key in enumerate(keyboard.keys):
        if key.y != current_row_y:
            current_row_y = key.y
            row_index = 0
        else:
            row_index += 1

        x_pos = key.x + (0.1 * row_index)
        y_pos = (-1.1 * key.y) 
        label = key.labels[0].upper() if key.labels else f"SW{i+1}"  
        file.write(f"ADD {switch_name} '{label}' ({x_pos:.2f} {y_pos:.2f});\n")
        file.write(f"ADD {capacitor_name} C_VCC_{label} R90 ({x_pos + capacitor_vcc_offset[0]:.2f} {y_pos + capacitor_vcc_offset[1]:.2f});\n")
        file.write(f"ADD {capacitor_name} C_OUT_{label} R90 ({x_pos + capacitor_out_offset[0]:.2f} {y_pos + capacitor_out_offset[1]:.2f});\n")
        file.write(f"VALUE C_VCC_{label} {c_vcc_value};\n")
        file.write(f"VALUE C_OUT_{label} {c_out_value};\n\n")
        # Cap to vcc
        file.write(f"NET VCC ({x_pos + net_vcc_offset[0]:.2f} {y_pos + net_vcc_offset[1]:.2f}) ({x_pos + net_vcc_offset[0]:.2f} {y_pos + 0.6 + net_vcc_offset[1]:.2f});\n\n")
        file.write(f"NET VCC ({x_pos + net_vcc_offset[0]:.2f} {y_pos + 0.6 + net_vcc_offset[1]:.2f}) ({x_pos:.2f} {y_pos + 0.5:.2f});\n\n")
        # Cap to analog out
        file.write(f"NET {label} ({x_pos + net_out_offset[0]:.2f} {y_pos + net_out_offset[1]:.2f}) ({x_pos + net_out_offset[0]} {y_pos -0.1});\n\n")
        # Caps and sensor to ground
        file.write(f"NET GND ({x_pos } {y_pos - 0.5}) ({x_pos - 0.4} {y_pos - 0.5});\n")
        file.write(f"NET GND ({x_pos } {y_pos - 0.5}) ({x_pos + 0.5} {y_pos - 0.5});\n\n")


    file.write("WINDOW FIT;\n")

print(f"Eagle schematic script written to {file_name}")


################# EAGLE .BRD ##################
file_name = f'{keyboard_name}_board_script.scr'
unit_to_mm = 19.05
capacitor_out_offset = [-2.5, -1.75]
capacitor_vcc_offset = [2.5, -1.75]
with open(file_name, 'w', encoding='utf-8') as file:
    file.write("GRID MM 19.05 1;\n")
    file.write("GRID ALT MM 1.27;\n")

    
    for i, key in enumerate(keyboard.keys):
        if key.width > 1:
            x_pos_mm = key.x * unit_to_mm + (0.5 * unit_to_mm * (key.width - 1)) 
        else:
            x_pos_mm = key.x * unit_to_mm
        y_pos_mm = key.y * unit_to_mm * -1
        label = key.labels[0].upper() if key.labels else f"SW{i+1}"

        file.write(f"MOVE '{label}' ({x_pos_mm:.2f} {y_pos_mm:.2f});\n")

        file.write(f"MOVE 'C_VCC_{label}' ({(x_pos_mm + capacitor_vcc_offset[0]):.2f} {y_pos_mm + capacitor_out_offset[1]:.2f});\n")

        file.write(f"ROTATE 'C_VCC_{label}' R90;\n")
        file.write(f"MIRROR 'C_VCC_{label}';\n")

        file.write(f"MOVE 'C_OUT_{label}' ({(x_pos_mm + capacitor_out_offset[0]):.2f} {(y_pos_mm + capacitor_out_offset[1]):.2f});\n")

        file.write(f"ROTATE 'C_OUT_{label}' R90;\n")
        file.write(f"MIRROR 'C_OUT_{label}';\n")

print(f"Eagle board script written to {file_name}")