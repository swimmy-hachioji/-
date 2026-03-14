# -*- coding: utf-8 -*-
"""
ダーツくじ
回るルーレットへダーツを投げて景品をゲットしよう！
"""


# imports


from typing import List, Tuple, Union, Dict

import os

import pygame
import math
from random import randrange

from time import sleep


""" ルーレット
"""


class Roulette:

    gifts_file_path: str
    pos: Tuple[int, int]
    size: int

    __gifts: List[str]
    @property
    def gifts(self) -> List[str]: return self.__gifts

    def __init__(self, gifts_file_path: str, pos: Tuple[int, int], size: int):
        """
        ルーレットの属性初期化
        """
        self.gifts_file_path = gifts_file_path
        self.pos = pos
        self.size = size
        self.__gifts = []
        return

    def _get_gifts(self):
        """
        景品を取得
        """
        with open(self.gifts_file_path, mode="r", encoding="utf-8") as rf:
            gifts = rf.read().split("\n")
        return gifts

    def _update_gifts_file(self, gifts: List[str]):
        """
        景品を更新
        """
        init_gifts_file(self.gifts_file_path, gifts)
        return

    def gifts_update(self):
        """
        現在の景品でルーレットを更新
        """
        self.__gifts = self._get_gifts()
        self.__gifts.sort()
        print(self.__gifts)
        return

    def _create_board_surface(
            self,
            gifts,
            size: Union[Tuple[int, int], Tuple],
            polygon_num=60
    ) -> Tuple[pygame.Surface, Dict]:
        """
        ルーレットの見た目を作成する
        :param gifts: 景品
        :param size: ルーレットの大きさ
        :param polygon_num: 円近似するポリゴン数
        :return: Board surface and gift colors
        """
        gift_nums = {}
        for gift in gifts:
            if gift in gift_nums:
                gift_nums[gift] += 1
                ...
            else:
                gift_nums[gift] = 1
                ...
            continue

        print("nums", gift_nums)

        gift_rates = {}
        gifts_sum = sum(gift_nums.values())
        for gift, num in gift_nums.items():
            gift_rates[gift] = num/gifts_sum
            continue

        print("rates", gift_rates)

        gift_polygons = {}
        total_rate = 0.
        for gift, rate in gift_rates.items():
            gift_polygons[gift] = polygon_num*total_rate
            total_rate += rate
            continue

        print("polygons", gift_polygons)

        surface = pygame.Surface(size)
        surface.fill((255, 255, 255))
        center = tuple(s/2 for s in size)
        r = min(size)/2
        step = 360/polygon_num
        polygons = list(gift_polygons.values())
        gift_idx = -1
        gift_colors = {}
        for i in range(0, polygon_num):
            if gift_idx+1 < len(polygons) and polygons[gift_idx+1] <= i:
                color = tuple(
                    randrange(255) if not gift_idx%3 == _ else
                    127
                    for _ in range(3)
                )
                gift_idx += 1
                gift_name = tuple(gift_polygons.keys())[gift_idx]
                print(gift_idx, gift_name, color, i)
                gift_colors[gift_name] = color
                ...
            thetas = tuple(theta / 180 * math.pi for theta in (i*step, (i+1)*step))
            ps = [(math.cos(theta_)*r+center[0], math.sin(theta_)*r+center[1]) for theta_ in thetas]
            pygame.draw.polygon(surface, color, (center, *ps))
            continue

        return surface, gift_colors

    def run(self, root: pygame.Surface):
        """
        ルーレットダーツ 1 play 開始
        """
        size = tuple(self.size for _ in range(2))
        surface, gift_colors = self._create_board_surface(self.__gifts, size, 120)
        print(gift_colors)
        font = pygame.font.Font(None, 50)
        for i, (name, color) in enumerate(gift_colors.items()):
            color_display = pygame.Surface((200, 50))
            color_display.fill(color)
            text = font.render(name, True, (0, 0, 0))
            color_display.blit(text, (80, 10))
            root.blit(color_display, (self.pos[0]+self.size/2*1.5, self.pos[1]-self.size/2+i*100))
            continue

        poss = (
            (0, 0),
            (20, 0),
            (10, 20)
        )
        print(poss)
        mark_surface = pygame.Surface((20, 20))
        mark_surface.fill((255, 255, 255))
        pygame.draw.polygon(mark_surface, (0, 0, 0,), poss)

        theta = -1
        speed = 0
        done = False
        stop = False
        top_speed = False
        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    ...
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and top_speed:
                    if not stop:
                        stop = True
                    elif speed < 0.1:
                        stop = False
                        top_speed = False
                continue

            if stop and speed > 0:
                speed -= 0.05
            elif speed < 6:
                speed += 0.05
            else:
                top_speed = True

            if not(stop and 0.05 >= speed):
                theta += speed
                rotated_surface = pygame.transform.rotate(surface, theta * math.pi)
            else:
                sleep(2)
            size = rotated_surface.get_rect()[2:]
            root.blit(
                rotated_surface,
                tuple(p-s//2 for p, s in zip(self.pos, size))
            )
            root.blit(mark_surface, (self.pos[0]-10, self.pos[1]-self.size//2-20))
            pygame.display.update()
            continue

        return

    ...


""" 
"""


""" Init gifts
"""


def init_gifts_file(gifts_file_path: str, gifts: List[str]):
    with open(gifts_file_path, mode="w", encoding="utf-8") as wf:
        wf.write("\n".join(gifts))
        ...
    return


""" main
"""


def main():
    gifts = "./gifts.txt"
    if not os.path.exists(gifts):
        init_gifts_file(gifts, [
            "A", "A", "A",
            "B", "B", "B",
            "C", "C", "C",
            "D", "D", "D",
        ])
        ...

    pygame.init()
    root = pygame.display.set_mode((1000, 600))
    root.fill((255, 255, 255))
    roulette = Roulette(gifts, (300, 300), 500)
    roulette.gifts_update()
    print(roulette.gifts)
    roulette.run(root)
    return


if __name__ == '__main__':
    main()
    ...
