import os
from urllib.parse import urlparse


def get_woosh_dir(url, whoosh_base_dir):
    """
    Based on the bigbed url and base whoosh directory
    from settings generate the path for whoosh directory for index of this bed file
    """
    path = urlparse(url).path
    filename = path.split('/')[-1]
    whoosh_dir = os.path.join(whoosh_base_dir, filename)
    return whoosh_dir