"""
Porcha/Khotian PDF Generator - Flask App
ল্যান্ড রেকর্ড (খতিয়ান) ডাইনামিক পিডিএফ জেনারেটর
"""

from flask import Flask, render_template, request, send_file
import pdfkit
import qrcode
import os
import base64
import tempfile
from io import BytesIO

# load environment variables from a `.env` file in development
# note: this requires the python-dotenv package which is listed
# in requirements.txt. In production you may not have a .env file
# and the variables will instead come from the real environment.
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# wkhtmltopdf path can come from an environment variable so the
# application is portable between development and production servers.
# Windows users may still keep a hardcoded default, but the env var
# overrides it. On Linux/Heroku deploys you should install wkhtmltopdf
# system‑wide and set WKHTMLTOPDF_PATH accordingly.
path_wkhtmltopdf = os.environ.get(
    'WKHTMLTOPDF_PATH',
    r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
)

if path_wkhtmltopdf:
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
else:
    config = None  # will be checked later and error raised if missing


@app.route('/')
def index():
    """ইনপুট ফরম পেজ"""
    return render_template('form.html')


def _file_to_data_url(file_storage):
    """আপলোড ফাইলকে base64 data URL এ রূপান্তর (কোনো সংরক্ষণ নেই)"""
    if not file_storage or not file_storage.filename:
        return ''
    raw = file_storage.read()
    ext = (file_storage.filename or '').rsplit('.', 1)[-1].lower()
    mime = 'image/png' if ext == 'png' else 'image/jpeg'
    b64 = base64.b64encode(raw).decode('ascii')
    return f'data:{mime};base64,{b64}'


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """ইউজার ডাটা দিয়ে HTML রেন্ডার করে PDF তৈরি ও ডাউনলোড"""
    seal_file = request.files.get('seal_file')
    sig_file_1 = request.files.get('sig_file_1')
    sig_file_2 = request.files.get('sig_file_2')
    sig_file_3 = request.files.get('sig_file_3')
    sig_file_4 = request.files.get('sig_file_4')
    seal_data_url = _file_to_data_url(seal_file)
    sig_data_url_1 = _file_to_data_url(sig_file_1)
    sig_data_url_2 = _file_to_data_url(sig_file_2)
    sig_data_url_3 = _file_to_data_url(sig_file_3)
    sig_data_url_4 = _file_to_data_url(sig_file_4)

    officer_name_1 = request.form.get('officer_name_1', '') or request.form.get('officer_name', '') or 'মোঃ আজাদ আলী'
    officer_name_2 = request.form.get('officer_name_2', '') or 'বিমল মহন্ত'
    officer_name_3 = request.form.get('officer_name_3', '') or 'মো: ফিরোজ মাহমুদ'
    officer_name_4 = request.form.get('officer_name_4', '') or 'জনস্টি চাকমা'

    # একের অধিক দাগ/প্লট — ফরম ৫৪৬২ কলাম অনুযায়ী
    def _get_land_rows():
        keys = [
            'land_tax', 'dag_plot_no', 'land_class_agri', 'land_class_non_agri',
            'total_acre', 'total_decimal', 'share_in_plot', 'lakh_share', 'part_acre', 'part_decimal', 'land_comments'
        ]
        lists = {k: request.form.getlist(k) for k in keys}
        n = max(len(l) for l in lists.values()) if any(lists.values()) else 0
        if n == 0:
            n = 1
        rows = []
        for i in range(n):
            rows.append({
                'serial': i + 1,
                'share': lists['share_in_plot'][i] if i < len(lists['share_in_plot']) and lists['share_in_plot'][i] else '১',
                'land_tax': lists['land_tax'][i] if i < len(lists['land_tax']) else '',
                'dag_plot_no': lists['dag_plot_no'][i] if i < len(lists['dag_plot_no']) else '',
                'land_class_agri': lists['land_class_agri'][i] if i < len(lists['land_class_agri']) else '',
                'land_class_non_agri': lists['land_class_non_agri'][i] if i < len(lists['land_class_non_agri']) else '',
                'total_acre': lists['total_acre'][i] if i < len(lists['total_acre']) else '',
                'total_decimal': lists['total_decimal'][i] if i < len(lists['total_decimal']) else '',
                'lakh_share': lists['lakh_share'][i] if i < len(lists['lakh_share']) else '',
                'part_acre': lists['part_acre'][i] if i < len(lists['part_acre']) else '',
                'part_decimal': lists['part_decimal'][i] if i < len(lists['part_decimal']) else '',
                'land_comments': lists['land_comments'][i] if i < len(lists['land_comments']) else '',
            })
        return rows

    land_rows = _get_land_rows()

    data = {
        "khotian_no": request.form.get('khotian_no', ''),
        "dist": request.form.get('dist', ''),
        "upazila": request.form.get('upazila', ''),
        "mouza": request.form.get('mouza', ''),
        "jl_no": request.form.get('jl_no', ''),
        "owner_name": request.form.get('owner_name', ''),
        "owner_father": request.form.get('owner_father', ''),
        "post_office": request.form.get('post_office', ''),
        "owner_address": request.form.get('owner_address', ''),
        "dag_no": request.form.get('dag_no', ''),
        "amount": request.form.get('amount', ''),
        "record_date": request.form.get('record_date', ''),
        "application_no": request.form.get('application_no', ''),
        "application_date": request.form.get('application_date', ''),
        "mutation_case_no": request.form.get('mutation_case_no', ''),
        "online_dcr_no": request.form.get('online_dcr_no', ''),
        "doc_title": request.form.get('doc_title', '').strip() or 'খতিয়ান পর্চা',
        "office_name": request.form.get('office_name', ''),
        "land_rows": land_rows,
        "seal_data_url": seal_data_url,
        "sig_data_url_1": sig_data_url_1,
        "sig_data_url_2": sig_data_url_2,
        "sig_data_url_3": sig_data_url_3,
        "sig_data_url_4": sig_data_url_4,
        "sig_date_1": request.form.get('sig_date_1', ''),
        "sig_date_2": request.form.get('sig_date_2', ''),
        "sig_date_3": request.form.get('sig_date_3', ''),
        "sig_date_4": request.form.get('sig_date_4', ''),
        "officer_name_1": officer_name_1,
        "officer_designation_1": request.form.get('officer_designation_1', '') or request.form.get('officer_designation', '') or 'ইউনিয়ন ভূমি উপ-সহকারী কর্মকর্তা',
        "officer_name_2": officer_name_2,
        "officer_designation_2": request.form.get('officer_designation_2', '') or 'অফিস সহকারী',
        "officer_name_3": officer_name_3,
        "officer_designation_3": request.form.get('officer_designation_3', '') or 'সার্ভেয়ার',
        "officer_name_4": officer_name_4,
        "officer_designation_4": request.form.get('officer_designation_4', '') or 'সহকারী কমিশনার (ভূমি)',
        "section_note_text": request.form.get('section_note_text', '') or '১৪০ ও ১১৬/১১৭ ধারামতে নোট বা পরিবর্তন মায় মোকদ্দমা এবং সন।',
        "section_note_share": request.form.get('section_note_share', '') or '১.০০',
        "section_note_part_acre": request.form.get('section_note_part_acre', '') or '০',
        "section_note_part_decimal": request.form.get('section_note_part_decimal', '') or '১০',
    }

    pdf_filename = f"khotian_{data['khotian_no'] or 'unknown'}.pdf"
    options = {
        'encoding': "UTF-8",
        'enable-local-file-access': None,
        'page-size': 'A4',
        'orientation': 'Landscape',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }

    if not config:
        # Fail early if wkhtmltopdf is unavailable; helps in production
        # when the binary isn't installed or the path env var is missing.
        raise RuntimeError(
            "wkhtmltopdf executable not found. "
            "Please install it from https://wkhtmltopdf.org/downloads.html "
            "and set the WKHTMLTOPDF_PATH environment variable appropriately."
        )

    def file_url(path):
        return 'file:///' + path.replace('\\', '/').lstrip('/')

    # QR ও PDF অস্থায়ী ফাইলে — ডাউনলোডের পর কিছু সংরক্ষণ হয় না
    with tempfile.TemporaryDirectory() as tmpdir:
        qr_content = f"Khotian: {data['khotian_no']}, Mouza: {data['mouza']}"
        qr = qrcode.make(qr_content)
        qr_path = os.path.join(tmpdir, 'qr.png')
        qr.save(qr_path)
        data["qr_url"] = file_url(qr_path)

        rendered = render_template('index.html', **data)
        pdf_path = os.path.join(tmpdir, 'out.pdf')
        pdfkit.from_string(rendered, pdf_path, configuration=config, options=options)

        with open(pdf_path, 'rb') as f:
            pdf_bytes = BytesIO(f.read())

    return send_file(pdf_bytes, mimetype='application/pdf', as_attachment=True, download_name=pdf_filename)


# expose the Flask app for WSGI servers (gunicorn, uwsgi, etc.)
# a simple `python app.py` will still work (useful for development), but
# production deployments should rely on a proper WSGI server.
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    debug_mode = os.environ.get('FLASK_DEBUG', '0') in ('1', 'true', 'True')
    app.run(debug=debug_mode, port=port, host='0.0.0.0')
