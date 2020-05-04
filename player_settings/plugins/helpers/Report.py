import logging
import os
import time
from datetime import datetime

import fpdf
from fpdf import FPDF

logger = logging.getLogger(__name__)


class Report(object):
    """
        PDF report for plots generated on the basis of raw eye-tracking data.
    """

    def __init__(self, file_handler, report_file_name, open_after_download_flag, properties):
        self.file_handler = file_handler
        self.open_after_download = open_after_download_flag
        self.properties = properties
        self.font_path = os.path.join(self.file_handler.fonts_dir, 'DejaVuSans.ttf')  # unicode font
        # self.font_path = "/home/domowy/Pulpit/PUPIL_PLUGIN/pupil/player_settings/plugins/helpers/fonts/DejaVuSans.ttf"  # unicode font
        self.pdf = FPDF(orientation='P', unit='mm', format='A4')
        fpdf.set_global("FPDF_CACHE_MODE", 1)

        # get date & time
        current_date = datetime.now().strftime("%d.%m.%Y  %H:%M")
        current_timestamp = str(time.time()).replace('.', '')

        self.title = properties.report_title
        self.subtitle = properties.report_subtitle
        self.subtitle_date = properties.subtitle_with_date.format(current_date)
        self.subtitle_rec_dir = properties.subtitle_with_rec_dir_path.format(self.file_handler.recording_dir)
        self.subtitle_export_dir = properties.subtitle_with_exported_dir_path.format(self.file_handler.exports_dir)
        self.pdf_file_name = properties.pdf_report_file_name.format(
            current_timestamp) if report_file_name == "" else report_file_name + ".pdf"

        # table with fixation_report.csv data
        self.fixation_detector_table_description = properties.fixation_detector_table_description
        self.parameter_table_header_name = properties.fixation_detector_settings_values_param
        self.value_table_header_name = properties.fixation_detector_settings_values_val

        self.target_file_path = os.path.join(self.file_handler.downloads_dir, self.pdf_file_name)

        self.title_font_size = 25
        self.subtitle_font_size = 20
        self.subsection_title_fontsize = 25
        self.paragraph_fontsize = 14

    def add_first_page(self):
        """
           Creates report first page with:
             title,
             date,
             # recording_directory
             # and exports_directory
        """

        title_line_break_value = 90
        self.pdf.add_page()  # add first report page
        self.pdf.ln(title_line_break_value)
        self.pdf.alias_nb_pages()  # Create the special value {nb}
        self.pdf.set_margins(left=10.00, top=10.00, right=10.00)

        self.pdf.set_font("Courier", 'B', size=self.title_font_size)
        self.pdf.cell(w=190, h=15, txt=self.title, ln=1, align="C")

        self.pdf.set_font("Courier", 'B', size=self.subtitle_font_size)
        self.pdf.cell(w=190, h=10, txt=self.subtitle, ln=1, align="C")

        self.pdf.set_font("Arial", size=10)
        self.pdf.cell(w=190, h=10, txt=self.subtitle_date, ln=1, align="C")

        left = self.pdf.l_margin
        right = self.pdf.r_margin
        top = self.pdf.t_margin
        bottom = self.pdf.b_margin
        # Effective page width and height
        epw = self.pdf.w - left - right
        eph = self.pdf.h - top - bottom
        self.pdf.rect(left, top, w=epw, h=eph)  # draw margins

    def add_subsection(self, title, description):
        self.pdf.add_page()
        self.pdf.set_font("Courier", 'B', size=self.subsection_title_fontsize)
        self.pdf.cell(w=190, h=15, txt=title, ln=1, align="L")
        self.add_unicode_font(14)
        self.pdf.multi_cell(w=190, h=10, txt=self.pdf.normalize_text(description))

    def add_fixation_report(self, fixation_report_obj):
        self.add_unicode_font(14)
        epw = self.pdf.w - 2 * self.pdf.l_margin  # effective page width, or just epw
        col_width = epw / 2  # distribute columns content evenly across table and page

        data = [
            [self.parameter_table_header_name, self.value_table_header_name],
            ["max_dispersion", fixation_report_obj.max_dispersion],
            ["min_duration", fixation_report_obj.min_duration],
            ["max_duration", fixation_report_obj.max_duration],
            ["fixation_count", fixation_report_obj.fixation_count]
        ]

        th = self.pdf.font_size
        self.pdf.multi_cell(w=190, h=8, txt=self.fixation_detector_table_description, align="L")
        for i, row in enumerate(data):
            for datum in row:
                if i == 0:
                    self.pdf.cell(w=col_width, h=(2 * th), txt=self.pdf.normalize_text(str(datum)), border=1, align="C")
                    self.pdf.set_font(family="font", size=10)
                else:
                    self.pdf.cell(col_width, 2 * th, self.pdf.normalize_text(str(datum)), border=1, align="C")
            self.pdf.ln(2 * th)

    def add_plot(self, plot):
        self.pdf.add_page()
        self.pdf.image(u'{}'.format(plot.image_path), w=190)
        self.add_unicode_font(plot.fontsize)
        self.pdf.multi_cell(w=190, h=10, txt=self.pdf.normalize_text(plot.description))

    def save_report(self):
        """
            Saves report in /exports/../downloads directory
        """
        logger.info(f'Save report into {self.target_file_path}')
        self.pdf.output(self.target_file_path)

        logger.info("Report '{}' saved".format(self.pdf_file_name))
        logger.info("Report directory: {}".format(self.file_handler.downloads_dir))

        if self.open_after_download:
            try:
                os.startfile(self.target_file_path)
            except:
                os.system("xdg-open \"%s\"" % self.target_file_path)

    def add_unicode_font(self, fontsize):
        print("FONT PATH:\n\n\n", self.font_path)
        self.pdf.add_font(family="font", fname=self.font_path, uni=True)
        self.pdf.set_font(family="font", size=fontsize)
