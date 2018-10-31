# Import the libraries for the Mycroft skill.
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import getLogger
#from mycroft.skills.audioservice import AudioService
from mycroft.util import play_wav, play_mp3
from mycroft.audio import wait_while_speaking
import os
import sys

#################################################

# Add the author and enable logging.
__author__ = 'kadams1463'

LOGGER = getLogger(__name__)

#################################################

# Set the skill path.
skill_path = "/opt/mycroft/skills/mycroft-relaxingsounds.kadams1463/"
sys.path.append(skill_path)

# Create the RelaxingSoundsSkill class.
class RelaxingSoundsSkill(MycroftSkill):

    def __init__(self):
        super(RelaxingSoundsSkill, self).__init__(name="RelaxingSoundsSkill")
        self.process = None

    # Initialize the RelaxingSoundsSkill.
    def initialize(self):
        # AudioService from Mycroft Skills library.
        self.audio_service = AudioService(self.emitter)

        # Create the RequestSoundIntent using the required request.voc file and optional <sound>.voc files.
        white_noise_intent = IntentBuilder("RequestSoundIntent").require("request").require("white-noise").build()

        # Call back for intents.
        self.register_intent(white_noise_intent, self.handle_request_sound_intent)


    # Create the dialog from the response.dialog for Mycroft to speak.
    def handle_request_sound_intent(self, message):
        self.speak_dialog("response")
        #self.audio_service.play("file:///sounds/whitenoise.wav")
        wait_while_speaking()
        play_wav(os.path.join(skill_path, 'sounds/whitenoise.wav'))
        


    def stop(self):
        pass

def create_skill():
    return RelaxingSoundsSkill()