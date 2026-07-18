import os

def create_svgs():
    images_dir = os.path.join('static', 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # 1. Pad Pro
    pad_pro = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#4f46e5;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#ec4899;stop-opacity:1" />
        </linearGradient>
        <filter id="glow1">
          <feGaussianBlur stdDeviation="15" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      <rect width="100%" height="100%" fill="url(#g1)"/>
      <rect x="80" y="60" width="240" height="280" rx="16" fill="#0f172a" stroke="#ffffff" stroke-width="4"/>
      <rect x="95" y="75" width="210" height="250" rx="8" fill="#020617"/>
      <circle cx="200" cy="200" r="40" fill="#a78bfa" opacity="0.4" filter="url(#glow1)"/>
      <rect x="180" y="328" width="40" height="4" rx="2" fill="#475569"/>
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="22" font-weight="bold">Pad Pro</text>
    </svg>'''
    
    # 2. Ultrabook
    ultrabook = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#8b5cf6;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#g2)"/>
      <!-- Screen -->
      <rect x="70" y="80" width="260" height="170" rx="8" fill="#1e293b" stroke="#ffffff" stroke-width="4"/>
      <rect x="80" y="90" width="240" height="150" rx="4" fill="#0f172a"/>
      <!-- Keyboard Base -->
      <polygon points="50,260 350,260 370,285 30,285" fill="#334155" stroke="#ffffff" stroke-width="3"/>
      <rect x="175" y="278" width="50" height="5" rx="1" fill="#1e293b"/>
      <text x="50%" y="42%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="20" font-weight="bold">ZenBook</text>
    </svg>'''
    
    # 3. Watch
    watch = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g3" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#06b6d4;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#10b981;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#g3)"/>
      <!-- Straps -->
      <rect x="165" y="40" width="70" height="320" rx="12" fill="#1e293b"/>
      <!-- Dial -->
      <circle cx="200" cy="200" r="85" fill="#0f172a" stroke="#ffffff" stroke-width="5"/>
      <circle cx="200" cy="200" r="75" fill="#020617"/>
      <!-- Screen Details -->
      <circle cx="200" cy="200" r="60" fill="none" stroke="#334155" stroke-dasharray="10 5" stroke-width="2"/>
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="18" font-weight="bold">10:09 AM</text>
      <text x="50%" y="60%" dominant-baseline="middle" text-anchor="middle" fill="#10b981" font-family="sans-serif" font-size="12" font-weight="bold">AeroFit v4</text>
    </svg>'''
    
    # 4. Band
    band = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g4" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#ec4899;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#f59e0b;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#g4)"/>
      <!-- Strap -->
      <rect x="175" y="30" width="50" height="340" rx="16" fill="#1e293b"/>
      <!-- Body -->
      <rect x="165" y="110" width="70" height="180" rx="20" fill="#0f172a" stroke="#ffffff" stroke-width="3"/>
      <rect x="172" y="117" width="56" height="166" rx="15" fill="#020617"/>
      <!-- Heartrate Line -->
      <path d="M 180 200 L 195 200 L 200 185 L 205 215 L 210 200 L 220 200" fill="none" stroke="#ec4899" stroke-width="3"/>
      <text x="50%" y="38%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="11" font-weight="bold">84 BPM</text>
    </svg>'''
    
    # 5. Headphones
    headphones = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g5" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#7c3aed;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#g5)"/>
      <!-- Band -->
      <path d="M 100 230 A 110 110 0 0 1 300 230" fill="none" stroke="#1e293b" stroke-width="12" stroke-linecap="round"/>
      <path d="M 100 230 A 110 110 0 0 1 300 230" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
      <!-- Ear Cups -->
      <rect x="75" y="200" width="45" height="85" rx="20" fill="#0f172a" stroke="#ffffff" stroke-width="3"/>
      <rect x="280" y="200" width="45" height="85" rx="20" fill="#0f172a" stroke="#ffffff" stroke-width="3"/>
      <text x="50%" y="42%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="18" font-weight="bold">SonicEcho</text>
    </svg>'''
    
    # 6. Earbuds
    earbuds = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g6" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#14b8a6;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#6366f1;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#g6)"/>
      <!-- Case -->
      <rect x="130" y="130" width="140" height="150" rx="35" fill="#0f172a" stroke="#ffffff" stroke-width="4"/>
      <line x1="130" y1="180" x2="270" y2="180" stroke="#334155" stroke-width="3"/>
      <!-- Glowing dot -->
      <circle cx="200" cy="215" r="4" fill="#14b8a6"/>
      <!-- Earbud elements on sides -->
      <rect x="90" y="90" width="25" height="40" rx="10" fill="#ffffff" transform="rotate(-15, 90, 90)"/>
      <rect x="285" y="90" width="25" height="40" rx="10" fill="#ffffff" transform="rotate(15, 285, 90)"/>
      <text x="50%" y="62%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold">SonicBuds</text>
    </svg>'''
    
    # 7. Speaker
    speaker = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g7" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#10b981;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:1" />
        </linearGradient>
        <radialGradient id="ring" cx="50%" cy="50%" r="50%">
          <stop offset="70%" stop-color="#020617"/>
          <stop offset="100%" stop-color="#06b6d4"/>
        </radialGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#g7)"/>
      <!-- Speaker cylinder -->
      <rect x="120" y="90" width="160" height="220" rx="80" fill="#0f172a" stroke="#ffffff" stroke-width="4"/>
      <circle cx="200" cy="140" r="40" fill="url(#ring)" stroke="#334155" stroke-width="2"/>
      <!-- Soundwave lines -->
      <path d="M 150 220 Q 175 210 200 220 T 250 220" fill="none" stroke="#10b981" stroke-width="3"/>
      <path d="M 160 240 Q 180 230 200 240 T 240 240" fill="none" stroke="#10b981" stroke-width="2"/>
      <text x="50%" y="71%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="16" font-weight="bold">Orbita</text>
    </svg>'''
    
    # 8. Lamp
    lamp = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g8" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#f59e0b;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#ef4444;stop-opacity:1" />
        </linearGradient>
        <filter id="lightglow">
          <feGaussianBlur stdDeviation="30" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      <rect width="100%" height="100%" fill="url(#g8)"/>
      <!-- Glowing light back -->
      <circle cx="200" cy="180" r="80" fill="#fef08a" opacity="0.6" filter="url(#lightglow)"/>
      <!-- Lamp base -->
      <rect x="150" y="300" width="100" height="15" rx="5" fill="#1e293b" stroke="#ffffff" stroke-width="2"/>
      <!-- Pole -->
      <path d="M 200 300 L 200 170" fill="none" stroke="#475569" stroke-width="8"/>
      <!-- Bulb cover -->
      <path d="M 160 170 L 240 170 L 220 120 L 180 120 Z" fill="#0f172a" stroke="#ffffff" stroke-width="3"/>
      <text x="50%" y="38%" dominant-baseline="middle" text-anchor="middle" fill="#0f172a" font-family="sans-serif" font-size="14" font-weight="bold">AURA</text>
    </svg>'''
    
    # 9. Keyboard
    keyboard = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g9" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#a855f7;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#g9)"/>
      <!-- Keyboard Frame -->
      <rect x="60" y="120" width="280" height="160" rx="10" fill="#0f172a" stroke="#ffffff" stroke-width="4"/>
      <!-- Key rows -->
      <rect x="75" y="135" width="35" height="20" rx="3" fill="#312e81" stroke="#818cf8" stroke-width="1.5"/>
      <rect x="115" y="135" width="35" height="20" rx="3" fill="#312e81" stroke="#818cf8" stroke-width="1.5"/>
      <rect x="155" y="135" width="35" height="20" rx="3" fill="#312e81" stroke="#818cf8" stroke-width="1.5"/>
      <rect x="195" y="135" width="35" height="20" rx="3" fill="#312e81" stroke="#818cf8" stroke-width="1.5"/>
      <rect x="235" y="135" width="35" height="20" rx="3" fill="#312e81" stroke="#818cf8" stroke-width="1.5"/>
      <rect x="275" y="135" width="50" height="20" rx="3" fill="#ec4899" stroke="#ffffff" stroke-width="1.5"/>
      
      <!-- Row 2 Spacebar -->
      <rect x="75" y="165" width="50" height="20" rx="3" fill="#4338ca" stroke="#818cf8" stroke-width="1"/>
      <rect x="130" y="165" width="140" height="20" rx="3" fill="#a855f7" stroke="#ffffff" stroke-width="1.5"/>
      <rect x="275" y="165" width="50" height="20" rx="3" fill="#4338ca" stroke="#818cf8" stroke-width="1"/>
      
      <text x="50%" y="58%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="18" font-weight="bold">VoltGrid</text>
    </svg>'''
    
    # 10. Mouse
    mouse = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
      <defs>
        <linearGradient id="g10" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#a855f7;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#g10)"/>
      <!-- Mouse body -->
      <rect x="130" y="90" width="140" height="220" rx="70" fill="#0f172a" stroke="#ffffff" stroke-width="4"/>
      <!-- Split line -->
      <line x1="200" y1="90" x2="200" y2="170" stroke="#ffffff" stroke-width="3"/>
      <!-- Scroll wheel -->
      <rect x="193" y="120" width="14" height="30" rx="7" fill="#06b6d4" stroke="#ffffff" stroke-width="1"/>
      <!-- Side buttons line -->
      <path d="M 128 170 Q 140 180 140 210" fill="none" stroke="#a855f7" stroke-width="3"/>
      <text x="50%" y="65%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-size="16" font-weight="bold">GlideFlow</text>
    </svg>'''
    
    svgs = {
        'pad_pro.svg': pad_pro,
        'ultrabook.svg': ultrabook,
        'watch.svg': watch,
        'band.svg': band,
        'headphones.svg': headphones,
        'earbuds.svg': earbuds,
        'speaker.svg': speaker,
        'lamp.svg': lamp,
        'keyboard.svg': keyboard,
        'mouse.svg': mouse
    }
    
    for filename, content in svgs.items():
        filepath = os.path.join(images_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {filepath}")

if __name__ == '__main__':
    create_svgs()
