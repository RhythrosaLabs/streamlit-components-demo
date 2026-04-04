import base64
import streamlit as st

st.set_page_config(page_title="Streamlit Components Demo", layout="wide", page_icon="🧩")

st.title("🧩 Streamlit Components Showcase")
st.caption("Four custom components by Dan Sheils — Kanban · Audio Editor · Stepper · Node Editor")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Kanban", "🎛️ Audio Editor", "🪜 Stepper", "🔗 Node Editor"])

# ─── Kanban ──────────────────────────────────────────────────────────────────
with tab1:
    from streamlit_kanban import st_kanban

    st.subheader("Drag-and-drop Kanban Board")
    st.caption("Move cards between columns, click to edit, add new cards.")

    DEFAULT_COLUMNS = [
        {
            "id": "backlog",
            "title": "Backlog",
            "color": "#6366f1",
            "cards": [
                {"id": "c1", "title": "Research competitors", "tag": "Research", "priority": "low"},
                {"id": "c2", "title": "Define MVP scope", "tag": "Strategy", "priority": "high"},
            ],
        },
        {
            "id": "in-progress",
            "title": "In Progress",
            "color": "#f59e0b",
            "cards": [
                {"id": "c3", "title": "Build auth flow", "tag": "Dev", "priority": "high"},
            ],
        },
        {
            "id": "review",
            "title": "In Review",
            "color": "#8b5cf6",
            "cards": [
                {"id": "c4", "title": "Landing page redesign", "tag": "Design", "priority": "high"},
            ],
        },
        {
            "id": "done",
            "title": "Done",
            "color": "#10b981",
            "cards": [
                {"id": "c5", "title": "Project kickoff", "tag": "Planning", "priority": "low"},
            ],
        },
    ]

    if "board" not in st.session_state:
        st.session_state.board = DEFAULT_COLUMNS

    result = st_kanban(st.session_state.board, key="demo_kanban")
    if result:
        st.session_state.board = result

    with st.expander("Board JSON"):
        st.json(st.session_state.board)

# ─── Audio Editor ────────────────────────────────────────────────────────────
with tab2:
    from streamlit_audio_editor import st_audio_editor

    st.subheader("Browser-Based Audio Editor & Jam Session")
    st.caption("Load audio or enable your mic. Apply effects in real time. Hit REC to capture your jam.")

    result = st_audio_editor(key="demo_audio")

    if result and result.get("type") == "export":
        col1, col2, col3 = st.columns(3)
        col1.metric("Trim start", f"{result['trimStart']:.3f}s")
        col2.metric("Trim end", f"{result['trimEnd']:.3f}s")
        col3.metric("Duration", f"{result['trimEnd'] - result['trimStart']:.3f}s")

        wav_bytes = base64.b64decode(result["wavBase64"])
        st.audio(wav_bytes, format="audio/wav")
        st.download_button("⬇ Download trimmed WAV", wav_bytes, "trimmed.wav", "audio/wav")

    if result and result.get("type") == "recording":
        st.success(f"🎤 Recording captured — {result['durationSec']:.1f}s")
        audio_bytes = base64.b64decode(result["recordingBase64"])
        st.audio(audio_bytes, format=result["mimeType"])
        st.download_button("⬇ Download recording", audio_bytes, "jam.webm", result["mimeType"])

# ─── Stepper ─────────────────────────────────────────────────────────────────
with tab3:
    from streamlit_stepper import st_stepper

    st.subheader("Multi-Step Wizard")
    st.caption("Fill out each step, validation blocks progress until required fields are complete.")

    STEPS = [
        {
            "label": "Project",
            "subtitle": "Name & describe",
            "icon": "◈",
            "fields": [
                {"key": "name", "label": "Project name", "type": "text",
                 "placeholder": "e.g. Apollo Dashboard", "required": True},
                {"key": "description", "label": "Description", "type": "textarea",
                 "placeholder": "What does this project do?", "required": False},
                {"key": "type", "label": "Project type", "type": "select",
                 "options": ["Web App", "Data Pipeline", "ML Model", "API Service"],
                 "required": True},
            ],
        },
        {
            "label": "Team",
            "subtitle": "Add collaborators",
            "icon": "◉",
            "fields": [
                {"key": "owner", "label": "Owner email", "type": "text",
                 "placeholder": "you@company.com", "required": True},
                {"key": "size", "label": "Team size", "type": "select",
                 "options": ["Solo", "2–5", "6–15", "15+"], "required": True},
            ],
        },
        {
            "label": "Review",
            "subtitle": "Confirm & launch",
            "icon": "◆",
            "fields": [],
        },
    ]

    result = st_stepper(STEPS, orientation="horizontal", key="demo_stepper")

    if result and result.get("completed"):
        st.balloons()
        st.success(f"Project **{result['values'].get('name', 'Untitled')}** created!")
        st.json(result["values"])

# ─── Node Editor ─────────────────────────────────────────────────────────────
with tab4:
    from streamlit_node_editor import st_node_editor

    st.subheader("Node Graph Editor")
    st.caption("Right-click the canvas to add nodes. Drag ports to connect. Click a wire to delete. Del key removes selected node.")

    NODE_DEFS = {
        "Load Checkpoint": {
            "category": "Loaders",
            "headerColor": "#fb923c",
            "inputs": [],
            "outputs": [
                {"name": "MODEL", "type": "MODEL"},
                {"name": "CLIP", "type": "CLIP"},
                {"name": "VAE", "type": "VAE"},
            ],
            "params": [
                {"key": "ckpt_name", "label": "Checkpoint", "type": "select",
                 "options": ["v1-5-pruned.ckpt", "sd_xl_base.safetensors"]},
            ],
        },
        "CLIP Text Encode": {
            "category": "Conditioning",
            "headerColor": "#facc15",
            "inputs": [{"name": "clip", "type": "CLIP"}],
            "outputs": [{"name": "CONDITIONING", "type": "LATENT"}],
            "params": [{"key": "text", "label": "Prompt", "type": "textarea"}],
        },
        "KSampler": {
            "category": "Sampling",
            "headerColor": "#818cf8",
            "inputs": [
                {"name": "model", "type": "MODEL"},
                {"name": "positive", "type": "LATENT"},
                {"name": "negative", "type": "LATENT"},
                {"name": "latent_image", "type": "LATENT"},
            ],
            "outputs": [{"name": "LATENT", "type": "LATENT"}],
            "params": [
                {"key": "steps", "label": "Steps", "type": "int", "default": 20},
                {"key": "cfg", "label": "CFG", "type": "float", "default": 7.0},
                {"key": "sampler", "label": "Sampler", "type": "select",
                 "options": ["euler", "euler_a", "dpm++2m", "ddim"]},
            ],
        },
        "Empty Latent Image": {
            "category": "Latent",
            "headerColor": "#c084fc",
            "inputs": [],
            "outputs": [{"name": "LATENT", "type": "LATENT"}],
            "params": [
                {"key": "width", "label": "Width", "type": "int", "default": 512},
                {"key": "height", "label": "Height", "type": "int", "default": 512},
            ],
        },
        "VAE Decode": {
            "category": "Latent",
            "headerColor": "#f87171",
            "inputs": [
                {"name": "samples", "type": "LATENT"},
                {"name": "vae", "type": "VAE"},
            ],
            "outputs": [{"name": "IMAGE", "type": "IMAGE"}],
            "params": [],
        },
        "Save Image": {
            "category": "Output",
            "headerColor": "#4ade80",
            "inputs": [{"name": "images", "type": "IMAGE"}],
            "outputs": [],
            "params": [
                {"key": "filename_prefix", "label": "Filename", "type": "string",
                 "default": "output"},
            ],
        },
    }

    graph = st_node_editor(NODE_DEFS, height=650, key="demo_graph")

    if graph:
        with st.expander(f"Graph JSON — {len(graph['nodes'])} nodes, {len(graph['connections'])} connections"):
            st.json(graph)
