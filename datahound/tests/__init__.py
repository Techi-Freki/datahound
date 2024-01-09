import unittest

from datahound.tests.dataproviderbase_testcase import TestCaseDataProviderBase


def test_suite():
    suite = unittest.TestSuite()
    add_dataproviderbase_tests(suite)

    return suite


def add_dataproviderbase_tests(suite):
    suite.addTest(TestCaseDataProviderBase('test_connection_error'))
    suite.addTest(TestCaseDataProviderBase('test_executeCreate'))
    suite.addTest(TestCaseDataProviderBase('test_executeInsertTruncate'))
    suite.addTest(TestCaseDataProviderBase('test_fetchall'))
    suite.addTest(TestCaseDataProviderBase('test_fetchmany'))
    suite.addTest(TestCaseDataProviderBase('test_fetchone'))
    suite.addTest(TestCaseDataProviderBase('test_execute_scripts'))
    suite.addTest(TestCaseDataProviderBase('test_execute_scripts_fail'))
    suite.addTest(TestCaseDataProviderBase('test_fetchallwithparameters'))
    suite.addTest(TestCaseDataProviderBase('test_insertreturnid'))
    suite.addTest(TestCaseDataProviderBase('test_insertreturnid_fail'))
    suite.addTest(TestCaseDataProviderBase('test_insertmany'))
    suite.addTest(TestCaseDataProviderBase('test_insertmany_fail'))


if __name__ == '__main__':
    unittest.main(defaultTest=test_suite())
