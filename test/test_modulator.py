import pytest
import numpy as np
import random
import numpy.testing as npt
import matplotlib.pylab as plt

from dsp import modulation, signal_quality

def _flip_symbols(sig, idx, d):
    for i in idx:
        if np.random.randint(0,2):
            if sig[i].real > 0:
                sig[i] -= d
            else:
                sig[i] += d
        else:
            if sig[i].imag > 0:
                sig[i] -= 1.j*d
            else:
                sig[i] += 1.j*d
    return sig

class TestModulatorAttr(object):
    Q = modulation.QAMModulator(16)
    d = np.diff(np.unique(Q.symbols.real)).min()

    def test_quantize_symbols_set(self):
        """Check if all quantized symbols are from Q.symbols"""
        sig, sym, bits = self.Q.generate_signal(2 ** 10, 30, beta=0.01, ndim=1)
        sym_demod = self.Q.quantize(sig)
        out = np.in1d(sym_demod.flatten(), self.Q.symbols.flatten())
        assert np.alltrue(out)

    def test_quantize_symbols_correct(self):
        """Check if all quantized symbols are from Q.symbols"""
        sig, sym, bits = self.Q.generate_signal(2 ** 10, None, beta=0.01, ndim=1)
        sym_demod = self.Q.quantize(sig)
        npt.assert_allclose(sym_demod, sym)

    def test_decode_correct(self):
        sig, sym, bits = self.Q.generate_signal(2 ** 10, None, beta=0.01, ndim=1)
        bb = self.Q.decode(sym[0])
        npt.assert_array_equal(bb, bits[0])

    def test_gen_signal(self):
        pass

    @pytest.mark.parametrize("Nerrors", range(5))
    @pytest.mark.parametrize("shiftN", np.random.randint(0,2**10, size=10))
    @pytest.mark.parametrize("ndims", range(1,4))
    def test_ser(self, Nerrors, shiftN, ndims):
        sig, sym, bits = self.Q.generate_signal(2 ** 10, None, beta=0.01, ndim=ndims)
        for i in range(ndims):
            idx = random.sample(range(sig.shape[1]), Nerrors)
            _flip_symbols(sig[i], idx, self.d)
        sig = np.roll(sig, shift=shiftN, axis=-1)
        ser = self.Q.cal_ser(sig)
        # note that for the npt.assert_... functions if the desired is scalar, all array values are checked
        # against the scalar hence it passes if ser is 1- or multi-dim
        npt.assert_almost_equal(ser, Nerrors/sig.shape[1])

    @pytest.mark.parametrize("Nerrors", range(5))
    @pytest.mark.parametrize("shiftN", np.random.randint(0,2**10, size=10))
    @pytest.mark.parametrize("ndims", range(1,3))
    def test_ber(self, Nerrors, shiftN, ndims):
        sig, sym, bits = self.Q.generate_signal(2 ** 10, None, beta=0.01, ndim=ndims)
        for i in range(ndims):
            idx = random.sample(range(sig.shape[1]), Nerrors)
            _flip_symbols(sig[i], idx, self.d)
            sig[i] = np.roll(sig[i], shift=(shiftN+i*np.random.randint(0, 100)))
        ber = self.Q.cal_ber(sig)
        npt.assert_almost_equal(ber, Nerrors/(sig.shape[1]*self.Q.Nbits))

    @pytest.mark.parametrize("snr", [10, 15, 20])
    @pytest.mark.parametrize("ndims", range(2,3))
    def test_evm(self, snr, ndims):
        sig, sym, bits = self.Q.generate_signal(2 ** 15, snr, beta=0.01, ndim=ndims)
        evm = self.Q.cal_evm(sig, blind=False)
        npt.assert_almost_equal(-10*np.log10(evm**2), snr, decimal=0)

    @pytest.mark.parametrize("snr", [10, 15, 20])
    def test_est_snr(self, snr):
        sig, sym, bits = self.Q.generate_signal(2 ** 15, snr, beta=0.01, ndim=1)
        e_snr = self.Q.est_snr(sig)
        npt.assert_almost_equal(10*np.log10(e_snr), snr, decimal=1)

@pytest.mark.parametrize("M", [16, 32, 64, 128, 256])
@pytest.mark.parametrize("ndims", range(1,3))
def test_gmi_cal(M, ndims):
    Q = modulation.QAMModulator(M)
    sig, syms, bits = Q.generate_signal(2**15, None, ndim=ndims)
    gmi = Q.cal_gmi(sig)[0]
    npt.assert_almost_equal(gmi, np.log2(M), decimal=1)









