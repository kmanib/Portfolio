import logging

class AndroidLog:
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s/ARES_LogBridge: [%(name)s] %(message)s')
    logger = logging.getLogger("Android")

    @classmethod
    def d(cls, tag, msg):
        cls.logger.debug(f"[{tag}] {msg}")
        return 0

    @classmethod
    def i(cls, tag, msg):
        cls.logger.info(f"[{tag}] {msg}")
        return 0

    @classmethod
    def w(cls, tag, msg):
        cls.logger.warning(f"[{tag}] {msg}")
        return 0

    @classmethod
    def e(cls, tag, msg):
        cls.logger.error(f"[{tag}] {msg}")
        return 0
