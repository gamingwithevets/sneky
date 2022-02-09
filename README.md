# Basic info
Snake, now made in Pygame!  

# Requirements
You just need a binary to run Sneky without having to install anything.

If you wanna run the game from source code... well, you can download the ZIP file, or if you prefer the Linux way, use `git clone https://github.com/gamingwithevets/sneky.git`.  
Then, install Python (I recommend the latest version). Then, you should update `pip` first. Run `pip install --upgrade pip` to do that.  
And, of course, run `pip install pygame`.
After that, run `main.py` to start the game!  

Currently, ports for **Windows and Linux** have been made.  
A macOS port *is planned*, but due to me having frustrations with installing macOS on VirtualBox in the past, I probably need a real Mac to make a macOS port.  
So please, if ***you*** have a real Mac, PLEASE ***open a new issue in the Issues tab*** with a title like "**macOS port for Sneky**".  
Then, if I find one, I'll be sure to check it out!

Also, the Linux port **does not support the *Windows Subsystem for Linux***, so you'll most likely encounter an error running it in WSL.  
However, I *might* be wrong! If you ran the Linux port of Sneky on WSL without issue, **PLEASE** post it [here](http://discord.gg/S4GQg5fEHN)!

## Building a Binary
If you want to build your own binary, especially for versions older than `v1.0.0b`, first, of course, you need to clone the repo.  
In addition to Pygame and Python, you need Pyinstaller. To install it, just use `pip install pyinstaller`.

Making a command of your own takes some time, so run this command in the root directory of the repo.  
For Windows:
```
pyinstaller --noconfirm --onefile --name "sneky" --icon icon.ico --add-data game.py;. --add-data logger.py;. --add-data menu.py;. --add-data audio;audio/ --add-data fonts;fonts/ --add-data images;images/ main.py
```
For Linux:
```
pyinstaller --noconfirm --onefile --name "sneky" --icon icon.ico --add-data game.py:. --add-data logger.py:. --add-data menu.py:. --add-data audio:audio/ --add-data fonts:fonts/ --add-data images:images/ main.py
```

Run that, and in the `dist` folder of the repo folder, there should be a file called `sneky`. Now you can share it with your friends who doesn't have Python!

# Gameplay
Currently, the game has 6 modes.
## Classic
It's just... Snake. You will die if you bump into yourself or hit the border.
## Apple Bag
Multiple apples are spawning! Will the snake eat them or be hungry?
## Portal Border
The border turns into a portal to go to the other side of the playfield!
## Ultimate Mode
The snake switches color and power every time you collect **a certain amount of apples**. Let's use the snake's powers to win!
## Angry Apple
**You** are the apple! You're tired of the snake eating all of your mates, so you try to escape the snake by running out of the playfield!  
If you escape the snake, you get 1 point and be spawned somewhere else, but the snake will recieve power. If the snake eats you, you die. If it dies, you win!
## De Snake Mode
The *Debug* Mode of Sneky. Like cheating? This is for you! You can walk through yourself, turn around, and walk through the portal borders!
## How to win
To win in a mode (except for Angry Apple), you must somehow fill the entire screen with yourself so that **no apples remain on-screen**!

# Game Features
## Turbo Mode
The snake's speed is 0% at first, which is VERY slow. Normally, eating an apple makes the snake speed up by *a little bit*.  
But that's slow, right? Hold down the Turbo key (default: LCTRL) to speed the snake up to max speed until you lift the key!  
In Angry Apple mode, this slows down the snake to a little over 0%, making escaping the snake easier.
## AI Snake
Serial Number **Q**5**U**4**E**X7YY2**E**9**N**, a.k.a. Queen from *Deltarune*, comes to help you! Press the AI Snake key (default: X) to receive help from her and let her play instead. Press the AI Snake key again to regain control of the snake.  
Keep in mind: The Queen will not help you in Angry Apple mode, since she's controlling the snake!
## The Snake's Colors
The snake has different colors, and that represents different powers.
- Green: The pain 'ol snake that dies when bumping into borders or itself.
- Super Yellow: Makes more apples spawn.
- God Red: Allows you to turn around and go past yourself.
- Light Blue: Makes the borders act as portals to the other side of the playfield.
- Ultra Instinct White: You become so fast that the border completely breaks, allowing you to go outside of the playfield. Be careful, because you can lose track of the snake. Ultimate Mode only.
## Miscellaneous
### Key Rebinding
Yup, that's right!!! You didn't expect this, right? You wouldn't think a game coming from GitHub wouldn't have key rebinding, right?  
Well, you can say it's very unnecessary, but who cares?  
In case you have one of your keys broken, especially if it's required to play Sneky (like the ESC key, you can rebind the key to a non-broken key!
Just go to Settings > Controls, and you can rebind any key you want. This can also be helpful if you wanna change up the controls, e.g. you prefer WASD to move (the default move keys are the arrow keys).
### Themes
Every time you load up Sneky, it checks the date to load the theme. For example, on December 24th, Sneky loads the Christmas theme!  
You can't change the game theme from within the game, though. What you can do to change the game theme is to change the date on your computer or modify the code!
### Splashes
On top of the logo is a splash that changes every time you reload the menu.  
What text it will show depends on RNG, the game theme, and the date.

# Planned Features
Here's the planned features of Sneky:
- Ports for macOS ~~and Linux~~ **There is a Linux port for v1.2.1! Check it out [here](https://github.com/gamingwithevets/sneky/releases/tag/v1.2.1).**
- Can be played with controller
- Halloween theme
- No lag
- Refreshing
- Checking for updates
- Multiplayer
- Online leaderboard
- Less lag in gameplay
- Fullscreen without issues

# Credits
Apple Graphic: Luna4s  
Title Screen & Snake Graphics: GamingWithEvets (GWE Inc.)  
Menu Music: "Nintendo Anti-Piracy Self-Reporter" - Joey Perleoni  
Game Music: "Nothing to Say" - Md Abdul Kader Zilani  
Sounds from DELTARUNE, Google Snake Game, Super Mario Bros. 2 USA, Brain Age  

Menu Template: ChristianD37  
Mode Menu: SeverusFate (SJ Studio)  
Other Menu Code: GamingWithEvets  
Game Code & Graphics Injection: SeverusFate & GamingWithEvets  
Music & SFX Injection: GamingWithEvets  
Crash Handler & Logger: GamingWithEvets  

**© 2021 SJ Studio + GamingWithEvets Inc. All rights go to their respective owners.**
