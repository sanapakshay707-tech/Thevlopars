import json
import logging
import re
from typing import Any, Dict, List, Optional
import httpx
from .config import (
    OLLAMA_BASE_URL,
    OLLAMA_GENERATE_URL,
    OLLAMA_TAGS_URL,
    OLLAMA_MODEL,
    REQUEST_TIMEOUT_SECONDS,
)

logger = logging.getLogger("courtlens.ollama_client")


class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, default_model: str = OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.generate_url = f"{self.base_url}/api/generate"
        self.tags_url = f"{self.base_url}/api/tags"
        self.default_model = default_model

    async def check_health(self) -> Dict[str, Any]:
        """Checks if Ollama is reachable and returns installed models."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(self.tags_url)
                if res.status_code == 200:
                    data = res.json()
                    models = [m.get("name") for m in data.get("models", [])]
                    model_ready = any(self.default_model in m for m in models)
                    return {
                        "ready": True,
                        "model": self.default_model,
                        "available_models": models,
                        "model_installed": model_ready,
                        "error": None,
                    }
                else:
                    return {
                        "ready": False,
                        "model": self.default_model,
                        "available_models": [],
                        "model_installed": False,
                        "error": f"Ollama HTTP {res.status_code}",
                    }
        except httpx.ConnectError:
            return {
                "ready": False,
                "model": self.default_model,
                "available_models": [],
                "model_installed": False,
                "error": f"Cannot connect to Ollama at {self.base_url}. Is Ollama running?",
            }
        except Exception as e:
            return {
                "ready": False,
                "model": self.default_model,
                "available_models": [],
                "model_installed": False,
                "error": str(e),
            }

    async def generate_json(self, prompt: str, system: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Sends generation request to Ollama with format='json'.
        Returns parsed python dictionary.
        """
        target_model = model or self.default_model
        payload = {
            "model": target_model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.1,
                "num_predict": 1200,
            },
        }
        if system:
            payload["system"] = system

        logger.info(f"Sending prompt to Ollama ({self.generate_url}) with model: {target_model}")
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
                response = await client.post(self.generate_url, json=payload)
                if response.status_code != 200:
                    raise RuntimeError(f"Ollama returned HTTP {response.status_code}: {response.text}")

                res_json = response.json()
                raw_text = res_json.get("response", "").strip()

                # Clean any markdown json code blocks if present
                clean_text = self._strip_fences(raw_text)
                try:
                    parsed = json.loads(clean_text)
                except json.JSONDecodeError:
                    # Try regex extraction of first JSON object
                    obj_match = re.search(r"\{.*\}", clean_text, re.DOTALL)
                    if obj_match:
                        parsed = json.loads(obj_match.group(0))
                    else:
                        parsed = {"summary": clean_text}

                # If parsed is a string (e.g. double encoded JSON)
                if isinstance(parsed, str):
                    try:
                        inner = json.loads(parsed)
                        if isinstance(inner, dict):
                            parsed = inner
                        else:
                            parsed = {"summary": parsed}
                    except Exception:
                        parsed = {"summary": parsed}

                # If parsed is a list
                if isinstance(parsed, list):
                    merged = {}
                    for item in parsed:
                        if isinstance(item, dict):
                            merged.update(item)
                    parsed = merged if merged else {"items": parsed}

                if not isinstance(parsed, dict):
                    parsed = {"summary": str(parsed)}

                return parsed

        except httpx.ConnectError:
            raise ConnectionError(f"Could not connect to Ollama at {self.generate_url}. Ensure Ollama is running.")
        except httpx.TimeoutException:
            raise TimeoutError(f"Ollama inference timed out after {REQUEST_TIMEOUT_SECONDS}s. Consider using a shorter document or faster model.")
        except Exception as e:
            logger.error(f"Ollama generation error: {type(e).__name__}: {e or repr(e)}")
            raise

    @staticmethod
    def _strip_fences(text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
