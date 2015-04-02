from pipeline.storage import PipelineMixin
from whitenoise.django import GzipManifestStaticFilesStorage


class WhitenoisePipelineStorage(PipelineMixin, GzipManifestStaticFilesStorage):
    """
    Extends PipelineMixin so that compression of JS files occur (which are found in
    mysite.settings.base.PIPELINE_JS).

    Extends GzipManifestStaticFilesStorage so that django-whitenoise can cache (md5 hash on filenames) and serve via
    wsgi.
    """
    pass
