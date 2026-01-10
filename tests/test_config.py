# test_config.py
import os
import sys
import unittest


from lifepim_ai_core.core.llm_runtime import config as cfg

class TestConfig(unittest.TestCase):
    def test_required_config_vars_exist(self):
        required = [
            "EMBED_MODEL",
            "PROVIDER",
            "MODEL_NAME",
            "TEMPERATURE",
            "MAX_TOKENS",
            "MAX_CONTEXT_MESSAGES",
            "TOP_K",
            "RAG_TOP_K",
            "EFFECTIVE_CONTEXT_LIMIT",
        ]

        missing = [name for name in required if not hasattr(cfg, name)]
        self.assertEqual(missing, [], f"Missing config vars: {missing}")

    def test_required_config_vars_not_blank(self):
        # strings
        for name in ["EMBED_MODEL", "PROVIDER", "MODEL_NAME"]:
            val = getattr(cfg, name)
            self.assertIsInstance(val, str, f"{name} must be str")
            self.assertTrue(val.strip(), f"{name} must not be blank")

    def test_config_types_and_ranges(self):
        self.assertIsInstance(cfg.EMBED_MODEL, str)
        self.assertIsInstance(cfg.PROVIDER, str)
        self.assertIsInstance(cfg.MODEL_NAME, str)

        self.assertIsInstance(cfg.TEMPERATURE, (int, float))
        self.assertGreaterEqual(cfg.TEMPERATURE, 0.0)
        self.assertLessEqual(cfg.TEMPERATURE, 2.0)  # common practical range

        self.assertIsInstance(cfg.MAX_TOKENS, int)
        self.assertGreater(cfg.MAX_TOKENS, 0)

        self.assertIsInstance(cfg.MAX_CONTEXT_MESSAGES, int)
        self.assertGreater(cfg.MAX_CONTEXT_MESSAGES, 0)

        self.assertIsInstance(cfg.TOP_K, int)
        self.assertGreater(cfg.TOP_K, 0)

        self.assertIsInstance(cfg.RAG_TOP_K, int)
        self.assertEqual(cfg.RAG_TOP_K, cfg.TOP_K, "RAG_TOP_K should match TOP_K")

        self.assertIsInstance(cfg.EFFECTIVE_CONTEXT_LIMIT, int)
        self.assertGreater(cfg.EFFECTIVE_CONTEXT_LIMIT, 0)

    def test_allowed_values(self):
        # Keep these lists small and intentional
        self.assertIn(cfg.PROVIDER.lower(), {"ollama", "openai", "lmstudio"})
        self.assertIn(cfg.EMBED_MODEL.lower(), {"nomic-embed-text", "huggingface", "openai"})
        
if __name__ == '__main__':
    unittest.main()