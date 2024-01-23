import sys
import os
import subprocess
import json
import time

UPLOAD_TEMP_PATH = "merged_sketch_temp/merged_sketch_temp.ino"
OTA_TEMPLATE_PATH = "../esp32_setup/esp32_first_connect/esp32_ota_template/esp32_ota_template.ino"
ESP32_LOG_PATH = "../esp32_setup/esp32_hostname_log/esp32_hostname_log.json"

COMPILE_CMD = "sudo ./arduino-cli compile --fqbn esp32:esp32:esp32 ./merged_sketch_temp"
UPLOAD_CMD = "sudo ./arduino-cli upload -p port --fqbn esp32:esp32:esp32 ./merged_sketch_temp"

# TODO: --help flag and --nocompile flag? help text file? README.md?
# TODO: ip address instead of hostname (seems hostname as ip when uploading is a feature not implemented in arduino-cli)
  
def log_esp32(ip):

    hostname = get_hostname()

    with open(ESP32_LOG_PATH, "r") as esp32_hostname_log_file:
        esp32_hostname_log = json.load(esp32_hostname_log_file)

    is_logged = False
    for esp32 in esp32_hostname_log:
        if esp32.get("hostname") == hostname:
            is_logged = True
            break

    if not is_logged:
        esp32_json = {
            "hostname": hostname,
            "ip": ip
        }
        esp32_hostname_log.append(esp32_json)
        print(f"Hostname not in esp32_hostname_log, added as {hostname}")
        with open(ESP32_LOG_PATH, "w") as esp32_hostname_log_file:
            json.dump(esp32_hostname_log, esp32_hostname_log_file, indent=4)


def get_esp32_ip():
    hostname = get_hostname()

    with open(ESP32_LOG_PATH, "r") as esp32_hostname_log_file:
        esp32_hostname_log = json.load(esp32_hostname_log_file)
    for esp32 in esp32_hostname_log:
        if esp32.get("hostname") == hostname:
            return esp32.get("ip")
    raise Exception("Hostname not found in esp32_hostname_log")


def get_hostname():
    # get the hostname from the path from command line argument
    path = sys.argv[1]
    parts = path.split('/')
    home_index = parts.index('home')
    hostname = '/'.join(parts[home_index + 1:-1]) + "/esp32_1"
    return hostname

def merge_ino_files(filepath_to_merge):

    wifi_ssid = os.environ.get("WIFI_SSID")
    wifi_password = os.environ.get("WIFI_PASSWORD")

    # Check if the environment variables exist
    if wifi_ssid is None or wifi_password is None:
        print(f"{wifi_ssid} {wifi_password}")
        print("WiFi credentials not set in environment variables.")
        print("forgot command: [source ~/.profile] ?")
        sys.exit(1)

    # Fetch the OTA setup code
    ota_setup = []
    with open(OTA_TEMPLATE_PATH, "r") as ota_template_file:
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
        with open(UPLOAD_TEMP_PATH, "w") as merged_file:
            merged_file.writelines(sketch_to_merge)


def arduino_compile(command):

    print("Starting compile")
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if process.returncode == 0:
        print("Sketch compiled successfully.")  

    else:
        print("Sketch compilation failed.")
        sys.exit(1)


def arduino_upload(command, port):

    command = command.replace("port", port)

    # TODO: cleaner way to run the command
    print("Uploading the sketch to the board")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:

        time.sleep(0.5)

        output = process.stdout.readline()
        poll = process.poll()

        if poll is not None and output == '':
            break
        if output:
            print(output.strip().decode())
            if "A fatal error occurred:" in str(output):
                break

            if "following info" in str(output):
                print("Press enter")

            if "New upload port" in str(output):
                output_string = str(output).split(" ")
                ip = output_string[3]

        if process.returncode == 0:
            print("Sketch uploaded successfully.")
            return 

    print("Sketch upload failed.")
    sys.exit(1)


def main():

    try:
        filepath_to_merge = sys.argv[1]
        # check if file is readable
        with open(filepath_to_merge, "r") as sketch_to_merge_file:
            pass
    
    except FileNotFoundError:
        print("File to upload not found.")
        sys.exit(1)
    except IndexError:
        print("No file to upload file path specified.")
        sys.exit(1)
    else:
        merge_ino_files(filepath_to_merge)

    if "compile" in sys.argv:
        arduino_compile(COMPILE_CMD)
    else:
        print("No compile flag, skipping compile step.")

    if "usb" in sys.argv:
        ip = arduino_upload(UPLOAD_CMD, "/dev/ttyUSB0")
        log_esp32(ip)

    if "upload" in sys.argv:
        ip = get_esp32_ip()
        arduino_upload(UPLOAD_CMD, ip)
    else:
        print("No upload flag, skipping upload step.")


if __name__ == "__main__":
    main()
