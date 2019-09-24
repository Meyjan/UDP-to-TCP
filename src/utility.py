import copy
import sys
MAX_PACKET_SIZE = 32775
# Receiver-side
# Classification of input
def packageOpening(data):
    dataType = data >> 65588
    dataId = (data >> 65584) & 15
    dataSequences = (data >> 65568) & 255
    dataLength = (data >> 65552) & 255
    dataChecksum = (data >> 65536) & 255
    dataReal = data ^ (data << 65536)
    return (dataType, dataId, dataSequences, dataLength, dataChecksum, dataReal)

# Sender-side
# Splitting data into packets if bigger than packet default size
def fileSplitting(data):
    chuckSize = 32775
    result = []
    with open(data, "rb") as bigfile:
        fileChunk = bigfile.read(chuckSize)
        while fileChunk:
            result.append(fileChunk)
            fileChunk = bigfile.read(chuckSize)
    return result

# Counting data length
def lengthCount(data):
    data2 = copy.deepcopy(data)
    count = 0
    while (data2):
        count += 1
        data2 >>= 8
    return count

# Setting the checksum for data
def crcPackage(dataType, dataId, dataSequence, dataLength, data):

    data <<= 16
    data += dataLength << 65568
    data += dataSequence << 65584
    data += dataId << 655
    while data >= 65535:
        print("run 1")
        key = 65535
        dataLength = lengthCount(data)
        key <<= (dataLength - 16)
        data ^= key
        print(data)
    print (data)
        


# Create message
def createPackage(dType, dId, dSequence, dLength, dChecksum, dReal):
    result = dType << 65588
    result += dId << 65584
    result += dSequence << 65568
    result += dLength << 65552
    result += dChecksum << 65536
    result += dReal
    return result

# Create response
def createResponse(number):
    return number << 65588

# Creating data sequence

# crcPackage (0, 0, 0, 1, 1)

def createPacketWithoutCheckSum(pType, pId, pSequenceNum, pData) :
    #Packet Type and ID
    packet = bytearray([(pType << 4) + pId])

    # Packet Sequence Number
    packet += bytearray([pSequenceNum >> 8])
    packet += bytearray([pSequenceNum % 256])

    # Packet length
    packet += bytearray([countLengthData(pData) >> 8])
    packet += bytearray([countLengthData(pData) % 256])

    # Empty packet for checksum
    packet += bytearray([0])
    packet += bytearray([0])

    #Packet Data
    packet += bytearray(pData,'utf8')
    return packet

def countCheckSum(packet) :
    if(isPacketOdd(packet)):
        packet += bytearray([0])

    checksum = (packet[0] << 8) + packet[1]

    for i in range(2, (len(packet) - 1) ,2):
        operand = (packet[i] << 8) + packet[i + 1]
        checksum ^= operand

    return checksum
    
def createPacketWithChecksum(packet,checksum) :
    packet[5] = checksum >> 8
    packet[6] = checksum % 256
    return packet

def countLengthData(pData) :
    return len(pData)

def isPacketOdd(packet):
    return len(packet) % 2 == 1
    

# Receiver Utility

def getPacketID(packet):
    packetByteArr = bytearray(packet)
    pID = packetByteArr[0] % 256
    return pID

def getPacketType(packet):
    packetByteArr = bytearray(packet)
    pType = packetByteArr[0] >> 4
    return pType

def getPacketSequenceNumber(packet):
    packetByteArr = bytearray(packet)
    return packetByteArr[1] << 8 + packetByteArr[2]

def getLengthData(packet):
    packetByteArr = bytearray(packet)
    return packetByteArr[3] << 8 + packetByteArr[4]

def getChecksum(packet):
    packetByteArr = bytearray(packet)
    print("index 5",packetByteArr[5])
    print("index 6", packetByteArr[6])
    return packetByteArr[5] * 256 + packetByteArr[6]

def getData(packet):
    pData = packet[8:len(packet)]
    return pData

def removeChecksum(packet):
    packetByteArr = bytearray(packet)
    packetByteArr[5] = bytearray([0])
    packetByteArr[6] = bytearray([0])
    return bytes(packetByteArr)

def removeData(packet):
    packet = packet[0:8]

def returnACK(packet):
    pType = getPacketType(packet)
    rType = 0
    if (pType == 0x00):
        rType = 0x01
    else:
        rType = 0x03

    packet = packet[0:7]
    packet = bytearray(packet)
    packet[0] = (int(packet[0]) % 256) + (rType << 4)

    return bytes(packet)