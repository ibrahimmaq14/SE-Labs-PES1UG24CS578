# Lab 4 - Vibe Coding: Dig Dug Repair

Assigned source: [SETAPESU26/29_digDug](https://github.com/SETAPESU26/29_digDug). The original `game.py` and README were copied into `dig_dug/` before any fixes. The work follows the four tasks in that README.

## What changed

1. Enemy route search now removes from the front of the queue, so it takes the shortest cleared tunnel route. In the recorded example, the old route is 10 steps and the fixed route is 8.
2. Dirt uses four distinct colors in three-row depth bands.
3. Popping an enemy awards an extra 50 points for each four rows of depth. The recorded row-8 pop scores 500 points total.
4. Enemy movement speed increases by 10% per level after level 1. Level 3 runs at 1.2x speed.

Each task has its own commit in the repository history.

## Deliverables

- [Before gameplay video](videos/before.mp4): 10 seconds using the unchanged source game.
- [After gameplay video](videos/after.mp4): 10 seconds using the completed game.
- [Updated game code](dig_dug/game.py)
- [Chat history PDF](Repo%20Link%20and%20Codex%20Chat%20History%20SE%20Lab%204.pdf) and [shared chat snapshot](https://chatgpt.com/s/cx_6ac62d6b77ec8191b745ac38588f7635). The PDF follows the reference submission style and distinguishes real chat messages from task briefs in the assigned README.

The videos replay a controlled tunnel layout through the actual game renderer and enemy update logic. Cyan outlines mark the 8-step shortest route; orange outlines mark the 10-step winding route. The after video also shows the dirt bands and deep-pop score. `record_demo.py` reproduces both recordings.

The current videos are scripted captures. The [recording guide](RECORDING_GUIDE.md) explains how to replace them with manual screen recordings before the final submission update is pushed.

## Run and verify

Requires Python 3.10 or newer. From this folder:

```powershell
python -m pip install -r requirements.txt
python dig_dug/game.py
python -m unittest test_game.py
```

Controls: arrow keys to move and dig, Space to pump, and R to reset.

For video regeneration, install `opencv-python` and `numpy`, then run `record_demo.py` with a game file, output MP4 path, and `before` or `after` mode. The before video must be regenerated from the [unchanged upstream source](https://github.com/SETAPESU26/29_digDug), not the modified `dig_dug/game.py`.
