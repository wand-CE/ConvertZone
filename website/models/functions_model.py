"""
Wanderson soares dos santos - UTF-8 - pt-Br - 26/08/2023
models.py
"""
import os


class FileManipulations:
    @classmethod
    def remove_background_photo(cls, image):
        """function to remove background"""
        try:
            import rembg
            from PIL import Image, UnidentifiedImageError

            output_path = os.path.splitext(image)[0]

            inp = Image.open(image)
            output = rembg.remove(inp)
            output.save(output_path + '.png')
        except UnidentifiedImageError:
            print('Formato de arquivo errado')
        except:
            print('Erro interno')

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
    def convert_to_png(cls, input_path, output_path=None):
        from PIL import Image
        if output_path is None:
            output_path = os.path.splitext(input_path)[0]

        with Image.open(input_path) as img:
            img.save(f'{output_path}.png', 'PNG')

    @classmethod
    def merge_pdf(cls, pdfs):
        import PyPDF2

        merger = PyPDF2.PdfFileMerger(strict=False)

        for pdf in pdfs:
            if ".pdf" in pdf:
                merger.append(f'{pdf}')

        merger.write('pdf_final.pdf')

    @classmethod
    def extract_img_pdf(cls, pdf):
        from pikepdf import Pdf, PdfImage

        final_pdf = Pdf.open(pdf)
        for page in final_pdf.pages:
            for name, image in page.images.items():
                save_img = PdfImage(image)
                # editar depois para o site
                save_img.extract_to(fileprefix=f'images/{name}')

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

    @classmethod
    def text_to_qrcode(cls, text):
        import qrcode

        qr = qrcode.QRCode(version=1,  # Nível de correção de erro (1 a 40)
                           box_size=50,  # Tamanho de cada pixel do QR code
                           border=2,)  # Tamanho da margem em torno do QR code
        qr.add_data(text)
        image = qr.make_image(fill_color="black", back_color="white")

        image.save("../qrcode.png")

    @classmethod
    def wordcloud(cls, text, image=None):
        import numpy as np
        from PIL import Image, ImageOps
        import matplotlib.pyplot as plt
        from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
        from scipy.ndimage import gaussian_gradient_magnitude

        canvas_width = 1920
        canvas_height = 1080

        if image is not None:
            image = np.array(Image.open(image))

            image_mask = image.copy()
            image[image_mask.sum(axis=2) == 0] = 255

            edges = np.mean([gaussian_gradient_magnitude(
                image[:, :, i] / 255., 2) for i in range(3)], axis=0)
            image_mask[edges > .1] = 255
            wordcloud = WordCloud(background_color='black',
                                  mask=image_mask, mode='RGBA')
            wordcloud.generate(text)
            image_colors = ImageColorGenerator(image)
            wordcloud.recolor(color_func=image_colors)
            plt.figure(figsize=(10, 10))
            plt.imshow(wordcloud, interpolation="bilinear")
            wordcloud.to_file("../color_masked_wordcloud.png")
        else:
            wordcloud = WordCloud(
                width=canvas_width, height=canvas_height, random_state=1).generate(text)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            wordcloud.to_file("simple_wordcloud.png")


# FileManipulations.remove_background_photo('../eu.jpg')
# FileManipulations.word_equal_pdf('../arquivos/curr.doc', 'word_to_pdf')
# FileManipulations.convert_to_png('../eu.jpg')
# FileManipulations.extract_img_pdf('../arquivos/curr.pdf')
# FileManipulations.join_audios('../')
# FileManipulations.text_to_qrcode('Ola mundo')
# with open('../Romeo and Juliet.txt', 'r') as file:
#    text = file.read()
# FileManipulations.new(text, '../romeo.jpg')
# FileManipulations.wordcloud(text, '../romeo.jpg')
