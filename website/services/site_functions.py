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
    def word_equal_pdf(cls, input_path, convert_to, output_path):
        """
        Convert between Word and PDF files.

        :param input_path: Path to the input file.
        :param convert_to: Conversion type: 'word_to_pdf' or 'pdf_to_word'.
        :param output_path: Path to the output file. Defaults to None.
        """
        if convert_to not in ['word_to_pdf', 'pdf_to_word']:
            raise ValueError(
                "Invalid conversion type. Choose 'word_to_pdf' or 'pdf_to_word'.")

        if convert_to == 'word_to_pdf':
            from docx2pdf import convert
            try:
                i = 1
                while f'PDF{i}.pdf' in os.listdir(output_path):
                    i += 1
                file = f'PDF{i}.pdf'
                output_path = os.path.join(output_path, file)
                convert(input_path, output_path)
                return file
            except Exception as e:
                print(f"Error converting Word to PDF: {e}")

        elif convert_to == 'pdf_to_word':
            from pdf2docx import Converter
            pdf = Converter(input_path)
            i = 1
            while f'WORD{i}.docx' in os.listdir(output_path):
                i += 1
            file = f'WORD{i}.docx'
            output_path = os.path.join(output_path, file)

            pdf.convert(output_path, start=0, end=None)
            pdf.close()
            return file

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
                    return f'final_pdf{i}.pdf'
            i += 1

    @classmethod
    def extract_img_pdf(cls, input_file, output_path):
        from pikepdf import Pdf, PdfImage

        pdf = Pdf.open(input_file)

        for page in pdf.pages:
            for name, image in page.images.items():
                save_img = PdfImage(image)
                i = 1
                while any(file.startswith(name[1:] + str(i)) for file in os.listdir(output_path)):
                    i += 1
                name = name + str(i)
                save_img.extract_to(
                    fileprefix=os.path.join(output_path, name[1:]))


class MediaManipulations:
    class_name = 'Manipulação de midias'
    attributes = {
        'remove_background_photo': ['Remova o fundo de uma imagem', False, 'image/*'],
        'convert_to_png': ['Converta uma imagem para png', False, 'image/*'],
        'video_to_audio': ['Converta .mp4 para .mp3', False, '.mp4'],
        'join_audios': ['Junte vários arquivos .mp3 em um só', True, '.mp3'],
    }

    @classmethod
    def remove_background_photo(cls, image, output_path):
        """function to remove background"""
        try:
            import rembg

            inp = Image.open(image)
            output = rembg.remove(inp)

            i = 1
            while f'image{i}.png' in os.listdir(output_path):
                i += 1

            output_file_path = os.path.join(output_path, f'image{i}.png')
            output.save(output_file_path)
        except UnidentifiedImageError:
            print('Formato de arquivo errado')
        except:
            print('Erro interno')

    @classmethod
    def convert_to_png(cls, input_path, output_path):
        i = 1
        while f'image{i}.png' in os.listdir(output_path):
            i += 1

        output_path = os.path.join(output_path, f'image{i}.png')

        with Image.open(input_path) as img:
            img.save(output_path, 'PNG')

    @classmethod
    def video_to_audio(cls, video_path, output_path):
        from moviepy.editor import VideoFileClip

        i = 1
        while f'music{i}.mp3' in os.listdir(output_path):
            i += 1
        output_path = os.path.join(output_path, f'music{i}.mp3')

        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_path)

    @classmethod
    def join_audios(cls, audios, output_path):
        from moviepy.editor import concatenate_audioclips, AudioFileClip

        clips = [AudioFileClip(aud) for aud in audios]
        final_clip = concatenate_audioclips(clips)

        i = 1
        while f'final_audio{i}.mp3' in os.listdir(output_path):
            i += 1
        output_path = os.path.join(output_path, f'final_audio{i}.mp3')

        final_clip.write_audiofile(output_path)


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
        wordcloud.recolor(color_func=image_colors)
        i = 1
        while True:
            file = f'wordcloud{i}.png'
            if file not in os.listdir(output_path):
                wordcloud.to_file(os.path.join(output_path, file))
                break
            i += 1
