import re, random

with open("toconvert.db", "rb") as infile:
    data = infile.read()

init = data.find(b"Overwatch") + 9
print("End of Overwatch file path: " + str(hex(init)))
start = init + 22
print("Start of language list: " + str(hex(start)))
end = data[start:].find(b"retail") + start
print("End of language list: " + str(hex(end)))

rawlist = re.split(b"\x10\x03|\x42\x08\x0A\x04", data[start:end])
rawlist = [r for r in rawlist[:-1] if r]

start = init + 12
print("Start of active langs: " + str(hex(start)))
current = data[start:start+4]
print("Current language is " + str(current))
rawlist.remove(current)
print("Available languages: " + ", ".join([r.decode("utf-8") for r in rawlist]))

picked = random.choice(rawlist)
print("The picked language is " + str(picked))

newdata = bytearray(data)

newdata[start:start+4] = picked
newdata[start+6:start+10] = picked

print(newdata[init:end])

with open("nibba.db", "wb") as outfile:
    outfile.write(newdata)
