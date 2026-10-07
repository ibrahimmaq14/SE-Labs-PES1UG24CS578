"""Render deterministic ten-second gameplay clips from either game version.

Usage: python record_demo.py path/to/game.py path/to/output.mp4 before|after
The recorder only scripts game state and captures Game.draw; it does not patch
the imported game module.
"""

import argparse
import importlib.util
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import cv2
import numpy as np
import pygame


def load_game(path):
    spec = importlib.util.spec_from_file_location("recorded_game", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_route_scene(module):
    game = module.Game()
    game.grid = [[True] * module.COLS for _ in range(module.ROWS)]
    cells = (
        [(4, c) for c in range(1, 8)]
        + [(6, c) for c in range(1, 4)]
        + [(7, c) for c in range(3, 6)]
        + [(6, c) for c in range(5, 8)]
        + [(5, 1), (5, 7)]
    )
    for row, col in cells:
        game.grid[row][col] = False
    game.player = (5, 7)
    game.facing = (0, -1)
    game.enemies = [module.Enemy((5, 1))]
    game.enemies[0].step_timer = module.ENEMY_DELAY
    game.enemies[0].ghost_timer = 999
    return game


def draw_frame(module, game, screen, caption, detail, show_routes=False):
    game.draw(screen)
    if show_routes:
        short = [(4, c) for c in range(1, 8)] + [(5, 7)]
        winding = (
            [(6, c) for c in range(1, 4)]
            + [(7, c) for c in range(3, 6)]
            + [(6, c) for c in range(5, 8)]
            + [(5, 7)]
        )
        for color, cells in (((75, 215, 255), short), ((255, 175, 75), winding)):
            for row, col in cells:
                rect = pygame.Rect(col * module.TILE + 2, row * module.TILE + 2, module.TILE - 4, module.TILE - 4)
                pygame.draw.rect(screen, color, rect, 2)
    font = pygame.font.Font(None, 24)
    panel = pygame.Surface((module.WIDTH, 63), pygame.SRCALPHA)
    panel.fill((9, 12, 24, 220))
    screen.blit(panel, (0, 0))
    screen.blit(font.render(caption, True, (255, 255, 255)), (12, 8))
    screen.blit(font.render(detail, True, (255, 228, 115)), (12, 34))
    return cv2.cvtColor(np.transpose(pygame.surfarray.array3d(screen), (1, 0, 2)), cv2.COLOR_RGB2BGR)


def record(game_path, output_path, mode):
    module = load_game(game_path)
    pygame.init()
    screen = pygame.Surface((module.WIDTH, module.HEIGHT))
    route = make_route_scene(module)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fps = 20
    writer = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (module.WIDTH, module.HEIGHT))
    if not writer.isOpened():
        raise RuntimeError("Could not open MP4 video writer")
    try:
        for frame in range(10 * fps):
            second = frame / fps
            if mode == "after" and second >= 6:
                if frame == 6 * fps:
                    game = module.Game()
                    game.grid = [[True] * module.COLS for _ in range(module.ROWS)]
                    game.player = (8, 8)
                    game.facing = (0, 1)
                    game.enemies = [module.Enemy((8, 10)), module.Enemy((10, 12))]
                    game.enemies[0].step_timer = 999
                    game.enemies[1].step_timer = 999
                    for cell in [(8, 8), (8, 9), (8, 10), (10, 12)]:
                        game.dig(cell)
                    game.level = 3
                if frame in [int(x * fps) for x in (6.4, 6.9, 7.4, 7.9)]:
                    game.time = second
                    game.pump()
                game.time = second
                caption = "AFTER: banded dirt + deep-pop bonus"
                detail = f"Level 3 speed x{module.enemy_speed_multiplier(3):.1f} | Score {game.score}"
                writer.write(draw_frame(module, game, screen, caption, detail))
                continue
            if frame == 0 or (frame == 100):
                route = make_route_scene(module)
            enemy = route.enemies[0]
            route.update_enemy(enemy, 1 / fps)
            if mode == "before":
                caption = "BEFORE: original pathfinding bug"
                detail = "Enemy takes orange 10-step route; cyan route is 8"
            else:
                caption = "AFTER: breadth-first pathfinding"
                detail = "Enemy takes cyan 8-step shortest route"
            writer.write(draw_frame(module, route, screen, caption, detail, show_routes=True))
    finally:
        writer.release()
        pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("game", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("mode", choices=["before", "after"])
    args = parser.parse_args()
    record(args.game, args.output, args.mode)
