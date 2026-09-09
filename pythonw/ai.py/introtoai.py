print("Hello I am your chat bot what's your name?")
name = input()
if name == "Chat bot":
    print("That's funny, my name is also Chat bot!")
else:
    print("Hello " + name + " nice to meet you!")
mood = input("How are you feeling today? ")
if mood == "good":
    print("That's great to hear!")
elif mood == "bad":
    print("I'm sorry to hear that. I hope your day gets better!")
else:
    print("I see. I hope you have a good day regardless!")        
print("It was nice to meet you " + name + "! Have a great day!")    
