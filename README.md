# d2r-sp-terror-zone
A simple script that modifies files to simulate Terror Zones in Single Player (only works in Hell Difficulty).

## Limitations
- Only works in Hell Difficulty but it cannot check if Baal is killed or not. You can use it anytime in Hell if you want.
- Does not have Terror Zone graphics / sound
- Only Bosses (Act bosses + Summoner, Nihlathak, etc..) and Superuniques (Eldritch, Pindleskin, etc...) drop Sunder Charms (~1% drop rate).
- The game has to be restarted everytime the script updates files, there is no way to force-update the game without restarting (happens only if you change character level in config.ini or after a new zone is chosen which is every hour at hh:59).
- Terrorized text will be added to the current level (couldn't color it so it's red). Sewers (Act II and Act III) uses the same id for their Level Entry text so if one is terrorized both areas will have the text but only 1 of them is actually terrorized.

## Requirements
- The script assumes you have already unpacked the game files. If you don't know what this means, visit https://www.reddit.com/r/Diablo/comments/qey05y/d2r_single_player_tips_to_improve_your_load_times/ and go to **Advanced Tip #2 - Extract game files and launch with -direct and -txt in the shortcut options**.
- Python (Tested on 3.10.2, probably needs 3.6 at least, might work on earlier versions too) installed (and the packages provided in requirements.txt): https://www.python.org/

## Usage
1. Open config.ini and update the 2 variables 
   - **Level**: the character's level you intend to play with (needs to be manually updated everytime you level up or change character)
   - **d2r_mod_data_folder_path**: the path to the **data** folder (this is the location of the files you have unpacked previously, should look something like this: C:\Program Files (x86)\Diablo II Resurrected\Data)
2. Navigate to the folder you have downloaded the script and its files and type **cmd** in the address bar then press Enter (don't worry about the .venv folder, you don't need it):
![image](https://user-images.githubusercontent.com/47192871/204891220-1f9e7c2a-9b6e-4e26-98cc-1def4d50b26b.png)
3. A command prompt will open. Type **terror_zone.py** (or **python3 terror_zone.py** if that does not work) then press Enter.
![image](https://user-images.githubusercontent.com/47192871/204891920-9aac2241-cbf6-4532-b713-cbaae097e4d1.png)
4. That's it, the script will run and update files until you terminate it. If you want changing zones every hour, leave the script running for as long as you play.


## Informations
- You will be asked if you would like to keep the current terror zone. Type **Y** or **N**.
  - if you chose to keep the current zone, it will still update the files just to be sure but nothing should change
  - if you typed **N** a new area will be selected randomly, it will look something like this:
    - ![image](https://user-images.githubusercontent.com/47192871/204898839-c989f70e-5211-4554-a485-be816c819614.png)
- The script checks the character level in config.ini every ~10 second. If it detects any change the game files will be updated accordingly (Game needs to be restarted if running).
- Every hour at hh:59 a new zone will be chosen (Game has to be restarted)
- If you want to terminate the script it will ask if you want to reset the files to their original state or keep it. If you want to start the game without TZ next time, type **N**.

