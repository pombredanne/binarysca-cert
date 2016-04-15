import logging
from optparse import OptionParser
from . import __version__, BinarySCABirthCert

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    main()

def main():
    parser = OptionParser(description="Generate software birth cert based on software composition analysis",
                          usage="binarysca-cert -o birthcert.json FILE", version=__version__)

    parser.add_option("-o", "--output", help="Output file",
                      default=None, dest="target")
    parser.add_option("-V", "--verbose", help="Be verbose",
                      dest="verbose", action="store_true", default=False)
    parser.add_option("-L", "--log", dest="log",
                      help="Log to file", default=None)
    (options, args) = parser.parse_args()

    if options.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(format=("%(asctime)s:%(name)s:%(levelname)s:%(message)s"),
                        level=level, filename=options.log)

    swcert = BinarySCABirthCert()
    for i in args:
        swcert.analyze_file(i)
    swcert.dump_cert(options.target)

