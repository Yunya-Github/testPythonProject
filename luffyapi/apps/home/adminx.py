import xadmin
from . import models

xadmin.site.register(models.Banner)
# The "Login" component has been registered but not used  vue/no-unused-components