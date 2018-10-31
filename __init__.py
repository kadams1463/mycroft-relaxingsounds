#################################################
# Library Imports
#################################################

# Import the libraries for the Mycroft skill.
from mycroft.skills.core import MycroftSkill, intent_handler
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
# Base Code for Author and Logging
#################################################

# Add the author and enable logging.
__author__ = 'kadams1463'

LOGGER = getLogger(__name__)

#################################################
# Class Definition and Super
#################################################

# Set the skill path.
skill_path = "/opt/mycroft/skills/mycroft-relaxingsounds.kadams1463/"
sys.path.append(skill_path)

# to_system definition from MyCroft AI (@MycroftAI) default alarm skill. Thank you!
try:
    from mycroft.util.time import to_system
except:
    # Until to_system is included in 18.08.3, define it here too
    from dateutil.tz import gettz, tzlocal
    def to_system(dt):
        """ Convert a datetime to the system's local timezone
        Args:
            dt (datetime): A datetime (if no timezone, assumed to be UTC)
        Returns:
            (datetime): time converted to the local timezone
        """
        tz = tzlocal()
        if dt.tzinfo:
            return dt.astimezone(tz)
        else:
            return dt.replace(tzinfo=gettz("UTC")).astimezone(tz)

# Create the RelaxingSoundsSkill class.
class RelaxingSoundsSkill(MycroftSkill):

    def __init__(self):
        super(RelaxingSoundsSkill, self).__init__(name="RelaxingSoundsSkill")
        self.process = None

        # Sound interval for the sounds.
        self.sound_interval = 29

#################################################
# Skill Initialization and Intent Building
#################################################

    # Initialize the RelaxingSoundsSkill.
    def initialize(self):

        # Create the Request<Sound>Intent using the required request.voc file and optional <sound>.voc files.
        white_noise_intent = IntentBuilder("RequestWhiteNoiseIntent").require("request").require("white-noise").build()
        wave_sound_intent = IntentBuilder("RequestWaveIntent").require("request").require("wave").build()
        rain_sound_intent = IntentBuilder("RequestRainIntent").require("request").require("rain").build()

        # Callback for intents.
        self.register_intent(white_noise_intent, self.handle_white_noise_intent)
        self.register_intent(wave_sound_intent, self.handle_wave_sound_intent)
        self.register_intent(rain_sound_intent, self.handle_rain_sound_intent)

#################################################
# Mycroft Responses for Each Sound
#################################################

    # Create the dialog from the response.dialog for Mycroft to speak.
    # White Noise
    def handle_white_noise_intent(self, message):
        self.speak_dialog("response")
        wait_while_speaking()
        self.play_white_noise()

    # Waves
    def handle_wave_sound_intent(self, message):
        self.speak_dialog("response")
        wait_while_speaking()
        self.play_waves()

    # Rain
    def handle_rain_sound_intent(self, message):
        self.speak_dialog("response")
        wait_while_speaking()
        self.play_rain()

#################################################
# Play Sound Files
#################################################

    def play_white_noise(self, message=None):
        now = now_local()
        self.sound_repeat = self.sound_interval
        next_loop = now + timedelta(seconds=(self.sound_repeat))
        self.cancel_scheduled_event('Loop')
        self.schedule_event(self.play_white_noise, to_system(next_loop), name='Loop')
        if self.process:
            self.process.kill()
        self.process = play_wav(os.path.join(skill_path, 'sounds/whitenoise.wav'))

    def play_waves(self, message=None):
        now = now_local()
        self.sound_repeat = self.sound_interval
        next_loop = now + timedelta(seconds=(self.sound_repeat))
        self.cancel_scheduled_event('Loop')
        self.schedule_event(self.play_waves, to_system(next_loop), name='Loop')
        if self.process:
            self.process.kill()
        self.process = play_wav(os.path.join(skill_path, 'sounds/waves.wav'))

    def play_rain(self, message=None):
        now = now_local()
        self.sound_repeat = self.sound_interval
        next_loop = now + timedelta(seconds=(self.sound_repeat))
        self.cancel_scheduled_event('Loop')
        self.schedule_event(self.play_rain, to_system(next_loop), name='Loop')
        if self.process:
            self.process.kill()
        self.process = play.wav(os.path.join(skill_path, 'sounds/rain.wav'))

#################################################
# Stop Request Section
#################################################

    def stop(self):
        if self.process:
            self.speak_dialog("stop-sound")
            self.process.kill()
            self.cancel_scheduled_event('Loop')
            self.process = None
            

def create_skill():
    return RelaxingSoundsSkill()