import speech_recognition as sr
import pyttsx3
import sys


tts = pyttsx3.init()


def speak(tts, text):
    tts.say(text)
    tts.runAndWait()

# Gets user input and adds the exit game option so they can quit whenever
def getUserInput(prompt, options):

    options.append("Exit game")

    # get audio from the microphone                                                                       
    listener = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        isInvalid = True

        # Checking if the input matches an option/exceptions
        while isInvalid:
            print(prompt)
            speak(tts, prompt)

            # Displaying options and tts-ing them
            for i in range(len(options)):
                print(str(i+1) + ":\t" + options[i])
                speak(tts, options[i])

            user_input = None

            #record audio
            audio = listener.listen(source)
            try:
                isInvalid = False

                #convert audio to text
                user_input = listener.recognize_google(audio)

                # Checking if input matches an option
                isOption = False
                i = 0
                while i < len(options) and isOption == False:
                    if options[i].lower() == user_input:
                        isOption = True
                    i += 1

                if user_input == "exit game":
                    sys.exit()

                if isOption == False:
                    isInvalid = True
                    invalidPrompt = "Please try again, what you said did not match one of the options."
                    print(invalidPrompt)
                    speak(tts, invalidPrompt)

            except sr.UnknownValueError:
                isInvalid = True
                print("Could not understand audio")
            except sr.RequestError as e:
                isInvalid = True
                print("Could not request results; {0}".format(e))

            sys.stdout.write("\n")

    return user_input

def main():
    options = ["hello", "no"]
    temp = getUserInput("yeet", options)
    print(temp)

if __name__ == "__main__":
    main()