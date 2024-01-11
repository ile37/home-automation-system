import sys
import os
import subprocess

if len(sys.argv) < 2:
    print("Usage: python3 arduino_sketch_merger.py <path_to_sketch_to_merge> ")
    sys.exit(1)

# Credentials for the WiFi are stored as environment variables in .profile file
wifi_ssid = os.environ.get("WIFI_SSID")
wifi_password = os.environ.get("WIFI_PASSWORD")

# Check if the environment variables exist
if wifi_ssid is None or wifi_password is None:
    print(f"{wifi_ssid} {wifi_password}")
    print("WiFi credentials not set in environment variables.")
    print("forgot command: [source ~/.profile] ?")
    sys.exit(1)

filepath_to_merge = sys.argv[1]

# Fetch the OTA setup code
ota_setup = []
with open("../esp32_setup/esp32_first_connect/esp32_ota_template/" + \
          "esp32_ota_template.ino", "r") as ota_template_file:
    ota_setup_block = ""
    setup_flag = False
    for line in ota_template_file:

        if "Start of OTA" in line:
            setup_flag = True

        if setup_flag:
            ota_setup_block += line   

        if "End of OTA" in line:
            setup_flag = False
            ota_setup_block += "\n"
            ota_setup.append(ota_setup_block)
            ota_setup_block = ""

# Wifi crediential swap
ota_setup[0] = ota_setup[0].replace("your_ssid", wifi_ssid)
ota_setup[0] = ota_setup[0].replace("your_password", wifi_password)          

with open(filepath_to_merge, "r") as sketch_file_indexs:

    # Some magic numbers to the indexes to insert the OTA setup code :)
    # So that the OTA setup code is inserted in the right place
    for i, line in enumerate(sketch_file_indexs):
        if "void setup() {" in line:
            void_setup_index = i + 2

        if "void loop() {" in line:
            void_loop_index = i + 3

#Fetch and merge the sketch
with open(filepath_to_merge, "r") as sketch_file:
    sketch_to_merge = sketch_file.readlines()

    sketch_to_merge.insert(0, ota_setup[0])
    sketch_to_merge.insert(void_setup_index, ota_setup[1])
    sketch_to_merge.insert(void_loop_index, ota_setup[2])

    # Written to a temp file to be accessed by the arduino-cli
    with open("merged_sketch_temp/merged_sketch_temp.ino", "w") as merged_file:
        merged_file.writelines(sketch_to_merge)


# TODO - Add a check to see if the sketch compiles before uploading
        # sudo ./arduino-cli compile --fqbn esp32:esp32:esp32 merged_sketch_temp.ino
command = "sudo ./arduino-cli compile --fqbn esp32:esp32:esp32 ./merged_sketch_temp"

print("Starting compile")
process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if process.returncode == 0:
    print("Sketch compiled successfully.")  

else:
    print("Sketch compilation failed.")
    sys.exit(1)

# TODO - Upload the sketch to the board
