def get_sample_voices():
    return [
        {
            "voice_id": "21m00Tcm4TlvDq8ikWAM",
            "name": "Rachel",
            "category": "premade",
            "description": "Friendly and professional female voice"
        },
        {
            "voice_id": "AZnzlk1XvdvUeBnXmlld",
            "name": "Domi",
            "category": "premade",
            "description": "Deep and authoritative male voice"
        },
        {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",
            "name": "Bella",
            "category": "premade",
            "description": "Soft and calming female voice"
        },
        {
            "voice_id": "ErXwobaYiN019PkySvjV",
            "name": "Antoni",
            "category": "premade",
            "description": "Energetic and cheerful male voice"
        },
        {
            "voice_id": "MF3mGyEYCl7XYWbV9V6O",
            "name": "Elli",
            "category": "premade",
            "description": "Playful and youthful female voice"
        }
    ]

def generate_waveform():
    import matplotlib.pyplot as plt
    import numpy as np
    import io
    
    np.random.seed(42)
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 10 * t)
    
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(t, signal, color='purple')
    ax.fill_between(t, signal, color='purple', alpha=0.3)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    buf.seek(0)
    plt.close(fig)
    
    return buf