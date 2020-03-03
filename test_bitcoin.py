import unittest 
from unittest import TestCase 
from unittest.mock import patch

import bitcoin
from bitcoin import BitCoinError

class TestBitCoin(TestCase):

    @patch('bitcoin.api_call')
    def test_convert(self, mock_api_call):

        # Example response. rate_float is 8735.44
        example_rate_float = 8735.44
        mock_response = {"time":{"updated":"Mar 3, 2020 16:14:00 UTC","updatedISO":"2020-03-03T16:14:00+00:00","updateduk":"Mar 3, 2020 at 16:14 GMT"},"disclaimer":"This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org","chartName":"Bitcoin","bpi":{"USD":{"code":"USD","symbol":"&#36;","rate":"8,735.4400","description":"United States Dollar","rate_float": example_rate_float},"GBP":{"code":"GBP","symbol":"&pound;","rate":"6,815.3466","description":"British Pound Sterling","rate_float":6815.3466},"EUR":{"code":"EUR","symbol":"&euro;","rate":"7,813.8161","description":"Euro","rate_float":7813.8161}}}
        mock_api_call.return_value = mock_response 
        example_dollars = 99.99
        expected_conversion = example_rate_float * example_dollars
        actual_conversion = bitcoin.convert_dollars_to_bitcoin(example_dollars, 'example url') 
        self.assertEqual(expected_conversion, actual_conversion)


    @patch('bitcoin.api_call')
    def test_convert_different_json_format(self, mock_api_call):
        # not the expected JSON
        mock_response = {"cat": "hello kitty", "pizza_count": 1000000}
        mock_api_call.return_value = mock_response 
        with self.assertRaises(BitCoinError):             
             bitcoin.convert_dollars_to_bitcoin(100, 'example url')


    #no mock needed here, testing the actual call
    def test_bad_response_from_server(self):
        with self.assertRaises(BitCoinError):             
            bitcoin.convert_dollars_to_bitcoin(100, 'not a real url')

    


if __name__ == '__main__':
    unittest.main()



