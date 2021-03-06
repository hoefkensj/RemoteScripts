import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.EncoderElement import *
from _Framework.ChannelStripComponent import ChannelStripComponent 
from _AbletonPlus.AbletonPlus import *
from _Framework.MixerComponent import *
from BCR2000Options import options
from _AbletonPlus.Master import Master
from _Framework.ButtonElement import ButtonElement
class BCR2000(ControlSurface, AbletonPlus):
    __doc__ = "BCR2000 Custom Script"
    
    def __init__(self,c_instance):
        ControlSurface.__init__(self, c_instance)
        AbletonPlus.__init__(self, options)
        
        self._main_encoders = []
        self._main_buttons = []
        self._effects_encoders = []
        self._extra_buttons = []
        self._mixer = None
               
        for index in range(0, 24):
            encoder = EncoderElement(MIDI_CC_TYPE,0,92 + index,Live.MidiMap.MapMode.absolute)
            self._main_encoders.append(encoder)
        
        for index in range(0,16):
            button = ButtonElement(False, MIDI_CC_TYPE,0, 76 + index)
            self._main_buttons.append(button)
            
        self._mixer = MixerComponent(8)
        
        self._remap_track_mixer_controls()
        
        self._enable_abletonplus()
        
        return None
        
    def _enable_abletonplus(self):
        if(self not in AbletonPlus._enabled_devices):
            AbletonPlus._enabled_devices.append(self)
            AbletonPlus._connect_active_instances(self)
            
    def disconnect(self):
        self._disconnect_instance()
        
    def _remap_track_mixer_controls(self):
        self._mixer.set_track_offset(AbletonPlus.get_track_offset())
        
        for index in range(8):
            strip = self._mixer.channel_strip(index)
            strip.name = 'Channel_Strip_' + str(index)
            strip.set_volume_control(self._main_encoders[(index * 3) + 2])
            strip.set_pan_control(self._main_encoders[(index * 3) + 1])
            strip.set_mute_button(self._main_buttons[index * 2])
            strip.set_arm_button(self._main_buttons[(index * 2)+ 1])
            strip.set_send_controls((self._main_encoders[index * 3],))
        return None
    
    def offset_update(self):
        self._remap_track_mixer_controls()
        return None
    
    def selected_change(self):
        self._remap_selected_track_devices()
        return None