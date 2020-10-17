"""
Brick breaker


"""
import arcade

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

BALL_RADIUS = 5

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50

BRICK_AMOUNT = 10
BRICK_WIDTH = 40
BRICK_HEIGHT = 10
BRICK_HP = 1

MOVE_AMOUNT = 5

SCORE_HIT = 5
SCORE_MISS = -5


class Point:
    def __init__(self):
        # sets a base render point
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT

class Velocity:
    def __init__(self):
        # sets base velocity 
        self.dx = MOVE_AMOUNT
        self.dy = MOVE_AMOUNT

class Ball:
    def __init__(self):
        # Ball init
        self.center = Point()
        self.velocity = Velocity()
        self.color = arcade.color.WHITE
        self.radius = BALL_RADIUS
    
    def draw(self):
        # Create Ball
        arcade.draw_circle_filled(self.center.x, self.center.y,
        self.radius, self.color)

    def advance(self):
        # move the ball
        self.center.x = self.velocity.dx
        self.center.y = self.velocity.dy

    def bounce_horizontal(self):
        self.velocity.dx = self.velocity.dx * -1

    def bounce_vertical(self):
        self.velocity.dy = self.velocity.dy * -1

    def restart(self):
        if self.center.y < 0:
            self.center.y = SCREEN_HEIGHT
            self.center.x = SCREEN_WIDTH / 2
            self.velocity.dx = MOVE_AMOUNT
            self.velocity.dy = MOVE_AMOUNT

class Brick():
    def __init__(self):
        # Brick init
        self.center = Point()
        self.center.y = 400
        self.center.x = SCREEN_WIDTH / 2
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT

    def draw(self):
        # render bricks
        arcade.draw_rectangle_filled(self.center.x, self.center.y,
        self.width, self.height, arcade.color.BRICK_RED)

    

class Paddle():
    def __init__(self):
        # paddle init
        self.center = Point()
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = 50
        self.width = PADDLE_HEIGHT
        self.height = PADDLE_WIDTH
        self.top = 400
        self.bottom = 0

    def draw(self):
        # render paddle
        arcade.draw_rectangle_filled(self.center.x, self.center.y,
        self.width, self.height, arcade.color.WHITE)
    
    def move_right(self):
        # move the paddle right
        if self.center.x < SCREEN_WIDTH:
            self.center.x += MOVE_AMOUNT

    def move_left(self):
        # move the paddle left
        if self.center.x > 0:
            self.center.x += MOVE_AMOUNT


class Breaker(arcade.Window):
    def __init__(self, width, height):
        # init main game function
        super().__init__(width, height)

        self.ball = Ball()
        self.paddle = Paddle()
        self.brick = Brick()
        self.score = 0

        self.holding_left = False
        self.holding_right = False

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):

        arcade.start_render()

        self.ball.draw()
        self.paddle.draw()
        self.brick.draw()

        self.draw_score()

    def draw_score(self):
        # Shows the score
        score_text = 'Score: {}'.format(self.score)
        x = 10
        y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x = x, start_y = y,
        font_size=12, color=arcade.color.WHITE)

    def update(self, delta_time):
        # Updates each object 
        self.ball.advance()
        self.check_keys()
        self.check_hit()
        self.check_miss()
        self.check_bounce()

    def check_hit(self):
        # Checks if the ball hits the paddle or a brick
        close_x = (PADDLE_WIDTH)
        close_y = (PADDLE_WIDTH)

        if (abs(self.ball.center.x - self.paddle.center.x) < close_x and
        abs(self.ball.center.y - self.paddle.center.y) < close_y and
        self.ball.velocity.dy < 0):
            self.ball.bounce_vertical()
            self.score += SCORE_HIT


    def check_miss(self):
        # resets the ball if it misses
        if self.center.y < 0:
            self.ball.restart()
            self.score -= SCORE_MISS

    def check_bounce(self):
        # bounces the ball if it hits something
        if self.ball.center.x < 0 and self.ball.velocity.dx < 0:
            self.ball.bounce_horizontal()

        if self.ball.center.x > 0 and self.ball.velocity.dx > 0:
            self.ball.bounce_horizontal()

        if self.ball.center.y > SCREEN_HEIGHT and self.ball.velocity.dy > 0:
            self.ball.bounce_vertical

    def check_keys(self):
        # checks for player input
        if self.holding_left:
            self.paddle.move_left()
        
        if self.holding_right:
            self.paddle.move_right()

    def on_key_press(self, key, key_modifiers):
        # used when a key is pressed
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = True
        
        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = True

    def on_key_release(self, key, key_modifiers):
        # used when a key is released
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = False
        
        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = False



window = Breaker(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
