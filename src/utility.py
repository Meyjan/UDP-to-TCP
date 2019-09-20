# Classification of input
def packageOpening(data):
    dataType = data >> 66588
    dataId = (data >> 66584) & 15
    dataSequences = (data >> 66568) & 255
    dataLength = (data >> 66552) & 255
    dataChecksum = (data >> 66536) & 255
    dataReal = data ^ (data << 66536)
    return (dataType, dataId, dataSequences, dataLength, dataChecksum, dataReal)

# Get data type
def getDataType(data):
    return data >> 66588


# Create message
def createPackage(dType, dId, dSequence, dLength, dChecksum, dReal):
    dType = 12 #CHANGE THIS LINE


# Create response
def createResponse(number):
    return number << 66588