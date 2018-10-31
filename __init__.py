# Import the libraries for the Mycroft skill.
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import getLogger
from mycroft.skills.audioservice import AudioService
from mycroft.util import play_wav, play_mp3
from mycroft.util.time import now_local
from mycroft.audio import wait_while_speaking
from mycroft.messagebus.message import Message
from datetime import datetime, timedelta
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

        # Sound interval for the sounds.
        self.sound_interval = 30.0

    # Initialize the RelaxingSoundsSkill.
    def initialize(self):
        # AudioService from Mycroft Skills library.
        #self.audio_service = AudioService(self.emitter)

        # Create the RequestSoundIntent using the required request.voc file and optional <sound>.voc files.
        white_noise_intent = IntentBuilder("RequestSoundIntent").require("request").require("white-noise").build()

        # Call back for intents.
        self.register_intent(white_noise_intent, self.handle_request_sound_intent)

    # Create the dialog from the response.dialog for Mycroft to speak.
    def handle_request_sound_intent(self, message):
        self.speak_dialog("response")
        wait_while_speaking()
        self.play_white_noise()
        #self.audio_service.play("file:///opt/mycroft/skills/mycroft-relaxingsounds.kadams1463/sounds/whitenoise.wav")

    def play_white_noise(self, message=None):
        now = now_local()
        self.sound_repeat = self.sound_interval
        next_loop = now + timedelta(seconds=(self.sound_repeat))
        self.cancel_scheduled_event('Loop')
        self.schedule_event(self.play_white_noise, next_loop, name='Loop')
        if self.process:
            self.process.kill()
        self.process = play_wav(os.path.join(skill_path, 'sounds/whitenoise.wav'))

    def stop(self):
        if self.process:
            self.speak_dialog("stop-sound")
            self.cancel_scheduled_event('Loop')
            self.process = None
            

def create_skill():
    return RelaxingSoundsSkill()