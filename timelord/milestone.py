from models import Milestone, session

from optparse import OptionParser


def milestone():
    parser = OptionParser()
    options, args = parser.parse_args()
    mlstn = Milestone(milestone=args[0])
    session.add(mlstn)
    session.commit()

if __name__ == '__main__':
    milestone()
