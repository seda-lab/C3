import sys
import os
import optparse

"""
Add paths
"""
main = os.path.realpath(__file__).split('/')
rootDir = "/".join(main[:len(main)-3])

def defaultOptions():
    """
    Set default options.
    """
    parser = optparse.OptionParser(usage=
            '%prog [options] <input data folder> <output data folder>'
            '\n  e.g. python3 skillsFromResume.py -d Typedoc pathToResume/ Result/'
            '\n       for more information, type \"python3 skillsFromResume.py\" without --help option'
            )
    parser.add_option('-d', '--docType', default='pdf', action="store", type='choice', choices=['pdf', 'docx'], help='Document Type: pdf or docx')
    parser.add_option('-r', '--recommendation', default= False, action="store_true", help='Job recommendation processing: booleen')
    parser.add_option('-m', '--model', default= False, action="store_true", help='Use pre-trained w2vec model: booleen')
    return parser
