# tests/test_env.py
import unittest
import json
import urllib.request
import urllib.error
from lifepim_ai_core.core.llm_runtime import config as cfg

class TestEnvironment(unittest.TestCase):
    def test_01_ollama(self):
        """
        Verify Ollama server is running and responding.
        This does NOT require a model to be loaded.
        """

        url = "http://127.0.0.1:11434/api/tags"

        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                self.assertEqual(resp.status, 200)

                data = json.loads(resp.read().decode("utf-8"))
                self.assertIn("models", data)
                self.assertIsInstance(data["models"], list)

        except urllib.error.URLError as e:
            self.fail(f"Ollama not reachable at {url}: {e}")
        except Exception as e:
            self.fail(f"Ollama check failed: {e}")


    def test_02_ollama_generate(self):
        """
        Optional: verify Ollama can generate text.
        Requires at least one model to be available.
        """
        url = "http://127.0.0.1:11434/api/generate"
        payload = {
            "model": cfg.MODEL_NAME,
            "prompt": "Say hello.",
            "stream": False
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("response", data)
            reply = data["response"]

            self.assertGreater(
                len(reply.strip()),
                2,
                f"Ollama returned empty/short response for model '{cfg.MODEL_NAME}': {reply}"
            )

if __name__ == '__main__':
    unittest.main()
