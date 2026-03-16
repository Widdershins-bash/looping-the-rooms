# 🎲 Looping The Rooms

Looping The Rooms is a dungeon-crawling Pygame project built around room-to-room exploration, looping floor generation, menu-driven state changes, and a steadily growing player movement system. The player navigates a modular dungeon, searches for the exit, collects upgrades, and advances through progressively expanding floors.

This project works as both a playable game jam release and a strong portfolio piece. It shows practical work in game-loop structure, procedural room generation, camera handling, menu/UI systems, collision logic, asset-driven rendering, browser deployment with `pygbag`, and cross-platform debugging between desktop and web builds. 🎮

## 🔗 Play On Itch

`[https://widdershins-bash.itch.io/looping-the-rooms]`

## ✨ Highlights

- Procedurally generated room layouts with entrance and exit placement
- State-driven menus for main menu, pause, settings, lose, and level-complete flows
- Upgrade pickup system that increases player speed
- Camera easing that follows the active room
- Logical-surface rendering with scaled viewport presentation
- Volume controls and sound-effect integration
- Browser-playable HTML5 build through `pygbag`

## 🕹️ Controls

- `Arrow Keys`: Move the player
- `Esc`: Exit during testing
- Mouse: Navigate menus and interact with buttons/sliders

## 🧱 Tech Stack

- Python 3.12+ recommended
- [`pygame-ce`](https://pypi.org/project/pygame-ce/) `2.5.7`
- [`pygbag`](https://pypi.org/project/pygbag/) `0.9.3`
- `numpy`

## 🧠 Technical Skills Used And Learned

- Building a modular game architecture across `main.py`, `system/`, and `game/`
- Managing menu flow with a state-machine style update loop
- Designing reusable button, slider, and widget UI components
- Implementing procedural path generation for connected dungeon rooms
- Handling player movement, wall collision, and item pickup logic
- Using camera offset systems to keep room-to-room movement readable
- Structuring sprite-sheet loading and reusable image slicing helpers
- Debugging cross-platform file path and case-sensitivity issues
- Adapting a desktop Pygame project for browser deployment with `pygbag`
- Tracking down web-only runtime issues such as input scaling, timer behavior, and annotation evaluation


## 🧪 Development Notes

- The project depends on local assets under [`assets/`](./assets).
- Rendering uses a logical surface that is scaled into the active window.
- Gameplay and menu flow are both coordinated through shared game-state transitions.
- The web build was validated through `pygbag`, which required browser-specific debugging and compatibility fixes.

## 🏗️ How the Game Works

At startup, `main.py` initializes Pygame, creates the screen, audio manager, world, and menu manager, then enters the main loop.

Inside that loop:

1. Delta time is calculated for frame-independent updates.
2. Input events are processed for quitting and gameplay interaction.
3. Menu and world state are synchronized depending on what the player is doing.
4. The world updates room logic, player position, collision handling, camera offset, and progression systems.
5. Menus update and draw over the gameplay layer when active.
6. The logical surface is scaled and presented through the window viewport.

This keeps gameplay, UI, and rendering responsibilities separated in a way that is easy to extend. 🧠

## 🗂️ File-by-File Overview

#### `main.py`

Application entrypoint. Initializes Pygame, loads the screen, image assets, sound system, world state, and menus, then runs the async main loop.

### `system/` modules

#### `system/constants.py`

Central configuration for screen dimensions, grid sizing, color palette values, asset paths, UI constants, fonts, and the `GameState` enum.

#### `system/screen.py`

Owns the display surface, logical render surface, alpha overlay surface, scaling-to-window behavior, viewport tracking, and basic window event handling.

#### `system/menu.py`

Handles menu orchestration and state transitions. `MenuManager` selects active menus while `Menu` updates buttons, backgrounds, and return-state behavior.

#### `system/button.py`

Defines interactive UI components including action buttons, the settings/pause widgets, the volume slider, and slider knob drag behavior.

#### `system/image.py`

Loads image assets and slices sprite sheets into reusable button sprites, player animation frames, and tile themes.

#### `system/audio.py`

Loads UI and gameplay sound effects, manages the current audio state, and synchronizes slider-driven volume changes.

#### `system/stats.py`

Tracks game stats like timer, floor progression, speed bonuses, and on-screen stat display.

### `game/` modules

#### `game/world.py`

Top-level gameplay coordinator. Updates the floor manager, player, collision handling, camera focus, room transitions, exit detection, and level progression.

#### `game/floor.py`

Implements procedural floor generation, room connection logic, entrance/exit placement, upgrade placement, and room tile construction.

#### `game/player.py`

Defines player movement, animation state, directional logic, sound timing, collision bounds, and rendering.

#### `game/camera.py`

Provides easing-based camera offset logic so the active room stays centered smoothly.

#### `game/tile.py`

Defines tile classes and factories for floors, doors, collision tiles, and item tiles.

### `assets/` folders

#### `assets/images/`

Stores environment, UI, player, and item graphics including sprite sheets for menus, tiles, and animations.

#### `assets/audio/`

Stores click sounds, movement sounds, level-complete feedback, collectible sounds, and background music.

#### `assets/fonts/`

Stores the font files used for menu text and stat displays.


## 🙌 Credits

- Art and sound design: `mafuyu-da-baller`
- Programming: `Widdershins-bash`
