# Failing repo2docker with Dockerfile

Example repository to demonstrate repo2docker failure for minimal example Dockerfile

**Note:** For reproducibility reasons in [PR #5](https://github.com/matthewfeickert/failing-repo2docker-with-dockerfile/pull/5) the Dockerfile has been made non-minimal to allow for lock file creation with `pip-tools`.

## Crossposted Issues

* [`binder-examples/minimal-dockerfile` Issue #8](https://github.com/binder-examples/minimal-dockerfile/issues/8#issuecomment-1374100001): forked but unchanged repo does not launch on mybinder.org
* [`jupyterhub/repo2docker` Issue #1231](https://github.com/jupyterhub/repo2docker/issues/1231): repo2docker fails to launch into jupyter lab properly from valid minimal Dockerfile

## Minimal Failing Example

The Dockerfile in this repository under `binder/` is a modified version of the example given in the [`binder-examples/minimal-dockerfile` project](https://github.com/binder-examples/minimal-dockerfile/tree/2cd2202f6e6fa8c47c644a38262eb0c093f82d15).
The modifications are minor in that it adopts `python:3.10-slim-bullseye` as the base image and installs all Python packages in a `NB_USER` controlled virtual environment which is automatically activated as its `bin/` directory is on `$PATH`.
The rest of it follows the [Preparing your Dockerfile](https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html#preparing-your-dockerfile) section of the [Use a Dockerfile for your Binder repository](https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html) tutorial website.
The Dockerfile builds successfully when repo2docker is run locally on the repository

```console
# if you don't use pipx just pip install in your local virtual environment
$ pipx install jupyter-repo2docker
$ repo2docker --version
2022.10.0
$ repo2docker .
```

However, when launching the environment from the URL with the token presented the user is brought to a login screen shown below that notes "Token authentication is enabled".

![repo2docker-password-notebook-launch](https://raw.githubusercontent.com/matthewfeickert/failing-repo2docker-with-dockerfile/main/repo2docker-password-notebook-launch.png)

If the user tries to log in with the token in the URL they are not able to.

From the tutorial it seems that `repo2docker` is running the equivalent of

```
docker run -it --rm -p 8888:8888 my-image jupyter notebook --NotebookApp.default_url=/lab/ --ip=0.0.0.0 --port=8888
```

after it builds the image. For simplicity of naming, if we retag the image

```
docker tag <r2d-hash>:latest matthewfeickert/failing-repo2docker-with-dockerfile:latest
```

(or just build the image ourselves

```
docker build -f binder/Dockerfile -t matthewfeickert/failing-repo2docker-with-dockerfile:latest .
```
)

and then run it as `repo2docker` is

```
docker run -it --rm -p 8888:8888 matthewfeickert/failing-repo2docker-with-dockerfile:latest jupyter notebook --NotebookApp.default_url=/lab/ --ip=0.0.0.0 --port=8888
```

we get the same issue.
It seems the problems stems from `--NotebookApp.default_url=/lab/` as if we run without this then we can run the classic Jupyter notebook environment fine

```
docker run -it --rm -p 8888:8888 matthewfeickert/failing-repo2docker-with-dockerfile:latest jupyter notebook --ip=0.0.0.0 --port=8888
```

![classic-jupyter-tree](https://raw.githubusercontent.com/matthewfeickert/failing-repo2docker-with-dockerfile/main/classic-jupyter-tree.png)

and if we run with `jupyter lab` things work fine

```
docker run -it --rm -p 8888:8888 matthewfeickert/failing-repo2docker-with-dockerfile:latest jupyter lab --ip=0.0.0.0 --port=8888
```

![jupyter-lab-launcher](https://raw.githubusercontent.com/matthewfeickert/failing-repo2docker-with-dockerfile/main/jupyter-lab-launcher.png)

I understand [from the tutorial](https://github.com/jupyterhub/mybinder.org-user-guide/blob/262366b9d653ea9c73031a27ec9a928a3c615aa8/doc/tutorials/dockerfile.md?plain=1#L90-L93) that the `--NotebookApp.default_url=/lab/` is required for Binder to act as a safeguard as

> If you install [the classic notebook interface](https://jupyter-notebook.readthedocs.io/en/stable/) but not [JupyterLab](https://jupyterlab.readthedocs.io/), you must manually change your mybinder.org URLs from `/lab` to `/tree` as described [in the user interface documentation](<https://mybinder.readthedocs.io/en/latest/howto/user_interface.html#jupyterlab>).
> Otherwise, you might get a `404: Not Found` error when launching your project on binder.

but it seems there is some interaction problem here for `repo2docker`.
