"""Utility functions to manage the dataset."""
import logging as lg
from pathlib import Path
from zipfile import ZipFile
import gdown

# GDOWN URL
DATASET_DOWNLOAD_URL = 'https://drive.google.com/uc?id=1Ii6X6AYzodwPB_DXL-nF2RT6LerTeyvV'

# Main dataset directory name
DATASET_DIR_NAME = 'dataset'

# The files of dataset
DATASET_FILES = ['tweets.csv', 'users.csv']


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


def download_dataset(force_download=False) -> None:
    path: Path = _create_path_(delete=force_download)

    if _dataset_already_downloaded_() and not force_download:
        # dataset already exist!
        return

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
    # done!
