# Audio-Reactive Rain with Timed Text Overlay Technique

This document captures the specific implementation used for generating an ASCII video with:
- Aggressive rain intensity tied to audio flux and bass (multiplicative)
- Rain effect confined to first three messages (0-29.5s) but persisting as backdrop
- Seamless transition from rain-dominant to text-dominant phase
- Large, centered text overlay with outline for readability
- Pure black background for maximum contrast

## Key Implementation Details

### 1. Audio Feature Extraction
- Compute flux (spectral difference) and bass band energy per frame
- Normalize features to [0,1] range
- Spawn rate for rain particles: `spawn_rate = 0.3 + 3.0 * flux * bass`
  - Base rate ensures constant rain; multiplicative term makes it aggressive during audio peaks

### 2. Particle System (Rain)
- Each particle: (x, y, speed, char, color, age, max_age)
- spawn particles each frame based on spawn_rate
- particle speed modulated by flux and bass: `speed = base_speed * (0.5 + flux * 0.5 + bass * 0.5)`
- color phase-dependent:
  - Messages 0-2 (Rain Dominant): hue/sat/val set per message (blue, red, purple) with increased brightness
  - Messages 3-5 (Text Dominant): deep amber backdrop with val = 0.5 + 0.3 * rms (audio-reactive)
- brightness modulation: `val = min(0.9, val * (0.7 + 0.3 * rms))`

### 3. Text Overlay
- Six predefined messages with start/end times
- Determine active message by current time
- Text draws whenever any message is active (condition: `if active_msg_idx is not None`)
- Font: DejaVuSans-Bold.ttf at size 96pt for large impact
- Text positioning:
  - Use `font.getbbox(message)` to get tight bounding box
  - `text_width = bbox[2] - bbox[0]`, `text_height = bbox[3] - bbox[1]`
  - `x_pos = (width - text_width) // 2`, `y_pos = (height - text_height) // 2` (centered)
- Outline effect: draw text in black at offsets [-1,0,1]x[-1,0,1] before main text
- Main text color: HSV hue=0.12 (amber), sat=0.7, val = 0.6 * pulse (pulse = 0.8 + 0.4 * rms)

### 4. Contrast and Visual Clarity
- Background: pure black (0,0,0) instead of dark blue-black
- Increased rain particle brightness in dominant phase (val=0.6/0.7 instead of 0.4/0.5)
- Increased text size (font_size=96) for visibility
- Text color boost during text phase for better visibility over rain backdrop

### 5. Implementation Notes
- Use `font.getbbox()` (not deprecated `getsize()`) for accurate text metrics
- Load TTF font once per frame: `font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)`
- Ensure ffmpeg pipes do not deadlock by avoiding `stderr=subprocess.PIPE`; redirect to DEVNULL or file
- Normalize audio features per-frame to avoid division by zero

## Result
Produces high-contrast ASCII video where rain drives the visual energy and text delivers the message, with seamless integration and audio reactivity throughout.
