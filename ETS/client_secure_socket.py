import logging
import threading
import time
import datetime
import threading
import random
import sys
import socket
import json
import xmltodict
import ssl
import os

server_address = ('172.16.16.102', 11000)


def make_socket(destination_address='localhost', port=11000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")


def make_secure_socket(destination_address='localhost', port=10000):
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode = ssl.CERT_OPTIONAL
        context.load_verify_locations(os.getcwd() + '/client_certs' + '/domain.crt')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        secure_socket = context.wrap_socket(sock, server_hostname=destination_address)
        logging.warning(secure_socket.getpeercert())
        return secure_socket
    except Exception as ee:
        logging.warning(f"error {str(ee)}")


def deserialisasi(s):
    logging.warning(f"deserialisasi {s.strip()}")
    return json.loads(s)


def send_command(command_str, is_secure=False):
    alamat_server = server_address[0]
    port_server = server_address[1]
    #    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # gunakan fungsi diatas
    if is_secure == True:
        sock = make_secure_socket(alamat_server, port_server)
    else:
        sock = make_socket(alamat_server, port_server)

    # logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received = ""  # empty string
        while True:
            # socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                # data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = deserialisasi(data_received)
        # logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False


def getdatapemain(nomor=0, is_secure=False):
    cmd = f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd, is_secure=is_secure)
    return hasil


def get_nomor_pemain(num_request, is_secure=False):
    for i in range(num_request):
        getdatapemain(random.randint(1, 10), is_secure)


# def lihatversi(is_secure=False):
#     cmd=f"versi \r\n\r\n"
#     hasil = send_command(cmd,is_secure=is_secure)
#     return hasil

def multi_thread(thread=1, num_request=1, is_secure=False):
    texec = dict()

    catat_awal = datetime.datetime.now()
    for k in range(thread):
        texec[k] = threading.Thread(target=get_nomor_pemain, args=(num_request, is_secure))
        texec[k].start()

    # setelah menyelesaikan tugasnya, dikembalikan ke main thread dengan join
    for k in range(thread):
        texec[k].join()

    catat_akhir = datetime.datetime.now()
    selesai = catat_akhir - catat_awal
    print(
        f"Jumlah thread: {thread}, Jumlah request: {num_request}, Jumlah response: {num_request * thread}, Latency: {selesai} detik")


if __name__ == '__main__':
    jml_thread1 = 1
    jml_thread2 = 5
    jml_thread3 = 10
    jml_thread4 = 20

    jml_request_data = 3
    is_secure = True  # mengaktifkan secure socket

    multi_thread(jml_thread4, jml_request_data, is_secure) 