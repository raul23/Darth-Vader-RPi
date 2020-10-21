import logging
import os
# import unittest
from logging import NullHandler

from darth_vader_rpi import utils, configs
from pyutils.genutils import get_qualname
from pyutils.testutils import TestBase

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


# TODO: pygame in requirements?
class TestUtils(TestBase):
    TEST_MODULE_QUALNAME = get_qualname(utils)
    LOGGER_NAME = __name__
    SHOW_FIRST_CHARS_IN_LOG = 0
    CREATE_SANDBOX_TMP_DIR = False
    CREATE_DATA_TMP_DIR = False

    # @unittest.skip("test_add_cfg_filenames()")
    def test_add_cfg_filenames(self):
        nb_config_types = 2
        self.log_test_method_name()
        self.log_main_message(extra_msg="Case where dictionaries are checked "
                                        "if they are <color>correctly filled"
                                        "</color>")
        msg = "Dictionary of config filenames not found"
        self.assertTrue(isinstance(utils._CFG_FILENAMES.default_cfg, dict), msg)
        self.assertTrue(isinstance(utils._CFG_FILENAMES.user_cfg, dict), msg)
        msg = "There should be {} types of config files".format(nb_config_types)
        self.assertTrue(
            len(utils._CFG_FILENAMES.default_cfg) == nb_config_types, msg)
        self.assertTrue(
            len(utils._CFG_FILENAMES.user_cfg) == nb_config_types, msg)
        startswith = "default"
        for k, v in utils._CFG_FILENAMES.default_cfg.items():
            msg = "Config file should start with {}".format(startswith)
            self.assertTrue(k.startswith(startswith), msg)
        logger.info("<color>RESULT:</color> The dictionaries of config "
                    "filenames seem to be filled <color>as expected</color>")

    # @unittest.skip("test_get_cfg_dirpath()")
    def test_get_cfg_dirpath(self):
        self.log_test_method_name()
        self.log_main_message(extra_msg="Case where the returned <color>"
                                        "directory path</color> to the "
                                        "<color>config files</color> is checked "
                                        "to be <color>valid</color>")
        cfg_dirpath = utils.get_cfg_dirpath()
        msg = "The returned directory path to the configuration files is invalid"
        # self.assertRegex(cfg_dirpath, "darth_vader_rpi\/configs$")
        self.assertEqual(cfg_dirpath, configs.__path__[0], msg)
        logger.info("<color>RESULT:</color> The directory path to the config "
                    "files is returned <color>as expected</color>")

    # @unittest.skip("test_get_cfg_filepath()")
    def test_get_cfg_filepath(self):
        self.log_test_method_name()
        self.log_main_message(extra_msg="Case where <color>config file types"
                                        "</color> return valid <color>file paths"
                                        "</color>")
        # TODO: test user log and main
        file_types = ['default_log', 'default_main']
        for ft in file_types:
            try:
                fp = utils.get_cfg_filepath(ft)
            except AssertionError as e:
                logger.exception("<color>{}</color>".format(e))
                msg = "Config file type not recognized: {}".format(ft)
                self.fail(msg)
            else:
                msg = "Returned path is invalid: {}".format(fp)
                self.assertTrue(os.path.isfile(fp), msg)
                self.assertIn(ft, fp)
        logger.info("<color>RESULT:</color> All config file types return "
                    "valid file paths <color>as expected</color>")
