import pyvisa
import pylab as pl
def main():
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource("USB0::0x3121::0x2100::SDSAHBAD4R0328::INSTR")
    inst.write("chdr off")
    vdiv = inst.query("c1:vdiv?")
    ofst = inst.query("c1:ofst?")
    tdiv = inst.query("tdiv?")
    sara = inst.query("sara?")
    sara_unit = {'G':1E9,'M':1E6,'k':1E3}
    for unit in sara_unit.keys():
        if sara.find(unit)!=-1:
            sara = sara.split(unit)
            sara = float(sara[0])*sara_unit[unit]
            break
    sara = float(sara)
    inst.timeout = 30000 #default value is 2000(2s)
    inst.chunk_size = 20*1024*1024 #default value is 20*1024(20k bytes)
    inst.write("c1:wf? dat2")
    recv = list(inst.read_raw())[15:]
    print(len(recv))
    recv.pop()
    recv.pop()
    volt_value = []
    for data in recv:
        if data > 127:
            data = data - 256
        else:
            pass
        volt_value.append(data)
    time_value = []
    for idx in range(0,len(volt_value)):
        volt_value[idx] = volt_value[idx]/25*float(vdiv)-float(ofst)
        time_data = -(float(tdiv)*14/2)+idx*(1/sara)
        time_value.append(time_data)
    print("Data convert finish,start to draw")
    pl.figure(figsize=(7,5))
    pl.plot(time_value,volt_value,markersize=2,label=u"Y-T")
    pl.legend()
    pl.grid()
    pl.show()
if __name__=='__main__':
    main()
