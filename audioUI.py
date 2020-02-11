import speech_recognition as sr
import pyttsx3
import sys
from googletrans import Translator

tts = pyttsx3.init()

def speak(tts, text):
    tts.say(text)
    tts.runAndWait()

# Gets user input and adds the exit program option so they can quit
def getUserInput(prompt, options):

    options.append("Exit program")

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

                # Checking if input matches an option (either number or the text)
                isOption = False
                i = 0
                numOption = -1
                while i < len(options) and not(isOption):
                    if options[i].lower() == user_input or str(i+1) == user_input:
                        isOption = True
                        numOption = i+1
                    i += 1

                # exits if they select exit of the last option (which is always exit)
                if user_input == "exit program" or numOption == len(options):
                    sys.exit()

                # handles invalid option selected
                if not(isOption):
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

    return numOption

def main():
    # translator = Translator()
    # translation = translator.translate('안녕하세요.')
    # print(translation.text)
    # print(translation)


    # options = ["Translate using a source and destination language", "Translate via auto detection and a destination language"]
    options = ["test 1","test 2"]
    # prompt = "This program is a text-to-speech based language translator.\nUse your voice to select one of the options below by saying the option or the number associated with it."
    temp = getUserInput("yeet", options)
    print(temp)

if __name__ == "__main__":
    main()