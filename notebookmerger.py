import os
with open('C:\\Users\\aadit\\OneDrive\\Documents\\Python Projects\\Handling.py', 'r') as f:
    for line in f:
        print(line)

with open('C:\\Users\\aadit\\OneDrive\\Documents\\Python Projects\\math-notes.txt', 'r') as f:
    for line in f:
        print(line)
    words=line.split()
    print("The number of words in the file are:", len(words))


if os.path.exists('C:\\Users\\aadit\\OneDrive\\Documents\\Python Projects\\all_notes.txt'):
    content = ''
    with open('C:\\Users\\aadit\\OneDrive\\Documents\\Python Projects\\Handling.py', 'r') as f:
        content += f.read()
    with open('C:\\Users\\aadit\\OneDrive\\Documents\\Python Projects\\all_notes.txt', 'r') as fl:
        content += fl.read()
    with open('C:\\Users\\aadit\\OneDrive\\Documents\\Python Projects\\all_notes.txt', 'r') as f:
        content += f.read()
    with open('C:\\Users\\aadit\\OneDrive\\Documents\\Python Projects\\all_notes.txt', 'w') as out:
        out.write(content)
    if os.path.exists('C:\\Users\\aadit\\OneDrive\\Documents\\Python Projects\\all_notes.txt'):
        os.remove('C:\\Users\\aadit\\OneDrive\\Documents\\Python Projects\\all_notes.txt')
    else:
        print("The file does not exist")         


        

    
