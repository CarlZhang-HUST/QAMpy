#import cProfile
import numpy as np

from qampy import equalisation, signals
from qampy.core import impairments

#pr = cProfile.Profile()
fb = 40.e9
os = 2
fs = os*fb
N = 10**6
theta = np.pi/2.45
theta2 = np.pi/4
M = 4
QAM = signals.QAMModulator(M)
snr = 12
mu = 1e-3
ntaps = 30

S, symbols, bits = QAM.generate_signal(N, snr, PRBSorder=(15,23), baudrate=fb, samplingrate=fs)

t_pmd = 75e-12

SS = impairments.apply_PMD_to_field(S, theta, t_pmd, fs)
#pr.enable()
wx, err = equalisation.equalise_signal(SS, os, M, Ntaps=ntaps, method="mcma", adaptive_stepsize=True)
E = equalisation.apply_filter(SS, os, wx)
#E, wx, wy, err = equalisation.FS_MCMA(SS, N-40, ntaps, os, mu, M)

E = E[:,1000:-1000]

try:
    berx = QAM.cal_ber(E[0], bits_tx=bits[0])
except:
    berx = QAM.cal_ber(E[1], bits_tx=bits[0])
try:
    bery = QAM.cal_ber(E[1], bits_tx=bits[1])
except:
    bery = QAM.cal_ber(E[0], bits_tx=bits[1])

print("X BER %f dB"%(10*np.log10(berx[0])))
print("Y BER %f dB"%(10*np.log10(bery[0])))
evmX = QAM.cal_evm(S[0, ::os])
evmY = QAM.cal_evm(S[1, ::os])
evmEx = QAM.cal_evm(E[0])
evmEy = QAM.cal_evm(E[1])
print("X EVM %f "%evmEx)
print("Y EVM %f "%evmEy)

#pr.disable()
#pr.print_stats(sort="time")


sys.exit()
plt.figure()
plt.subplot(121)
plt.title('Recovered')
plt.plot(E[0].real, E[0].imag, 'ro', label=r"$EVM_x=%.1f\%%$"%(100*evmEx))
plt.plot(E[1].real, E[1].imag, 'go' ,label=r"$EVM_y=%.1f\%%$"%(evmEy*100))
plt.legend()
plt.subplot(122)
plt.title('Original')
plt.plot(S[0,::2].real, S[0,::2].imag, 'ro', label=r"$EVM_x=%.1f\%%$"%(100*evmX))
plt.plot(S[1,::2].real, S[1,::2].imag, 'go', label=r"$EVM_y=%.1f\%%$"%(100*evmY))
plt.legend()
plt.show()

# plt.figure()
# plt.subplot(211)
# plt.title('Taps')
# plt.plot(wx[0,:], 'r')
# plt.plot(wx[1,:], '--r')
# plt.plot(wy[0,:], 'g')
# plt.plot(wy[1,:], '--g')
# plt.subplot(212)
# plt.title('error')
# plt.plot(err[0], color='r')
# plt.plot(err[1], color='g')
# plt.show()


