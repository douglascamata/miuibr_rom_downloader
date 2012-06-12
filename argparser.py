import argparse

parser = argparse.ArgumentParser(description='Download MIUI China stock rooms.')
parser.add_argument('--log', type=str, default='',
                   help='a level to the default logger.')
parser.add_argument('--log-db', dest='log_db', default='',
                   help='a level to the database logger')

def parsear_argumentos():
    return parser.parse_args()
