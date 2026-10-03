import streamlit as st
from pathlib import Path
import json
import subprocess
import signal
import os

BASE = Path(__file__).resolve().parent
CONFIG_DIR = BASE / "config"
PLAYLIST_FILE = CONFIG_DIR / "playlist.json"
PID_FILE = BASE / "live.pid"

st.set_page_config(page_title="3D GOKIL LIVE", page_icon="🎸", layout="wide")

st.markdown("""
<style>
.stApp { background: #050505; }
h1, h2, h3 { color: #39FF14; }
.status { padding:12px; border-radius:10px; background:#101010;
          border:1px solid #39FF14; margin-bottom:15px; }
</style>
""", unsafe_allow_html=True)

def load_playlist():
    if not PLAYLIST_FILE.exists():
        return []
    try:
        return json.loads(PLAYLIST_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        st.error(f"Gagal membaca playlist.json: {e}")
        return []

def live_running():
    if not PID_FILE.exists():
        return False
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)
        return True
    except Exception:
        try: PID_FILE.unlink()
        except FileNotFoundError: pass
        return False

def start_live(selected):
    script = BASE / "scripts" / "live_engine.sh"
    if not script.exists():
        st.error("scripts/live_engine.sh belum ada.")
        return
    if live_running():
        st.warning("LIVE sudah berjalan.")
        return
    (CONFIG_DIR / "active_playlist.json").write_text(
        json.dumps(selected, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    try:
        proc = subprocess.Popen(
            ["bash", str(script)], cwd=str(BASE),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        PID_FILE.write_text(str(proc.pid), encoding="utf-8")
        st.success(f"LIVE engine dimulai. PID: {proc.pid}")
    except Exception as e:
        st.error(f"Gagal menjalankan LIVE engine: {e}")

def stop_live():
    if not PID_FILE.exists():
        st.info("LIVE tidak sedang berjalan.")
        return
    try:
        pid = int(PID_FILE.read_text().strip())
        os.killpg(pid, signal.SIGTERM)
        st.success("Perintah STOP dikirim ke LIVE engine.")
    except Exception as e:
        st.error(f"Gagal menghentikan LIVE: {e}")
    finally:
        try: PID_FILE.unlink()
        except FileNotFoundError: pass

playlist = load_playlist()

st.title("🎸 3D GOKIL LIVE")
st.markdown(
    '<div class="status"><b>DNA:</b> '
    '<span style="color:#39FF14;font-weight:700;">NEON GREEN</span> + '
    '<span style="color:#FF1744;font-weight:700;">CRIMSON RED</span> '
    '| Indonesian Cyber-Mystic Rock Dangdut</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎵 Playlist")
    if not playlist:
        st.warning("Playlist masih kosong. Isi config/playlist.json.")
        selected = []
    else:
        labels = [f"{i+1:02d}. {x.get('title','Tanpa Judul')}" for i,x in enumerate(playlist)]
        selected_labels = st.multiselect("Pilih lagu untuk LIVE", labels, default=labels)
        selected = [playlist[labels.index(x)] for x in selected_labels]

with col2:
    st.subheader("📡 LIVE CONTROL")
    if live_running():
        st.success("🟢 LIVE ENGINE AKTIF")
    else:
        st.error("🔴 OFFLINE")

    if st.button("▶ START LIVE", use_container_width=True, type="primary"):
        if not selected:
            st.error("Pilih minimal 1 lagu.")
        else:
            start_live(selected)
            st.rerun()

    if st.button("⏹ STOP LIVE", use_container_width=True):
        stop_live()
        st.rerun()

st.divider()
st.subheader("📋 Daftar Lagu")
for i, item in enumerate(playlist, 1):
    st.write(f"**{i:02d}. {item.get('title','Tanpa Judul')}** — `{item.get('music','')}`")

with st.expander("ℹ️ Struktur proyek"):
    st.code("""3d-gokil-live/
├── app.py
├── requirements.txt
├── config/
│   ├── playlist.json
│   └── active_playlist.json
├── music/
├── image/
└── scripts/
    └── live_engine.sh
""")

st.caption("Tahap 1: panel Streamlit + kontrol engine. FFmpeg/YouTube RTMP disambungkan berikutnya.")
