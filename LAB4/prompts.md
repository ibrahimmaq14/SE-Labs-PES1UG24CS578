# Lab 4 task prompts and review notes

The user/Codex conversation and verified task actions are in `Repo Link and Codex Chat History SE Lab 4.pdf` and the linked shared chat. The assignment was handled as four separate task iterations. These are concise task prompts derived from the assigned README, with the result checked after each change.

1. **Pathfinding:** "Find why `bfs_path` reaches the player by a longer route. Change the search to true breadth-first order without changing tunnel collision rules." Review: the controlled layout returned an 8-cell route via row 4, where the original returned a 10-cell route via rows 6 and 7.
2. **Dirt bands:** "Implement `dirt_color(row)` with valid RGB values that form distinct depth bands." Review: rows 1-3, 4-6, 7-9, and 10-13 each use a separate color.
3. **Deep-pop bonus:** "Use `on_enemy_popped(enemy, score)` to add a depth-based bonus and make sure the displayed score receives it." Review: four pumps at row 8 remove the enemy and raise the score to 500.
4. **Level speed:** "Implement `enemy_speed_multiplier(level)` so enemies move faster on later levels while level 1 keeps the original timing." Review: level 3 has multiplier 1.2 and a step delay of `0.35 / 1.2` seconds.
