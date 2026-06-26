# pyscg-0045: Enforce Consistent Encoding

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-693 (pillar), CWE-707 (pillar), CWE-176 (Improper Handling of Unicode Encoding), CWE-838 (Inappropriate Encoding for Output Context).

## Rule

**Use a single, explicit encoding (UTF-8) end-to-end.** Never silently transcode or down-convert data between systems — especially not from UTF-8 to ASCII with `errors="ignore"`, which can collapse harmless strings into executable payloads.

## Why

Changing encoding mid-pipeline can turn a filtered-but-harmless string into a dangerous one. For example, `<script生>` is rejected by a UTF-8 validator but becomes a working `<script>` tag after `decode("ascii", "ignore")` strips the CJK character. Similarly, reading a UTF-8 stream with the wrong codec raises `UnicodeDecodeError`, hiding forensic data or crashing the application. Always declare encodings explicitly at every I/O boundary; never rely on platform defaults.

## Non-compliant

```python
import io

LOREM = "..."  # UTF-8 text

output = io.BytesIO()
wrapper = io.TextIOWrapper(output, encoding='utf-8', line_buffering=True)
wrapper.write(LOREM)
wrapper.seek(0, 0)
# Wrong codec — raises UnicodeDecodeError
print(f"{len(output.getvalue().decode('utf-16le'))} characters in string")
```

```python
# Encoding collapse: validate in UTF-8, output in ASCII — creates XSS.
# The two functions model two systems that disagree on encoding.
def write_message(text: str) -> bytes:
    return text.encode("utf-8")                # System A: stores/validates as UTF-8

def read_message(message: bytes):
    print(message.decode("ascii", "ignore"))   # System B: strips non-ASCII silently

floppy = write_message("<script生>")  # passes a UTF-8 validator (生 is harmless)
read_message(floppy)                  # System B prints: <script>  (XSS payload)
```

## Compliant

```python
import io

LOREM = "..."  # UTF-8 text

output = io.BytesIO()
wrapper = io.TextIOWrapper(output, encoding='utf-8', line_buffering=True)
wrapper.write(LOREM)
wrapper.seek(0, 0)
# Consistent codec — works correctly
print(f"{len(output.getvalue().decode('utf-8'))} characters in string")
```

```python
import base64


def report_record_attack(stream: bytearray):
    try:
        decoded_text = stream.decode("utf-8")
    except UnicodeDecodeError as e:
        # Preserve data losslessly; flag for forensic analysis
        encoded_payload = base64.b64encode(stream).decode("utf-8")
        print("Base64 Encoded Payload for Forensic Analysis:", encoded_payload)
        print("Error decoding payload:", e)
    else:
        print("Important text:", decoded_text)
```

> Cross-ref: pyscg-0044 (canonicalize before validating), pyscg-0047 (use allow lists over deny lists). Use `base64` for lossless logging of binary/suspect payloads.
