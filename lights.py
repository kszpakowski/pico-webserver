from machine import Pin, PWM


class PwmLight:
    
    is_on = True
    brightness = 100
    FULL_DUTY = 65535
    
    def __init__(self, pin):
        self.pwmled=PWM(Pin(pin))
        self.pwmled.freq(1000)
        self.pwmled.duty_u16(self.FULL_DUTY)
    
    def _set_light_brightness(self):
        print(f"Setting led state to: {self.is_on}, brightness to: {self.brightness}")
        duty = int((self.FULL_DUTY/100))*self.brightness if self.is_on else 0
        self.pwmled.duty_u16(duty)
        
    def turn_on(self):
        self.is_on=True
        self._set_light_brightness()
        
    def turn_off(self):
        self.is_on=False
        self._set_light_brightness()
        
    # TODO add validation >= 0, <= 100    
    def set_brightness(self, value):
        self.brightness=value
        self._set_light_brightness()
        
    def get_state(self):
        print(f"Returning current state. Is on: {self.is_on}, Brightness: {self.brightness}")
        return { "on": self.is_on, "brightness": self.brightness }
        
        
