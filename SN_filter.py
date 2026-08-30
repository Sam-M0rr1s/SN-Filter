valid_prefixes = ["PB", "PF", "PW", "PC"]

def get_serial_number():
    while True:
        raw_scan = input("please scan the serial number: ")


        if raw_scan.startswith("1S") or raw_scan.startswith("1s"):
            print("Serial number is valid")
        else:
            print("Serial number is invalid")
            print("Please scan a valid serial number")
            continue

        start_index = -1
        for prefix in valid_prefixes:
            if prefix in raw_scan:
                print(f"Serial number contains {prefix}")
                start_index = raw_scan.find(prefix)
                break

        if start_index == -1:
            man_device = input("Do you want to enter a SN Manuelly? ")
            if man_device = "yes":
                man_make = input("please enter the make of the device. "),
                man_model = input("Please enter the model of this device. "),
                man_sn = input("please enter the serial number. ")
            continue

        filtered_scan = raw_scan[start_index:start_index + 8]
        return filtered_scan
    





