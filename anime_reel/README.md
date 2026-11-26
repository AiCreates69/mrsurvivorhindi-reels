# LAAL JHOOTH — Part 1 (code-only anime-style reel)

A 9:16 Hindi reel built only with code: no image or video AI. It follows the same format as the reference "Teen Second"
reel: a first-person deadpan narrator, a superpower with a funny limit, quick comedic proofs and a cliffhanger. The
premise, characters and art are original.

- `out/laal_jhooth_part1.mp4`: the finished video (1080x1920, 24 fps, ~50 s)
- `lines.py`: narration (Hindi for TTS, plus Hinglish subtitles)
- `episode.py`: timeline, 9 shots, glitch "lie turns red" text, captions, post FX, music + SFX mix
- `chars.py`: anime bust characters (Kabir, Mummy, Sir, Meera, Bunty, the Stranger)
- `sets.py`: painted backgrounds (storm terrace, kitchen, bedroom, classroom, arched corridor, rainy bus stop)
- `gfx.py`: cairo/PIL helpers; `audio_kit.py`: Kokoro TTS + SFX (from Code Reels Studio)

Render: `python episode.py` (needs pycairo, pillow, numpy, scipy, soundfile, kokoro-onnx, ffmpeg and the Code Reels
Studio voice model/fonts). Preview stills: `python episode.py --stills 1,5,10`.
