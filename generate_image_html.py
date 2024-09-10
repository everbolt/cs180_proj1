import os

def create(file_name, green_alignment, blue_alignment, autocrop_dimensions):
    nice_name = file_name.replace('_', ' ').title()
    
    return f'''<h3 style="display: block; text-align: center; margin-top: 20px">{nice_name}</h3><div
      style="
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
        max-width: 100vw;
      "
    >
      <img
        src="./images/uncropped/{file_name}.jpg"
        alt="{nice_name} Image"
        style="width: 30vw"
      />
      <img
        src="./images/cropped/{file_name}.jpg"
        alt="{nice_name} Image"
        style="width: 30vw"
      />
    </div>
    <ul>
      <li>Green Alignment: {green_alignment[0]}, {green_alignment[1]}</li>
      <li>Blue Alignment: {blue_alignment[0]}, {blue_alignment[1]}</li>
      <li>
        Autocrop Dimensions: (Bottom {autocrop_dimensions[0]}) (Top {autocrop_dimensions[1]}) (Right {autocrop_dimensions[2]}) (Left {autocrop_dimensions[3]})
      </li>
    </ul>'''




def get_cropped_image_names(): 
    image_names = [] 
    directory = './web/images/cropped' 
    for filename in os.listdir(directory): 
        if filename.endswith(".jpg"): 
            image_names.append(filename) 
    return image_names

file_names = ['cathedral.jpg', 'monastery.jpg', 'tobolsk.jpg',  'emir.jpg', 'onion_church.jpg', 'icon.jpg', 'in_italy.jpg', 'train.jpg', 'melons.jpg', 'three_generations.jpg', 'church.jpg','lady.jpg',  'sculpture.jpg', 'harvesters.jpg', 'self_portrait.jpg', 'camel_packs.jpg', 'uniform.jpg', 'peonies.jpg']

res = ""
for file_name in file_names:
    # Read {file_name}_alignment.txt from ./v2/cropped/
    temp = file_name.split('.')[0]
    with open(f'./v2/cropped/{temp}_alignment.txt', 'r') as f:
        lines = f.readlines()
        green_alignment = tuple(map(int, lines[0].split(': ')[1].split(', ')))
        blue_alignment = tuple(map(int, lines[1].split(': ')[1].split(', ')))
        autocrop_dimensions = tuple(map(int, lines[2].split(': ')[1].split(', ')))
        res += create(temp, green_alignment, blue_alignment, autocrop_dimensions)

with open('out.txt', 'w') as f:
    f.write(res)
