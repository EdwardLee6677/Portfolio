#Single instance capture of ATI mini45 FT sensor data
#DAQ: NI USB-6211
# 6 channels for Fx,Fy,Fz,Tx,Ty,Tz
#dependencies: nidaqmx - pip install nidaqmx


import numpy as np
import time
import nidaqmx
from nidaqmx.constants import AcquisitionType
from nidaqmx.constants import Edge
import keyboard

'''
    nidaqmx:데이터 수집 라이브러리
    DAQ장치는 아날로그 또는 디지털 신호를 측정하고 기록하는 장치
    여기서는 NI USB-6211과 같은 DAQ 장치에서 데이터를 읽음

    AcquisitionType:데이터 수집모드를 정의
    여기서는 'FINITE' 모드를 사용하여 정해진 샘플 수만큼 데이터 수집

    Edge:샘플 클럭의 활성 에지를 정의
    여기서는 'RISING' 에지를 사용하여 상승 에지에서 샘플 수집

    keybord:키보드 입력을 감지하기 위한 라이브러리
    여기서는 'q'키가 눌렀을떄 프로그램을 종료하는데 사용
'''
# pp = pprint.PrettyPrinter(indent=3)
# numpy 배열을 출력할 때 소수점 이하 3자리까지 표시하도록 설정
np.set_printoptions(precision=5) 

class FT_NI:
    
    def __init__(self,**kwargs):
        self.Nsamples = kwargs['samples'] 
        '''
            수집할 샘플 수 저장
            'kwargs'는 키워드 인수들을 딕셔너리 형태로 받아오는 매개변수
            만약 FT_NI(samples=100, rate=1000)으로 호출하면 samples 키의 값을 self.Nsamples에 저장
        '''
        self.Ratesamples = kwargs['rate']
        '''
            샘플링 속도(초당 샘플 수)를 저장
            마찬가지로 kwargs에서 rate 키의 값을 self.Ratesamples에 저장장
        '''
        self.task=nidaqmx.Task() # NI DAQ장치와 상호작용하기 위한 task를 생성
        self.offset = np.asarray([.0,.0,.0,.0,.0,.0]) # Please do not change this!!
        # 초기 오프셋 값을 설정 / 오프셋 값은 calibration(보정) 단계에서 계산된 평균 값으로 업데이트됨
        self.FTsetup() # 데이터 수집 설정을 위한 메서드를 호출
        data = np.asarray(self.task.read()) # 초기 데이터를 읽어옴 / 데이터를 'asarray'를 사용하여  numpy 배열로 변환
        # 데이터 출력    
        print("==================================================")
        print(f'Initial raw data: {data}')
        print("==================================================")
        

    def FTsetup(self):
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5")
        self.task.timing.cfg_samp_clk_timing(self.Ratesamples, source="", active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=1000)
        # self.task.timing.cfg_samp_clk_timing(self.Ratesamples, source="", active_edge=Edge.RISING, sample_mode=AcquisitionType.CONTINUOUS)
    '''
        FTsetup 메서드는 NI DAQ 장치의 데이터 수집 작업을 설정
        아날로그 입력 채널을 추가하고, 샘플 클럭 타이밍을 구성

        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5"):NI DAQ 장치의 아날로그 입력 채널을 추가
        "Dev1/ai0:5"은 장치 'Dev1'(장치 이름)의 아날로그 입력 채널 'ai0'부터 'ai5'까지를 의미
        'add_ai_voltage_chan'메서드는 전압 입력 채널을 추가

        self.task.timing.cfg_samp_clk_timing(self.Ratesamples, source="", active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=11):
        데이터 수집 작업의 샘플 클럭 타이밍을 설정
        'cfg_samp_clk_timing' 메서드를 사용해 샘플링 속도와 모드를 설정
        'self.Ratesamples'는 샘플링 속도를 설정 / ex) rate=1000으로 설정하면 초당 1000개의 샘플 수집
        'source='는 샘플 클럭의 소스를 설정 / 빈 문자열이므로 내부 클럭 사용을의미
        'active_edge=Edge.RISING'는 샘플 클럭의 활성 에지를 설정 / Edge.RISING은 상승 에지에서 샘플을 수집함을 의미
        'sample_mode=AcquisitionType.FINITE'는 샘플 수집 모드를 설정 / 정해진 수의 샘플을 수집하는 모드
        'samps_per_chan=11'는 채널당 수집할 샘플 수를 설정 / 각 채널에서 11개의 샘플을 수집함을 의미함 / 현재 6개의 채널(Fx~Tz)이므로 총 66개의 샘플을 수집
    '''

    def convertingRawData(self):
        #FOR FT52560   편차가 양수라면 bias를 증가. 편차가 음수라면 bias를 감소. 편차의 크기에 따라 조정 범위를 정함 (작게 ±0.1 ~ 0.5 사이에서 시작).
        # bias = [16.1561, -17.2971, -16.9903, -0.5803, -0.5015, 0.0062]
        # bias = [16.3561, -17.5971, -17.9903, -0.5803, -0.5015, 0.0062]
        bias = [16.4561, -19.0971, -19.0903, -0.5803, -0.5015, 0.0062]
        userAxis = [[-1.02858, 0.18418, 1.36183, -24.02903, -0.82081, 23.15249],
                    [-0.91985, 27.92548, -0.26029, -13.77562, 1.29482, -13.47009],
                    [33.89379, -0.15208, 33.73134, -0.44341, 34.45569, -0.03268],
                    [0.00139, 0.19360, -0.55008, -0.08926, 0.56750, -0.09470],
                    [0.63145, -0.00571, -0.31746, 0.17198, -0.31691, -0.15847],
                    [0.02107, -0.35645, 0.00886, -0.35259, 0.00985, -0.34886]]
        
        offSetCorrection = self.rawData - np.transpose(bias)
        self.forces = np.dot(userAxis, np.transpose(offSetCorrection))
    '''
        convertingRawData 메서드는 수집된 raw 데이터를 보정하고 변환하여 실제 힘과 토크 값으로 변환
        보정된 데이터를 self.forces 변수에 저장함

        bias 배열은 각 채널의 보정값 / 이 값들은 센서가 초기 상태에서 측정한 편향을 보정하기 위해 사용
        이러한 보정값은 센서 제조사에서 제공하거나 calibration과정에서 얻을 수 있음

        userAxis는 각 축의 변환 행렬
        이 행렬은 raw 전압 데이터를 실제 힘과 토크값으로 변환하는데 사용됨
        각 행렬 요소는 센서 제조사에서 제공하거나 calibration과정에서 얻을 수 있음
        이 변환 행렬을 사용하여 raw 데이터를 실제값으로 변환하게됨

        offSetCorrection = self.rawData - np.transpose(bias): 
        raw data에서 bias 배열을 빼서 오프셋을 보정함 **offset이란 제어계에서 원하는 출력 상태와 실제 출력상태의 차이의 정상값을 의미 / 쉽게 말해서 원하는 값과 실제 값의 편차

        'self.forces = np.dot(userAxis, np.transpose(offSetCorrection))':
        'np.dot'을 사용하여 변환 행렬'userAxis'와 보정된 데이터 'offsetCorrection'의 전치를 곱함
        이 계산을 통해 raw data를 실제 힘과 토크 값으려 변환
        변환된 데이터는 'self.forces' 변수에 저장됨

    '''

    def readFT(self):
        self.voltages = self.task.read(self.Nsamples)
        self.rawData = np.mean(self.voltages,axis=1)
        self.convertingRawData()
        return self.forces
    '''
        readFT 메서드는 장치에서 raw data를 일고 평균을 계산하여 보정된 힘과 토크값으로 변환
        최종적으로 변환된 힘과 토크값을 반환

        'self.voltages = self.task.read(self.Nsamples)':
        NI DAQ장치에서 지정된 샘플 수 만큼 데이터를 읽어와 self.voltages에 저장
        ex) 'self.Nsamples'가 100이면 100개의 샘플을 읽어옴 (샘플=각 채널(Fx~Tz)에서 측정된 전압값)
            반환된 데이터는 2차원 배열 형태로 저장
            각 행은 한 번의 샘플링에서 측정된 값들을 포함
            각 열은 채널에 해당됨
        
        ' self.rawData = np.mean(self.voltages, axis=1)':
        'np.mean(self.voltages, axis=1)'을 사용하여 각 채널의 평균 전압 값을 계산 / axis=1은 열(columns)을 따라 평균을 계산함을 의미

        'self.convertingRawData()'을 호출하여 raw data를 실제 힘과 토크값으로 변환
        
        이 후 self.forces 변수에 저장하여 return

    '''
    
    
    def calibration(self, second=1): # 주어진 시간 동안 데이터를 수집하여 오프셋 값을 계산하는 메서드
        print(f'Calibration started for {second} second(s) ...')
        start_time = time.time() 
        # 시작 시간을 저장 / time.time()은 현재 시간을 초 단위로 반환
        
        count = 0 # 수집된 데이터의 샘플 수를 세기 위한 변수
        stacked_offset = np.asarray([.0,.0,.0,.0,.0,.0]) # 수집된 모든 데이터를 누적하여 저장하기 위한 배열

        while time.time() - start_time < second:
            stacked_offset += self.readFT()
            count += 1

        mean_offset = stacked_offset/count
        self.offset = mean_offset
        print(f'Calibration is done ...')
        
        return mean_offset
    '''
        현재 시간과 start_time의 차이가 second보다 작을 동안 반복
        self.readFT()를 호출하여 현재 데이터를 읽어옴
        읽어온 데이터를 'stacked_offset'에 더함
        샘플 수를 세기 위해 count를 1 증가

        누적된 데이터를 샘플 수로 나누어 평균 오프셋 값을 계산 후 반환
    '''
    
    
    
    def readFT_calibrated(self):
        if self.offset.sum() == 0:
            print("Calibration step should take place first... I recommend running 'FT_NI.calibration(1)'")

        return self.readFT() - self.offset

    '''
        해당 메서드는 보정된 데이터를 반환
        
        'if self.offset.sum() == 0:'는 오프셋 값의 합이 0인지 확인
        합이 0이면, calibration이 수행되지 않았음을 의미

        ' return self.readFT() - self.offset'는 self.readFT()를 호출하여 현재 데이터를 읽어옴
        읽어온 데이터에서 오프셋 값을 빼서 보정된 데이터를 계산 후 반환

    '''

if __name__ == '__main__':

    FT = FT_NI(samples=1000,rate=10000)

    FT_calibrated = FT.calibration(1) # in second
    print(f'Offset after calibration: {FT_calibrated}')

    print(f'(Raw-Offset) after calibration: {FT.readFT_calibrated()}')

    while True:
        FTdata = FT.readFT_calibrated()
        # print(f'[Fx, Fy, Fz, Tx, Ty, Tz]={FTdata}')
        print(f'[Fx, Fy, Fz, Tx, Ty, Tz]=[{FTdata[0]:.4f}, {FTdata[1]:.4f}, {FTdata[2]:.4f}, {FTdata[3]:.4f}, {FTdata[4]:.4f}, {FTdata[5]:.4f}]')
        
        # If 'q' is pressed then quit the while loop
        if keyboard.is_pressed("q"):
            FT.task.close()
            break

        time.sleep(1)