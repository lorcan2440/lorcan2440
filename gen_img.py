import xml.etree.ElementTree as ET
import requests
import os

'''
This script dynamically creates an SVG image.
The image contains the icons listed in the variable `imgs` below.
Below each icon, the name (key) of the icon is displayed in small text, centred below the icon.
The icons are aligned horizontally, with a small margin between them.
This image is to be displayed in a GitHub Readme, so due to restrictions, 
it cannot load the URLs of the icons, so the icons are downloaded locally, then placed inside
the SVG to create a fully self-contained SVG image. This is done using the XML library.
'''

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
IMG_URL = 'https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg'
OUTPUT_FILE = 'skills.svg'
HOST_URL = f'https://lorcan.netlify.app/uploads/hosting_gh/{OUTPUT_FILE}'

imgs = {
    'Python': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg',
    'OpenCV': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/opencv/opencv-original.svg',
    'NumPy': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg',
    'Pandas': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg',
    'TensorFlow': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/tensorflow/tensorflow-original.svg',
    'C++': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/cplusplus/cplusplus-original.svg',
    'MATLAB': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/matlab/matlab-original.svg',
    'Lua': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/lua/lua-original.svg',
    'R': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/r/r-original.svg',
    #'Illustrator': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/illustrator/illustrator-line.svg',
    #'Premiere Pro': 'https://raw.githubusercontent.com/devicons/devicon/master/icons/premierepro/premierepro-original.svg'
}

imgs_2 = {
    'SOLIDWORKS': None,
    'COMSOL': None,
}






def gen_image(urls_only: bool = True):

    # download each of the images in the imgs dict
    for key, url in imgs.items():
        r = requests.get(url)
        with open(os.path.join(DIR_PATH, f'{key}.svg'), 'wb') as f:
            f.write(r.content)
    
    # load the CSS file  # TODO: can also try <?xml-stylesheet type="text/css" href="style.css"?>
    with open(os.path.join(DIR_PATH, 'style.css'), 'r') as f:
        css_data = f.read()

    # create a new blank SVG file
    root = ET.Element('div', attrib={'xmlns': 'http://www.w3.org/1999/xhtml', 'xmlns:xlink': 'http://www.w3.org/1999/xlink', 'class': 'container_img'})
    tree = ET.ElementTree(root)
    style = ET.SubElement(root, 'style')
    style.text = css_data

    # add each of the icons to the group
    for key in imgs.keys():
        # add a new div
        div = ET.SubElement(root, 'div', attrib={'class': 'item'})

        # add a new icon
        icon = ET.SubElement(div, 'svg', attrib={'width': '100%', 'height': '100%', 'xmlns': 'http://www.w3.org/2000/svg', 'class': 'icon'})

        if urls_only:
            # add the URL to the icon
            icon_url = ET.SubElement(icon, 'image', attrib={'xlink:href': imgs[key], 'width': '110', 'height': '60'})
        else:
            # get XML code from the icon SVG
            img_tree = ET.parse(os.path.join(DIR_PATH, f'{key}.svg'))
            svg = img_tree.getroot()
            svg.attrib = {'width': '100', 'height': '60', 'viewBox': '0 0 128 128'}
            # add the XML to the icon
            icon.append(svg)

        # add the text below the icon
        icon_text = ET.SubElement(icon, 'text', attrib={'x': '55', 'y': '70', 'class': 'label'})
        icon_text.text = key
    
    # write the SVG to a file
    tree.write(os.path.join(DIR_PATH, OUTPUT_FILE))

    # delete the online icons
    for key in imgs.keys():
        os.remove(os.path.join(DIR_PATH, f'{key}.svg'))
    
    print(f'Created {OUTPUT_FILE}, push to make available at: \n\t{HOST_URL}')


if __name__ == '__main__':
    gen_image(urls_only=True)
