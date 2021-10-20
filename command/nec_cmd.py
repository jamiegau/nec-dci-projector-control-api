#!/usr/bin/python3
import socket
import sys
import argparse
import re

#defaults
projector_ip: str = '10.30.100.12'
network_port: int = 43728

def Main():
    global projector_ip
    parser = argparse.ArgumentParser(description='Command line to control NEC Digital Cinema Projectors.')

    command_help = 'Command to send Projector:' 
    command_help += 'serial, power_status, power_on, power_off, version_data_request, '
    command_help += 'input_switch_change, picture_mute_on, picture_mute_off, '
    command_help += 'dowser_open, dowser_close, lamp_info_request2, input_status_request, '
    command_help += 'mute_status_request, lamp_on, lamp_off, lamp_mode'

    parser.add_argument('command', metavar='cmd', type=str,
                        help=command_help)

    parser.add_argument('-ip', dest='ip',
                        help=f'Projector IP (Default: {projector_ip})')

    parser.add_argument('-channel', dest='channel',
                        help=f'Switch to channel (1-99')

    args = parser.parse_args()

    if args.ip:
        projector_ip = args.ip

    if args.command == 'serial':
        ProjSerial()
    elif args.command == 'power_status':
        ProjPowerStatus()
    elif args.command == 'power_on':
        ProjPowerOn()
    elif args.command == 'power_off':
        ProjPowerOff()
    elif args.command == 'version_data_request':
        ProjVersionDataRequest()
    elif args.command == 'input_switch_change':
        if args.channel is None:
            print('Channel not supplied')
            return
        else:
            ProjInputSwitchChange(int(args.channel))
    elif args.command == 'picture_mute_on':
        ProjPictureMute('on')
    elif args.command == 'picture_mute_off':
        ProjPictureMute('off')
    elif args.command == 'dowser_open':
        ProjDowser('open')
    elif args.command == 'dowser_close':
        ProjDowser('close')
    elif args.command == 'lamp_info_request2':
        ProjLampInfoRequest2()
    elif args.command == 'input_status_request':
        ProjInputStatusRequest()
    elif args.command == 'mute_status_request':    
        ProjMuteStatusRequest()
    elif args.command == 'lamp_on':
        ProjLamp('on')
    elif args.command == 'lamp_off':
        ProjLamp('off')
    elif args.command == 'lamp_mode':
        ProjLampMode()
    else:
        print('Command not supported')


def ProjSerial():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    print(f'Connected to {projector_ip}:{network_port}')
    try:
        s.connect((projector_ip, network_port))
    except OSError as eee:
        print(f'Error connecting to projector: {eee}')
        sys.exit(-1)
    message = b'\x00\x86\x00\xC0\x01\x08\x4f'
    s.send(message)
    try:
        data = s.recv(4096)
        data = data.replace(b'\x86\x00\xc0\x11\x08', b'')
        data = data.replace(b'\x00\x00\x00\x00\x00\x00\x00u', b'')
        print(f'Received: ({data.decode("utf-8").strip()})')
    except socket.timeout:
        pass
    s.close()
    return


def ProjPowerStatus():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    # message = b'\x00\x85\x00\x00\x01\x01\x87'
    message = b'\x00\x85\x00\x00\x01\x01\x87'
    message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)

    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')

        # External_Control_Status
        if data[6] == 0:
            External_Control_Status = 'Off'
        elif data[6] == 1:
            External_Control_Status = 'On'
        else:
            External_Control_Status = 'Unknown'
        print(f'External_Control_Status: {External_Control_Status}')

        # Power_Status
        if data[7] == 0:
            Power_Status = 'Off'
        elif data[7] == 1:
            Power_Status = 'On'
        else:
            Power_Status = 'Unknown'
        print(f'Power_Status: {Power_Status}')

        # Lamp Cooling Processing
        if data[8] == 0:
            Lamp_Cooling_Processing = 'No execution'
        elif data[8] == 1:
            Lamp_Cooling_Processing = 'During execution'
        else:
            Lamp_Cooling_Processing = 'Unknown'
        print(f'Lamp_Cooling_Processing: {Lamp_Cooling_Processing}')

        # On/Off Processing
        if data[9] == 0:
            On_Off_Processing = 'No execution'
        elif data[9] == 1:
            On_Off_Processing = 'During execution'
        else:
            On_Off_Processing = 'Unknown'
        print(f'On_Off_Processing: {On_Off_Processing}')

        # Projector Process Status
        if data[10] == 0:
            Projector_Process_Status = 'Standby'
        elif data[10] == 1:
            Projector_Process_Status = 'Power On Protect (before Lamp(Light) control)'
        elif data[10] == 2:
            Projector_Process_Status = 'Ignition'
        elif data[10] == 3:
            Projector_Process_Status = 'Power On Running'
        elif data[10] == 4:
            Projector_Process_Status = 'Running (Power On / Lamp(Light) On)'
        elif data[10] == 5:
            Projector_Process_Status = 'Cooling'
        # b'06' Reserved
        elif data[10] == 7:
            Projector_Process_Status = 'Reset Wait'
        elif data[10] == 8:
            Projector_Process_Status = 'Fan Stop Error (before Cooling)'
        elif data[10] == 9:
            Projector_Process_Status = 'Lamp Retry'
        elif data[10] == 10:
            Projector_Process_Status = 'Lamp(Light) Error (before Cooling)'
        elif data[10] == 12:
            Projector_Process_Status = 'Running (Power On / Lamp(Light) Off)'    
        else:
            On_Off_Processing = 'Unknown'
        print(f'Projector_Process_Status: {Projector_Process_Status}')

        # Store Processing
        if data[13] == 0:
            Store_Processing = 'No execution'
        elif data[13] == 1:
            Store_Processing = 'During execution'
        else:
            Store_Processing = 'Unknown'
        print(f'Store_Processing: {Store_Processing}')

        # Lamp Status
        if data[14] == 0:
            Lamp_Status = 'Lamp(Light) Off'
        elif data[14] == 1:
            Lamp_Status = 'Lamp(Light) On,  Dual-Lamp: Lamp1 On/Lamp2 Off'
        elif data[14] == 2:
            Lamp_Status = 'Lamp1 Off/Lamp2 On'
        elif data[14] == 3:
            Lamp_Status = 'Lamp1and2 On'
        else:
            Lamp_Status = 'Unknown'
        print(f'Lamp_Status: {Lamp_Status}')

        # Processing of Lamp
        if data[15] == 0:
            Processing_of_Lamp = 'No execution'
        elif data[15] == 1:
            Processing_of_Lamp = 'During execution'
        else:
            Processing_of_Lamp = 'Unknown'
        print(f'Processing_of_Lamp: {Processing_of_Lamp}')

        # Lamp Mode Setting (NC900C-A and NC1000C)
        if data[16] == 0:
            Lamp_Mode_Setting = 'Dual'
        elif data[16] == 1:
            Lamp_Mode_Setting = 'Lamp1'
        elif data[16] == 2:
            Lamp_Mode_Setting = 'Lamp2'
        else:
            Lamp_Mode_Setting = 'Unknown'
        print(f'Lamp_Mode_Setting: {Lamp_Mode_Setting}  (NC900C-A and NC1000C)')

        # Cooling Remaining Time(in sec)
        b_low = data[17]
        b_high = data[18]
        Cooling_Remaining_Time = int.from_bytes(bytes([b_high, b_low]), 'little')
        print(f'Cooling_Remaining_Time: {Cooling_Remaining_Time} seconds')

        # Remaining Time of Lamp
        b_low = data[19]
        b_high = data[20]
        Remaining_Time_of_Lamp = int.from_bytes(bytes([b_high, b_low]), 'big')
        print(f'Remaining_Time_of_Lamp: {Remaining_Time_of_Lamp} hours (NC900C and NC1000C')

    except socket.timeout:
        pass
    s.close()
    return


def ProjPowerOn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    message = b'\x02\x00\x00\x00\x00\x02'
    message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if b'\x00\x00\xc0\x00\xe2' in data:
            print(f'power_on Command OK')
        elif b'\x00\x00\xc0\x00\xe2' in data:
            print('Projector appears to be already ON')
    except socket.timeout:
        pass
    s.close()
    return

def ProjPowerOff():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    message = b'\x02\x01\x00\x00\x00\x03'
    message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if b'\x02\x01\x00\x00\x00\x03' in data:
            print(f'power_off Command OK')
        elif b'\x01\x00\xc0\x00\xe3' in data:
            print('Projector appears to be already OFF')
    except socket.timeout:
        pass
    s.close()
    return


def ProjVersionDataRequest():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    message1 = b'\x00\x86\x00\xc0\x01'
    message_main = message1 + b'\x08'  # Unit Serial Number
    # print('{}  should = 05'.format(calculate_cks(b'\x02\x03')))
    cks = calculate_cks(message_main)
    message = message_main + cks
    message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if data.startswith(b'\x20\x86\x00\xc0\x11'):
            chars = []
            for iter in range(6, 16):
                if data[iter] != 00:
                    chars.append(chr(data[iter]))
            Serial_No = ''.join(chars)
            print(f'Got response, Serial Number: {Serial_No}')
    except socket.timeout:
        print('Message Ignored.  Was it CRC corectly?')
    s.close()
    return


# INPUT SW CHANGE
def ProjInputSwitchChange(channel_number):
    channel_number -= 1  # as interface starts on 1, not 0.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    message1 = b'\x02\x03\x00\x00\x02\x00'
    message_main = message1 + channel_number.to_bytes(1, 'big')  # change to channel number
    cks = calculate_cks(message_main)
    message = message_main + cks
    message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if data.startswith(b'\x22\x03\x00\xc0\x01\x00'):
            print('Success')
        else:
            print('Error')

    except socket.timeout:
        print('Message Ignored.  Was it CRC corectly?')
    s.close()
    return


# PictureMute (Note this is not the dowser, its digital mute.)
def ProjPictureMute(mute):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    if mute == 'off':
        message = b'\x02\x11\x00\x00\x00\x13'
        message_hex_str = rejoined(message.hex(), sep=':')
    elif mute == 'on':
        message = b'\x02\x10\x00\x00\x00\x12'
        message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if data.startswith(b'\x22\x10\x00\xc0\x00') or data.startswith(b'\x22\x11\x00\xc0\x00'):
            print('Success')
        else:
            print('Error')

    except socket.timeout:
        print('Message Ignored.  Was it CRC corectly?')
    s.close()
    return


# ProjDowser
def ProjDowser(open_close):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    if open_close == 'open':
        message = b'\x02\x17\x00\x00\x00\x19'
        message_hex_str = rejoined(message.hex(), sep=':')
    elif open_close == 'close':
        message = b'\x02\x16\x00\x00\x00\x18'
        message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if data.startswith(b'\x22\x16\x00\xc0\x00') or data.startswith(b'\x22\x17\x00\xc0\x00'):
            print('Success')
        else:
            print('Error')

    except socket.timeout:
        print('Message Ignored.  Was it CRC corectly?')
    s.close()
    return


# ProjLampInfoRequest
def ProjLampInfoRequest2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    message = b'\x03\x94\x00\x00\x00\x97'
    message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if data.startswith(b'\x23\x94\x00\xc0\x05'):
            # get the result
            # Cooling Remaining Time(in sec)
            n1 = data[5]
            n2 = data[6]
            n3 = data[7]
            n4 = data[8]
            lamp_time_in_seconds = int.from_bytes(bytes([n1, n2, n3, n4]), 'little')
            print(f'Lamp time in seconds: {lamp_time_in_seconds} seconds')
        else:
            print('Error')

    except socket.timeout:
        print('Message Ignored.  Was it CRC corectly?')
    s.close()
    return


# ProjInputStatusRequest
def ProjInputStatusRequest():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    message = b'\x00\x85\x00\x00\x01\x02\x88'
    message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if data.startswith(b'\x20\x85\x00\xc0\x10'):
            # get the result
            # Cooling Remaining Time(in sec)
            ssp = data[5]
            if ssp == 0:
                Selecting_signal_processing = 'No execution(Normal condition)'
            elif ssp == 1:
                Selecting_signal_processing = 'During execution'
            else:
                Selecting_signal_processing = 'Unknown'
            print(f'Selecting_signal_processing: {Selecting_signal_processing}')
            #
            channel = data[6] + 1  # app starts from 1, not 0
            print(f'Channel Number: {channel}')
            # Port Name
            pn1 = data[7]
            pn2 = data[8]
            if pn1 == 0 and pn2 == 6:
                port_name = 'Test Patten'
            elif pn1 == 1 and pn2 == 6:
                port_name = '292A'
            elif pn1 == 2 and pn2 == 6:
                port_name = '292B'
            elif pn1 == 1 and pn2 == 13:
                port_name = '292C'
            elif pn1 == 2 and pn2 == 13:
                port_name = '292D'
            elif pn1 == 3 and pn2 == 6:
                port_name = '292Dual(AB)'
            elif pn1 == 3 and pn2 == 13:
                port_name = '292Dual(CD'
            elif pn1 == 4 and pn2 == 13:
                port_name = '292Quad'
            elif pn1 == 1 and pn2 == 12:
                port_name = 'DVIA'
            elif pn1 == 2 and pn2 == 12:
                port_name = 'DVIB'
            elif pn1 == 3 and pn2 == 12:
                port_name = 'DVI Dual/Twin'
            elif pn1 == 4 and pn2 == 12:
                port_name = 'IMB'
            else:
                port_name = 'Unknown'
            print(f'Port Name: {port_name}')
            #
            tp = data[10]
            if tp == 0:
                test_pattern_status = 'No Display (Normal condition)'
            elif tp == 1:
                test_pattern_status = 'Displaying'
            else:
                test_pattern_status = 'Unknown'
            print(f'Test Pattern: {test_pattern_status}')
        else:
            print('Error')

    except socket.timeout:
        print('Message Ignored.  Was it CRC corectly?')
    s.close()
    return

#ProjMuteStatusRequest
def ProjMuteStatusRequest():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    message = b'\x00\x85\x00\x00\x01\x03\x89'
    message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if data.startswith(b'\x20\x85\x00\xc0\x10'):
            msr = data[5]
            if msr == 0:
                Picture_mute = 'OFF'
            elif msr == 1:
                Picture_mute = 'ON'
            else:
                Picture_mute = 'Unknown'
            print(f'Picture_mute: {Picture_mute}')
        else:
            print('ERROR')
    except socket.timeout:
        pass
    s.close()
    return
#
# ProjLamp
def ProjLamp(on_off):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    if on_off == 'on':
        message = b'\x03\x2f\x00\x00\x02\x12\x01'
        message = message + calculate_cks(message)
        message_hex_str = rejoined(message.hex(), sep=':')
    elif on_off == 'off':
        message = b'\x03\x2f\x00\x00\x02\x12\x02'
        message = message + calculate_cks(message)
        message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if data.startswith(b'\x23\x2f\x00\xc0\x02'):
            print('Success')
        else:
            print('Error')

    except socket.timeout:
        print('Message Ignored.  Was it CRC corectly?')
    s.close()
    return
#
# ProjLampMode
def ProjLampMode():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((projector_ip, network_port))
    print(f'Connected to {projector_ip}:{network_port}')
    message = b'\x03\x2f\x00\x00\x01\x11\x44'
    message_hex_str = rejoined(message.hex(), sep=':')
    print(f' Message: {message_hex_str}')
    s.send(message)
    try:
        data = s.recv(4096)
        data_hex_str = rejoined(data.hex(), sep=':')
        print(f'Response: {data_hex_str}')
        if data.startswith(b'\x23\x2f\x00\xc0\x02\x11'):
            lcm = data[6]
            if lcm == 0:
                Lamp_Control_Mode = 'Standard mode in conjunction with Power On/Off'
            elif lcm == 1:
                Lamp_Control_Mode = 'Lamp(Light) On Mode'
            elif lcm == 2:
                Lamp_Control_Mode = 'Lamp(Light) Off Mode'
            else:
                Lamp_Control_Mode = 'Unknown'
            print(f'Lamp_Control_Mode: {Lamp_Control_Mode}')
        else:
            print('Error')

    except socket.timeout:
        print('Message Ignored.  Was it CRC corectly?')
    s.close()
    return
#
######################################################################################
#

def calculate_cks(msg):
    crc = sum(msg) % 256
    # calc = 0
    # for b in msg:
    #     calc += b
    # res = bytes(calc)
    return crc.to_bytes(1, 'big')


def rejoined(src, sep='-', _split=re.compile('..').findall):
    return sep.join(_split(src))

if __name__ == '__main__':
    Main()
