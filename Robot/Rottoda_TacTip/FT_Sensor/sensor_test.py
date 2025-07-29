import numpy as np
import time
import nidaqmx
from nidaqmx.constants import AcquisitionType
from nidaqmx.constants import Edge
import keyboard

# pp = pprint.PrettyPrinter(indent=3)
np.set_printoptions(precision=3)
class FT_NI:
    def __init__(self,**kwargs):
        self.Nsamples = kwargs['samples']
        self.Ratesamples = kwargs['rate']
        self.task=nidaqmx.Task()
        self.offset = np.asarray([.0,.0,.0,.0,.0,.0]) # Please do not change this!!
        self.FTsetup()
        data = np.asarray(self.task.read())

        print("==================================================")
        print(f'Initial raw data: {data}')
        print("==================================================")

    def FTsetup(self):
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5")
        self.task.timing.cfg_samp_clk_timing(self.Ratesamples, source="", active_edge=Edge.RISING, 
                                             sample_mode=AcquisitionType.FINITE, samps_per_chan=1000)

    def convertingRawData(self):
        # For FT52560
        bias = [0.1663, 1.5724, -0.0462, -0.0193, -0.0029, 0.0093]
        userAxis = [[-1.46365, 0.26208, 1.93786, -34.19271, -1.16799, 32.94542],
                    [-1.30893, 39.73726, -0.37039, -19.60236, 1.84250, -19.16761],
                    [19.26259, -0.08643, 19.17027, -0.25200, 19.58193, -0.01857],
                    [0.46529, 0.12592, -33.14392, 0.31541, 33.76824, -0.14065],
                    [37.74417, -0.26852, -18.62546, 0.43466, -19.49703, 0.01865],
                    [1.16572, -19.72447, 0.49027, -19.51112, 0.54533, -19.30472]]
        offSetCorrection = self.rawData - np.transpose(bias)
        self.forces = np.dot(userAxis, np.transpose(offSetCorrection))

    def readFT(self):
        self.voltages = self.task.read(self.Nsamples)
        self.rawData = np.mean(self.voltages,axis=1)
        self.convertingRawData()
        return self.forces
        
    def calibration(self, second=1):
        print(f'Calibration started for {second} second(s) ...')
        start_time = time.time()
        count = 0
        stacked_offset = np.asarray([.0,.0,.0,.0,.0,.0])

        while time.time() - start_time < second:
            stacked_offset += self.readFT()
            count += 1

        mean_offset = stacked_offset/count
        self.offset = mean_offset
        print(f'Calibration is done ...')

        return mean_offset
        
    def readFT_calibrated(self):
        if self.offset.sum() == 0:
            print("Calibration step should take place first... I recommend running 'FT_NI.calibration(1)'")

        return self.readFT() - self.offset
        

if __name__ == "__main__":

    FT = FT_NI(samples=100,rate=1000)
    FT_calibrated = FT.calibration(0.5) # in second
    print(f'Offset after calibration: {FT_calibrated}')
    print(f'(Raw-Offset) after calibration: {FT.readFT_calibrated()}')

    while True:
        FTdata = FT.readFT_calibrated()
        # print(f'[Fx, Fy, Fz, Tx, Ty, Tz]={FTdata}')
        print(f'[Fx, Fy, Fz, Tx, Ty, Tz]=[{FTdata[0]:.4f}, {FTdata[1]:.4f}, {FTdata[2]:.4f}, {FTdata[3]:.4f}, {FTdata[4]:.4f}, {FTdata[5]:.4f}]')

        # If 'q' is pressed, exit the loop
        if keyboard.is_pressed('q'):
            FT.task.close()
            print("Exit")
            break

        time.sleep(1) 