from project import collision, stick_v, puck_v
import pygame


def test_collision():
    puck = pygame.Rect(10, 10, 10, 10)
    s_top = pygame.Rect(10, 10, 10, 10)
    s_bot = pygame.Rect(10, 10, 10, 10)

    result = collision(puck, s_top, s_bot)
    assert result == pygame.math.Vector2()

    result = collision(puck, s_bot, s_top)
    assert result == [0, 0]

    result = collision(pygame.Rect(-10, 10, 10, 10), s_bot, s_top)
    assert result == None


def test_stick_v():
    stick = pygame.Rect(0, 0, 0, 0)
    prev = pygame.Vector2(stick.center)
    player1 = "top"
    player2 = "bottom"
    v, prev = stick_v(stick, prev, player1)
    assert v == pygame.math.Vector2()
    assert prev == pygame.math.Vector2(0, 0)

    v, prev = stick_v(stick, prev, player2)
    assert v == pygame.math.Vector2()
    assert prev == pygame.math.Vector2(0, 0)

    v = stick_v(stick, prev, "player3")
    prev = stick_v(stick, prev, "player3")
    assert v == None
    assert prev == None


def test_puck_v():
    v = pygame.math.Vector2()
    d = pygame.math.Vector2()
    p = puck_v(v, d)
    assert p == (0, 0)
