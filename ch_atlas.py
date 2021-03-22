import sys
import os 
import json

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Pillow is not installed !\nPlease run command\n\tpip install --user pillow")
    exit()

def stitch(version, atlas):
    textures_path = "textures/"+version+"/"
    json_path = "json/"+version+"/"

    coordinates_file = open(json_path+"coordinates.json")
    names_file = open(json_path+"names.json")

    coordinates = json.load(coordinates_file)
    names = json.load(names_file)
    
    atlas_img = Image.new('RGBA', coordinates['size'], color = (0, 0, 0, 0))

    textures = coordinates['textures']
    for texture in textures:
        data = textures[texture]
        name = names[texture] if texture in names else texture
        try:
            with Image.open(textures_path+name+".png").transpose(Image.FLIP_TOP_BOTTOM) as tex:
                ulx = int(float(data['x']))
                uly = int(float(data['y']))
                atlas_img.paste(tex, (ulx, uly))
        except IOError:
            print("textures/"+sys.argv[1]+"/"+texture+".png not found !")
    atlas_img.transpose(Image.FLIP_TOP_BOTTOM).save(atlas)

def explode(version, atlas):
    if not os.path.isdir('textures'): os.mkdir('textures')
    if not os.path.isdir('textures/'+version): os.mkdir('textures/'+version)
        
    textures_path = "textures/"+version+"/"
    json_path = "json/"+version+"/"
    
    coordinates_file = open(json_path+"coordinates.json")
    names_file = open(json_path+"names.json")
    
    coordinates = json.load(coordinates_file)
    names = json.load(names_file)
    
    atlas_img = Image.open(atlas).transpose(Image.FLIP_TOP_BOTTOM)

    textures = coordinates['textures']
    for texture in textures:
        data = textures[texture]
        name = names[texture] if texture in names else texture
        ulx = float(data['x'])
        uly = float(data['y'])
        lrx = ulx + float(data['width'])
        lry = uly + float(data['height'])
        tex = atlas_img.crop((ulx, uly, lrx, lry)).transpose(Image.FLIP_TOP_BOTTOM)
        tex.save(textures_path+name+".png")

if(__name__=="__main__"):
    versions = os.listdir("json")
    if len(sys.argv) == 4:
        if sys.argv[1] == "explode":
            explode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "stitch":
            stitch(sys.argv[2], sys.argv[3])
        else:
            print("Invalid argument " + sys.argv[1])
    else:
        print("Usage : py ch_atlas.py [MODE] [GAME VERSION] [ATLAS TEXTURE FILE]")
        print("      :")
        print("      : [MODE] : explode OR stitch")
        print("      : [GAME VERSION] : Self Explanatory")
        print("      : [ATLAS TEXTURE FILE] : Path to atlas to explode / stitch")
        print("      :")
        print("      : Supported game versions :", versions)

