"""
Wanderson soares dos santos - UTF-8 - pt-Br - 26/08/2023
models.py
"""
import os
import numpy as np
from PIL import Image, UnidentifiedImageError
from flask import url_for


# all classes have a dictionary named 'attributtes', where the key is the name of the functions,
# and receive a list on value, where the first element of list is the name that goes on site,
# and the second value is a boolean that specifies if the element will receive many files
# in the input on the page, the third value represents the extensions accept by the functions.


class DocumentManipulations:
    class_name = 'Manipulação de documentos'
    attributes = {
        'word_equal_pdf': ['Converta Docx para PDF ou PDF para Docx', False, '.pdf,.docx'],
        'merge_pdf': ['Junte vários PDFs', True, '.pdf'],
        'extract_img_pdf': ['Extraia imagens de um PDF', False, '.pdf'],
    }

    @classmethod
    def word_equal_pdf(cls, input_path, convert_to, output_path=None):
        """
        Convert between Word and PDF files.

        :param input_path: Path to the input file.
        :param convert_to: Conversion type: 'word_to_pdf' or 'pdf_to_word'.
        :param output_path: Path to the output file. Defaults to None.
        """
        if convert_to not in ['word_to_pdf', 'pdf_to_word']:
            raise ValueError(
                "Invalid conversion type. Choose 'word_to_pdf' or 'pdf_to_word'.")
        if output_path is None:
            output_path = os.path.splitext(input_path)[0]

        if convert_to == 'word_to_pdf':
            from docx2pdf import convert
            try:
                convert(input_path, output_path)
            except Exception as e:
                print(f"Error converting Word to PDF: {e}")
        elif convert_to == 'pdf_to_word':
            from pdf2docx import Converter
            pdf = Converter(input_path)
            pdf.convert(output_path, start=0, end=None)

            pdf.close()

    @classmethod
    def merge_pdf(cls, pdfs, path):
        import PyPDF2

        merger = PyPDF2.PdfMerger(strict=False)

        for pdf in pdfs:
            if ".pdf" in pdf:
                merger.append(f'{pdf}')

        i = 1
        while True:
            files = os.listdir(path)
            if f'final_pdf{i}.pdf' not in files:
                with open(os.path.join(path, f'final_pdf{i}.pdf'), 'wb') as output_file:
                    merger.write(output_file)
                    break
            i += 1

    @classmethod
    def extract_img_pdf(cls, pdf, folder_path):
        from pikepdf import Pdf, PdfImage

        final_pdf = Pdf.open(pdf)
        for page in final_pdf.pages:
            for name, image in page.images.items():
                save_img = PdfImage(image)
                save_img.extract_to(fileprefix=f'{folder_path}/{name}')


class MediaManipulations:
    class_name = 'Manipulação de midias'
    attributes = {
        'remove_background_photo': ['Remova o fundo de uma imagem', False, 'image/*'],
        'convert_to_png': ['Converta uma imagem para png', False, 'image/*'],
        'video_to_audio': ['Converta .mp4 para .mp3', False, '.mp4'],
        'join_audios': ['Junte vários arquivos .mp3 em um só', True, '.mp3'],
    }

    @classmethod
    def remove_background_photo(cls, image):
        """function to remove background"""
        try:
            import rembg

            output_path = os.path.splitext(image)[0]

            inp = Image.open(image)
            output = rembg.remove(inp)
            output.save(output_path + '.png')
        except UnidentifiedImageError:
            print('Formato de arquivo errado')
        except:
            print('Erro interno')

    @classmethod
    def convert_to_png(cls, input_path, output_path=None):
        if output_path is None:
            output_path = os.path.splitext(input_path)[0]

        with Image.open(input_path) as img:
            img.save(f'{output_path}.png', 'PNG')

    @classmethod
    def video_to_audio(cls, video_path, format_to_save='.mp3', output_audio_path=None):
        from moviepy.editor import VideoFileClip

        if output_audio_path is None:
            output_audio_path = video_path.rsplit('.', 1)[0] + format_to_save

        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_audio_path)

    @classmethod
    def join_audios(cls, input_path, output_path=None):
        from moviepy.editor import concatenate_audioclips, AudioFileClip

        files = os.listdir(input_path)
        audios = [os.path.join(input_path, file)
                  for file in files if '.mp3' in file]

        if output_path is None:
            output_path = os.path.splitext(input_path)[0]

        clips = [AudioFileClip(aud) for aud in audios]

        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(output_path + 'final_audio.mp3')


class TextToImage:
    class_name = 'Criar imagens'
    attributes = {
        'text_to_qrcode': ['Crie seu próprio QR Code', False, ''],
        'wordcloud': ['Crie sua própria nuvem de palavras', False, ''],
    }

    @classmethod
    def text_to_qrcode(cls, text, output_path):
        import qrcode

        qr = qrcode.QRCode(version=1,  # Nível de correção de erro (1 a 40)
                           box_size=50,  # Tamanho de cada pixel do QR code
                           border=2,)  # Tamanho da margem em torno do QR code
        qr.add_data(text)
        image = qr.make_image(fill_color="black", back_color="white")
        i = 0
        while True:
            file = f'qrcode{i}.png'
            if file not in os.listdir(output_path):
                image.save(os.path.join(output_path, file))
                break
            i += 1

    @classmethod
    def wordcloud(cls, text, output_path, image=None):

        import matplotlib.pyplot as plt
        from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
        from scipy.ndimage import gaussian_gradient_magnitude

        canvas_width = 1920
        canvas_height = 1080

        if image is not None:
            image = np.array(Image.open(image))
        else:
            image = np.array(Image.open(os.path.join(
                os.getcwd(), 'website', 'static', 'img', 'nuvem.png')))

        image_mask = image.copy()
        image[image_mask.sum(axis=2) == 0] = 255

        edges = np.mean([gaussian_gradient_magnitude(
            image[:, :, i] / 255., 2) for i in range(3)], axis=0)
        image_mask[edges > .1] = 255
        wordcloud = WordCloud(width=canvas_width, height=canvas_height, background_color='white',
                              mask=image_mask, mode='RGBA')
        wordcloud.generate(text)
        image_colors = ImageColorGenerator(image)
        # wordcloud.recolor(color_func=image_colors)
        i = 1
        while True:
            file = f'wordcloud{i}.png'
            if file not in os.listdir(output_path):
                wordcloud.to_file(os.path.join(output_path, file))
                break
            i += 1


# MediaManipulations.remove_background_photo('../eu.jpg')
# FileManipulations.word_equal_pdf('../arquivos/curr.doc', 'word_to_pdf')
# FileManipulations.convert_to_png('../eu.jpg')
# FileManipulations.extract_img_pdf('../arquivos/curr.pdf')
# FileManipulations.join_audios('../')
"""with open('../romeo.txt', 'r') as text:
    TextToImage.wordcloud(text.read())"""
# TextToImage.text_to_qrcode('https://github.com/wand-CE')
# with open('../Romeo and Juliet.txt', 'r') as file:
#    text = file.read()
# FileManipulations.new(text, '../romeo.jpg')
# FileManipulations.wordcloud(text, '../romeo.jpg')
