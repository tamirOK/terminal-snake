from random import randint

import curses


def draw_points_sector(width):
    """
        coordinates for sector with user points
    """
    result = []

    for i in range(3):
        result.append([i, width // 2 - 4])
    for i in range(3):
        result.append([i, width // 2 + 1])
    for i in range(4):
        result.append([2, width // 2 - i])

    return result


def snakes(stdscr):
    direction, prev_direction = curses.KEY_RIGHT, 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    render_apple = True
    points = 0

    # initial location of snake
    # 0-th element is head of the snake
    dots = [[0, i] for i in range(7, -1, -1)]

    # for correct moves
    opposite = {}
    opposite[curses.KEY_DOWN] = curses.KEY_UP
    opposite[curses.KEY_UP] = curses.KEY_DOWN
    opposite[curses.KEY_LEFT] = curses.KEY_RIGHT
    opposite[curses.KEY_RIGHT] = curses.KEY_LEFT

    # set cursor invisible
    curses.curs_set(0)
    # getch() blocks for 50 mseces and returns -1 if no key was pressed
    stdscr.timeout(50)
    height, width = stdscr.getmaxyx()

    points_sector = draw_points_sector(width)

    while direction != ord('q'):

        # Initialization
        stdscr.clear()   

        for y, x in points_sector:
            stdscr.addstr(y, x, '-')
        stdscr.addstr(1, width // 2 - 2, str(points))

        # if move wasn't in opposite direction
        if prev_direction != 0 and direction != opposite[prev_direction]:
            old_dots = [line[:] for line in dots]

            # move head according to key pressed
            if direction == curses.KEY_DOWN:
                dots[0][0] += 1
            elif direction == curses.KEY_UP:
                dots[0][0] -= 1
            elif direction == curses.KEY_RIGHT:
                dots[0][1] += 1
            elif direction == curses.KEY_LEFT:
                dots[0][1] -= 1

            # handle collisions to border    
            if dots[0][0] >= height:
                dots[0][0] -= height
            elif dots[0][0] < 0:
                dots[0][0] += height

            if dots[0][1] >= width:
                dots[0][1] -= width
            elif dots[0][1] < 0:
                dots[0][1] += width 

            # moving snake   
            for i in range(1, len(dots)):
                dots[i] = old_dots[i - 1]

            # if snake ate apple, then generate new one    
            if dots[0] == [apple_y, apple_x]:    
                dots.append(old_dots[-1])
                render_apple = True 
                points += 1

            # handle snake collision    
            if dots[0] in dots[1:]:
                # print available actions
                stdscr.addstr(height // 2, width // 2 - 5, "GAME OVER!")
                stdscr.addstr(height // 2 + 1, width // 2 - 11, "PRESS f TO\
                                                                START AGAIN")
                stdscr.addstr(height // 2 + 2, width // 2 - 6, "PRESS q TO QUIT")

                # wait user input
                stdscr.timeout(-1)
                option = stdscr.getch()

                # end game
                if option == ord('q'):
                    break
                # restart game
                elif option == ord('f'):
                    snakes(stdscr)
                    return    

        # render snake       
        for y, x in dots:
            stdscr.addstr(y, x, '#')

        # generate new coordinates for apple    
        if render_apple:    
            apple_x = randint(0, width - 1)
            apple_y = randint(0, height - 1)

            while [apple_y, apple_x] in dots:
                apple_x = randint(0, width - 1)
                apple_y = randint(0, height - 1)

            render_apple = False
        
        stdscr.addstr(apple_y, apple_x, '@')

        if prev_direction == 0 or direction != opposite[prev_direction]:
            prev_direction = direction

        direction = stdscr.getch()

        if direction == -1:
            direction = prev_direction


def main():
    curses.wrapper(snakes)


if __name__ == "__main__":
    main()
    