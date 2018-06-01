import numpy as np
import matplotlib.pyplot as plt
from qampy import signals

""" Check the symbol rate of a QAM signal against the theoretical symbol rate"""

M = 32
snr = np.arange(5, 25, 1)
N = 10**5
ser = []
ser2 = []

modl = signals.QAMModulator(M)
for sr in snr:
    data_rx, symbols, bits = modl.generate_signal(N, sr)
    ser.append(modl.cal_ser(data_rx, symbol_tx=symbols))
    ser2.append(modl.cal_ser(data_rx, bits_tx=bits))

ser = 10*np.log10(np.array(ser))
ser2 = 10*np.log10(np.array(ser2))
theory_ser = 10*np.log10(modl.theoretical_ser(10**(snr/10)))
assert np.allclose(ser, ser2), "SER calculated from symbol is different to ser calculated from bits"
#assert np.allclose(ser, theory_ser, atol=1), "SER calculated from symbol is different to theoretical ser"
plt.figure()
plt.plot(snr, theory_ser, label='theory')
plt.plot(snr, ser, 'or',label='calculation')
plt.xlabel('SNR [dB]')
plt.ylabel('SER [dB]')
plt.legend()
plt.show()

