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

    def test_send_to_controller(self):
        with self.assertLogs(level='INFO') as log:
            typewise_alert.send_to_controller('TOO_HIGH')
            self.assertIn('INFO:root:0xfeed, TOO_HIGH', log.output)

    def test_send_to_email_for_too_low(self):
        with self.assertLogs(level='INFO') as log:
            typewise_alert.send_to_email('TOO_LOW')
            self.assertIn('INFO:root:To: a.b@c.com', log.output)
            self.assertIn('INFO:root:Hi, the temperature is too low', log.output)

    def test_send_to_email_for_too_high(self):
        with self.assertLogs(level='INFO') as log:
            typewise_alert.send_to_email('TOO_HIGH')
            self.assertIn('INFO:root:To: a.b@c.com', log.output)
            self.assertIn('INFO:root:Hi, the temperature is too high', log.output)

    def test_check_and_alert_to_controller(self):
        with self.assertLogs(level='INFO') as log:
            battery_char = {'coolingType': 'PASSIVE_COOLING'}
            typewise_alert.check_and_alert('TO_CONTROLLER', battery_char, 36)
            self.assertIn('INFO:root:0xfeed, TOO_HIGH', log.output)

    def test_check_and_alert_to_email(self):
        with self.assertLogs(level='INFO') as log:
            battery_char = {'coolingType': 'PASSIVE_COOLING'}
            typewise_alert.check_and_alert('TO_EMAIL', battery_char, 36)
            self.assertIn('INFO:root:To: a.b@c.com', log.output)
            self.assertIn('INFO:root:Hi, the temperature is too high', log.output)


if __name__ == '__main__':
    unittest.main()
