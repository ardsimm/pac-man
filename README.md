*This project has been created as part of the 42 curriculum by smenard, jbenhass.*

# Pac-Man

<!-- One-sentence pitch + a screenshot or GIF of the game once it runs. -->

![Gameplay screenshot](docs/assets/screenshot.png)

## Table of contents

- [Description](#description)
- [Instructions](#instructions)
- [Configuration](#configuration)
- [Controls](#controls)
- [Highscore](#highscore)
- [Maze Generation](#maze-generation)
- [Implementation](#implementation)
- [General Software Architecture](#general-software-architecture)
- [Project Management](#project-management)
- [Resources](#resources)

---

## Description

<!--
Goal of the project and brief overview:
- what the game is (Pac-Man recreated in Python with MLX)
- main features: generated mazes, 10+ levels, ghosts, highscores, cheat mode
- where to play it (itch.io link)
-->

TODO

## Instructions

### Requirements

<!-- Python version, OS, system libraries needed by MLX, etc. -->

- Python 3.10 or later
- TODO

### Installation

```bash
git clone <repo-url>
cd pac-man
make install
```

### Running

```bash
make run
# or
python3 pac-man.py config.json
```

### Makefile rules

| Rule | Description |
|---|---|
| `make install` | Install dependencies |
| `make run` | Run the game with the default config |
| `make debug` | Run the game under `pdb` |
| `make lint` | Run `flake8` and `mypy` with the required flags |
| `make lint-strict` | Run `flake8` and `mypy --strict` |
| `make clean` | Remove caches and temporary files |
| `make package` | TODO: build the distributable package |

### Packaged build

<!-- itch.io link, how to install/launch the packaged game, how to rebuild it. -->

TODO

## Configuration

<!--
- File format: JSON with comments (lines starting with `#`, and `//` if supported)
- Behaviour on faulty values: clamped to defaults, warning logged, unknown keys ignored
-->

TODO

### Keys

| Key | Type | Default | Valid range | Description |
|---|---|---|---|---|
| `highscore_filename` | string | TODO | | Path of the highscore file |
| `levels` | array | TODO | ≥ 10 entries | Level list (see below) |
| `lives` | int | 3 | TODO | Starting lives |
| `points_per_pacgum` | int | 10 | TODO | Points for a pacgum |
| `points_per_super_pacgum` | int | 50 | TODO | Points for a super-pacgum |
| `points_per_ghost` | int | 200 | TODO | Points for an edible ghost |
| `seed` | int | 42 | TODO | Seed of the first level |
| `level_max_time` | int | 90 | TODO | Time limit per level (seconds) |

### Example

```jsonc
# Example configuration
{
    "lives": 3,
    "seed": 42
}
```

## Controls

| Key | Action |
|---|---|
| Arrow keys / WASD | Move |
| Escape | Pause |
| TODO | Cheat mode (see below) |

### Cheat mode

<!-- How to enable it and what each cheat does. -->

| Key | Cheat |
|---|---|
| TODO | Invincibility |
| TODO | Skip level |
| TODO | Freeze ghosts |
| TODO | Extra life |
| TODO | Speed boost |

## Highscore

<!--
- Where and how scores are stored (format, location)
- Validation rules: name ≤ 10 chars, alphanumeric and spaces; scores ≥ 0
- Behaviour on missing or corrupted file
- WHY this implementation was chosen
-->

TODO

## Maze Generation

<!--
- Which A-Maze-ing package was assigned (group, link, version)
- Its interface and how our adapter translates it into our grid
- PERFECT = False
- Seeds: fixed for level 1, random afterwards
- Error handling if the generator fails
-->

TODO

## Implementation

<!--
Technical summary:
- fixed-timestep game loop (engine) and how it fits in the MLX loop
- scene stack (menu, playing, pause, game over...)
- player movement and buffered direction
- ghost behaviour (chase / frightened / eaten) and chosen strategy
- collision detection
- timers counted in ticks
- error handling strategy ("no traceback")
-->

TODO

## General Software Architecture

<!-- High-level overview: modules, classes and their relationships.
     Keep the diagrams in docs/architecture/ and link or embed them here. -->

### Components

| Component | Responsibility |
|---|---|
| Engine | Window, input events, fixed-timestep clock |
| SceneManager | Scene stack, routes events/update/draw to the active scene |
| Scene | Menu, playing, pause, game over, name entry... |
| SceneAdapter | Translates what a scene wants to show into drawing calls |
| Render | Drawing primitives on top of MLX |
| Config | Parsing, validation and defaults of the config file |
| Maze | Adapter around the assigned A-Maze-ing package |
| Scores | Highscore persistence |

### Diagrams

- [Component diagram](docs/architecture/pacman_components.drawio)
- TODO: scene state machine, class diagram, sequence diagrams

## Project Management

<!--
- Method used (Scrum/Kanban, sprint length, rituals)
- Tools (GitHub Projects + link)
- Team organization: who did what, how decisions were made
- Short summary of planned vs actual, main risks, blocking points
-->

TODO

All project management documents are in [`docs/project-management/`](docs/project-management/).

## Resources

### References

<!-- Documentation, articles, tutorials used. -->

- [MiniLibX documentation](TODO)
- [The Pac-Man Dossier](https://pacman.holenet.info/) — original game mechanics
- TODO

### AI usage

<!--
Required by the subject: for which tasks and which parts of the project AI was used.
-->

| Task | Part of the project | How AI was used |
|---|---|---|
| Architecture review | docs/architecture | TODO |
| Backlog writing | User stories | TODO |
| TODO | | |
