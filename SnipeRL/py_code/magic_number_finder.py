from RLmethods.MAB_models import MultiArmBandit
from tqdm import tqdm
import multiprocessing
from joblib import Parallel, delayed


def return_roi(val):
    return mab.upper_confidence_bound(exploration=val)["roi"]


if __name__ == "__main__":

    num_cores = multiprocessing.cpu_count()
    mab = MultiArmBandit()
    mab.set_filepath("IntradayDatasetPrep/5mins_data/")
    mab.prepare_data()
    data = mab.get_data()
    inputs = tqdm(range(data.shape[0]))
    processed_list = Parallel(n_jobs=num_cores)(delayed(return_roi)(i) for i in inputs)