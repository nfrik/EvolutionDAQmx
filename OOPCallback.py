from PyDAQmx import *
from PyDAQmx.DAQmxTypes import *
import matplotlib.pyplot as plt
from numpy import zeros

"""This example is a PyDAQmx version of the ContAcq_IntClk.c example
It illustrates the use of callback functions

This example demonstrates how to acquire a continuous amount of
data using the DAQ device's internal clock. It incrementally stores the data
in a Python list.
"""



class CallbackTask(Task):
    def __init__(self):
        Task.__init__(self)
        self.data = zeros(1000)
        self.a = []
        self.CreateAIVoltageChan("Analog_Input/ai0","",DAQmx_Val_RSE,-10.0,10.0,DAQmx_Val_Volts,None)
        self.CfgSampClkTiming("",100000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,1000)
        self.AutoRegisterEveryNSamplesEvent(DAQmx_Val_Acquired_Into_Buffer,1000,0)
        self.AutoRegisterDoneEvent(0)
        self.hl, = plt.plot([], [])
    def EveryNCallback(self):
        read = int32()
        self.ReadAnalogF64(1000,10.0,DAQmx_Val_GroupByScanNumber,self.data,1000,byref(read),None)
        self.a.extend(self.data.tolist())
        print self.data[0]
        self.update_line(self.data)
        return 0 # The function should return an integer
    def DoneCallback(self, status):
        print "Status",status.value
        return 0 # The function should return an integer

    def update_line(self,new_data):
        self.hl.set_xdata(numpy.append(self.hl.get_xdata(), new_data))
        self.hl.set_ydata(numpy.append(self.hl.get_ydata(), new_data))
        # self.hl.relim()
        # self.hl.autoscale_view()
        plt.draw()


task=CallbackTask()
task.StartTask()

raw_input('Acquiring samples continuously. Press Enter to interrupt\n')

task.StopTask()
task.ClearTask()