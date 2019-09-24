# Read integer
num = 7
result = bytearray([num])

num = 123
nextResult = bytearray([num])

result += nextResult

# Read string
nextStr = "asdf"
nextByte = nextStr.encode("utf-8")
result += bytearray(nextByte)

# Read file
chuckSize = 32768
file_result = []
with open("487232.jpg", "rb") as bigfile:
    fileChunk = bigfile.read(chuckSize)
    while fileChunk != b"":
        file_result.append(fileChunk)
        fileChunk = bigfile.read(chuckSize)

print(file_result[0][0])
print(file_result[0][1])
print(result)


print(len(file_result))
for res in file_result:
    print("Res:", len(res))
    result += res
    print("Res2:", len(result))

for i in  range(9):
    print(result[i])