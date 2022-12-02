# D2R Single Player Terror Zone Mod
A simple script that modifies files to simulate Terror Zones in Single Player (only works in Hell Difficulty). I haven't tested every zone, there might be bugs or crashes (obviously only the script crashes, not your game :) ), let me know if you experience any (with screenshot(s) if possible).
A
The script modifies levels.txt, monstats.txt, uniqueitems.txt, treasureclassex.txt, hudlevelsnameshd.json and levels.json file. If any of your mod depends on these files, they will probably no longer work as expected.

## Limitations
- Only works in Hell Difficulty but it cannot check if Baal is killed or not. You can use it anytime in Hell if you want.
- Does not have Terror Zone graphics / sound
  - No icons next to the monster's name
  - Does not show the terrorized zone in the top right corner (the purple text)
  - No sound effect on entry
- Only Bosses (Act bosses + Summoner, Nihlathak, etc..) and Superuniques (Eldritch, Pindleskin, etc...) drop Sunder Charms (~1% drop rate).
- The game has to be restarted everytime the script updates files, there is no way to force-update the game without restarting (happens only if you change character level in config.ini or after a new zone is chosen which is every hour at hh:59).
- Terrorized text will be added to the current area (couldn't color it so it's red).
  - Sewers (Act II and Act III) uses the same id for their Level Entry text so if one is terrorized both areas will have the text but only 1 of them will actually be terrorized.
  - Text won't show in all languages, only English.

## Extra
- Monster density will be set to 2200 (this is the value for Tal Rasha Tomb / WSK so I guess it's nothing gamebreaking) in Terror Zones, definitely improves some areas with bad monster density.
- Added 2 extra boss packs (added 2 to the Min and Max value that controls the number of boss packs in an area) to Terror Zones.

These features cannot be turned off now, might be in a future version.

## Requirements
- The script assumes you have already unpacked the game files. If you don't know what this means, visit https://www.reddit.com/r/Diablo/comments/qey05y/d2r_single_player_tips_to_improve_your_load_times/ and go to **Advanced Tip #2 - Extract game files and launch with -direct and -txt in the shortcut options**.
- Python (Tested on 3.10.2, probably needs 3.6 at least, might work on earlier versions too) installed (and the packages provided in requirements.txt): https://www.python.org/
  - if you don't know how to do this, go to the last section: https://github.com/night0wl117/d2r-sp-terror-zone#installing-python-and-the-packages

## Usage
0. Copying files:
   - Copy **hudlevelnameshd.json** to <your_game_folder_you_have_unpacked_the_files_to>\data\global\ui\layouts\ and overwrite the existing file there. This is needed for the "Terrorized" text to show up. If you don't do this, the area names may look weird.
   - Copy **treasureclassex.txt** and **uniqueitems.txt** to <your_game_folder_you_have_unpacked_the_files_to>\data\global\excel\ and overwrite the existing file there.
2. Open config.ini and update the 2 variables 
   - **Level**: the character's level you intend to play with (needs to be manually updated everytime you level up or change character)
   - **d2r_mod_data_folder_path**: the path to the **data** folder (this is the location of the files you have unpacked previously, should look something like this: C:\Program Files (x86)\Diablo II Resurrected\Data)
3. Navigate to the folder you have downloaded the script and its files and type **cmd** in the address bar then press Enter (don't worry about the .venv folder, you don't need it):
![image](https://user-images.githubusercontent.com/47192871/204891220-1f9e7c2a-9b6e-4e26-98cc-1def4d50b26b.png)
3. A command prompt will open. Type **terror_zone.py** (or **python terror_zone.py** or **python3 terror_zone.py** if that does not work) then press Enter.
   - ![image](https://user-images.githubusercontent.com/47192871/204891920-9aac2241-cbf6-4532-b713-cbaae097e4d1.png)
4. That's it, the script will run and update files until you terminate it. If you want changing zones every hour, leave the script running for as long as you play.


## Informations
- You will be asked if you would like to keep the current terror zone. Type **Y** or **N**.
  - if you chose to keep the current zone, it will still update the files just to be sure but nothing should change
  - if you typed **N** a new area will be selected randomly, it will look something like this:
    - ![image](https://user-images.githubusercontent.com/47192871/204898839-c989f70e-5211-4554-a485-be816c819614.png)
- The script checks the character level in config.ini every ~10 second. If it detects any change the game files will be updated accordingly (Game needs to be restarted if running).
- Every hour at hh:59 a new zone will be chosen (Game has to be restarted)
- If you want to terminate the script (Ctrl + C) it will ask if you want to reset the files to their original state or keep it. If you want to start the game without TZ next time, type **N**.
- Do not change the content of the **zones.ini** file, it's just there to keep track of the previous zone.
- If you get an error like **"FileNotFoundError: [Errno 2] No such file or directory:"** you probably have a wrong path in **config.ini** for the **d2r_mod_data_folder_path** variable.
- You can terminate/stop the script by pressing Ctrl + C (having the cmd window active).


## Installing Python and the packages
When installing python make sure to add python to PATH 
![image](https://user-images.githubusercontent.com/47192871/204991382-046b6fd9-dcc6-4672-89d4-7569a1d2d070.png)

After python is installed, navigate to the script folder and type **cmd** in the address bar (see image above). Then type **pip install -r requirements.txt** and you should be good to go.
