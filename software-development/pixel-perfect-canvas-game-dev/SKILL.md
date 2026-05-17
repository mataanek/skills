---
name: pixel-perfect-canvas-game-dev
description: Approach for building precise specification-based canvas games with vanilla JavaScript
category: software-development
---

# Pixel-Perfect Canvas Game Development

## Approach for building precise specification-based canvas games with vanilla JavaScript

### When to Use
This skill is for building 2D canvas games where pixel-perfect implementation of specific requirements is critical, such as:
- Games requiring exact collision detection to prevent tunneling
- Pixel art rendering with specific grid-based approaches
- Precise timing and animation requirements
- Complex audio integration with Web Audio API
- Multi-file project organization with strict dependency order

### Key Principles Learned
1. **Canvas Setup is Foundational** - Always explicitly set dimensions, disable image smoothing for pixel art, and handle resize events
2. **Collision Detection Must Prevent Tunneling** - Use circle-to-circle distance checks with appropriate radii, never point-in-rect for fast-moving objects
3. **Pixel Art Requires Specific Techniques** - Use grid-based fillRect rendering with cell size calculations, never smooth arcs for authentic pixelated look
4. **Particle Systems Need Central Management** - Ensure draw() is called in main loop, spawn particles from appropriate update methods
5. **Audio Integration Requires Planning** - Web Audio API procedural sounds work well for retro effects but need careful envelope design
6. **State Machine Architecture Prevents Spaghetti** - Clear separation of menu/playing/paused/gameover states with distinct update/draw logic
7. **Precise Implementation Beats "Close Enough"** - Following exact specifications (like lerp factor 0.35, specific enemy sizes) creates noticeably better feel

### Step-by-Step Process

#### 1. Project Structure & Setup
```
project/
├── index.html
├── css/
│   └── styles.css
└── js/
    ├── config.js          # All constants and tuning parameters
    ├── game.js            # Main loop, state machine, collision
    ├── player.js          # Ship logic, input, weapons
    ├── enemies.js         # Enemy types, spawning, behavior
    ├── particles.js       # Visual effects system
    ├── background.js      # Parallax layers
    ├── ui.js              # HUD, menus, text rendering
    └── audio.js           # Procedural sound effects
```

#### 2. Implementation Sequence (Critical Order)
1. **config.js** - Define ALL constants first (sizes, speeds, colors, timings)
2. **background.js** - Implement parallax layers (test visibility)
3. **player.js** - Ship rendering and mouse tracking (verify smooth movement)
4. **audio.js** - Procedural sound foundations (test basic sounds)
5. **particles.js** - Core particle system (test spawning/drawing)
6. **enemies.js** - Pixel art rendering and basic movement
7. **game.js** - Main loop, state machine, collision detection
8. **ui.js** - HUD and menu systems
9. **index.html** - Wire everything up with correct script order

#### 3. Critical Implementation Details

**Canvas Initialization (in game.js init()):**
```javascript
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
ctx.imageSmoothingEnabled = false; // Pixel art essential
window.addEventListener('resize', resizeCanvas);
```

**Pixel Art Enemy Rendering:**
```javascript
function drawOctopus(ctx, x, y, size, grid, frame) {
    const cellSize = size / grid.length;
    ctx.fillStyle = getEnemyColor(type);
    
    for (let row = 0; row < grid.length; row++) {
        for (let col = 0; col < grid[row].length; col++) {
            if (grid[row][col] === 1) {
                const px = x + col * cellSize;
                const py = y + row * cellSize;
                ctx.fillRect(px, py, cellSize, cellSize);
            }
        }
    }
    // Animate tentacles by modifying bottom row based on frame
}
```

**Collision Detection (Prevents Tunneling):**
```javascript
function checkCollision(circle1, circle2) {
    const dx = circle1.x - circle2.x;
    const dy = circle1.y - circle2.y;
    const distanceSquared = dx * dx + dy * dy;
    const radiiSum = circle1.radius + circle2.radius;
    return distanceSquared < radiiSum * radiiSum;
}

// Bullet radius = bulletWidth/2
// Enemy radius = enemySize/2
```

**Ship Mouse Tracking:**
```javascript
// In player.update()
ship.x += (mouseX - ship.x) * 0.35; // Critical factor for feel
ship.y += (mouseY - ship.y) * 0.35;
```

**Hit Feedback System:**
```javascript
// When bullet hits enemy:
enemy.hitFlash = 3; // 3 frames of white flash
spawnSparkParticles(hitX, hitY, 5); // 3-5 spawn particles
spawnDamageNumber(hitX, hitY, damage); // Floating text
playHitSound(); // Short noise burst
applyScreenShake(enemy.size * 0.02); // Scale with enemy size
```

**Particle System Integration:**
```javascript
// In game.js draw loop:
function gameLoop() {
    update();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    background.draw(ctx);
    enemies.draw(ctx);
    player.draw(ctx);
    particles.draw(ctx); // CRITICAL: Must be called here
    ui.draw(ctx);
    requestAnimationFrame(gameLoop);
}
```

#### 4. Verification Checklist
- [ ] Canvas dimensions set explicitly on init and resize
- [ ] imageSmoothingDisabled = false for pixel art
- [ ] Enemy sizes match spec (small:36, medium:48, baby:20, boss:150)
- [ ] Bullet speeds prevent tunneling (tier1:8, tier2:10, tier3:12, tier4:14)
- [ ] Ship tracking uses lerp factor 0.35 exactly
- [ ] All collision uses circle-to-circle distance check
- [ ] Octopus rendering uses grid-based fillRect, NO ctx.arc()
- [ ] Background scrolls DOWNWARD only (vertical shooter)
- [ ] Particles.draw() called in main draw loop
- [ ] Hit feedback: 3-frame white flash, damage numbers, hit sound
- [ ] HUD layout: 20px monospace, score x=20, y=40; level center; combo right edge
- [ ] Power-up system: orb drops, 5-sec unleash, 3x score, visual effects
- [ ] Audio: All specified procedural sounds implemented
- [ ] Game states: menu/playing/paused/gameover properly separated

#### 5. Common Pitfalls & Solutions
- **Bullet Tunneling** → Switch to circle collision with appropriate radii
- **Sluggish Ship Movement** → Increase lerp factor (0.35 is sweet spot)
- **Smooth-Looking Enemies** → Force grid-based rendering, ban ctx.arc()
- **Particles Not Showing** → Verify draw() call in main loop, check spawn rates
- **Audio Clicks/Pops** → Use proper envelope attack/release in oscillators
- **State Confusion** → Implement clear state enum with enter/exit handlers
- **Performance Issues** → Object pooling for particles, limit draw calls
- **Stale Browser Cache** → After updating JS/CSS, browser may serve old versions causing missing features (bullets not drawing, enemies not moving). Solution: hard refresh (Ctrl+Shift+R), add cache-busting query string (?v=2), or restart server on a different port to avoid proxy caching.
- **Responsive Design Breakage** → Test resize handler thoroughly
- **Game Not Initializing** → Ensure init() runs after DOMContentLoaded; use defer on scripts or add DOMContentLoaded listener

#### 6. Tools & Environment
- Modern browser with Canvas 2D API and Web Audio API
- Local development server (python3 -m http.server)
- Browser dev tools for debugging
- No external libraries or frameworks
- Vanilla JavaScript ES6+

### Why This Works
This approach succeeds because it:
1. Separates concerns clearly (config, rendering, logic, audio, UI)
2. Implements specifications exactly as given (no interpretation drift)
3. Builds incrementally with verification at each step
4. Focuses on the critical details that make games "feel right"
5. Creates reusable patterns for pixel-perfect canvas development
6. Maintains strict dependency order to prevent initialization issues

The key insight is that game feel lives in the details: exact lerp factors, precise collision radii, specific particle counts, and strict adherence to pixel art techniques. Deviating even slightly from specifications can dramatically alter the player experience.