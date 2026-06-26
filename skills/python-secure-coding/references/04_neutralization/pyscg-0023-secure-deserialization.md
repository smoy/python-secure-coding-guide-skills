# pyscg-0023: Secure Deserialization

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-502 (Deserialization of Untrusted Data).

*Overlaps the security-guidance plugin (the reactive/detective layer); this is the proactive Python-idiom complement.*

## Rule

Prefer text-based serialization formats (`json`, `yaml`) over `pickle`. If `pickle` is architecturally unavoidable, sign serialized payloads with `hmac` using a secret key and verify the signature before calling `pickle.loads()`. Never unpickle data from an untrusted or network-accessible source.

## Why

`pickle.loads()` executes arbitrary Python opcodes during deserialization — an attacker who controls the byte stream can run any OS command before the deserialized object is even returned. JSON and YAML serialize only data values and cannot encode executable opcodes, eliminating this attack surface. When pickle must be used (e.g., for complex object graphs), an HMAC digest over the pickle bytes detects tampering: if the digest does not match, refuse to deserialize.

## Non-compliant

```python
import pickle

class Preserver:
    def uncan(self, jar) -> object:
        return pickle.loads(jar)   # no integrity check; executes attacker opcodes

# Attacker-crafted payload that runs 'whoami' on deserialization:
PAYLOAD = b"cos\nsystem\n(S'whoami'\ntR."
Preserver().uncan(PAYLOAD)         # executes os.system('whoami')
```

## Compliant (preferred: JSON)

```python
import json

class Message:
    def __init__(self, sender_id: int = 0, text: str = ""):
        self.sender_id = sender_id
        self.text = text

class Preserver:
    def can(self, message: Message) -> str:
        return json.dumps(vars(message))           # data only, no methods

    def uncan(self, jar: str) -> Message:
        j = json.loads(jar)                        # JSONDecodeError on a pickle payload
        msg = Message()
        msg.sender_id = int(j["sender_id"])        # explicit type coercion
        msg.text = str(j["text"])
        return msg
```

## Compliant (if pickle is required: HMAC guard)

```python
import hashlib, hmac, pickle, secrets

class Preserver:
    def __init__(self, key: bytes):
        self._key = key

    def can(self, message) -> tuple:
        jar = pickle.dumps(message)
        digest = hmac.new(self._key, jar, hashlib.sha256).hexdigest()
        return digest, jar

    def uncan(self, expected_digest: str, jar: bytes) -> object:
        digest = hmac.new(self._key, jar, hashlib.sha256).hexdigest()
        if expected_digest != digest:
            raise ValueError("Integrity of jar compromised")   # refuse to unpickle
        return pickle.loads(jar)
```

> Note: the HMAC example above demonstrates integrity only. The pickle payload is still not encrypted. Use proper key management and encryption (`pyca/cryptography`) in production.
