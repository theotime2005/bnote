"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import unittest


def main():
    failfast = False

    # Build the test suite
    import tests.tests_edt as tests_edt
    import tests.tests_others as tests_others
    import tests.tests_translation as tests_translation

    loader = unittest.TestLoader()
    suite = tests_others.load_tests(loader, None, None)
    suite.addTests(tests_edt.load_tests(loader, None, None))
    suite.addTests(tests_translation.load_tests(loader, None, None))

    unittest.installHandler()  # Fancy handling for ^C during test
    unittest.TextTestRunner(verbosity=2, failfast=failfast, descriptions=False).run(suite)


if __name__ == '__main__':
    main()
