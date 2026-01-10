# test_llm_runtime.py
import os
import sys
import unittest


import lifepim_ai_core.core.llm_runtime.runtime as llm_rt
from lifepim_ai_core.core.llm_runtime import config as cfg

class TestLLMRuntime(unittest.TestCase):
    def test_builds_llm_object_with_expected_interface(self):
        llm = llm_rt.get_llm(cfg)

        self.assertTrue(hasattr(llm, "invoke"))
        self.assertTrue(callable(llm.invoke))
        self.assertTrue(hasattr(llm, "_chain"))
        self.assertIsNotNone(llm._chain)

        # check required params are set - 'model': 'gpt-oss:20b', 'temperature': 0.2, 'max_tokens': 256}
        self.assertIn("model", llm._params)
        self.assertEqual(llm._params["model"], cfg.MODEL_NAME)

        self.assertIn("temperature", llm._params)
        self.assertEqual(llm._params["temperature"], cfg.TEMPERATURE)

        self.assertIn("max_tokens", llm._params)
        self.assertEqual(llm._params["max_tokens"], cfg.MAX_TOKENS)


    def test_llm_invoke_returns_text(self):
        llm = llm_rt.get_llm(cfg)

        prompt = "Reply with a short sentence."
        result = llm.invoke(prompt)

        # Basic sanity checks
        self.assertIsInstance(result, str)
        self.assertGreater(len(result.strip()), 2)

        # Optional: avoid obvious failure modes
        self.assertNotIn("error", result.lower())
        self.assertNotIn("exception", result.lower())

if __name__ == '__main__':
    unittest.main()

    