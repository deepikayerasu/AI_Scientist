import os
import fitz


class PDFParser:

    def __init__(self, pdf_path):

        self.pdf_path = pdf_path

        self.document = None

    def open(self):

        if not os.path.exists(self.pdf_path):

            raise FileNotFoundError(
                f"PDF not found:\n{self.pdf_path}"
            )

        self.document = fitz.open(self.pdf_path)

    def close(self):

        if self.document is not None:

            self.document.close()

    def extract(self):

        self.open()

        full_text = ""

        page_data = []

        total_words = 0

        total_characters = 0

        for page_number, page in enumerate(self.document, start=1):

            text = page.get_text("text")

            if text is None:
                text = ""

            words = len(text.split())

            characters = len(text)

            total_words += words

            total_characters += characters

            page_data.append({

                "page_number": page_number,

                "text": text,

                "words": words,

                "characters": characters

            })

            full_text += text + "\n"

        metadata = self.document.metadata

        reading_time = max(
            1,
            round(total_words / 200)
        )

        data = {

            "filename": os.path.basename(
                self.pdf_path
            ),

            "filepath": self.pdf_path,

            "pages": len(self.document),

            "words": total_words,

            "characters": total_characters,

            "reading_time": reading_time,

            "metadata": metadata,

            "page_data": page_data,

            "text": full_text

        }

        self.close()

        return data