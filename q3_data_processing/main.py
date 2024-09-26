import xml.etree.ElementTree as ET
import os
import inspect
import re

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def q1_process_xml_and_save():
    # Get the current directory path and set input/output file paths
    infile_path = os.path.join(currentdir, "sample-hyp.xml")
    outfile_path_en = os.path.join(currentdir, "en.txt")
    outfile_path_ha = os.path.join(currentdir, "ha.txt")

    # Open input and output files
    infile = open(infile_path, 'r')
    outfile_en = open(outfile_path_en, 'w')
    outfile_ha = open(outfile_path_ha, 'w')

    # Read the raw XML data and parse it using ElementTree
    raw_xml = infile.read()
    xml_root = ET.fromstring(raw_xml)
    docs = xml_root.findall('doc')

    # Iterate over each document in the XML
    for doc in docs:
        # Find the English and Hausa text elements within each document
        doc_en = doc.find('src[@lang="en"]')
        doc_ha = doc.find('hyp[@language="ha"]')

        # Process and write English text
        for line in doc_en.iter('seg'):
            line_text = line.text
            # Convert all text to lowercase
            line_text = line_text.lower()
            # Remove punctuation
            line_text = re.sub(r'[^\w\s]', '', line_text)
            line_text += '\n'
            outfile_en.write(line_text)

        # Process and write Ha text
        for line in doc_ha.iter('seg'):
            line_text = line.text
            # Convert all text to lowercase
            line_text = line_text.lower()
            # Remove punctuation
            line_text = re.sub(r'[^\w\s]', '', line_text)
            line_text += '\n'
            outfile_ha.write(line_text)

    # Close all file handles
    infile.close()
    outfile_en.close()
    outfile_ha.close()


def q2_create_bpe_vocab():
    infiles = ["en", "ha"]

    for infile in infiles:
        cmd = f'''
            subword-nmt \
            learn-joint-bpe-and-vocab \
            --input {os.path.join(currentdir, infile+".txt")} \
            -s 10000 \
            -o {os.path.join(currentdir, "codes_file.code")} \
            --write-vocabulary {os.path.join(currentdir, "vocab_file_"+infile+".txt")}
        '''
        os.system(cmd)


if __name__ == "__main__":
    q1_process_xml_and_save()
    q2_create_bpe_vocab()