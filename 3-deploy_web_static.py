#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers,
using the function deploy.
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os.path

env.hosts = ['100.25.19.204', '54.157.159.85']


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        Archive path if generated successfully, None otherwise.
    """
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(date_str)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        True if all operations succeeded, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_file = os.path.basename(archive_path)
        folder_name = archive_file.split(".")[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)

        put(archive_path, "/tmp/{}".format(archive_file))
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_file, release_path))
        run("rm /tmp/{}".format(archive_file))
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to your web servers.

    Returns:
        Return value of do_deploy, or False on failure.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
