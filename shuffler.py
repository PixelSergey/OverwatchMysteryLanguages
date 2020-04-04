import re, random, os

# Change to Battle.net directory; should be the same on all Windows computers
os.chdir(r"C:\ProgramData\Battle.net\Agent")

# Read product.db into data
with open("product.db", "rb") as infile:
    data = infile.read()


# Find initial address by finding the end of the first occurence of the word "Overwatch"
# This should be the filepath and therefore correct; not fully tested
init = data.find(b"Overwatch") + 9
print("End of Overwatch file path: " + str(hex(init)))
# Seek 22 bytes forward, this seems to be constant; not fully tested
start = init + 22
print("Start of language list: " + str(hex(start)))
# Set end position at the string "retail", which seems to occur almost right after the lang list
end = data[start:].find(b"retail") + start
print("End of language list: " + str(hex(end)))

# Split the languages; they are stored in the format "0x42 0x08 0x0A 0x04 xxXX 0x10 0x03" where xxXX is one language
rawlist = re.split(b"\x10\x03|\x42\x08\x0A\x04", data[start:end])
# Cut off last value (junk after the language list) and filter out empty values
rawlist = [r for r in rawlist[:-1] if r]

# Seek back to the start of active language and find out what it is, then remove it from the list of languages
start = init + 12
print("Start of active language: " + str(hex(start)))
current = data[start:start+4]
print("Current language is " + current.decode("utf-8"))
rawlist.remove(current)

# If the list is empty, we know there's only one language installed
if not rawlist:
    print("Only one language installed! Install more from the Battle.net launcher to use the shuffler.")
    exit()

print("Available languages: " + ", ".join([r.decode("utf-8") for r in rawlist]))

# Random language
picked = random.choice(rawlist)
print("The picked language is " + picked.decode("utf-8"))

# Copy data to a new bytearray for modification
newdata = bytearray(data)

# Replace the addresses with the current language with the new language
newdata[start:start+4] = picked
newdata[start+6:start+10] = picked

# Write new file into product2.db
with open("product_new.db", "wb") as outfile:
    outfile.write(newdata)

# Since writing to product.db is forbidden, we simply delete it first and replace it with the new file
os.remove("product.db")
os.rename("product_new.db", "product.db")

print("Written new language data successfully!")
