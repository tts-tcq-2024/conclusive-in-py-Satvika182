import unittest
from unittest.mock import patch
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

    @patch('typewise_alert.send_to_controller')
    def test_check_and_alert_to_controller(self, mock_send_to_controller):
        battery_char = {'coolingType': 'PASSIVE_COOLING'}
        typewise_alert.check_and_alert('TO_CONTROLLER', battery_char, 36)
        mock_send_to_controller.assert_called_with('TOO_HIGH')

    @patch('typewise_alert.send_to_email')
    def test_check_and_alert_to_email(self, mock_send_to_email):
        battery_char = {'coolingType': 'PASSIVE_COOLING'}
        typewise_alert.check_and_alert('TO_EMAIL', battery_char, -1)
        mock_send_to_email.assert_called_with('TOO_LOW')

    @patch('builtins.print')
    def test_send_to_controller(self, mock_print):
        typewise_alert.send_to_controller('TOO_HIGH')
        mock_print.assert_called_with('65261, TOO_HIGH')

    @patch('builtins.print')
    def test_send_to_email_too_low(self, mock_print):
        typewise_alert.send_to_email('TOO_LOW')
        mock_print.assert_any_call('To: a.b@c.com')
        mock_print.assert_any_call('Hi, the temperature is too low')

    @patch('builtins.print')
    def test_send_to_email_too_high(self, mock_print):
        typewise_alert.send_to_email('TOO_HIGH')
        mock_print.assert_any_call('To: a.b@c.com')
        mock_print.assert_any_call('Hi, the temperature is too high')

    def classify_temperature_breach(cooling_type, temperature_in_c):
     if cooling_type not in TEMPERATURE_LIMITS:
        return NORMAL  # Return NORMAL if the cooling type is invalid
    lower_limit, upper_limit = TEMPERATURE_LIMITS[cooling_type]
    return infer_breach(temperature_in_c, lower_limit, upper_limit)


    def test_check_and_alert_invalid_alert_target(self):
        battery_char = {'coolingType': 'PASSIVE_COOLING'}
        result = typewise_alert.check_and_alert('INVALID_TARGET', battery_char, 36)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
