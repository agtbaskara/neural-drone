import pygame

class Remote:
    def __init__(self, min_pwm = 988, max_pwm = 2012):
        pygame.init()
        pygame.joystick.init()
        self.__joystick = pygame.joystick.Joystick(0)
        self.__joystick.init()

        self.__min_pwm = min_pwm
        self.__max_pwm = max_pwm
        self.__rcin = [0, 0, 0, 0, 0, 0, 0, 0]

        self.__init_calibration()
    
    def __remap(self, x, in_min, in_max, out_min, out_max):
        return(int)((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def __init_calibration(self):
        print("Calibrate Remote: Please Move All Axis and Button")
        joystick_input = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while any(i == 0 for i in joystick_input):
            for event in pygame.event.get():
                for j in range(0, 4):
                    if self.__joystick.get_axis(j):
                        joystick_input[j] = 1
                for j in range(0, 12):
                    if self.__joystick.get_button(j):
                        joystick_input[j+4] = 1
                
                self.__rcin[0] = self.__remap(self.__joystick.get_axis(0), -1, 1, self.__min_pwm, self.__max_pwm)
                self.__rcin[1] = self.__remap(self.__joystick.get_axis(1), -1, 1, self.__min_pwm, self.__max_pwm)
                self.__rcin[2] = self.__remap(self.__joystick.get_axis(2), -1, 1, self.__min_pwm, self.__max_pwm)
                self.__rcin[3] = self.__remap(self.__joystick.get_axis(3), -1, 1, self.__min_pwm, self.__max_pwm)
                if(self.__joystick.get_button(0)==True):
                    self.__rcin[4] = self.__min_pwm
                elif(self.__joystick.get_button(1)==True):
                    self.__rcin[4] = (self.__max_pwm-self.__min_pwm)/2+self.__min_pwm
                elif(self.__joystick.get_button(2)==True):
                    self.__rcin[4] = self.__max_pwm
                if(self.__joystick.get_button(3)==True):
                    self.__rcin[5] = self.__min_pwm
                elif(self.__joystick.get_button(4)==True):
                    self.__rcin[5] = (self.__max_pwm-self.__min_pwm)/2+self.__min_pwm
                elif(self.__joystick.get_button(5)==True):
                    self.__rcin[5] = self.__max_pwm
                if(self.__joystick.get_button(6)==True):
                    self.__rcin[6] = self.__min_pwm
                elif(self.__joystick.get_button(7)==True):
                    self.__rcin[6] = (self.__max_pwm-self.__min_pwm)/2+self.__min_pwm
                elif(self.__joystick.get_button(8)==True):
                    self.__rcin[6] = self.__max_pwm
                if(self.__joystick.get_button(9)==True):
                    self.__rcin[7] = self.__min_pwm
                elif(self.__joystick.get_button(10)==True):
                    self.__rcin[7] = (self.__max_pwm-self.__min_pwm)/2+self.__min_pwm
                elif(self.__joystick.get_button(11)==True):
                    self.__rcin[7] = self.__max_pwm
        print("Remote Calibrated")

    def get_input(self):
        for event in pygame.event.get():
            self.__rcin[0] = self.__remap(self.__joystick.get_axis(0), -1, 1, self.__min_pwm, self.__max_pwm)
            self.__rcin[1] = self.__remap(self.__joystick.get_axis(1), -1, 1, self.__min_pwm, self.__max_pwm)
            self.__rcin[2] = self.__remap(self.__joystick.get_axis(2), -1, 1, self.__min_pwm, self.__max_pwm)
            self.__rcin[3] = self.__remap(self.__joystick.get_axis(3), -1, 1, self.__min_pwm, self.__max_pwm)
            if(self.__joystick.get_button(0)==True):
                self.__rcin[4] = self.__min_pwm
            elif(self.__joystick.get_button(1)==True):
                self.__rcin[4] = (self.__max_pwm-self.__min_pwm)/2+self.__min_pwm
            elif(self.__joystick.get_button(2)==True):
                self.__rcin[4] = self.__max_pwm
            if(self.__joystick.get_button(3)==True):
                self.__rcin[5] = self.__min_pwm
            elif(self.__joystick.get_button(4)==True):
                self.__rcin[5] = (self.__max_pwm-self.__min_pwm)/2+self.__min_pwm
            elif(self.__joystick.get_button(5)==True):
                self.__rcin[5] = self.__max_pwm
            if(self.__joystick.get_button(6)==True):
                self.__rcin[6] = self.__min_pwm
            elif(self.__joystick.get_button(7)==True):
                self.__rcin[6] = (self.__max_pwm-self.__min_pwm)/2+self.__min_pwm
            elif(self.__joystick.get_button(8)==True):
                self.__rcin[6] = self.__max_pwm
            if(self.__joystick.get_button(9)==True):
                self.__rcin[7] = self.__min_pwm
            elif(self.__joystick.get_button(10)==True):
                self.__rcin[7] = (self.__max_pwm-self.__min_pwm)/2+self.__min_pwm
            elif(self.__joystick.get_button(11)==True):
                self.__rcin[7] = self.__max_pwm
        return self.__rcin

if __name__ == "__main__":
    remote = Remote()
    while(True):
        print(remote.get_input())