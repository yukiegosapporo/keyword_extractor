from functions import get_module_path, KeyphraseExtractor
from config import logger, args

if __name__ == "__main__":

    project_path = get_module_path(__file__)

    KE = KeyphraseExtractor(project_path, args.user_cluster, args.top_n)
    KE.get_phrase_list()
    KE.get_phrase_scores()
    KE.get_key_phrases()
