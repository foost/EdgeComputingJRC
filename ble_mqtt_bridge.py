# This script is based on https://github.com/Ladvien/arduino_ble_sense/blob/master/app.py
# all modifications by F. Ostermann;
# it adds support for sending received data to an MQTT broker in the
# notification handler function;
# removes calls to unnecessary functions;
# NOT intended for production, only demonstration;
# several unresolved warnings and now unused imports left

import os, sys
import asyncio
import platform
from datetime import datetime
from typing import Callable, Any

from aioconsole import ainput
from bleak import BleakClient, discover

import random
import time

# imports and variables for MQTT connection
import paho.mqtt.publish as publish
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt/tinyml/"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

root_path = os.environ["HOME"]
output_file = f"{root_path}/Desktop/microphone_dump.csv"

#selected_device = [00001c80-0000-1000-8000-00805f9b34fb]

read_characteristic = "00002a56-0000-1000-8000-00805f9b34fb"
write_characteristic = ""

class DataToFile:

    column_names = ["time", "delay", "data_value"]

    def __init__(self, write_path):
        self.path = write_path

    def write_to_csv(self, times: [int], delays: [datetime], data_values: [Any]):

        if len(set([len(times), len(delays), len(data_values)])) > 1:
            raise Exception("Not all data lists are the same length.")

        with open(self.path, "a+") as f:
            if os.stat(self.path).st_size == 0:
                print("Created file.")
                f.write(",".join([str(name) for name in self.column_names]) + ",\n")
            else:
                for i in range(len(data_values)):
                    f.write(f"{times[i]},{delays[i]},{data_values[i]},\n")
                    



class Connection:
    
    client: BleakClient = None
    
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        read_characteristic: str,
        write_characteristic: str,
        data_dump_handler: Callable[[str, Any], None],
        data_dump_size: int = 256,
    ):
        self.loop = loop
        self.read_characteristic = read_characteristic
        self.write_characteristic = write_characteristic
        self.data_dump_handler = data_dump_handler

        self.last_packet_time = datetime.now()
        self.dump_size = data_dump_size
        self.connected = False
        self.connected_device = None

        self.rx_data = []
        self.rx_timestamps = []
        self.rx_delays = []

    def on_disconnect(self, client: BleakClient, future: asyncio.Future):
        self.connected = False
        # Put code here to handle what happens on disconnet.
        print(f"Disconnected from {self.connected_device.name}!")

    async def cleanup(self):
        if self.client:
            await self.client.stop_notify(read_characteristic)
            await self.client.disconnect()

    async def manager(self):
        print("Starting connection manager.")
        while True:
            if self.client:
                await self.connect()
            else:
                await self.select_device()
                await asyncio.sleep(15.0, loop=loop)       

    async def connect(self):
        if self.connected:
            return
        try:
            await self.client.connect()
            self.connected = await self.client.is_connected()
            if self.connected:
                print(F"Connected to {self.connected_device.name}")
                self.client.set_disconnected_callback(self.on_disconnect)
                await self.client.start_notify(
                    self.read_characteristic, self.notification_handler,
                )
                while True:
                    if not self.connected:
                        break
                    await asyncio.sleep(3.0, loop=loop)
            else:
                print(f"Failed to connect to {self.connected_device.name}")
        except Exception as e:
            print(e)

    async def select_device(self):
        print("Bluetooh LE hardware warming up...")
        await asyncio.sleep(2.0, loop=loop) # Wait for BLE to initialize.
        devices = await discover()

        print("Please select device: ")
        for i, device in enumerate(devices):
            print(f"{i}: {device.name}")

        response = -1
        while True:
            response = input("Select device: " )
            try:
                response = int(response.strip())
            except:
                print("Please make valid selection.")
            
            if response > -1 and response < len(devices):
                break
            else:
                print("Please make valid selection.")

        print(f"Connecting to {devices[response].name}")
        self.connected_device = devices[response]
        self.client = BleakClient(devices[response].address, loop=self.loop)

    def record_time_info(self):
        present_time = datetime.now()
        self.rx_timestamps.append(present_time)
        self.rx_delays.append((present_time - self.last_packet_time).microseconds)
        self.last_packet_time = present_time

    def clear_lists(self):
        self.rx_data.clear()
        self.rx_delays.clear()
        self.rx_timestamps.clear()

    def notification_handler(self, sender: str, data: Any):
        self.rx_data.append(int.from_bytes(data, byteorder="big"))
        self.record_time_info()
        if len(self.rx_data) >= self.dump_size:
            self.data_dump_handler(self.rx_data, self.rx_timestamps, self.rx_delays)
            self.clear_lists()

        print("detected something: ")
        print(data)
        publish.single(topic=topic, payload=data, hostname=broker, port=port, client_id=client_id,
                       auth={'username': username, 'password': password})

#############
# Loops
#############
async def user_console_manager(connection: Connection):
    while True:
        if connection.client and connection.connected:
            input_str = await ainput("Enter string: ")
            bytes_to_send = bytearray(map(ord, input_str))
            await connection.client.write_gatt_char(write_characteristic, bytes_to_send)
            print(f"Sent: {input_str}")
        else:
            await asyncio.sleep(2.0, loop=loop)


async def main():
    while True:
        # YOUR APP CODE WOULD GO HERE.
        print("main")
        await asyncio.sleep(5)



#############
# App Main
#############


if __name__ == "__main__":

    # Create the event loop.
    loop = asyncio.get_event_loop()

    data_to_file = DataToFile(output_file)

    connection = Connection(
        loop, read_characteristic
    )
#     connection = Connection(
#         loop, read_characteristic, write_characteristic, data_to_file.write_to_csv
#     )
    try:
        asyncio.ensure_future(connection.manager())
        #asyncio.ensure_future(user_console_manager(connection))
        asyncio.ensure_future(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(connection.cleanup())
