"""Offline functional tests; no connected instrument required.
SPDX-License-Identifier: GPL-3.0-or-later
"""
import argparse
import csv
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import main_export as exporter
from protocol import MessageType, build_message, decode_spectrum


def response(kind, payload=b''):
    raw = b'\xcc\x81' + (9 + len(payload)).to_bytes(3, 'little') + bytes([kind]) + payload
    return raw + bytes([sum(raw) & 255]) + b'\r\n'


def spectral_payload(status, exposure_ms):
    exponent = int.from_bytes(struct.pack('>H', 8848 ^ 3), 'little')
    keys = decode_spectrum([0] * 661, exponent, exposure_ms, 1, 2)
    encoded = [i ^ round(key * 1000) for i, key in enumerate(keys)]
    return struct.pack('<BIHIQ', status, int(exposure_ms * 1000), exponent, 1, 2) + struct.pack('<661H', *encoded)


class SimulatedSerial:
    def __init__(self, *args, fragmented=False, **kwargs):
        self.data = b''
        self.fragmented = fragmented
        self.rx = b''
        self.tx = b''

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    @property
    def in_waiting(self):
        return len(self.data)

    def write(self, value):
        self.tx += value
        kind = value[5]
        if kind == 8:
            self.data += response(8, b'SIMULATED_Y2')
        elif kind == 15:
            self.data += response(15, struct.pack('<HH', 340, 1000))
        elif kind == 11:
            self.data += response(11, b'\x01')
        elif kind == 51:
            self.data += response(51, spectral_payload(2, 1000))
            self.data += response(51, spectral_payload(0, 2000))
        elif kind == 4:
            self.data += response(4)
        return len(value)

    def read(self, count):
        if self.fragmented:
            count = min(count, 23)
        result, self.data = self.data[:count], self.data[count:]
        self.rx += result
        return result


class PCWorkflowTests(unittest.TestCase):
    def test_stop_command(self):
        self.assertEqual(build_message(MessageType.STOP, b''),
                         b'\xcc\x01\x09\x00\x00\x04\xda\r\n')

    def test_full_and_fragmented_measurement(self):
        for fragmented in (False, True):
            with self.subTest(fragmented=fragmented), tempfile.TemporaryDirectory() as temp:
                port = SimulatedSerial(fragmented=fragmented)
                args = argparse.Namespace(port='SIMULATED', output=temp, name='simulated',
                                          timeout=5, decimal_comma=True, no_plot=False,
                                          show=False, photoperiod_hours=16)
                result, folder = exporter.acquire(args, lambda *a, **kw: port)
                self.assertEqual(result, 0)
                saved = json.loads((folder / 'measurement.json').read_text())
                meta = saved['metadata']
                self.assertEqual(meta['observations_exported'], 2)
                self.assertEqual(meta['point_count'], 661)
                self.assertTrue(meta['stop_acknowledged'])
                self.assertEqual(meta['warnings'], [])
                self.assertIn('metrics', meta)
                with (folder / 'spectrum.csv').open(encoding='utf-8-sig') as f:
                    rows = list(csv.DictReader(f, delimiter=';'))
                self.assertEqual(len(rows), 661)
                self.assertEqual(rows[0]['wavelength_nm'], '340')
                self.assertEqual(rows[-1]['wavelength_nm'], '1000')
                self.assertEqual(rows[-1]['spectral_irradiance_W_m2_nm'], '0,66')
                self.assertEqual((folder / 'received.bin').read_bytes(), port.rx)
                self.assertEqual((folder / 'sent.bin').read_bytes(), port.tx)
                for name in ('spectrum.png', 'metrics.csv', 'bands.csv', 'ratios.csv', 'cri_samples.csv'):
                    self.assertGreater((folder / name).stat().st_size, 0)

    def test_plot_colours_and_axes(self):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        x = np.arange(340, 1001)
        values = np.exp(-((x - 550) / 170) ** 2)
        with tempfile.TemporaryDirectory() as temp:
            with patch('matplotlib.pyplot.close'):
                exporter.plot_spectrum(Path(temp), {'spectrum': values.tolist(), 'exposure_time': 1},
                                       {'start_wavelength_nm': 340, 'device_id': 'SIMULATED'}, False)
                fig = plt.gcf()
                ax = fig.axes[0]
                self.assertEqual(tuple(ax.get_xlim()), (340, 1000))
                self.assertIn('Wellenlänge', ax.get_xlabel())
                self.assertTrue(np.allclose(np.diff(ax.xaxis.get_majorticklocs()), 100))
                self.assertIn('UV', [text.get_text() for text in ax.texts])
                self.assertIn('NIR', [text.get_text() for text in ax.texts])
                rgb = np.asarray(ax.images[0].get_array())[0]
                self.assertGreater(rgb[0, 2], rgb[0, 1])
                self.assertGreater(rgb[-1, 0], rgb[-1, 1])
                self.assertGreater((Path(temp) / 'spectrum.png').stat().st_size, 1000)
            plt.close('all')


if __name__ == '__main__':
    unittest.main()
