import unittest
import typewise_alert


class TypewiseTest(unittest.TestCase):

    def test_infers_breach_as_too_low(self):
        self.assertEqual(typewise_alert.infer_breach(20, 50, 100), 'TOO_LOW')

    def test_infers_breach_as_too_high(self):
        self.assertEqual(typewise_alert.infer_breach(105, 50, 100), 'TOO_HIGH')

    def test_infers_breach_as_normal(self):
        self.assertEqual(typewise_alert.infer_breach(75, 50, 100), 'NORMAL')

    def test_classify_temperature_breach_for_passive_cooling(self):
        self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 36), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 20), 'NORMAL')
        self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', -5), 'TOO_LOW')

    def test_classify_temperature_breach_for_hi_active_cooling(self):
        self.assertEqual(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 46), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 40), 'NORMAL')
        self.assertEqual(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', -1), 'TOO_LOW')

    def test_classify_temperature_breach_for_med_active_cooling(self):
        self.assertEqual(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 41), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 39), 'NORMAL')
        self.assertEqual(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 0), 'NORMAL')


if __name__ == '__main__':
    unittest.main()
