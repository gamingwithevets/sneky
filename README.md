# Basic info
Snake, now made in Pygame!  
NOTE: This branch is for the **Christmas version**. For regular Sneky, please switch to the **main** branch.

# Requirements
Just like regular Sneky, you just need a binary to run this version without having to install anything.

If you wanna run the game from source code... well, you can download the ZIP file, or if you prefer the Linux way, use `git clone https://github.com/gamingwithevets/sneky.git`.  
Then, install Python (I recommend the latest version). Then, you should update `pip` first. Run `pip install --upgrade pip` to do that.  
And, of course, run `pip install pygame`.
After that, run `main.py` to start the game!  
NOTE: The game only supports Windows, due to the game saving in %LOCALAPPDATA%, which is not present in Linux.
## Building a Binary
If you want to build your own binary of this version as well, first, of course, you need to clone the repo.  
In addition to Pygame and Python, you need Pyinstaller. To install it, just use `pip install pyinstaller`.

Making a command of your own takes some time, so run this command in the root directory of the repo.

```
pyinstaller --noconfirm --onefile --name "sneky" --icon icon.ico --add-data game.py;. --add-data logger.py;. --add-data menu.py;. --add-data audio;audio/ --add-data fonts;fonts/ --add-data images;images/ main.py
```

Run that, and in the `dist` folder of the repo folder, there should be a file called `sneky.exe`. Now you can share it with your friends who doesn't have Python!

# Gameplay
Currently, the game has 6 modes.
## Classic
It's Christmas! The snake wants the candy cones! Eat 'em and don't touch yourself or the border, or you'll die!
## Treat Bag
Santa's giving out more candy cones! The snake doesn't hesitate to eat 'em!
## Portal Border
The border turns into a portal to go to the other side of the playfield!
## Ultimate Mode
The snake switches color and power every time you collect **a certain amount of candy cones**. Let's use the snake's powers to win!
## Angry Treat
**You** are a candy cone! You see that the snake has eaten too much cones and isn\'t stopping! He\'s gonna get fat at this rate.  
So, you attempt to escape the snake and return to Santa to be sent somewhere else, but... uh oh! You look back and discover the snake chasing you!  If you escape the snake, you get 1 point and be spawned somewhere else, but the snake will recieve power. If the snake eats you, you die. If it dies, you win!
## De Snake Mode
The *Debug* Mode of Sneky. Like cheating? This is for you! You can walk through yourself, turn around, and walk through the portal borders!
## How to win
To win in a mode (except for Angry Treat), you must somehow fill the entire screen with yourself so that **no apples remain on-screen**!

# Game Features
## Turbo Mode
The snake's speed is 0% at first, which is VERY slow. Normally, eating an apple makes the snake speed up by *a little bit*.  
But that's slow, right? Hold down the Turbo key (default: LCTRL) to speed the snake up to max speed until you lift the key!  
In Angry Apple mode, this slows down the snake to a little over 0%, making escaping the snake easier.
## AI Snake
Serial Number **Q**5**U**4**E**X7YY2**E**9**N**, a.k.a. Queen from *Deltarune*, comes to help you! Press the AI Snake key (default: X) to receive help from her and let her play instead. Press the AI Snake key again to regain control of the snake.  
Keep in mind: The Queen will not help you in Angry Treat mode, since she's controlling the snake!
## The Snake's Colors
The snake has different colors, and that represents different powers.
- Green: The pain 'ol snake that dies when bumping into borders or itself.
- Super Yellow: Makes more apples spawn.
- God Red: Allows you to turn around and go past yourself.
- Light Blue: Makes the borders act as portals to the other side of the playfield.
- Ultra Instinct White: You become so fast that the border completely breaks, allowing you to go outside of the playfield. Be careful, because you can lose track of the snake. Ultimate Mode only.
## Key Rebinding
Yup, that's right!!! You didn't expect this, right? You wouldn't think a game coming from GitHub wouldn't have key rebinding, right?  
Well, you can say it's very unnecessary, but who cares?  
In case you have one of your keys broken, especially if it's required to play Sneky (like the ESC key, you can rebind the key to a non-broken key!
Just go to Settings > Controls, and you can rebind any key you want. This can also be helpful if you wanna change up the controls, e.g. you prefer WASD to move (the default move keys are the arrow keys).

# Credits
Candy Cane Image: Kandi Patterns  
Santa Hat: John3 from TopPNG  
Title Screen & Snake Graphics: GamingWithEvets (GWE Inc.)  
Menu Music: ["Jingle Bells\"](https://www.youtube.com/watch?v=R1gskElaLNo) - From [YouTube](https://www.youtube.com/)/[KON](https://www.youtube.com/channel/UCcmWi0LJKaovJG_DaEhGD_g)  
Game Music: ["We Wish You A Merry Christmas"](https://www.youtube.com/watch?v=8vdXR_igALU) - From [YouTube](https://www.youtube.com/)/[Pudding TV - Nursery Rhymes](https://www.youtube.com/channel/UCjPZm-0TqBPNAzxSrs6zMHw)  
Sounds from DELTARUNE, Google Snake Game, Super Mario Bros. 2 USA, Brain Age  

Menu Template: ChristianD37  
Mode Menu: SeverusFate (SJ Studio)  
Other Menu Code: GamingWithEvets  
Game Code & Graphics Injection: SeverusFate & GamingWithEvets  
Music & SFX Injection: GamingWithEvets  
Crash Handler & Logger: GamingWithEvets  

**© 2021 SJ Studio + GamingWithEvets Inc. All rights go to their respective owners.**
