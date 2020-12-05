# Django会自动将名为LOGGER的dict添加到logger.config.dictConfig()中
# 所以我们不需要再让logger生成对象时添加配置文件

import logging
log = logging.getLogger("django")