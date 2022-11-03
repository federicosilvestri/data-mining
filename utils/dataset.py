"""Utility functions to manage the dataset."""
import logging as lg
import typing
from pathlib import Path
from zipfile import ZipFile
import gdown
import pandas as pd

# GDOWN URL
DATASET_DOWNLOAD_URL = 'https://drive.google.com/uc?id=1Ii6X6AYzodwPB_DXL-nF2RT6LerTeyvV'

# Main dataset directory name
DATASET_DIR_NAME = 'dataset'

# The files of dataset
DATASET_FILES = ['tweets.csv', 'users.csv']

# Google Drive shared Drive Name
GOOGLE_DRIVE_SHARED_NAME = 'DM'

GOOGLE_DRIVE_MOUNT_PATH = '/content/gdrive/'


def _rmdir_recursive_(directory: Path) -> None:
    """
    Delete directory recursively.
    Parameters
    ----------
    directory the directory to be deleted

    Returns
    -------
    None
    """
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            _rmdir_recursive_(item)
        else:
            item.unlink()
    directory.rmdir()


def _create_path_(delete=False) -> Path:
    """
    Create the path for dataset. If the path already exists it returns the Path object, unless you specify
    delete parameter to True.
    Parameters
    ----------
    delete True if you want to delete the path and create it again.

    Returns
    -------
    The path object of directory that contains the dataset.
    """
    path: Path = Path(__file__).parent.parent / DATASET_DIR_NAME

    if delete:
        lg.info("Deleting path, as specified in parameter")
        _rmdir_recursive_(path)

    if not path.exists():
        path.mkdir()

    return path


def _dataset_already_downloaded_() -> bool:
    """
    Checks if dataset exists.
    Returns
    -------
    True if dataset already exists, false if not.
    """
    path: Path = _create_path_()
    exist = True

    for file_name in DATASET_FILES:
        exist = exist and path.joinpath(file_name).exists()

    return exist


def _download_dataset_(force_download=False) -> typing.Dict[str, Path]:
    path: Path = _create_path_(delete=force_download)

    if _dataset_already_downloaded_() and not force_download:
        # dataset already exist!
        return _make_dataset_(path)

    download_file_path = Path(path / 'dataset.zip').absolute()

    lg.info("Starting the download of dataset")
    # download the dataset using wget
    gdown.download(
        url=DATASET_DOWNLOAD_URL,
        output=str(download_file_path)
    )

    # unzip it
    lg.info("Unzipping dataset...")
    with ZipFile(download_file_path.absolute(), 'r') as zip_fh:
        zip_fh.extractall(path.absolute())

    # deleting zip file
    download_file_path.unlink()
    lg.info("Dataset unzipped!")
    return _make_dataset_(path)


def _make_dataset_(dataset_path: Path) -> typing.Dict[str, Path]:
    # dataset object
    ds: dict[str, Path] = {}

    for file_name in DATASET_FILES:
        path: Path = dataset_path / file_name
        ds[file_name] = path

    return ds


def _is_colab_running_() -> bool:
    """
    Check if script is running on Google Colab or locally.
    Returns
    -------
    True if script is running on Colab, False if not.
    """
    try:
        from google.colab import drive  # noqa: F401
        return True
    except ImportError:
        return False


def _fetch_from_colab_() -> typing.Dict[str, Path]:
    from google.colab import drive  # noqa: F401

    # mounting the drive
    drive.mount(GOOGLE_DRIVE_MOUNT_PATH)
    # creating main path
    main_path = Path(GOOGLE_DRIVE_MOUNT_PATH + f"Shareddrives/{GOOGLE_DRIVE_SHARED_NAME}/dataset/")

    return _make_dataset_(main_path)


def fetch_dataset_path() -> typing.Dict[str, Path]:
    """
    Fetch dataset. It builds the dictionary of str, Path.
    Returns
    -------
    A dictionary of str, Path where str is the name of dataset and Path is the posix path of file.
    """
    if _is_colab_running_():
        return _fetch_from_colab_()
    else:
        return _download_dataset_()


def fetch_dataset() -> typing.Dict[str, pd.DataFrame]:
    """
    Fetch dataset. It builds the dictionary of str, pd.DataFrame.
    Returns
    -------
    A dictionary of str, pd.DataFrame where str is the name of dataset and pd.DataFrame is the Pandas DataFrame object.
    """
    ds_path: typing.Dict[str, Path] = fetch_dataset_path()
    ds: typing.Dict[str, pd.DataFrame] = {}

    for name, path in ds_path.items():
        lg.info(f"Pandas reading dataset {name}...")
        ds[name] = pd.read_csv(path)

    return ds


def store_preprocessed_dataset(step_name: str, file_name: str, df: pd.DataFrame) -> None:
    """
    Store a preprocessed dataset into a file.
    Parameters
    ----------
    step_name The step of preprocess
    file_name The name of file
    df Dataframe to be saved

    Returns
    -------
    None
    """
    path = Path(__file__).parent.parent.joinpath(DATASET_DIR_NAME).joinpath(step_name)

    if not path.exists():
        path.mkdir(parents=True)
    file_path = path.joinpath(file_name)
    df.to_pickle(file_path)


def fetch_preprocessed_dataset(step_name: str) -> typing.Dict[str, pd.DataFrame]:
    """
    Load all preprocessed datasets of specific step_name
    Parameters
    ----------
    step_name the step name of preprocess

    Returns
    -------
    A dictionary of str and Pandas DataFrame, where str is the name of dataset.
    """
    path = Path(__file__).parent.parent.joinpath(DATASET_DIR_NAME).joinpath(step_name)

    ds: typing.Dict[str, pd.DataFrame] = {}
    if not path.exists():
        raise RuntimeError(f"The processed dataset {step_name} does not exists")
    for element in path.iterdir():
        if element.is_file() and element.suffix == '.pickle':
            df = pd.read_pickle(element)
            ds[element.name] = df
    return ds