#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from io import BytesIO
from random import choice

from PIL import Image, ImageDraw, ImageOps, ImageFont


async def create_group_photo(language: str, client_photo: BytesIO) -> BytesIO:
    base_image = Image.new(mode='RGB', size=(1080, 1080), color=(255, 255, 255))

    # Open client avatar and resize
    client_photo = Image.open(client_photo)
    client_photo_color = get_most_frequent_color(image=client_photo)
    nexium_photo = Image.open(f'static/images/{language}/nexium.png')
    client_photo = client_photo.resize((384, 384))
    nexium_photo = nexium_photo.resize((384, 384))

    # Polygons
    draw = ImageDraw.Draw(base_image)
    color1 = (18, 18, 18)
    color2 = client_photo_color
    draw.polygon([(0, 0), (1080, 0), (0, 1080)], fill=color1)
    draw.polygon([(1080, 1080), (1080, 0), (0, 1080)], fill=color2)

    add_photo(
        position=(540, 540),
        base_image=base_image,
        photo=client_photo,
    )
    add_photo(
        position=(156, 156),
        base_image=base_image,
        photo=nexium_photo,
    )

    # Save
    avatar = BytesIO()
    base_image.save(avatar, format='PNG')
    avatar.seek(0)

    return avatar


def add_photo(position, base_image: Image, photo: Image):
    mask = Image.new(mode='L', size=photo.size, color=0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 384, 384), fill=255)
    rounded_avatar = ImageOps.fit(photo, mask.size, centering=(0.5, 0.5))
    rounded_avatar.putalpha(mask)
    base_image.paste(rounded_avatar, position, rounded_avatar)


def get_most_frequent_color(image: Image, darken_factor: float = 0.8, lighten_factor: float = 4):
    small_image = image.resize((100, 100))
    colors = small_image.getcolors(10000)
    most_frequent_color = max(colors, key=lambda item: item[0])[1]

    brightness = sum(most_frequent_color) / 3

    if brightness < 128:
        adjusted_color = tuple(min(int(c * lighten_factor), 255) for c in most_frequent_color)
    else:
        adjusted_color = tuple(int(c * darken_factor) for c in most_frequent_color)

    return adjusted_color


async def create_invite_photo(language: str, group_photo: BytesIO, title: str, time: str):
    main_image = Image.open(f'static/images/{language}/consultation.png')
    overlay_image = Image.open(group_photo)
    group_photo.seek(0)
    overlay_image = overlay_image.resize((95, 95))

    # Round
    mask = Image.new('L', overlay_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, overlay_image.size[0], overlay_image.size[1]), fill=255)
    overlay_image = ImageOps.fit(overlay_image, mask.size, centering=(0.5, 0.5))
    overlay_image.putalpha(mask)

    # Add overlay
    main_image.paste(overlay_image, (122, 833), overlay_image)

    font_1 = ImageFont.truetype(font='static/fonts/Manrope-Bold.ttf', size=29)
    font_2 = ImageFont.truetype(font='static/fonts/Manrope-ExtraLight.ttf', size=24)

    draw = ImageDraw.Draw(main_image)
    draw.text((249, 845), title, font=font_1, fill='#000000')
    draw.text((802, 823), time, font=font_2, fill='#000000')

    photo = BytesIO()
    main_image.save(photo, format='PNG')
    photo.seek(0)

    return photo


async def create_client_photo(text: str):
    width, height = 1080, 1080
    colors = [
        {'bg': (244, 164, 96), 'text': (255, 255, 255)},  # Sandy Brown background with white text
        {'bg': (135, 206, 250), 'text': (0, 0, 128)},  # Light Sky Blue background with navy text
        {'bg': (255, 182, 193), 'text': (255, 105, 180)},  # Light Pink background with hot pink text
        {'bg': (152, 251, 152), 'text': (0, 100, 0)},  # Pale Green background with dark green text
        {'bg': (221, 160, 221), 'text': (75, 0, 130)},  # Plum background with indigo text
        {'bg': (240, 230, 140), 'text': (139, 69, 19)},  # Khaki background with saddle brown text
        {'bg': (173, 216, 230), 'text': (25, 25, 112)},  # Light Blue background with midnight blue text
        {'bg': (255, 228, 181), 'text': (139, 69, 19)},  # Moccasin background with saddle brown text
        {'bg': (255, 222, 173), 'text': (160, 82, 45)},  # Navajo White background with sienna text
        {'bg': (176, 224, 230), 'text': (70, 130, 180)},  # Powder Blue background with steel blue text
    ]

    colors = choice(colors)
    background_color = colors['bg']
    text_color = colors['text']

    img = Image.new('RGB', (width, height), color=background_color)

    font = ImageFont.truetype(font='static/fonts/Manrope-Bold.ttf', size=514)
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2 - bbox[1]

    draw.text((text_x, text_y), text, font=font, fill=text_color)

    photo = BytesIO()
    img.save(photo, format='PNG')
    photo.seek(0)

    return photo
