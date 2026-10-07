# Record the two Lab 4 gameplay videos

The assigned source repository is already cloned on this PC, and its `game.py` is unchanged. Use it for the **before** clip. Use this lab folder's modified game for the **after** clip.

## 1. Launch the before game

Open PowerShell and run:

```powershell
Set-Location -LiteralPath 'C:\Users\ibrah\OneDrive\Documents\SEM5\SE_jackfruit\digDug-lab4-source'
python game.py
```

Use the arrow keys to dig and move, Space to pump, and R to reset. Try to show an enemy taking a winding route through connected tunnels. This is the original pathfinding bug.

## 2. Record the before clip

With the game window open, press **Windows + Shift + R** to open Snipping Tool's video recorder. Select the game window area, choose **Start**, play for at least 10 seconds, then choose **Stop**. Save the MP4 as:

`C:\Users\ibrah\OneDrive\Documents\SEM5\SE_jackfruit\SE-Labs-PES1UG24CS578\LAB4\videos\before.mp4`

Replace the existing file when prompted. Microsoft's [Snipping Tool guide](https://support.microsoft.com/en-us/windows/apps/use-snipping-tool-to-capture-screenshots) confirms these recording steps.

## 3. Launch and record the after game

Close the first game. In PowerShell, run:

```powershell
Set-Location -LiteralPath 'C:\Users\ibrah\OneDrive\Documents\SEM5\SE_jackfruit\SE-Labs-PES1UG24CS578\LAB4\dig_dug'
python game.py
```

Record the changed dirt colors, enemy movement, and a successful four-pump pop if possible. Save the MP4 as:

`C:\Users\ibrah\OneDrive\Documents\SEM5\SE_jackfruit\SE-Labs-PES1UG24CS578\LAB4\videos\after.mp4`

Replace the existing file. Aim for about 10 seconds for each clip; I can check the duration and trim any extra seconds after both files are in place.
