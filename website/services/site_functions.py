"""
Wanderson soares dos santos - UTF-8 - pt-Br - 26/08/2023
models.py
"""
import os
import numpy as np
from PIL import Image, UnidentifiedImageError


# all classes have a dictionary named 'attributtes', where the key is the name of the functions,
# and receive a list on value, where the first element of list is the name that goes on site,
# and the second value is a boolean that specifies if the element will receive many files
# in the input on the page, the third value represents the extensions accept by the functions.


class DocumentManipulations:
    """
    Class responsible for document manipulation, including conversion between formats,
    merging PDF files, and extracting images from PDFs.
    """
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
        :return str: The name of the converted file.
        """
        if convert_to not in ['word_to_pdf', 'pdf_to_word']:
            raise ValueError("Invalid conversion type. Choose 'word_to_pdf' or 'pdf_to_word'.")

        index_file = 1
        if convert_to == 'word_to_pdf':
            from docx2pdf import convert
            try:
                while f'PDF{index_file}.pdf' in os.listdir(output_path):
                    index_file += 1

                filename = f'PDF{index_file}.pdf'
                output_path = os.path.join(output_path, filename)

                convert(input_path, output_path)

                return filename
            except Exception as e:
                print(f"Error converting Word to PDF: {e}")

        elif convert_to == 'pdf_to_word':
            from pdf2docx import Converter

            index_file = 1
            while f'WORD{index_file}.docx' in os.listdir(output_path):
                index_file += 1

            filename = f'WORD{index_file}.docx'
            output_path = os.path.join(output_path, filename)

            pdf = Converter(input_path)
            pdf.convert(output_path)
            pdf.close()

            return filename

    @classmethod
    def merge_pdf(cls, pdfs, output_path):
        """
        Merge multiple PDF files into a single PDF.

        :param pdfs: List of PDF files to merge.
        :param output_path: Directory where the merged PDF will be saved.
        :return str: The name of the merged file.
        """
        import PyPDF2

        merger = PyPDF2.PdfMerger(strict=False)

        for pdf in pdfs:
            if ".pdf" in pdf:
                merger.append(f'{pdf}')

        index_pdf = 1
        while True:
            files = os.listdir(output_path)
            filename = f'final_pdf{index_pdf}.pdf'
            if filename not in files:
                with open(os.path.join(output_path, filename), 'wb') as output_file:
                    merger.write(output_file)
                    return filename

            index_pdf += 1

    @classmethod
    def extract_img_pdf(cls, input_file, output_path):
        """
        Extracts images from a PDF file and saves them as image files.

        :param input_file: Path of the input file.
        :param output_path: Directory where the zipfile will be saved. Defaults to None.
        :return str: The name of the extracted file.
        """
        from pikepdf import Pdf, PdfImage
        import zipfile

        pdf = Pdf.open(input_file)
        list_images = []

        for page in pdf.pages:
            for name, image in page.images.items():
                save_img = PdfImage(image)
                index_file = 1
                while any(file.startswith(name[1:] + str(index_file)) for file in os.listdir(output_path)):
                    index_file += 1

                name += str(index_file)
                path = str(os.path.join(output_path, name[1:]))
                file = save_img.extract_to(fileprefix=path).replace('\\', '/')
                list_images.append(file.split('/')[-1])

        index_file = 1
        while f'images{index_file}.zip' in os.listdir(output_path):
            index_file += 1

        filename = f'images{index_file}.zip'

        with zipfile.ZipFile(os.path.join(output_path, filename), 'w') as new_zip:
            for image in list_images:
                new_zip.write(os.path.join(output_path, str(image)), os.path.basename(arquivo))

        return filename


class MediaManipulations:
    """
       Class for media manipulations such as background removal from images,
       image format conversion, video-to-audio conversion, and audio merging.
    """
    class_name = 'Manipulação de midias'
    attributes = {
        'remove_background_photo': ['Remova o fundo de uma imagem', False, 'image/*'],
        'convert_to_png': ['Converta uma imagem para png', False, 'image/*'],
        'video_to_audio': ['Converta .mp4 para .mp3', False, '.mp4'],
        'join_audios': ['Junte vários arquivos .mp3 em um só', True, '.mp3'],
    }

    @classmethod
    def remove_background_photo(cls, image, output_path):
        """
        Removes the background from an image and saves the resulting image with a transparent background.

        :param image: Image to remove background from.
        :param output_path: Directory where the image will be saved.
        :return str: The name of the new image.
        """
        try:
            import rembg

            model_folder = 'rembg_models'

            for root, dirs, files in os.walk('.'):
                if model_folder in dirs:
                    os.environ['U2NET_HOME'] = os.path.join(root, model_folder)

            inp = Image.open(image)
            output = rembg.remove(inp)
            i = 1
            while f'image{i}.png' in os.listdir(output_path):
                i += 1

            output_file_path = os.path.join(output_path, f'image{i}.png')
            output.save(output_file_path)

            return f'image{i}.png'
        except UnidentifiedImageError:
            print('Formato de arquivo errado')
        except Exception as e:
            print(f'Erro interno: {e}')

    @classmethod
    def convert_to_png(cls, input_path, output_path):
        """
        Converts an image to PNG format.

        :param input_path: Path to the input image.
        :param output_path: Path to the output image.
        :return str: The name of the converted image.
        """
        index_image = 1
        while f'image{index_image}.png' in os.listdir(output_path):
            index_image += 1

        image_name = f'image{index_image}.png'

        output_path = os.path.join(output_path, image_name)

        with Image.open(input_path) as img:
            img.save(output_path, 'PNG')

        return image_name

    @classmethod
    def video_to_audio(cls, video_path, output_path):
        """
        Extracts audio from a video file and saves it as an MP3 file.

        :param video_path: Path to the video file.
        :param output_path: Directory where the audio will be saved.
        :return str: The name of the converted audio.
        """
        from moviepy.editor import VideoFileClip

        index_audio = 1
        while f'audio{index_audio}.mp3' in os.listdir(output_path):
            index_audio += 1
        audio_name = f'audio{index_audio}.mp3'
        output_path = os.path.join(output_path, audio_name)

        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_path)

        return audio_name

    @classmethod
    def join_audios(cls, audios, output_path):
        """
        Joins multiple MP3 audio files into a single MP3 file.

        :param audios: List of audio files.
        :param output_path: Directory where the audio will be saved.
        :return str: The name of the converted audio.
        """
        from moviepy.editor import concatenate_audioclips, AudioFileClip

        clips = [AudioFileClip(aud) for aud in audios]
        final_clip = concatenate_audioclips(clips)

        index_audio = 1
        while f'final_audio{index_audio}.mp3' in os.listdir(output_path):
            index_audio += 1

        audio_name = f'final_audio{index_audio}.mp3'
        output_path = os.path.join(output_path, audio_name)

        final_clip.write_audiofile(output_path)

        return audio_name


class TextToImage:
    """
    Class for creating images from text, such as generating QR codes and word clouds.
    """
    class_name = 'Criar imagens'
    attributes = {
        'text_to_qrcode': ['Crie seu próprio QR Code', False, ''],
        'wordcloud': ['Crie sua própria nuvem de palavras', False, ''],
    }

    @classmethod
    def text_to_qrcode(cls, text, output_path):
        """
        Generates a QR code from the provided text and saves it as an image.

        :param text: Text to be converted.
        :param output_path: Directory where the image will be saved.
        :return str: The name of the qrcode image.
        """
        import qrcode

        qr = qrcode.QRCode(version=1,  # Nível de correção de erro (1 a 40)
                           box_size=50,  # Tamanho de cada pixel do QR code
                           border=2, )  # Tamanho da margem em torno do QR code
        qr.add_data(text)
        image = qr.make_image(fill_color="black", back_color="white")
        i = 0
        while True:
            file = f'qrcode{i}.png'
            if file not in os.listdir(output_path):
                image.save(os.path.join(output_path, file))
                return file
            i += 1

    @classmethod
    def wordcloud(cls, text, output_path, image=None, color=None):
        """
        Generates a word cloud from the provided text and saves it as an image.

        :param text: Text to be converted into wordcloud.
        :param output_path: Directory where the image will be saved.
        :param image: Image to be used as mask.
        :param color: Color of the word cloud.
        :return str: The name of the word cloud image.
        """
        import matplotlib.pyplot as plt
        from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
        from scipy.ndimage import gaussian_gradient_magnitude

        canvas_width = 1920
        canvas_height = 1080

        if image is None:
            image = os.path.join(os.getcwd(), 'website', 'static', 'img', 'nuvem.png')

        image = np.array(Image.open(image))

        image_mask = image.copy()
        image[image_mask.sum(axis=2) == 0] = 255

        edges = np.mean([gaussian_gradient_magnitude(image[:, :, i] / 255., 2) for i in range(3)], axis=0)
        image_mask[edges > .1] = 255
        wordcloud = WordCloud(width=canvas_width, height=canvas_height, background_color='white', mask=image_mask,
                              mode='RGBA')
        wordcloud.generate(text)
        # editar depois
        if color:
            image_colors = ImageColorGenerator(image)
            wordcloud.recolor(color_func=image_colors)

        index_file = 1
        while True:
            filename = f'wordcloud{index_file}.png'
            if filename not in os.listdir(output_path):
                wordcloud.to_file(os.path.join(output_path, filename))
                return filename

            index_file += 1
