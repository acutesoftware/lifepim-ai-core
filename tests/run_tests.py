# run_tests.py
import unittest

#if __name__ == "__main__":
#    all_tests = unittest.TestLoader().discover('.', pattern='test*.py')
#    unittest.TextTestRunner().run(all_tests)    

if __name__ == "__main__":
    suite = unittest.TestLoader().discover(".", pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)