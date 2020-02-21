import speech_recognition as sr
import pyttsx3
import sys
from googletrans import Translator, LANGUAGES

tts = pyttsx3.init()
translator = Translator()

langOptions = dict(map(reversed, LANGUAGES.items()))

# Modifying some of the keys/values because tts makes these difficult to select or repeats
del langOptions["Filipino"]                         #Filipino had two keys so removed the capitalized version
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


def speak(tts, text):
    tts.say(text)
    tts.runAndWait()


def listLanguages():
    i = 1
    print("Available languages:")
    for key in langOptions.keys():
        key = key.capitalize()
        print(str(i) + ":\t" + key)
        i += 1
    print()

# Translate using language codes


def translate(sourceCode, destCode, toTranslate):
    translation = translator.translate(toTranslate, src=sourceCode, dest=destCode)
    text = translation.text
    print(text)
    speak(tts, text)

# Translates using auto detection
def translateAuto(destCode, toTranslate):
    translation = translator.translate(toTranslate, dest=destCode)
    text = translation.text
    print(text)
    speak(tts, text)

# determines what language the user wants for translation and selects the proper language code
def getLanguageInput(prompt):

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

            # record audio
            audio = listener.listen(source)
            try:

                # convert audio to text
                user_input = listener.recognize_google(audio)

                # Checking if they said one of the languages
                if user_input.lower() in langOptions:
                    print(user_input)
                    langCode = langOptions.get(user_input.lower())
                    isInvalid = False
                else:
                    invalidPrompt = "Please try again, what you said did not match one of the languages."
                    print(invalidPrompt)
                    speak(tts, invalidPrompt)

            except sr.UnknownValueError:
                isInvalid = True
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results, exiting; {0}".format(e))
                sys.exit()

            sys.stdout.write("\n")

    return langCode

# Gets speech for translation (loops if cannot understand audio, if request fails just exits)
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

            # record audio
            audio = listener.listen(source)
            try:
                isInvalid = False

                # convert audio to text
                user_input = listener.recognize_google(audio)

            except sr.UnknownValueError:
                isInvalid = True
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results, exiting; {0}".format(e))
                sys.exit()

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
                toPrint = str(i+1) + ":\t" + options[i]
                print(toPrint)
                speak(tts, toPrint)

            user_input = None

            # record audio
            audio = listener.listen(source)
            
            try:
                isInvalid = False

                # convert audio to text
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

# Wrapper for selecting language
def languageMenu(prompt, option):

    optionSelected = 0
    while optionSelected != 1:
        options = ["Select " + option + " language", "List languages"]
        prompt = "Select an option below:"
        optionSelected = getMenuInput(prompt, options)

        if optionSelected == 2:
            listLanguages()

    langPrompt = "Say the " + option + " language's name:"
    langCode = getLanguageInput(langPrompt)

    return langCode


def main():

    print("This program is a text-to-speech based language translator.")
    speak(tts, "This program is a text-to-speech based language translator.")

    while True:

        options = ["Translate using a source and destination language", "Translate using auto detection and a destination language"]
        prompt = "\nUse your voice to select one of the options below by saying the option or the number associated with it."

        optionSelected = getMenuInput(prompt, options)

        if optionSelected == 1:

            option = "source"
            prompt = "Select an option below:"
            sourceCode = languageMenu(prompt, option)

            option = "destination"
            prompt = "Select an option below:"
            destCode = languageMenu(prompt, option)
        
            translatePrompt = "Say what you would like to be translated:"
            toTranslate = getTranslationInput(translatePrompt)
            print(toTranslate.capitalize() + "\n")

            print("Translation: ")
            speak(tts, "Translation: ")
            translate(sourceCode, destCode, toTranslate)

        if optionSelected == 2:

            option = "destination"
            prompt = "Select an option below:"
            destCode = languageMenu(prompt, option)

            translatePrompt = "Say what you would like to be translated:"
            toTranslate = getTranslationInput(translatePrompt)
            print(toTranslate.capitalize() + "\n")

            print("Translation: ")
            speak(tts, "Translation: ")
            translateAuto(destCode, toTranslate)


if __name__ == "__main__":
    main()
