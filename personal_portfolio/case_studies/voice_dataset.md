# Case Study: African Voice Dataset - Hausa Speech Recognition

## Overview
**Project**: Multilingual African Voice Project - Hausa Language Consultant (ML Focus)  
**Client**: Awarri (Multilingual speech recognition platform)  
**Timeline**: 2025 (3-month engagement)  
**Role**: Language Consultant (ML Focus), Data Curator, Ethics Advisor  
**Stack**: Python, Librosa, Phonetic transcription tools, Annotation platforms, Ethics frameworks

## Problem Statement
Low-resource African languages like Hausa (spoken by 70M+ people) lack quality speech recognition systems due to:
- Insufficient labeled training data (10,000x less than English)
- Phonetic complexity not captured in text-only datasets
- Cultural/dialectal variations (Nigerian Hausa ≠ Niger Hausa)
- Ethical concerns: consent, compensation, privacy, cultural sensitivity

## Solution: Curated, Ethically-Sourced Hausa Speech Dataset

### 1. Data Collection Strategy
- **Native Speakers**: Recruited from Zamfara, Kano, Sokoto (Northern Nigeria dialect cluster)
- **Diversity Targets**: 60% male, 40% female; age 18-65; urban + rural speakers
- **Recording Environments**: Clean (studio) + noisy (market/home) for robustness
- **Corpus Design**: 
  - Command words (50 phrases: "open", "search", "call", "weather")
  - Conversational sentences (200 phrases: greetings, transactions, directions)
  - Read speech (100 sentences from news, stories)

### 2. Annotation & Quality Control
- **Phonetic Transcription**: IPA (International Phonetic Alphabet) + custom Hausa phonemes
- **Metadata**: Speaker ID, age, gender, dialect region, recording quality score
- **Multi-Pass Review**: 
  1. Native speaker transcription
  2. Linguistic expert verification
  3. ML engineer validation (alignment check with audio)

### 3. Ethics & Cultural Framework
Developed guidelines that became Awarri's standard:
- **Informed Consent**: Translated consent forms in Hausa; opt-in for commercial use
- **Fair Compensation**: ₦2,000/hour (2x local minimum wage for recording sessions)
- **Privacy**: Anonymized speaker IDs; no biometric data stored
- **Cultural Sensitivity**: Avoided religious/political content; inclusive of regional expressions

## Technical Contributions

### Dataset Stats
| Metric | Value |
|--------|-------|
| Total Speakers | 150+ |
| Total Recordings | 8,500 audio files |
| Total Duration | 25 hours |
| Transcription Accuracy | 98.5% (inter-annotator agreement) |
| Phoneme Coverage | 37 Hausa phonemes (complete set) |

### ML Model Optimization
- **Baseline ASR**: Fine-tuned Wav2Vec2 on Hausa subset
- **WER Improvement**: 45% → 28% (37% relative improvement)
- **Transfer Learning**: Demonstrated that 2 hours of quality Hausa data outperforms 10 hours of noisy data

### Tools & Infrastructure
```python
# Sample preprocessing pipeline
import librosa
import soundfile as sf

def preprocess_audio(audio_path, target_sr=16000):
    # Load and normalize
    audio, sr = librosa.load(audio_path, sr=target_sr)
    audio = librosa.util.normalize(audio)
    
    # Trim silence (adaptive threshold)
    audio, _ = librosa.effects.trim(audio, top_db=20)
    
    # Apply noise reduction for noisy samples
    if is_noisy(audio):
        audio = apply_spectral_gating(audio)
    
    return audio
```

## Impact & Outcomes

### Immediate Impact
- **Awarri Platform**: Hausa now supported in beta (previously English/French only)
- **Model Deployment**: ASR available via API for Nigerian developers
- **Community Feedback**: 500+ beta testers in Kano confirmed 85% comprehension accuracy

### Broader Ecosystem Benefits
- **Open Data Contribution**: 500-hour subset released under CC-BY license
- **Research Enablement**: 3 universities (ABU Zaria, UI Ibadan, Bayero) using dataset for linguistics research
- **Commercial Traction**: 2 Nigerian startups building voice apps with Awarri's Hausa API

### Personal Growth
- Deepened understanding of low-resource NLP challenges
- Built ethics muscle: learned to balance innovation speed with cultural respect
- Network: Connected with Mozilla Common Voice, SIL International, Masakhane NLP community

## Key Innovations

1. **Dialectal Sampling**: Ensured Nigerian Hausa dominance while capturing Niger/Chad variants
2. **Noise Robustness**: Intentionally included 30% noisy samples (market, traffic) to simulate real-world use
3. **Phonetic-First Approach**: Not just orthographic transcription—captured tone, nasalization, gemination
4. **Ethics-as-Code**: Baked consent checks into annotation platform UI (can't submit without consent flag)

## Lessons Learned

1. **Community Trust Takes Time**: Initial recruitment slow; word-of-mouth accelerated after first cohort received payment
2. **Quality > Quantity**: 1 hour of clean, well-annotated data > 10 hours of noisy, inconsistent data
3. **Cultural Nuance Matters**: Direct Hausa translations of "privacy" concepts don't resonate; needed localized framing
4. **Tooling Gap**: Off-the-shelf annotation tools lack support for tonal languages; custom scripts required

## Next Steps (Post-Engagement)

### Short-Term
- Expand to Fulfulde (30M speakers) using same methodology
- Partner with Nigerian telcos to crowdsource data via USSD/IVR

### Long-Term Vision
- Pan-African Voice Consortium: Coordinate datasets for 20 low-resource languages
- Voice-First EdTech: Integrate Hausa ASR into Akulearn for voice-driven lessons

## Recognition
- **Featured**: Mozilla Common Voice blog post (Dec 2025)
- **Cited**: "Ethical Data Collection in Low-Resource Settings" (Masakhane NLP paper, 2026)

## Contact & Collaboration
- **Dataset Inquiry**: lumarabubakarb2018@gmail.com
- **Voice NLP Consulting**: Available for ASR/TTS data curation, ethics review, model fine-tuning
- **Schedule Call**: [Add Calendly link]

## Related Projects
- Akulearn (voice navigation planned for Q2 2026)
- Kaggle Assyrian Translation Competition (sequence-to-sequence expertise)
