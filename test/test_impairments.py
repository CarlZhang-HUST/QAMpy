import pytest
import numpy as np

from qampy import signals, impairments

class TestReturnDtype(object):
    @pytest.mark.parametrize("dtype", [np.complex64, np.complex128])
    def test_rotate_field(self, dtype):
        s = signals.ResampledQAM(16, 2**14, fs=2, nmodes=2, dtype=dtype)
        s2 = impairments.rotate_field(s, np.pi / 3)
        assert np.dtype(dtype) is s2.dtype

    @pytest.mark.parametrize("dtype", [np.complex64, np.complex128])
    def test_apply_PMD(self, dtype):
        s = signals.ResampledQAM(16, 2**14, fs=2, nmodes=2, dtype=dtype)
        s2 = impairments.apply_PMD(s, np.pi / 3, 1e-3)
        assert np.dtype(dtype) is s2.dtype

    @pytest.mark.parametrize("dtype", [np.complex64, np.complex128])
    def test_apply_phase_noise(self, dtype):
        s = signals.ResampledQAM(16, 2**14, fs=2, nmodes=2, dtype=dtype)
        s2 = impairments.apply_phase_noise(s, 1e-3)
        assert np.dtype(dtype) is s2.dtype

    @pytest.mark.parametrize("dtype", [np.complex64, np.complex128])
    def test_change_snr(self, dtype):
        s = signals.ResampledQAM(16, 2**14, fs=2, nmodes=2, dtype=dtype)
        s2 = impairments.change_snr(s, 30)
        assert np.dtype(dtype) is s2.dtype

    @pytest.mark.parametrize("dtype", [np.complex64, np.complex128])
    def test_add_carrier_offset(self, dtype):
        s = signals.ResampledQAM(16, 2**14, fs=2, nmodes=2, dtype=dtype)
        s2 = impairments.add_carrier_offset(s, 1e-3)
        assert np.dtype(dtype) is s2.dtype


class TestReturnObjects(object):
    s = signals.ResampledQAM(16, 2 ** 14, fs=2, nmodes=2)

    def test_rotate_field(self):
        s2 = impairments.rotate_field(self.s, np.pi / 3)
        assert type(self.s) is type(s2)

    def test_apply_PMD(self):
        s2 = impairments.apply_PMD(self.s, np.pi / 3, 1e-3)
        assert type(self.s) is type(s2)

    def test_apply_phase_noise(self):
        s2 = impairments.apply_phase_noise(self.s, 1e-3)
        assert type(self.s) is type(s2)

    def test_change_snr(self):
        s2 = impairments.change_snr(self.s, 30)
        assert type(self.s) is type(s2)

    def test_add_carrier_offset(self):
        s2 = impairments.add_carrier_offset(self.s, 1e-3)
        assert type(self.s) is type(s2)

    def test_simulate_transmission(self):
        s2 = impairments.simulate_transmission(self.s, snr=20, freq_off=1e-4, lwdth=1e-4,
                                               dgd=1e-2)
        assert type(self.s) is type(s2)

    @pytest.mark.parametrize("attr", ["fs", "symbols", "fb"])
    def test_add_awgn(self, attr):
        s2 = impairments.add_awgn(self.s, 0.01)
        assert getattr(self.s, attr) is getattr(s2, attr)

    @pytest.mark.parametrize("attr", ["fs", "symbols", "fb"])
    def test_rotate_field_attr(self, attr):
        s2 = impairments.rotate_field(self.s, np.pi / 3)
        assert getattr(self.s, attr) is getattr(s2, attr)

    @pytest.mark.parametrize("attr", ["fs", "symbols", "fb"])
    def test_apply_PMD_attr(self, attr):
        s2 = impairments.apply_PMD(self.s, np.pi / 3, 1e-3)
        assert getattr(self.s, attr) is getattr(s2, attr)

    @pytest.mark.parametrize("attr", ["fs", "symbols", "fb"])
    def test_apply_phase_noise_attr(self, attr):
        s2 = impairments.apply_phase_noise(self.s, 1e-3)
        assert getattr(self.s, attr) is getattr(s2, attr)

    @pytest.mark.parametrize("attr", ["fs", "symbols", "fb"])
    def test_add_awgn_attr(self, attr):
        s2 = impairments.add_awgn(self.s, 0.01)
        assert getattr(self.s, attr) is getattr(s2, attr)
