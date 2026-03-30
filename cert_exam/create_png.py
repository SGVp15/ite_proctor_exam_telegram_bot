from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .CertContact import CertContact

from .config_cert_exam import TEMPLATE_FOLDER


def create_png(cert_contact: CertContact):
    img = Image.open(f'{TEMPLATE_FOLDER}/{cert_contact.template}')

    image_draw = ImageDraw.Draw(img)

    Geometria_70 = ImageFont.truetype(Path('./fonts/Geometria/geometria_light.otf'), 70)
    image_draw.text((647, 1220),
                    f'№ {cert_contact.number:06}   {cert_contact.date_exam.strftime('%d.%m.%Y')}', font=Geometria_70,
                    fill=(16, 21, 84))

    Rubik_115 = ImageFont.truetype(Path('./fonts/Rubik/Rubik-Regular.ttf'), 115, )
    image_draw.text((round(0.59 * img.width), 1550),
                    f'{cert_contact.name_rus}', font=Rubik_115, fill=(16, 21, 84),
                    anchor='mm')

    Rubik_70 = ImageFont.truetype('./fonts/Rubik/Rubik-Regular.ttf', 70)
    image_draw.text((round(0.59 * img.width), 1700),
                    f'{cert_contact.name_eng}', font=Rubik_70, fill=(16, 21, 84), anchor='mm')

    img.save(cert_contact.file_out_png)
