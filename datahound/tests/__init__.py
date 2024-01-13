import unittest

from datahound.tests.dataproviderbase_testcase import TestCaseDataProviderBase


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCaseDataProviderBase))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite())
