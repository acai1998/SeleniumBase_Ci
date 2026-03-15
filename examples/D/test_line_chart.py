from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class MyChartMakerClass(BaseCase):
    @pytest.mark.owner('zhouqiang')
    @pytest.mark.priority('P0')
    @pytest.mark.description('验证折线图表的绘制和显示')
    def test_line_chart(self):
        self.create_presentation()
        self.create_line_chart(
            title="Time Outside", subtitle="Last Week", unit="Minutes"
        )
        self.add_data_point("Sun", 5)
        self.add_data_point("Mon", 10)
        self.add_data_point("Tue", 20)
        self.add_data_point("Wed", 40)
        self.add_data_point("Thu", 80)
        self.add_data_point("Fri", 65)
        self.add_data_point("Sat", 50)
        self.add_slide("<p>Line Chart</p>" + self.extract_chart())
        self.begin_presentation(filename="line_chart.html", interval=4)
