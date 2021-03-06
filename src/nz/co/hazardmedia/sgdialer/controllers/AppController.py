__author__ = 'Michael Andrew michael@hazardmedia.co.nz'

import pygame
from pygame.event import Event
from pygame import key
from nz.co.hazardmedia.sgdialer.controllers.DialerController import DialerController
from nz.co.hazardmedia.sgdialer.controllers.SoundController import SoundController
from nz.co.hazardmedia.sgdialer.events.EventType import EventType


class AppController:

    sound_controller = SoundController()
    dialer_controller = DialerController()

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        #init sounds
        self.sound_controller.preload_sounds({
            "dhd-button-press-auto": {"file_name": "dhd-button.wav", "delay_min": 1000, "delay_max": 1500},
            #"dhd-button-press-auto": {"file_name": "dhd-button.wav", "delay": 500},
            "dhd-button-press": {"file_name": "dhd-button.wav"},
            "gate-dial-single": {"file_name": "gate-dial.wav"},
            "gate-engage": {"file_name": "dhd-kawoosh2.wav"},
            "gate-no-engage": {"file_name": "cancel1.wav"},
            "gate-loop": {"file_name": "singlepuddle.wav"},
            "gate-close": {"file_name": "gate-close3.wav"}
        })

        #self.dialer_controller.dial_auto(27, 7, 15, 32, 12, 30, 1) #gate dial success
        #self.dialer_controller.dial_auto(27, 7, 15, 32, 12, 29, 1) #gate dial failed

    def on_event(self, event):
        """
        On Event
        :param event: The event object
        """
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == EventType.SOUND_PLAY:
            self.sound_controller.play(event.value)

        elif event.type == EventType.SOUND_ADD_TO_QUEUE:

            if hasattr(event, "callback"):
                self.sound_controller.play(event.value, True, False, False, event.callback)
            else:
                self.sound_controller.play(event.value, True, False)

        elif event.type == EventType.SOUND_LOOPING_PLAY_WHEN_IDLE:
            self.sound_controller.play_when_idle(event.value, True)

        elif event.type == EventType.SOUND_PLAY_WHEN_IDLE:
            self.sound_controller.play_when_idle(event.value)

        elif event.type == EventType.SOUND_STOP:
            self.sound_controller.stop(event.value)

        elif event.type == pygame.KEYUP:
            self.dialer_controller.on_key_press(event.key)

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

        self.on_cleanup()