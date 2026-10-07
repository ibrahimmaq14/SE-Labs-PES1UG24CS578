"""Focused checks for the four Dig Dug lab tasks."""

import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
sys.path.insert(0, str(Path(__file__).parent / "dig_dug"))

import pygame

import game


class DigDugTasks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_enemy_chooses_shortest_tunnel(self):
        grid = [[True] * game.COLS for _ in range(game.ROWS)]
        cells = (
            [(4, col) for col in range(1, 8)]
            + [(6, col) for col in range(1, 4)]
            + [(7, col) for col in range(3, 6)]
            + [(6, col) for col in range(5, 8)]
            + [(5, 1), (5, 7)]
        )
        for row, col in cells:
            grid[row][col] = False
        path = game.bfs_path(grid, (5, 1), (5, 7))
        self.assertEqual(len(path), 8)
        self.assertEqual(path[0], (4, 1))

    def test_dirt_bands_change_with_depth(self):
        self.assertEqual(game.dirt_color(1), game.dirt_color(3))
        self.assertNotEqual(game.dirt_color(3), game.dirt_color(4))
        self.assertNotEqual(game.dirt_color(6), game.dirt_color(7))
        for row in range(1, game.ROWS):
            self.assertTrue(all(0 <= value <= 255 for value in game.dirt_color(row)))

    def test_deep_enemy_pop_adds_bonus(self):
        session = game.Game()
        session.grid = [[True] * game.COLS for _ in range(game.ROWS)]
        session.player = (8, 8)
        session.facing = (0, 1)
        target = game.Enemy((8, 10))
        session.enemies = [target, game.Enemy((10, 12))]
        for cell in [(8, 8), (8, 9), (8, 10)]:
            session.dig(cell)
        for _ in range(4):
            session.pump()
        self.assertNotIn(target, session.enemies)
        self.assertEqual(session.score, 500)

    def test_speed_rises_with_level(self):
        self.assertEqual(game.enemy_speed_multiplier(1), 1)
        self.assertAlmostEqual(game.enemy_speed_multiplier(3), 1.2)
        session = game.Game()
        session.level = 3
        session.grid = [[False] * game.COLS for _ in range(game.ROWS)]
        session.player = (1, 1)
        enemy = game.Enemy((1, 8))
        enemy.step_timer = 0
        enemy.ghost_timer = 999
        session.update_enemy(enemy, 0.01)
        self.assertAlmostEqual(enemy.step_timer, game.ENEMY_DELAY / 1.2)


if __name__ == "__main__":
    unittest.main()
