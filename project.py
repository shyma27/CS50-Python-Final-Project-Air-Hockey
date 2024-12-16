import pygame
import sys


def collision(puck, stick_top, stick_bottom):
    if puck.colliderect(stick_top):
        # in order to get to direction after collision, it's required to subsctruct the vector of the hitting object (stick) from the hit object (puck)
        # direction is a resulting vector
        direction = pygame.math.Vector2(puck.center) - pygame.math.Vector2(
            stick_top.center
        )
        return direction
    elif puck.colliderect(stick_bottom):
        direction = pygame.math.Vector2(puck.center) - pygame.math.Vector2(
            stick_bottom.center
        )
        return direction


def stick_v(stick, prev_pos, player):
    current_pos = pygame.Vector2(stick.center)
    stick_velocity = prev_pos - current_pos
    if player == "top":
        stick_top_previous_pos = current_pos
        return stick_velocity, stick_top_previous_pos
    if player == "bottom":
        stick_bottom_previous_pos = current_pos
        return stick_velocity, stick_bottom_previous_pos


def puck_v(stick_v, direction):
    puck_velocity = direction * stick_v.length() * 0.1
    return puck_velocity


def main():
    pygame.init()

    """Predifined variables"""
    stick_color = (228, 100, 63)
    stick_pos_top = (220, 250)
    stick_pos_bottom = (220, 650)
    clicked_player_top = None
    clicked_player_bottom = None
    screen_width = 500
    screen_height = 900
    puck_x = 245
    puck_y = 460
    border_x = 43
    border_y = 44
    border_w = 408
    border_h = 818
    puck_velocity = pygame.Vector2(0, 0)
    puck_max_velocity = 20
    friction = 0.99
    total_score = 0
    top_player_score = 0
    bottom_player_score = 0

    """Creating the window (main surface) and setting it's title"""
    # set the name of the program displayed in the upper left cornver of the window instead of 'pygame window'
    # create object of Clock class
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Air Hockey")
    fps = pygame.time.Clock()

    """Uploading images (surfaces)"""
    table = pygame.image.load("img/table.jpeg")
    table = pygame.transform.scale(table, (screen_width, screen_height))
    border = pygame.Rect(border_x, border_y, border_w, border_h)
    top_half = pygame.Rect(border_x, border_y, border_w, (border_h / 2))
    bottom_half = pygame.Rect(
        border_x, (screen_height / 2) + 8, border_w, (border_h / 2) - 5
    )

    # upload img for puck, re-size it, create a rect from a surface
    puck_img = pygame.image.load("img/hockey-puck.jpg").convert_alpha()
    puck_img = pygame.transform.scale(puck_img, (60, 60))
    puck = puck_img.get_rect(center=(puck_x, puck_y))

    # create rectangles for sticks and setting their prev positions for calculation of stick velocity
    stick_player_top = pygame.Rect(stick_pos_top[0], stick_pos_top[1], 50, 20)
    stick_player_bottom = pygame.Rect(stick_pos_bottom[0], stick_pos_bottom[1], 50, 20)
    stick_top_previous_pos = pygame.Vector2(stick_player_top.center)
    stick_bottom_previous_pos = pygame.Vector2(stick_player_bottom.center)

    # render font object as a surface
    score_player = pygame.font.SysFont("verdana", 40, bold=False, italic=False)

    while True:
        """Create and update backgrounds, score"""
        screen.blit(table, (0, 0))

        """Create and update puck and sticks"""
        screen.blit(puck_img, puck)

        # draw sticks that move inside border Rect
        stick_player_top.clamp_ip(top_half)
        stick_player_bottom.clamp_ip(bottom_half)
        puck.clamp_ip(border)

        # pygame.draw.rect(screen, (5, 5, 5), border)
        pygame.draw.rect(screen, stick_color, stick_player_top)
        pygame.draw.rect(screen, stick_color, stick_player_bottom)

        # draw lines for goals
        goal_top = pygame.draw.line(
            screen, (0, 0, 0), (190, border.top), (300, border.top), width=4
        )
        goal_bottom = pygame.draw.line(
            screen, (0, 0, 0), (190, border.bottom), (300, border.bottom), width=4
        )

        # render score
        score_top = score_player.render(f"{top_player_score}", False, (240, 140, 0))
        score_bottom = score_player.render(
            f"{bottom_player_score}", False, (240, 140, 0)
        )
        screen.blit(score_top, (50, 380))
        screen.blit(score_bottom, (415, 480))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # if event.button == 1:
                if stick_player_top.collidepoint(event.pos):
                    clicked_player_top = True
                if stick_player_bottom.collidepoint(event.pos):
                    clicked_player_bottom = True

            if event.type == pygame.MOUSEBUTTONUP:
                clicked_player_top = False
                clicked_player_bottom = False

            if event.type == pygame.MOUSEMOTION:
                if clicked_player_top:
                    stick_player_top.move_ip(event.rel)
                if clicked_player_bottom:
                    stick_player_bottom.move_ip(event.rel)

        # get the direction of the puck movement
        direction = collision(puck, stick_player_top, stick_player_bottom)
        stick_player_top_v, stick_top_previous_pos = stick_v(
            stick_player_top, stick_top_previous_pos, "top"
        )
        stick_player_bottom_v, stick_bottom_previous_pos = stick_v(
            stick_player_bottom, stick_bottom_previous_pos, "bottom"
        )

        # calculating puck velocity based on stick velocity
        if direction:
            # moving stick hits the puck
            if stick_player_top_v.length() != 0:
                puck_velocity = puck_v(stick_player_top_v, direction)
            elif stick_player_bottom_v.length() != 0:
                puck_velocity = puck_v(stick_player_bottom_v, direction)
            else:
                # puck moves backwards when hitting static stick (-puck_velocity.x = moving the opposite way on x scale)
                puck_velocity.x = -puck_velocity.x
                puck_velocity.y = -puck_velocity.y

        puck.x = puck.x + int(puck_velocity.x)
        puck.y = puck.y + int(puck_velocity.y)

        # calculate the loss of velocity due to friction
        puck_velocity = puck_velocity * friction

        if puck_velocity.length() > puck_max_velocity:
            puck_velocity = puck_velocity.normalize() * puck_max_velocity

        """Set puck collision with border"""
        # check for puck.topleft, topright and so on
        # if puck top is already inside, then change puck position to the edge of border and velocity with -
        if puck.top < border.top or puck.bottom > border.bottom:
            puck_velocity.y = -puck_velocity.y
        if puck.left < border.left or puck.right > border.right:
            puck_velocity.x = -puck_velocity.x

        """Score"""
        puck_goal_top_colide = pygame.Rect.colliderect(puck, goal_top)
        puck_goal_bottom_colide = pygame.Rect.colliderect(puck, goal_bottom)
        if puck_goal_top_colide:
            # colliderect can capture multiple collisions so score can be updated with more then 1. so if it hits, no matter how many collisions were captured, s will always be 1
            s = 1
            if s == 1:
                top_player_score += s
                total_score += 1
            puck_velocity.x = 0
            puck_velocity.y = 0
            puck.x = 220
            puck.y = 310
            stick_player_top = pygame.Rect(220, 135, 50, 20)

        if puck_goal_bottom_colide:
            s = 1
            if s == 1:
                bottom_player_score += s
                total_score += 1
            puck_velocity.x = 0
            puck_velocity.y = 0
            puck.x = 220
            puck.y = 540
            stick_player_bottom = pygame.Rect(220, 750, 50, 20)

        if total_score == 10:
            total_score = 0
            top_player_score = 0
            bottom_player_score = 0
            puck_velocity.x = 0
            puck_velocity.y = 0
            puck.x = puck_x
            puck.y = puck_y
            stick_pos_top = (250, 150)

        # set 60 max frames per second
        fps.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()
