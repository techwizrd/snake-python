from collections import deque, namedtuple
import random
import pygame

BOARD_LENGTH = 32
OFFSET = 16


#class DIRECTIONS:
#    Up, Down, Left, Right = range(4)

DIRECTIONS = namedtuple('DIRECTIONS',
                        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)


def find_food(spots):
    while True:
        food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[food[0]][food[1]] == 1 or
                 spots[food[0]][food[1]] == 2)):
            break
    return food


def end_condition(board, coord):
    if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or
            coord[1] >= BOARD_LENGTH):
        return True
    if (board[coord[0]][coord[1]] == 1):
        return True
    return False


def update_board(screen, snake, food):
    white = (255, 255, 255)
    black = (0, 0, 0)

    rect = pygame.Rect(0, 0, OFFSET, OFFSET)

    spots = [[] for i in range(BOARD_LENGTH)]
    num1 = 0
    num2 = 0
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
            temprect = rect.move(num1 * OFFSET, num2 * OFFSET)
            pygame.draw.rect(screen, white, temprect)
            num2 += 1
        num1 += 1
    spots[food[0]][food[1]] = 2
    temprect = rect.move(food[1] * OFFSET, food[0] * OFFSET)
    pygame.draw.rect(screen, black, temprect)
    for coord in snake:
        spots[coord[0]][coord[1]] = 1
        temprect = rect.move(coord[1] * OFFSET, coord[0] * OFFSET)
        pygame.draw.rect(screen, black, temprect)
    return spots


def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
                                      BOARD_LENGTH * OFFSET])
    pygame.display.set_caption("Snaake")
    clock = pygame.time.Clock()

    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)

    # Board set up
    tailmax = 4
    direction = DIRECTIONS.Right
    snake = deque()
    snake.append((0, 0))
    spots[0][0] = 1
    food = find_food(spots)
    spots[food[0]][food[1]] = 2

    while True:
        # Event processing
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = DIRECTIONS.Up
                elif event.key == pygame.K_DOWN:
                    direction = DIRECTIONS.Down
                elif event.key == pygame.K_RIGHT:
                    direction = DIRECTIONS.Right
                elif event.key == pygame.K_LEFT:
                    direction = DIRECTIONS.Left
        if done:
            break

        # Game logic
        head = snake.pop()
        if (direction == DIRECTIONS.Up):
            next_head = (head[0] - 1, head[1])
        elif (direction == DIRECTIONS.Down):
            next_head = (head[0] + 1, head[1])
        elif (direction == DIRECTIONS.Left):
            next_head = (head[0], head[1] - 1)
        elif (direction == DIRECTIONS.Right):
            next_head = (head[0], head[1] + 1)
        if (end_condition(spots, next_head)):
            print(next_head)
            print("end condition reached")
            break

        if spots[next_head[0]][next_head[1]] == 2:
            tailmax += 4
            food = find_food(spots)

        snake.append(head)
        snake.append(next_head)

        if len(snake) > tailmax:
            tail = snake.popleft()

        # Draw code
        black = (0, 0, 0)
        white = (255, 255, 255)
        screen.fill(white)  # makes screen white

        spots = update_board(screen, snake, food)

#        pygame.draw.line(screen, white, (60, 60), (120, 60), 4)
        pygame.display.update()

        clock.tick(20)
    pygame.quit()

if __name__ == "__main__":
    main()
