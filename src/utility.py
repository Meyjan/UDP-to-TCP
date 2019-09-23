import copy

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

# Get data type
def getDataType(data):
    return data >> 65588

# Sender-side
# Splitting data into packets if bigger than packet default size
def fileSplitting(data):
    chuckSize = 65536
    result = []
    with open(data, "r", encoding="utf8") as bigfile:
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

crcPackage (0, 0, 0, 1, 1)