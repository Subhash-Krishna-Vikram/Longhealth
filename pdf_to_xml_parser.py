# pdfx usage: http://pdfx.cs.man.ac.uk/usage
# requests docs: http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file
import requests
import pdfx
from io import BytesIO,StringIO
from pdfminer.converter import TextConverter, XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
# get it from http://python-requests.org or do 'pip install requests'

url = "http://pdfx.cs.man.ac.uk"

def get_xml_py2(file_path, output_string):
    in_fp = BytesIO()
    with open(file_path, 'rb') as x:
        in_fp.write(x.read())

    laparams = LAParams(all_texts=True)
    rsrcmgr = PDFResourceManager()
    outfp = StringIO()
    device = XMLConverter(rsrcmgr, outfp, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(in_fp):
        interpreter.process_page(page)
        yield outfp.getvalue()
        device.close()
        outfp.close()

    in_fp.close()
    return outfp

def pypdfx(file_name):
    """
    Filename is a name of a pdf file WITHOUT the extension
    The function will print messages, including the status code,
    and will write the XML file to <filename>.xml
    """
    fin = open(file_name + '.pdf', 'rb')
    files = {'file': fin}
    try:
        print('Sending', file_name, 'to', url)
        r = requests.post(url, files=files, headers={'Content-Type': 'application/pdf'})
        print('Got status code', r.status_code)
    finally:
        fin.close()
    fout = open(file_name + '.xml', 'w')
    fout.write(r.content)
    fout.close()
    print('Written to', file_name + '.xml')


if __name__ == '__main__':
    # self promotion - get the pdf file here: http://onlinelibrary.wiley.com/doi/10.1111/j.1558-5646.2012.01576.x
    # /abstract
    # filename = 'Referral_Form'
    # output_string = StringIO()
    # # pypdfx(filename)
    # output_string = get_xml_py2('Referral_Form.pdf', output_string)
    # print(output_string.getvalue())
    pdf = pdfx.PDFx("Referral_Form.pdf")
    print(pdf.get_text())
