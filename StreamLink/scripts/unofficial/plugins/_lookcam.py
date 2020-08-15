import logging
import re

from streamlink.plugin import Plugin
from streamlink.plugin.api import useragents
from streamlink.utils import update_scheme
from streamlink.stream._ffmpegmux import FFMPEGMuxer

log = logging.getLogger(__name__)


class lookcam(Plugin):
    #<iframe width="960" height="540" src="https://lookcam.live/player/GQpmGYCbbA/" frameborder="0" scrolling="no" allowfullscreen></iframe>
    #https://lookcam.live/player/GQpmGYCbbA/
    
    _url_re = re.compile(r"https?://lookcam.live/player/")
    _addr_re = re.compile(r'[ ]*source src="([^"]+)"')

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url) is not None

    def _get_streams(self):
        #self.session.set_option('hls-live-edge', 10)
        self.session.http.headers.update({'User-Agent': useragents.CHROME})
        res = self.session.http.get(self.url)
        #log.debug(res.text)
        
        try:
            address = self._addr_re.search(res.text).group(1)
            log.debug("Found address: %s" % address)
        except Exception as e:
            log.debug(str(e))
            return
        
        return {"rtsp_stream": FFMPEGMuxer(self.session, *(address,), is_muxed=False, format='mpegts', vcodec = 'copy', acodec = 'copy' )}

__plugin__ = lookcam
