# 3D GOKIL LIVE

Control panel Streamlit untuk LIVE 3D GOKIL.

## DNA visual
- Neon Green `#39FF14`
- Crimson Red `#FF1744`
- Black/dark background
- Chrome/white accents
- Indonesian Cyber-Mystic Rock Dangdut

## Struktur
```text
3d-gokil-live/
├── app.py
├── requirements.txt
├── config/
│   └── playlist.json
├── music/
├── image/
└── scripts/
    └── live_engine.sh
```

## Jalankan lokal
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Tahap pertama hanya menguji panel dan tombol START/STOP.
FFmpeg + YouTube RTMP belum diaktifkan.
