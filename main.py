# Try to add seasonal change for Minecraft resource packs.
# Requires pillow(PIL)

import os
import json
from PIL import Image

lang = 'en'
available_list = ['acacia_leaves', 'birch_leaves',
                  'dark_oak_leaves', 'jungle_leaves', 'oak_leaves', 'spruce_leaves']
default_color = {'acacia_leaves': (174, 164, 42, 255), 'birch_leaves': (26, 191, 0, 255), 'dark_oak_leaves': (
    26, 191, 0, 255), 'jungle_leaves': (26, 191, 0, 255), 'oak_leaves': (26, 191, 0, 255), 'spruce_leaves': (96, 161, 123, 255)}
t_r, t_g, t_b, t_a = target_color = (255, 217, 0, 255)
translation = {'zh': {"Fuck! ": "你🐴死了"}}

# Seasonal leaves frames
frames = 24

# example root_dir: 'G:\sjfhsjfh\hmcl'
dir = ''
dir_list = []

# Function definition.

# language choosing.


def trans(text: str) -> str:
    """Translation. """
    global lang, translation
    if lang != 'en':
        try:
            dictionary = translation[lang]
        except:
            print("* Translation Error")
            print("* Language ", lang, " not found, using en instead. ")
            lang = 'en'
            return text
        try:
            text = dictionary[text]
        except:
            pass
    return text

# Img processing & .mcmeta writing


def convert(img_dir: str, tint: bool = False) -> None:
    """Processing the .png image only. """
    global frames, default_color, t_r, t_g, t_b, t_a

    # Img part
    if os.path.isfile(img_dir):
        pname, fname = os.path.split(img_dir)
        name, ename = os.path.splitext(fname)
        try:
            img = Image.open(img_dir)
        except:
            print(trans("* Unable to open image:"), img_dir)
            exit()
        # Save the raw image
        img.save(os.path.join(pname, 'raaaaaw_' + name + ename))
        w, h = img.size
        ans_size = (w, h * 2 * (frames - 1))
        ans = Image.new('RGBA', ans_size, '#00000000')
        raw_pix = img.load()

        # Detect if black-and-white
        for x in range(0, w):
            for y in range(0, h):
                r_r, r_g, r_b, r_a = raw_pix[x, y]
                if abs(r_r - r_g) > 1 or abs(r_r - r_b) > 1 or abs(r_g - r_b) > 1:
                    tint = True
                    break

        # Forced coloring (only green now)
        if tint == False:
            for x in range(0, w):
                for y in range(0, h):
                    r_r, r_g, r_b, r_a = raw_pix[x, y]
                    if r_a > 0:
                        r_r, r_g, r_b, r_a = default_color[name]
                    raw_pix[x, y] = (r_r, r_g, r_b, r_a)

        # Frames
        for i in range(0, frames):
            frame = img.copy()
            frame_pix = frame.load()

            # COLOR!!!!!!!!!!
            for x in range(0, w):
                for y in range(0, h):
                    r, g, b, a = frame_pix[x, y]
                    r_r, r_g, r_b, r_a = raw_pix[x, y]
                    if r_a == 255:
                        r = round(r_r + (i / (frames - 1)) * (t_r - r_r))
                        g = round(r_g + (i / (frames - 1)) * (t_g - r_g))
                        b = round(r_b + (i / (frames - 1)) * (t_b - r_b))
                    frame_pix[x, y] = (r, g, b, a)

            # Paste the frame on the ans img
            ans.paste(frame, (0, i * h))
            if i != 1:
                ans.paste(frame, (0, (2 * frames - 1 - i) * h))

        # Save the output
        ans.save(img_dir)

    # If no, use default texture(generated)
    else:
        pname, fname = os.path.split(img_dir)
        name, ename = os.path.splitext(fname)
        pydir = os.path.split(__file__)[0]
        print(trans("* No texture found for"), name,
              trans(", trying to use the generated texture. "))
        try:
            ans = Image.open(os.path.join(
                pydir, 'default_texture', 'generated', fname))
        except:
            print(trans("* No generated texture found for"), name,
                  trans(". Please make sure the tool is downloaded completely. "))
            exit()
        ans.save(img_dir)

    # mcmeta part
    try:
        with open(os.path.join(pname, fname + '.mcmeta'), 'r') as mcmeta_file:
            raw_mcmeta = mcmeta_file.read()
            # Later to support animated textures
            #mcmeta = json.loads(raw_mcmeta)
            # mcmeta["animation"]
            with open(os.path.join(pname, 'raaaaaw_' + fname + '.mcmeta'), 'w') as backup:
                backup.write(raw_mcmeta)
    except:
        with open(os.path.join(pname, fname + '.mcmeta'), 'w') as mcmeta_file:
            mcmeta = {'animation': {'frametime': round(4383000 / frames)}}
            mcmeta = json.dumps(mcmeta, ensure_ascii=False, indent=4)
            mcmeta_file.write(mcmeta)


# Main
# Get and enter the resourcepacks folder in .minecraft folder
ok = False
while ok == False:
    try:
        dir_get = input(
            trans("* Please enter your .minecraft folder directory: \n"))
        dir_list = os.listdir(dir_get)
        ok = True
    except:
        print(trans("* The path is not available. \n"))
    if '.minecraft' in dir_list:
        dir = os.path.join(dir_get, '.minecraft', 'resourcepacks')
    elif 'resourcepacks' in dir_list:
        dir = os.path.join(dir_get, 'resourcepacks')
    if os.path.isdir(dir):
        ok = True
    else:
        ok = False
        print(trans("* No 'resourcepacks' folder found in '.minecraft' folder. "))
dir_list = os.listdir(dir)

# Try to find resource packs
resourcepacks = []
for f in dir_list:
    if os.path.isdir(os.path.join(dir, f)):
        print(trans("* Resource pack < ") + f + trans(" > detected. "))
        resourcepacks.append(f)

# If no resource packs found
if len(resourcepacks) == 0:
    print(trans("* No resource packs found in 'resourcepacks' folder. \n"))
    quit()

# Choose a resource pack
ok = False
while ok == False:
    target_resourcepack = input(
        trans("* Please choose a resource pack: (Name is case sensitive)\n"))
    if target_resourcepack in resourcepacks:
        ok = True
    else:
        print(trans("* Resource pack < ") +
              target_resourcepack + trans(" > not found. "))

# Enter the resource pack
dir = os.path.join(dir, target_resourcepack, 'assets', 'minecraft')

# Edit the model json file
try:
    with open(os.path.join(dir, 'models', 'leaves.json'), 'r') as leaves:
        setting = leaves.read()
    setting = json.loads(setting)
    for face in ['down', 'up', 'north', 'south', 'west', 'east']:
        for i in range(len(setting['elements'])):
            try:
                del setting['elements'][i]['faces'][face]['tintindex']
            except:
                pass
    setting = json.dumps(setting)

# Add one according to the default texture
except:
    with open(os.path.join(os.path.split(__file__)[0], 'default_texture', 'leaves.json'), 'r') as leaves:
        setting = leaves.read()

# Write the model json file
with open(os.path.join(dir, 'models', 'leaves.json'), 'w') as leaves:
    leaves.write(setting)

# Process the leaves
for leaf in available_list:
    convert(os.path.join(dir, 'textures', 'block', leaf + '.png'))
    print(trans("* Processed texture < ") + leaf +
          '.png' + trans(" > successfully. "))
