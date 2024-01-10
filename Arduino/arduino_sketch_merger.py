import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 arduino_sketch_merger.py <path_to_sketch_to_merge> ")
    sys.exit(1)

wifi_ssid = os.environ.get("WIFI_SSID")
wifi_password = os.environ.get("WIFI_PASSWORD")

# Check if the environment variables exist
if wifi_ssid is None or wifi_password is None:
    print("WiFi credentials not set in environment variables.")
    print("forgot command: source ~/.profile")

filepath_to_merge = sys.argv[1]

ota_setup = []
with open("../esp32_setup/esp32_first_connect/esp32_ota_template/esp32_ota_template.ino", "r") as ota_template_file:
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
ota_setup[0] = ota_setup[0].replace("your_ssid", wifi_ssid).replace("your_password", wifi_password)          

with open(filepath_to_merge, "r") as sketch_file:

    for i, line in enumerate(sketch_file):
        if "void setup() {" in line:
            void_setup_index = i + 2

        if "void loop() {" in line:
            void_loop_index = i + 4
            arduino_ota_index = i

with open(filepath_to_merge, "r") as sketch_file:
    sketch_to_merge = sketch_file.readlines()

    sketch_to_merge.insert(0, ota_setup[0])
    sketch_to_merge.insert(void_setup_index, ota_setup[1])
    sketch_to_merge.insert(arduino_ota_index, ota_setup[2])
    sketch_to_merge.insert(void_loop_index, ota_setup[3])

    with open("merged_sketch_temp.ino", "w") as merged_file:
        merged_file.writelines(sketch_to_merge)
