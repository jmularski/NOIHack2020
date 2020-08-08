
from network import LoRa
import socket
import machine
import time

# initialise LoRa in LORA mode
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, sf=7)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)


def start_sending(num_chunks):

    # send some data
    s.setblocking(True)
    s.send('START|' + str(num_chunks))
    time.sleep(2)

    for i in range(5):
        # get any data received...
        s.setblocking(False)
        data = s.recv(64)

        if data == b"OK":
            return True

        # wait a random amount of time
        time.sleep(1)

    return False


def send_chunks(chunks):
    s.setblocking(True)
    for i, chunk in enumerate(chunks):
        s.send("{0:b}".format(i) + chunk)


def resend_wrong_chunks(chunks):
    while True:
        s.setblocking(False)
        data = s.recv(64)

        if len(data) == 0:
            continue

        if data == b"OK":
            return
        else:
            data = data.decode('utf-8')
            malformed_chunks = [int(data[i:i+8], 2)
                                for i in range(0, len(data), 8)]

            for chunk in malformed_chunks:
                s.send("{0:b}".format(chunk) + chunks[chunk])


chunks = ['011000001010101111110111010111111010100111110100010111101010100111110011010111111010101111110100010111101010101011110011010111101010101111110010010111001010110011101111010111101010110011110000011000001010110011110001',
          '010111011010100111110010010110111010100011110011010111111010100011110101010111111010011011110011010110111010011011110100010111001010011111110111010111101010011111110001010111011010101111101111010110101010100011110000',
          '011000001010010111110000011000001010010011110011010111101010001111110010010111111010011011101101010111001010001011101110010111011010010011110000010111001010011111101101010111001010011111101110010110101010011111101101',
          '010110101010011111101101010110111010101111101101010110111010101011101101010101101010010111101101010110001010011011110001010111111010100011110000010101101010100011101001010110101010010011101111011000101010010111101101',
          '011000101010010011101011010111111010000111110000010111111010001111110100010111011010011011101101010111001010010011110000011000001010011111101110010111001010011111110000010110101010011011110100010111001010100111110010',
          '010101111010010011110111010110101010011011110010010110101010001111110011010110011010001111110110010110111010001111110100010111001010010011110011010111101010010011110110010111111010010111110100010111001010001111110001',
          '010111001010010011110001010111011010010111110010010110111010011011110010010111011010010011110001010110111010001011101111010111011010011011110000010110111010001011101111010110111010010011101101010111001010011011101111',
          '010110101010010011101101010110111010001111101101010110011010000011101101010101011010011011101101010111011010010111101100010111101001111111101000010101011010010111101110010111011010011011101101010111111010000011101011',
          '010110011001101111110011010111001010000011110010010101101010010011101111010101101010000111101110010101111001111111101111010101011010001111110101010101001010001011101010010101111010001011101100010110011001111011110101',
          '010101111001100111110110010110001001111011110100010101101010000111101101010110011001110111110001010110111001111111110101010110101010001011101111010110101010000011101101010110011001110011101100010110001010000011101011']
ack_message = False
while not ack_message:
    ack_message = start_sending(len(chunks))
print("received ACK message")
send_chunks(chunks)
resend_wrong_chunks(chunks)
