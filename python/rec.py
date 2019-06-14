import csv
import multiprocessing as mp
import time

import mdk.arduino as ard
import mdk.arduino.digital as digi
import mdk.arduino.front
import mdk.arduino.instance
import mdk.arduino.tag_conf

# import mdk.arduino.tag_conf

recorder = ard.instance.arduino()
controler = ard.instance.arduino()
tags = ard.tag_conf.tags()

# tags = ard.tag_conf.tags()

ard_prog_path = "../arduino"
recorder._path_to_arduino = "arduino"

print("settings for recorder")
names = ard.front.check_available_board(tags)
name = ard.front.select(names)
port = ard.front.name_to_port(tags, name)
# ports = ard.front.check_available_port()
# port = ard.front.select(ports)
is_set = recorder.set_port(port)

if not is_set:
    ard.front.do_exit()

is_set = recorder.set_baudrate(115200)
if not is_set:
    ard.front.do_exit()

ard_progs = ard.front.check_available_arduino_programs(ard_prog_path)
ard_prog = ard.front.select(ard_progs)
is_set = recorder.set_arduino_program(ard_prog)
if not is_set:
    ard.front.do_exit()

is_set = recorder.check_config()
if not is_set:
    ard.front.do_exit()


print("settings for controler")
names = ard.front.check_available_board(tags)
name = ard.front.select(names)
port = ard.front.name_to_port(tags, name)
# ports = ard.front.check_available_port()
# port = ard.front.select(ports)
is_set = controler.set_port(port)

if not is_set:
    ard.front.do_exit()

is_set = controler.set_baudrate(115200)
if not is_set:
    ard.front.do_exit()

ard_progs = ard.front.check_available_arduino_programs(ard_prog_path)
ard_prog = ard.front.select(ard_progs)
is_set = controler.set_arduino_program(ard_prog)
if not is_set:
    ard.front.do_exit()

is_set = controler.check_config()
if not is_set:
    ard.front.do_exit()

response = mp.Value("i", 0)
reward = mp.Value("i", 0)
flag = mp.Value("i", 1)
rec = []


def main(response, reward):
    try:
        while flag.value:
            read_val = digi.readline(recorder).rstrip().decode().split(" ")
            rec.append(read_val)
            if read_val[0] == "100":
                response.value += 1
            elif read_val[0] == "255":
                reward.value += 1
    except KeyboardInterrupt:
        with open("test.csv", "w") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerows(rec)
        f.close()


def monitor():
    st = time.perf_counter()
    while flag.value:
        print("time: {:.2f}\nresponse: {}\nreward: {}".format(
            time.perf_counter() - st,
            response.value,
            reward.value
        ))
        print("\u001B[3A", end="")
        time.sleep(.01)


if __name__ == "__main__":
    proc0 = mp.Process(target=main, args=[response, reward])
    proc1 = mp.Process(target=monitor)

    procs = [
        proc0,
        proc1
    ]

    ard.front.write_program(recorder)
    recorder.connenct_board()
    recorder.start()
    ard.front.write_program(controler)
    controler.connenct_board()
    controler.start()

    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()
