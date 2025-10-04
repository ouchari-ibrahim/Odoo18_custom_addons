import inspect
import logging

import odoo
from odoo.tools import translate  # ✅ NOT `from odoo.tools.translate import _`

from .models.ir_translation import debrand

_logger = logging.getLogger(__name__)

# ✅ Save the original internal function
_get_translation_original = translate._get_translation

# ✅ Your patched version
def _get_translation(source, module=None):
    source = _get_translation_original(source, module)

    frame = inspect.currentframe().f_back.f_back
    try:
        cr, _ = translate._get_cr(frame, allow_create=False)
    except Exception:
        return source

    try:
        uid = translate._get_uid(frame)
    except Exception:
        return source

    if cr and uid:
        env = odoo.api.Environment(cr, uid, {})
        source = debrand(env, source)

    return source

# ✅ Apply the monkey patch safely
translate._get_translation = _get_translation
