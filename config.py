import colorlog
import argparse

logger = colorlog.getLogger()
logger.setLevel(colorlog.colorlog.logging.DEBUG)
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(log_colors={
        "DEBUG":    "cyan",
        "INFO":     "green",
        "WARNING":  "yellow",
        "ERROR":    "red",
        "CRITICAL": "orange",
    }))
logger.addHandler(handler)

parser = argparse.ArgumentParser()
parser.add_argument('--use-cluster', dest="user_cluster", default=True)
parser.add_argument('--top-n',dest="top_n",default=50)
args = parser.parse_args()