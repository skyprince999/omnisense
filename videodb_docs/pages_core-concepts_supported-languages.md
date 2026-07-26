### Start Here

- [Welcome to VideoDB](\)
- [Quickstart](\pages\getting-started\quickstart)
- SDK Installation
- [AI Agent Skills](\pages\getting-started\agent-skills)
- [Core Concepts in 5 Minutes](\pages\getting-started\core-concepts-in-5-min)

### Core Concepts

- [Core Concepts Overview](\pages\core-concepts\overview)
- [Data Model](\pages\core-concepts\data-model)
- [Indexes &amp; Search](\pages\core-concepts\indexes-and-search)
- [Supported Languages](\pages\core-concepts\supported-languages)
- [Sandbox Compute](\pages\core-concepts\sandbox-compute)
- [Sandbox Models](\pages\core-concepts\sandbox-models)
- [Events &amp; Real-time](\pages\core-concepts\events-and-realtime)
- [Programmable Editing](\pages\core-concepts\programmable-editing)
- [Security &amp; Privacy](\pages\core-concepts\security-privacy)

### Ingest

- Files and Collections
- Live Streams
- Capture SDKs
- Transcoding

### Understand

- Understanding &amp; Indexing Pipelines
- Search and Retrieval
- Legacy Indexing &amp; Search
- Quality and Evaluation

### Act

- Programmable Editing
- Live Action
- Generative Media
- Output and Delivery

### Automate

- [Integrations Overview](\pages\automate\integrations-overview)
- n8n Workflows
- Zapier Workflows

### Open Source Frameworks

- [MCP Server](\pages\build-with-agents\mcp-server)
- [LlamaIndex Retriever](\pages\community\open-source\llamaindex-retriever)
- Director Framework

## On this page

- [Supported speech-to-text languages](#supported-speech-to-text-languages)

[Core Concepts](\pages\core-concepts\overview)

# Supported Languages

Copy page

Language codes supported by VideoDB speech-to-text and spoken-word indexing.

Copy page

Use these language codes with speech-to-text workflows, including:

- video.understand(analyzers=[{"type": "spoken\_words", "config": {"language": "..."}}])
- video.index\_spoken\_words(language\_code="...")
- video.generate\_transcript(language\_code="...")
- audio.generate\_transcript(language\_code="...")

If you omit the language code, VideoDB uses the default behavior for the selected transcription engine. Pass a code when you want to provide an explicit language hint.

Use lower-case codes. Regional English variants use underscores, such as `en_us` , `en_uk` , and `en_au` .

## [ Supported speech-to-text languages](#supported-speech-to-text-languages)

| Language                | Code    | Language                 | Code    |
|-------------------------|---------|--------------------------|---------|
| Afrikaans               | `af`    | Albanian                 | `sq`    |
| Amharic                 | `am`    | Arabic                   | `ar`    |
| Armenian                | `hy`    | Assamese                 | `as`    |
| Azerbaijani             | `az`    | Bashkir                  | `ba`    |
| Basque                  | `eu`    | Belarusian               | `be`    |
| Bengali                 | `bn`    | Bosnian                  | `bs`    |
| Breton                  | `br`    | Bulgarian                | `bg`    |
| Burmese                 | `my`    | Catalan                  | `ca`    |
| Chinese                 | `zh`    | Croatian                 | `hr`    |
| Czech                   | `cs`    | Danish                   | `da`    |
| Dutch                   | `nl`    | English                  | `en`    |
| English (Australia)     | `en_au` | English (United Kingdom) | `en_uk` |
| English (United States) | `en_us` | Estonian                 | `et`    |
| Faroese                 | `fo`    | Finnish                  | `fi`    |
| French                  | `fr`    | Galician                 | `gl`    |
| Georgian                | `ka`    | German                   | `de`    |
| Greek                   | `el`    | Gujarati                 | `gu`    |
| Haitian Creole          | `ht`    | Hausa                    | `ha`    |
| Hawaiian                | `haw`   | Hebrew                   | `he`    |
| Hindi                   | `hi`    | Hungarian                | `hu`    |
| Icelandic               | `is`    | Indonesian               | `id`    |
| Italian                 | `it`    | Japanese                 | `ja`    |
| Javanese                | `jw`    | Kannada                  | `kn`    |
| Kazakh                  | `kk`    | Khmer                    | `km`    |
| Korean                  | `ko`    | Lao                      | `lo`    |
| Latin                   | `la`    | Latvian                  | `lv`    |
| Lingala                 | `ln`    | Lithuanian               | `lt`    |
| Luxembourgish           | `lb`    | Macedonian               | `mk`    |
| Malagasy                | `mg`    | Malay                    | `ms`    |
| Malayalam               | `ml`    | Maltese                  | `mt`    |
| Maori                   | `mi`    | Marathi                  | `mr`    |
| Manipuri                | `mni`   | Mongolian                | `mn`    |
| Nepali                  | `ne`    | Norwegian                | `no`    |
| Norwegian Nynorsk       | `nn`    | Occitan                  | `oc`    |
| Odia                    | `or`    | Pashto                   | `ps`    |
| Persian                 | `fa`    | Polish                   | `pl`    |
| Portuguese              | `pt`    | Punjabi                  | `pa`    |
| Rajasthani              | `raj`   | Romanian                 | `ro`    |
| Russian                 | `ru`    | Sanskrit                 | `sa`    |
| Serbian                 | `sr`    | Shona                    | `sn`    |
| Sindhi                  | `sd`    | Sinhala                  | `si`    |
| Slovak                  | `sk`    | Slovenian                | `sl`    |
| Somali                  | `so`    | Spanish                  | `es`    |
| Sundanese               | `su`    | Swahili                  | `sw`    |
| Swedish                 | `sv`    | Tagalog                  | `tl`    |
| Tajik                   | `tg`    | Tamil                    | `ta`    |
| Tatar                   | `tt`    | Telugu                   | `te`    |
| Thai                    | `th`    | Tibetan                  | `bo`    |
| Turkish                 | `tr`    | Turkmen                  | `tk`    |
| Ukrainian               | `uk`    | Urdu                     | `ur`    |
| Uzbek                   | `uz`    | Vietnamese               | `vi`    |
| Welsh                   | `cy`    | Yiddish                  | `yi`    |
| Yoruba                  | `yo`    |                          |         |

[Indexes &amp; Search](\pages\core-concepts\indexes-and-search) [Sandbox Compute](\pages\core-concepts\sandbox-compute)

⌘ I