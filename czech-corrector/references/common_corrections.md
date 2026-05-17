# Common Czech Corrections

This file lists typical errors and their corrections used by the rule‑based fallback in the czech_check tool.

## Typo / Agreement Corrections

| Wrong | Correct | Note |
|-------|---------|------|
| skvela | skvělý | masculine singular nominal |
| skvely | skvělý |  |
| skvele | skvěle | adverb |
| rada (before space/verb) | rád | masculine "I am glad" |
| rada (as noun) | rada | keep as noun when not followed by space/verb |
| ma rada | má rád | "has glad" → "likes" |
| ma rad | má rád | missing á |
| dejd | dej | imperative |
| prosim | prosím |  |
| Prosim | Prosím |  |
| dekuji | děkuji |  |
| Dekuji | Děkuji |  |
| mam | mám |  |
| Mam | Mám |  |
| mas | máš |  |
| Mas | Máś |  |
| ma (standalone) | má |  |
| krasny | krásný |  |
| Krasny | Krásný |  |
| krasna | krásná |  |
| Krasna | Krásná |  |
| krasne | krásně |  |
| Krasne | Krásně |  |
| Vcerra | Včera | common typo |
| vcerra | včera |  |
| ... | ... | (extend as needed)

## Usage

The rule‑based fallback applies these via case‑insensitive regex substitution.
LanguageTool jar (if available) is preferred for deeper grammatical correction.
