import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType, Edge
import matplotlib.pyplot as plt
import time
from threading import Thread, Event

class FT_NI:
    def __init__(self, **kwargs):
        self.Nsamples = kwargs['samples']
        self.Ratesamples = kwargs['rate']
        self.task = nidaqmx.Task()
        self.offset = np.asarray([.0, .0, .0, .0, .0, .0])
        self.FTsetup()
        data = np.asarray(self.task.read())
        print("==================================================")
        print(f'Initial raw data: {data}')
        print("==================================================")

    def FTsetup(self):
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5")
        self.task.timing.cfg_samp_clk_timing(self.Ratesamples, source="", active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=11)

    def convertingRawData(self):
        bias = [16.1451, -17.1071, -16.9401, -0.5803, -0.5015, 0.0062]
        userAxis = [[-1.02858, 0.18418, 1.36183, -24.02903, -0.82081, 23.15249],
                    [-0.91985, 27.92548, -0.26029, -13.77562, 1.29482, -13.47009],
                    [33.89379, -0.15208, 33.73134, -0.44341, 34.45569, -0.03268],
                    [0.00139, 0.19360, -0.55008, -0.08926, 0.56750, -0.09470],
                    [0.63145, -0.00571, -0.31746, 0.17198, -0.31691, -0.15847],
                    [0.02107, -0.35645, 0.00886, -0.35259, 0.00985, -0.34886]]

        offSetCorrection = self.rawData - np.transpose(bias)
        self.forces = np.dot(userAxis, np.transpose(offSetCorrection))

    def readFT(self):
        self.voltages = self.task.read(self.Nsamples)
        self.rawData = np.mean(self.voltages, axis=1)
        self.convertingRawData()
        return self.forces

    def calibration(self, second=1):
        print(f'Calibration started for {second} second(s) ...')
        start_time = time.time()
        count = 0
        stacked_offset = np.asarray([.0, .0, .0, .0, .0, .0])

        while time.time() - start_time < second:
            stacked_offset += self.readFT()
            count += 1

        mean_offset = stacked_offset / count
        self.offset = mean_offset
        print(f'Calibration is done ...')
        return mean_offset

    def readFT_calibrated(self):
        if self.offset.sum() == 0:
            print("Calibration step should take place first... I recommend running 'FT_NI.calibration(1)'")
        return self.readFT() - self.offset

    def close_task(self):
        if self.task is not None:
            self.task.close()
            self.task = None  # Task 종료 후 None으로 설정


class DataCollector:
    def __init__(self, ft_sensor, trigger_Fz=-0.1, duration=0.2):
        self.ft_sensor = ft_sensor
        self.trigger_value = trigger_Fz
        self.duration = duration
        self.data_collected = []
        self.time_collected = []
        self.trigger_event = Event()

    def monitor_Fz(self):
        while not self.trigger_event.is_set():
            FTdata = self.ft_sensor.readFT_calibrated()
            Fz = FTdata[2]
            if Fz <= self.trigger_value:
                print(f'Trigger activated: Fz={Fz:.4f}')
                self.trigger_event.set()
                self.collect_data()

    def collect_data(self):
        start_time = time.time()
        while time.time() - start_time < self.duration:
            FTdata = self.ft_sensor.readFT_calibrated()
            self.data_collected.append(FTdata)
            self.time_collected.append(time.time() - start_time)
            print(f'[Fx, Fy, Fz, Tx, Ty, Tz]=[{FTdata[0]:.4f}, {FTdata[1]:.4f}, {FTdata[2]:.4f}, {FTdata[3]:.4f}, {FTdata[4]:.4f}, {FTdata[5]:.4f}]')

    def start_monitoring(self):
        monitor_thread = Thread(target=self.monitor_Fz)
        monitor_thread.start()
        return monitor_thread


def main():
    ft = FT_NI(samples=1, rate=124)
    ft.calibration(1)

    print(f'(Raw-Offset) after calibration: {ft.readFT_calibrated()}')

    data_collector = DataCollector(ft, trigger_Fz=-0.2, duration=0.2)
    monitor_thread = data_collector.start_monitoring()
    
    # 기다리면서 데이터를 수집합니다.
    monitor_thread.join()
    
    # 수집된 데이터를 플롯합니다.
    data_collected = np.array(data_collector.data_collected)
    time_collected = np.array(data_collector.time_collected)

    fig, axs = plt.subplots(6, 1, figsize=(10, 12))
    labels = ['Fx', 'Fy', 'Fz', 'Tx', 'Ty', 'Tz']
    for i in range(6):
        axs[i].plot(time_collected, data_collected[:, i])
        axs[i].scatter(time_collected, data_collected[:, i])
        axs[i].set_ylabel(labels[i])
        axs[i].grid(True)
    
    axs[5].set_xlabel('Time (s)')
    plt.tight_layout()
    plt.show()

    # 닫기 작업
    ft.close_task()


if __name__ == '__main__':
    main()
