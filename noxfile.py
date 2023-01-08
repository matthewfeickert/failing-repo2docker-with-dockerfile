from pathlib import Path

import nox

# Default sessions to run if no session handles are passed
nox.options.sessions = ["lock"]


DIR = Path(__file__).parent.resolve()


@nox.session()
def lock(session):
    """
    Build a lockfile for the image

    Examples:

        $ nox --session lock
    """

    docker_base_image = "python:3.10-slim-bullseye"
    session.run("docker", "pull", docker_base_image, external=True)
    session.run(
        "docker",
        "run",
        "--rm",
        "-v",
        f"{DIR}:/build",
        "-w",
        "/build",
        docker_base_image,
        "/bin/bash",
        "compile_lock.sh",
        external=True,
    )
    session.run(
        "cp", "_tmp.lock", "requirements.lock", external=True
    )
    session.log("rm _tmp.lock")
    root_controlled_file = DIR / "docker" / "_tmp.lock"
    if root_controlled_file.exists():
        root_controlled_file.unlink()


@nox.session(reuse_venv=True)
def build(session):
    """
    Build image with repo2docker
    """

    session.install("--upgrade", "jupyter-repo2docker==2022.10.0")

    session.run(
        "repo2docker",
        "--image-name",
        "matthewfeickert/failing-repo2docker-with-dockerfile:latest",
        ".",
    )
