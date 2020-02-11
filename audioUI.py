import speech_recognition as sr
import pyttsx3
import sys
from googletrans import Translator, LANGUAGES

tts = pyttsx3.init()

def speak(tts, text):
    tts.say(text)
    tts.runAndWait()

def listLanguages(langOptions):
    i = 1
    for key in langOptions.keys():
        key = key.capitalize()
        print(str(i) + ":\t" + key)
        i+=1

# gets speech for translation (loops if cannot understand audio, if request fails just exits)
def getTranslationInput(prompt):

    # get audio from the microphone                                                                       
    listener = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        isInvalid = True

        # Checking if the input matches an option/exceptions
        while isInvalid:
            print(prompt)
            speak(tts, prompt)

            user_input = None

            #record audio
            audio = listener.listen(source)
            try:
                isInvalid = False

                #convert audio to text
                user_input = listener.recognize_google(audio)

            except sr.UnknownValueError:
                isInvalid = True
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results, exiting; {0}".format(e))
                sys.exit()

            sys.stdout.write("\n")

    return user_input



# Gets user input and adds the exit program option so they can quit at any point
def getMenuInput(prompt, options):

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
                print("Could not request results, exiting; {0}".format(e))
                sys.exit()

            sys.stdout.write("\n")

    return numOption

def main():
    # HOW TO USE TRANSLATOR
    # translator = Translator()
    # translation = translator.translate('안녕하세요.')
    # print(translation.text)
    # print(translation)

    # HOW TO ACCESS LANGUAGES FOR TRANSLATION   
    langOptions = dict(map(reversed, LANGUAGES.items()))

    # Modifying some of the keys/values because tts makes these difficult to select or repeats
    del langOptions["Filipino"]
    del langOptions["chinese (simplified)"]
    langOptions["chinese simplified"] = "zh-cn"
    del langOptions["chinese (traditional)"]
    langOptions["chinese traditional"] = "zh-tw"
    del langOptions["myanmar (burmese)"]
    langOptions["myanmar"] = "my"
    del langOptions["Hebrew"]
    langOptions["hebrew"] = "he"
    del langOptions["kurdish (kurmanji)"]
    langOptions["kurdish"] = "ku"
    # print(langOptions["afrikaans"])

    listLanguages(langOptions)

    # options = ["Translate using a source and destination language", "Translate via auto detection and a destination language"]
    # prompt = "This program is a text-to-speech based language translator.\nUse your voice to select one of the options below by saying the option or the number associated with it."
    
    # options = ["test 1","test 2"]
    # optionSelected = getMenuInput("yeet", options)
    # print(optionSelected)

    # if optionSelected == 1:
    #     print("yeet")

    # if optionSelected == 2:
    #     print("yeet")




if __name__ == "__main__":
    main()