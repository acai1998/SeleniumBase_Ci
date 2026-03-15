import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class PdfTests(BaseCase):
    @pytest.mark.owner('sunfang')
    @pytest.mark.priority('P1')
    @pytest.mark.description('验证提取 PDF 文本内容的功能')
    def test_get_pdf_text(self):
        self.open("data:,")
        pdf = (
            "https://nostarch.com/download/"
            "Automate_the_Boring_Stuff_sample_ch17.pdf"
        )
        pdf_text = self.get_pdf_text(pdf, page=1)
        print("\n" + pdf_text)
