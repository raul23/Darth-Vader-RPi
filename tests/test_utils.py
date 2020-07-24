import logging
import unittest

from logging import NullHandler

from darth_vader_rpi import utils, configs
from pyutils.genutils import get_qualname
from pyutils.testutils import TestBase


logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


class TestUtils(TestBase):
    TEST_MODULE_QUALNAME = get_qualname(utils)
    LOGGER_NAME = __name__
    SHOW_FIRST_CHARS_IN_LOG = 0
    CREATE_SANDBOX_TMP_DIR = True
    CREATE_DATA_TMP_DIR = False

    # @unittest.skip("test_get_cfg_dirpath()")
    def test_add_cfg_filenames(self):
        msg = "Dictionary of config filenames not found"
        self.assertTrue(isinstance(utils._cfg_filenames.default_cfg, dict), msg)
        self.assertTrue(isinstance(utils._cfg_filenames.user_cfg, dict), msg)
        nb_configs = 2
        msg = "There should be {} types of config files".format(nb_configs)
        self.assertTrue(len(utils._cfg_filenames.default_cfg) == nb_configs, msg)
        self.assertTrue(len(utils._cfg_filenames.user_cfg) == nb_configs, msg)
        for k, v in utils._cfg_filenames.default_cfg.items():
            startswith = "default"
            msg = "Config file should start with {}".format(startswith)
            self.assertTrue(k.startswith(startswith), msg)

    # @unittest.skip("test_get_cfg_dirpath()")
    def test_get_cfg_dirpath(self):
        cfg_dirpath = utils.get_cfg_dirpath()
        msg = "The returned directory path to the configuration files is invalid"
        # self.assertRegex(cfg_dirpath, "darth_vader_rpi\/configs$")
        self.assertEqual(cfg_dirpath, configs.__path__[0], msg)
