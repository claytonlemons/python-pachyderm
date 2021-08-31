import io
import itertools
import tarfile
from contextlib import contextmanager
from typing import Iterator, Union, List, BinaryIO

from python_pachyderm.pfs import commit_from, Commit, uuid_re
from python_pachyderm.proto.v2 import pfs
from python_pachyderm.service import pfs_proto, Service
from google.protobuf import empty_pb2, wrappers_pb2


BUFFER_SIZE = 19 * 1024 * 1024


class FileTarstream:
    """Implements a file-like interface over a GRPC byte stream,
    so we can use tarfile to decode the file contents.
    """

    def __init__(self, res):
        self.res = res
        self.buf = []

    def __next__(self):
        return next(self.res).value

    def close(self):
        self.res.cancel()

    def read(self, size=-1):
        if self.res.cancelled():
            return b""

        buf = []
        remaining = size if size >= 0 else 2 ** 32

        if self.buf:
            buf.append(self.buf[:remaining])
            self.buf = self.buf[remaining:]
            remaining -= len(buf[-1])

        try:
            while remaining > 0:
                b = next(self)

                if len(b) > remaining:
                    buf.append(b[:remaining])
                    self.buf = b[remaining:]
                else:
                    buf.append(b)

                remaining -= len(buf[-1])
        except StopIteration:
            pass

        return b"".join(buf)


class PFSFile:
    """The contents of a file stored in PFS. You can treat these as
    file-like objects, like so:

    ```
    source_file = client.get_file("montage/master", "/montage.png")
    with open("montage.png", "wb") as dest_file:
        shutil.copyfileobj(source_file, dest_file)
    ```
    """

    def __init__(self, stream, is_tar=False):
        if is_tar:
            # Pachyderm's GetFileTar API returns its result (which may include
            # several files, e.g. when getting a directory) as a tar
            # stream--untar the response byte stream as we receive it from
            # GetFileTar.
            # TODO how to handle multiple files in the tar stream?
            f = tarfile.open(fileobj=stream, mode="r|*")
            self._file = f.extractfile(f.next())
        else:
            self._file = stream

    def __enter__(self):
        return self

    def __exit__(self, type, val, tb):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        x = self.read()
        if not x:
            raise StopIteration
        return x

    def read(self, size: int = -1) -> bytes:
        """Reads from the ``PFSFile`` buffer.

        Parameters
        ----------
        size : int, optional
            If set, the number of bytes to read from the buffer.

        Returns
        -------
        bytes
            Content from the stream.
        """
        return self._file.read(size)

    def close(self) -> None:
        """Closes the ``PFSFile``."""
        self._file.close()


class PFSMixin:
    """A mixin with pfs-related functionality."""

    def create_repo(
        self, repo_name: str, description: str = None, update: bool = False
    ) -> None:
        """Creates a new repo object in PFS with the given name. Repos are the
        top level data object in PFS and should be used to store data of a
        similar type. For example rather than having a single repo for an
        entire project you might have separate repos for logs, metrics,
        database dumps etc.

        Parameters
        ----------
        repo_name : str
            Name of the repo.
        description : str, optional
            Description of the repo.
        update : bool, optional
            Whether to update if the repo already exists.
        """
        self._req(
            Service.PFS,
            "CreateRepo",
            repo=pfs_proto.Repo(name=repo_name, type="user"),
            description=description,
            update=update,
        )

    def inspect_repo(self, repo_name: str) -> pfs_proto.RepoInfo:
        """Inspects a repo.

        Parameters
        ----------
        repo_name : str
            Name of the repo.

        Returns
        -------
        pfs_proto.RepoInfo
            A protobuf object with info on the repo.
        """
        return self._req(
            Service.PFS, "InspectRepo", repo=pfs_proto.Repo(name=repo_name, type="user")
        )

    def list_repo(self, type: str = "user") -> Iterator[pfs_proto.RepoInfo]:
        """Lists all repos in PFS.

        Parameters
        ----------
        type : str, optional
            The type of repos that should be returned ("user", "meta", "spec").
            If unset, returns all types of repos.

        Returns
        -------
        Iterator[pfs_proto.RepoInfo]
            An iterator of protobuf objects that contain info on a repo.
        """
        return self._req(Service.PFS, "ListRepo", type=type)

    def delete_repo(self, repo_name: str, force: bool = False) -> None:
        """Deletes a repo and reclaims the storage space it was using.

        Parameters
        ----------
        repo_name : str
            The name of the repo.
        force : bool, optional
            If set to true, the repo will be removed regardless of errors.
            Use with care.
        """
        self._req(
            Service.PFS,
            "DeleteRepo",
            repo=pfs_proto.Repo(name=repo_name, type="user"),
            force=force,
        )

    def delete_all_repos(self) -> None:
        """Deletes all repos."""
        self._req(Service.PFS, "DeleteAll", req=empty_pb2.Empty())

    def start_commit(
        self,
        repo_name: str,
        branch: str,
        parent: Union[str, tuple, dict, Commit, pfs_proto.Commit] = None,
        description: str = None,
    ) -> pfs_proto.Commit:
        """Begins the process of committing data to a repo. Once started you
        can write to the commit with ModifyFile. When all the data has been
        written, you must finish the commit with FinishCommit. NOTE: data is
        not persisted until FinishCommit is called.

        Parameters
        ----------
        repo_name : str
            The name of the repo.
        branch_name : str
            A string specifying the branch.
        parent : Union[str, tuple, dict, Commit, pfs_proto.Commit], optional
            A commit specifying the parent of the newly created commit. Upon
            creation, before data is modified, the new commit will appear
            identical to the parent.
        description : str, optional
            A description of the commit.

        Returns
        -------
        pfs_proto.Commit
            A protobuf object that represents an open subcommit (commit at the
            repo-level).
        """
        if parent and isinstance(parent, str):
            parent = pfs_proto.Commit(
                id=parent,
                branch=pfs_proto.Branch(
                    repo=pfs_proto.Repo(name=repo_name, type="user"), name=None
                ),
            )
        return self._req(
            Service.PFS,
            "StartCommit",
            parent=commit_from(parent),
            branch=pfs_proto.Branch(
                repo=pfs_proto.Repo(name=repo_name, type="user"), name=branch
            ),
            description=description,
        )

    def finish_commit(
        self,
        commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        description: str = None,
        error: str = None,
        force: bool = False,
    ) -> None:
        """Ends the process of committing data to a repo and persists the
        commit. Once a commit is finished the data becomes immutable and
        future attempts to write to it with ModifyFile will error.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The subcommit (commit at the repo-level) object to close.
        description : str, optional
            A description of the commit. It will overwrite the description set
            in ``start_commit()``.
        error : str, optional
            If set, a message that errors out the commit. Don't use unless you
            want the finish commit request to fail.
        force : bool, optional
            If true, forces commit to finish, even if it breaks provenance.
        """
        self._req(
            Service.PFS,
            "FinishCommit",
            commit=commit_from(commit),
            description=description,
            error=error,
            force=force,
        )

    @contextmanager
    def commit(
        self,
        repo_name: str,
        branch: str,
        parent: Union[str, tuple, dict, Commit, pfs_proto.Commit] = None,
        description: str = None,
    ) -> Iterator[pfs_proto.Commit]:
        """A context manager for running operations within a commit.

        Parameters
        ----------
        repo_name : str
            The name of the repo.
        branch_name : str
            A string specifying the branch.
        parent : Union[str, tuple, dict, Commit, pfs_proto.Commit], optional
            A commit specifying the parent of the newly created commit. Upon
            creation, before data is modified, the new commit will appear
            identical to the parent.
        description : str, optional
            A description of the commit.

        Yields
        -------
        pfs_proto.Commit
            A protobuf object that represents a commit.
        """
        commit = self.start_commit(repo_name, branch, parent, description)
        try:
            yield commit
        finally:
            self.finish_commit(commit)

    def inspect_commit(
        self,
        commit: Union[str, tuple, dict, Commit, pfs_proto.Commit],
        commit_state: pfs_proto.CommitState = pfs_proto.CommitState.STARTED,
    ) -> Iterator[pfs_proto.CommitInfo]:
        """Inspects a commit.

        Parameters
        ----------
        commit : Union[str, tuple, dict, Commit, pfs_proto.Commit]
            The commit to inspect. Can either be a commit ID or a commit object
            that represents a subcommit (commit at the repo-level).
        commit_state : pfs_proto.CommitState, optional
            An enum that causes the method to block until the commit is in the
            specified state: {`pfs_proto.CommitState.STARTED`,
            `pfs_proto.CommitState.READY`, `pfs_proto.CommitState.FINISHING`,
            `pfs_proto.CommitState.FINISHED`}.

        Returns
        -------
        Iterator[pfs_proto.CommitInfo]
            An iterator of protobuf objects that contain info on a subcommit
            (commit at the repo-level).
        """
        if not isinstance(commit, str):
            return iter(
                [
                    self._req(
                        Service.PFS,
                        "InspectCommit",
                        commit=commit_from(commit),
                        wait=commit_state,
                    )
                ]
            )
        elif uuid_re.match(commit):
            return self._req(
                Service.PFS,
                "InspectCommitSet",
                commit_set=pfs_proto.CommitSet(id=commit),
                wait=commit_state == pfs_proto.CommitState.FINISHED,
            )
        raise ValueError(
            "bad argument: commit should either be a commit ID (str) or a commit-like object"
        )

    def list_commit(
        self,
        repo_name: str = None,
        to_commit: Union[tuple, dict, Commit, pfs_proto.Commit] = None,
        from_commit: Union[tuple, dict, Commit, pfs_proto.Commit] = None,
        number: int = None,
        reverse: bool = False,
        all: bool = False,
        origin_kind: pfs_proto.OriginKind = pfs_proto.OriginKind.USER,
    ) -> Union[Iterator[pfs_proto.CommitInfo], Iterator[pfs_proto.CommitSetInfo]]:
        """Lists commits.

        Parameters
        ----------
        repo_name : str, optional
            The name of a repo. If set, returns subcommits (commit at
            repo-level) only in this repo.
        to_commit : Union[tuple, dict, Commit, pfs_proto.Commit], optional
            A subcommit (commit at repo-level) that only impacts results if
            `repo_name` is specified. If set, only the ancestors of
            `to_commit`, including `to_commit`, are returned.
        from_commit : Union[tuple, dict, Commit, pfs_proto.Commit], optional
            A subcommit (commit at repo-level) that only impacts results if
            `repo_name` is specified. If set, only the descendants of
            `from_commit`, including `from_commit`, are returned.
        number : int, optional
            The number of subcommits to return. If unset, all subcommits that
            matched the aforementioned criteria are returned. Only impacts
            results if `repo_name` is specified.
        reverse : bool, optional
            If true, returns the subcommits oldest to newest. Only impacts
            results if `repo_name` is specified.
        all : bool, optional
            If true, returns all types of subcommits. Otherwise, alias
            subcommits are excluded. Only impacts results if `repo_name` is
            specified.
        origin_kind : pfs_proto.OriginKind, optional
            An enum that specifies how a subcommit originated. Returns only
            subcommits of this enum type: {`pfs_proto.OriginKind.USER`,
            `pfs_proto.OriginKind.AUTO`, `pfs_proto.OriginKind.FSCK`,
            `pfs_proto.OriginKind.ALIAS`}. Only impacts results if `repo_name`
            is specified.

        Returns
        -------
        Union[Iterator[pfs_proto.CommitInfo], Iterator[pfs_proto.CommitSetInfo]]
            An iterator of protobuf objects that either contain info on a
            subcommit (commit at the repo-level), if `repo_name` was specified,
            or a commit, if `repo_name` wasn't specified.
        """
        if repo_name is not None:
            req = pfs_proto.ListCommitRequest(
                repo=pfs_proto.Repo(name=repo_name, type="user"),
                number=number,
                reverse=reverse,
                all=all,
                origin_kind=origin_kind,
            )
            if to_commit is not None:
                req.to.CopyFrom(commit_from(to_commit))
            if from_commit is not None:
                getattr(req, "from").CopyFrom(commit_from(from_commit))
            return self._req(Service.PFS, "ListCommit", req=req)
        else:
            return self._req(Service.PFS, "ListCommitSet")

    def squash_commit(self, commit_id: str) -> None:
        """Squashes a commit into its parent.

        Parameters
        ----------
        commit_id : str
            The ID of the commit.
        """
        self._req(
            Service.PFS,
            "SquashCommitSet",
            commit_set=pfs_proto.CommitSet(id=commit_id),
        )

    def drop_commit(self, commit_id: str) -> None:
        """
        Drops an entire commit.

        Parameters
        ----------
        commit_id : str
            The ID of the commit.
        """
        self._req(
            Service.PFS,
            "DropCommitSet",
            commit_set=pfs_proto.CommitSet(id=commit_id),
        )

    def wait_commit(
        self, commit: Union[str, tuple, dict, Commit, pfs_proto.Commit]
    ) -> List[pfs_proto.CommitInfo]:
        """Waits for the specified commit to finish.

        Parameters
        ----------
        commit : Union[str, tuple, dict, Commit, pfs_proto.Commit]
            A commit object to wait on. Can either be an entire commit or a
            subcommit (commit at the repo-level).

        Returns
        -------
        List[pfs_proto.CommitInfo]
            A list of protobuf objects that contain info on subcommits (commit
            at the repo-level). These are the individual subcommits this
            function waited on.
        """
        return list(self.inspect_commit(commit, pfs_proto.CommitState.FINISHED))

    def subscribe_commit(
        self,
        repo_name: str,
        branch: str,
        from_commit: Union[str, tuple, dict, Commit, pfs_proto.Commit] = None,
        state: pfs_proto.CommitState = pfs_proto.CommitState.STARTED,
        all: bool = False,
        origin_kind: pfs_proto.OriginKind = pfs_proto.OriginKind.USER,
    ) -> Iterator[pfs_proto.CommitInfo]:
        """Returns all commits on the branch and then listens for new commits
        that are created.

        Parameters
        ----------
        repo_name : str
            The name of the repo.
        branch : str
            The name of the branch.
        from_commit : Union[str, tuple, dict, Commit, pfs_proto.Commit], optional  # noqa: W505
            Return commits only from this commit and onwards. Can either be an
            entire commit or a subcommit (commit at the repo-level).
        state : pfs_proto.CommitState, optional
            Return commits only when they're at least in the specifed enum
            state: {`pfs_proto.CommitState.STARTED`,
            `pfs_proto.CommitState.READY`, `pfs_proto.CommitState.FINISHING`,
            `pfs_proto.CommitState.FINISHED`}.
        all : bool, optional
            If true, returns all types of commits. Otherwise, alias commits are
            excluded.
        origin_kind : pfs_proto.OriginKind, optional
            An enum that specifies how a commit originated. Returns only
            commits of this enum type: {`pfs_proto.OriginKind.USER`,
            `pfs_proto.OriginKind.AUTO`, `pfs_proto.OriginKind.FSCK`,
            `pfs_proto.OriginKind.ALIAS`}.

        Returns
        -------
        Iterator[pfs_proto.CommitInfo]
            An iterator of protobuf objects that contain info on subcommits
            (commits at the repo-level). Use ``next()`` to iterate through as
            the returned stream is potentially endless. Might block your code
            otherwise.
        """
        repo = pfs_proto.Repo(name=repo_name, type="user")
        req = pfs_proto.SubscribeCommitRequest(
            repo=repo,
            branch=branch,
            state=state,
            all=all,
            origin_kind=origin_kind,
        )
        if from_commit is not None:
            if isinstance(from_commit, str):
                getattr(req, "from").CopyFrom(
                    pfs_proto.Commit(repo=repo, id=from_commit)
                )
            else:
                getattr(req, "from").CopyFrom(commit_from(from_commit))
        return self._req(Service.PFS, "SubscribeCommit", req=req)

    def create_branch(
        self,
        repo_name: str,
        branch_name: str,
        head_commit: Union[tuple, dict, Commit, pfs_proto.Commit] = None,
        provenance: List[pfs_proto.Branch] = None,
        trigger: pfs_proto.Trigger = None,
        new_commit: bool = False,
    ) -> None:
        """Creates a new branch.

        Parameters
        ----------
        repo_name : str
            The name of the repo.
        branch_name : str
            The name of the new branch.
        head_commit : Union[tuple, dict, Commit, pfs_proto.Commit], optional
            A subcommit (commit at repo-level) indicating the head of the
            new branch.
        provenance : List[pfs_proto.Branch], optional
            A list of branches to establish provenance with this newly created
            branch.
        trigger : pfs_proto.Trigger, optional
            Sets the conditions under which the head of this branch moves.
        new_commit : bool, optional
            If true and `head_commit` is specified, uses a different commit ID
            for head than `head_commit`.
        """
        self._req(
            Service.PFS,
            "CreateBranch",
            branch=pfs_proto.Branch(
                repo=pfs_proto.Repo(name=repo_name, type="user"), name=branch_name
            ),
            head=commit_from(head_commit),
            provenance=provenance,
            trigger=trigger,
            new_commit_set=new_commit,
        )

    def inspect_branch(self, repo_name: str, branch_name: str) -> pfs_proto.BranchInfo:
        """Inspects a branch.

        Parameters
        ----------
        repo_name : str
            The name of the repo.
        branch_name : str
            The name of the branch.

        Returns
        -------
        pfs_proto.BranchInfo
            A protobuf object with info on a branch.
        """
        return self._req(
            Service.PFS,
            "InspectBranch",
            branch=pfs_proto.Branch(
                repo=pfs_proto.Repo(name=repo_name, type="user"), name=branch_name
            ),
        )

    def list_branch(
        self, repo_name: str, reverse: bool = False
    ) -> Iterator[pfs_proto.BranchInfo]:
        """Lists the active branch objects in a repo.

        Parameters
        ----------
        repo_name : str
            The name of the repo.
        reverse : bool, optional
            If true, returns branches oldest to newest.

        Returns
        -------
        Iterator[pfs_proto.BranchInfo]
            An iterator of protobuf objects that contain info on a branch.
        """
        return self._req(
            Service.PFS,
            "ListBranch",
            repo=pfs_proto.Repo(name=repo_name, type="user"),
            reverse=reverse,
        )

    def delete_branch(
        self, repo_name: str, branch_name: str, force: bool = False
    ) -> None:
        """Deletes a branch, but leaves the commits themselves intact. In other
        words, those commits can still be accessed via commit IDs and other
        branches they happen to be on.

        Parameters
        ----------
        repo_name : str
            The name of the repo.
        branch_name : str
            The name of the branch.
        force : bool, optional
            If true, forces the branch deletion.
        """
        self._req(
            Service.PFS,
            "DeleteBranch",
            branch=pfs_proto.Branch(
                repo=pfs_proto.Repo(name=repo_name, type="user"), name=branch_name
            ),
            force=force,
        )

    @contextmanager
    def modify_file_client(
        self, commit: Union[tuple, dict, Commit, pfs_proto.Commit]
    ) -> Iterator["ModifyFileClient"]:
        """A context manager that gives a `ModifyFileClient`. When the context
        manager exits, any operations enqueued from the `ModifyFileClient` are
        executed in a single, atomic `ModifyFile` call.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            An open subcommit (commit at the repo-level) to modify.

        Yields
        -------
        ModifyFileClient
            An object that can queue operations to modify a commit atomically.
        """
        pfc = ModifyFileClient(commit)
        yield pfc
        self._req(Service.PFS, "ModifyFile", req=pfc._reqs())

    def put_file_bytes(
        self,
        commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        path: str,
        value: Union[bytes, BinaryIO],
        datum: str = None,
        append: bool = False,
    ) -> None:
        """Uploads a PFS file from a file-like object, bytestring, or iterator
        of bytestrings.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            An open subcommit (commit at the repo-level) to modify.
        path : str
            The path in the repo the file(s) will be written to.
        value : Union[bytes, BinaryIO]
            The file contents as bytes, represented as a file-like object,
            bytestring, or iterator of bystrings.
        datum : str, optional
            A tag for the added file(s).
        append : bool, optional
            If true, appends the data to the file(s) specified at `path`, if
            they already exist. Otherwise, overwrites them.
        """
        with self.modify_file_client(commit) as pfc:
            if hasattr(value, "read"):
                pfc.put_file_from_fileobj(
                    path,
                    value,
                    datum=datum,
                    append=append,
                )
            else:
                pfc.put_file_from_bytes(
                    path,
                    value,
                    datum=datum,
                    append=append,
                )

    def put_file_url(
        self,
        commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        path: str,
        url: str,
        recursive: bool = False,
        datum: str = None,
        append: bool = False,
    ) -> None:
        """Puts a file using the content found at a URL. The URL is sent to the
        server which performs the request.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            An open subcommit (commit at the repo-level) to modify.
        path : str
            The path in the repo the file(s) will be written to.
        url : str
            The URL of the file to put.
        recursive : bool, optional
            If true, allows for recursive scraping on some types URLs, for
            example on s3:// URLs
        datum : str, optional
            A tag for the added file(s).
        append : bool, optional
            If true, appends the data to the file(s) specified at `path`, if
            they already exist. Otherwise, overwrites them.
        """
        with self.modify_file_client(commit) as pfc:
            pfc.put_file_from_url(
                path,
                url,
                recursive=recursive,
                datum=datum,
                append=append,
            )

    def copy_file(
        self,
        source_commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        source_path: str,
        dest_commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        dest_path: str,
        datum: str = None,
        append: bool = False,
    ) -> None:
        """Efficiently copies files already in PFS. Note that the destination
        repo cannot be an output repo, or the copy operation will silently fail.

        Parameters
        ----------
        source_commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The subcommit (commit at the repo-level) which holds the source
            file.
        source_path : str
            The path of the source file.
        dest_commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The open subcommit (commit at the repo-level) to which to add the
            file.
        dest_path : str
            The path of the destination file.
        datum : str, optional
            A tag for the added file.
        append : bool, optional
            If true, appends the content of `source_path` to the file at
            `dest_path`, if it already exists. Otherwise, overwrites the file.
        """
        with self.modify_file_client(dest_commit) as pfc:
            pfc.copy_file(
                source_commit, source_path, dest_path, datum=datum, append=append
            )

    def get_file(
        self,
        commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        path: str,
        datum: str = None,
        URL: str = None,
        offset: int = 0,
    ) -> PFSFile:
        """Gets a file from PFS.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The subcommit (commit at the repo-level) to get the file from.
        path : str
            The path of the file.
        datum : str, optional
            A tag that filters the files.
        URL : str, optional
            Specifies an object storage URL that the file will be uploaded to.
        offset : int, optional
            Allows file read to begin at `offset` number of bytes.

        Returns
        -------
        PFSFile
            The contents of the file in a file-like object.
        """
        res = self._req(
            Service.PFS,
            "GetFile",
            file=pfs_proto.File(commit=commit_from(commit), path=path, datum=datum),
            URL=URL,
            offset=offset,
        )
        return PFSFile(io.BytesIO(next(res).value))

    def get_file_tar(
        self,
        commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        path: str,
        datum: str = None,
        URL: str = None,
        offset: int = 0,
    ) -> PFSFile:
        """Gets a file from PFS.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The subcommit (commit at the repo-level) to get the file from.
        path : str
            The path of the file.
        datum : str, optional
            A tag that filters the files.
        URL : str, optional
            Specifies an object storage URL that the file will be uploaded to.
        offset : int, optional
            Allows file read to begin at `offset` number of bytes.

        Returns
        -------
        PFSFile
            The contents of the file in a file-like object.
        """
        res = self._req(
            Service.PFS,
            "GetFileTAR",
            req=pfs_proto.GetFileRequest(
                file=pfs_proto.File(commit=commit_from(commit), path=path, datum=datum),
                URL=URL,
                offset=offset,
            ),
        )
        return PFSFile(io.BytesIO(next(res).value), is_tar=True)

    def inspect_file(
        self,
        commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        path: str,
        datum: str = None,
    ) -> pfs_proto.FileInfo:
        """Inspects a file.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The subcommit (commit at the repo-level) to inspect the file from.
        path : str
            The path of the file.
        datum : str, optional
            A tag that filters the files.

        Returns
        -------
        pfs_proto.FileInfo
            A protobuf object that contains info on a file.
        """
        return self._req(
            Service.PFS,
            "InspectFile",
            file=pfs_proto.File(commit=commit_from(commit), path=path, datum=datum),
        )

    def list_file(
        self,
        commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        path: str,
        datum: str = None,
        details: bool = False,
    ) -> Iterator[pfs_proto.FileInfo]:
        """Lists the files in a directory.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The subcommit (commit at the repo-level) to list files from.
        path : str
            The path to the directory.
        datum : str, optional
            A tag that filters the files.
        details : bool, optional
            Unused.

        Returns
        -------
        Iterator[pfs_proto.FileInfo]
            An iterator of protobuf objects that contain info on files.
        """
        return self._req(
            Service.PFS,
            "ListFile",
            file=pfs_proto.File(commit=commit_from(commit), path=path, datum=datum),
        )

    def walk_file(
        self,
        commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        path: str,
        datum: str = None,
    ) -> Iterator[pfs_proto.FileInfo]:
        """Walks over all descendant files in a directory.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The subcommit (commit at the repo-level) to walk files in.
        path : str
            The path to the directory.
        datum : str, optional
            A tag that filters the files.

        Returns
        -------
        Iterator[pfs_proto.FileInfo]
            An iterator of protobuf objects that contain info on files.
        """
        return self._req(
            Service.PFS,
            "WalkFile",
            file=pfs_proto.File(commit=commit_from(commit), path=path, datum=datum),
        )

    def glob_file(
        self, commit: Union[tuple, dict, Commit, pfs_proto.Commit], pattern: str
    ) -> Iterator[pfs_proto.FileInfo]:
        """Lists files that match a glob pattern.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The subcommit (commit at the repo-level) to query against.
        pattern : str
            A glob pattern.

        Returns
        -------
        Iterator[pfs_proto.FileInfo]
            An iterator of protobuf objects that contain info on files.
        """
        return self._req(
            Service.PFS, "GlobFile", commit=commit_from(commit), pattern=pattern
        )

    def delete_file(
        self, commit: Union[tuple, dict, Commit, pfs_proto.Commit], path: str
    ) -> None:
        """Deletes a file from an open commit. This leaves a tombstone in the
        commit, assuming the file isn't written to later while the commit is
        still open. Attempting to get the file from the finished commit will
        result in a not found error. The file will of course remain intact in
        the commit's parent.

        Parameters
        ----------
        commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The open subcommit (commit at the repo-level) to delete a file
            from.
        path : str
            The path to the file.
        """
        with self.modify_file_client(commit) as pfc:
            pfc.delete_file(path)

    def fsck(self, fix: bool = False) -> Iterator[pfs_proto.FsckResponse]:
        """Performs a file system consistency check on PFS, ensuring the
        correct provenance relationships are satisfied.

        Parameters
        ----------
        fix : bool, optional
            If true, attempts to fix as many problems as possible.

        Returns
        -------
        Iterator[pfs_proto.FsckResponse]
            An iterator of protobuf objects that contain info on either what
            error was encountered (and was unable to be fixed, if `fix` is set
            to ``True``) or a fix message (if `fix` is set to ``True``).
        """
        return self._req(Service.PFS, "Fsck", fix=fix)

    def diff_file(
        self,
        new_commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        new_path: str,
        old_commit: Union[tuple, dict, Commit, pfs_proto.Commit] = None,
        old_path: str = None,
        shallow: bool = False,
    ) -> Iterator[pfs_proto.DiffFileResponse]:
        """Diffs two PFS files (file = commit + path in Pachyderm) and returns
        files that are different. Similar to ``git diff``.

        If `old_commit` or `old_path` are not specified, `old_commit` will be
        set to the parent of `new_commit` and `old_path` will be set to
        `new_path`.

        Parameters
        ----------
        new_commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The newer subcommit (commit at the repo-level).
        new_path : str
            The path in `new_commit` to compare with.
        old_commit : Union[tuple, dict, Commit, pfs_proto.Commit], optional
            The older subcommit (commit at the repo-level).
        old_path : str, optional
            The path in `old_commit` to compare with.
        shallow : bool, optional
            Unused.

        Returns
        -------
        Iterator[pfs_proto.DiffFileResponse]
            An iterator of protobuf objects that contain info on files whose
            content has changed between commits. If a file under one of the
            paths is only in one commit, than the ``DiffFileResponse`` for it
            will only have one ``FileInfo`` set.
        """
        if old_commit is not None and old_path is not None:
            old_file = pfs_proto.File(commit=commit_from(old_commit), path=old_path)
        else:
            old_file = None

        return self._req(
            Service.PFS,
            "DiffFile",
            new_file=pfs_proto.File(commit=commit_from(new_commit), path=new_path),
            old_file=old_file,
            shallow=shallow,
        )


class ModifyFileClient:
    """`ModifyFileClient` puts or deletes PFS files atomically."""

    def __init__(self, commit: Union[tuple, dict, Commit, pfs_proto.Commit]):
        self._ops = []
        self.commit = commit_from(commit)

    def _reqs(self) -> Iterator[pfs_proto.ModifyFileRequest]:
        yield pfs_proto.ModifyFileRequest(set_commit=self.commit)
        for op in self._ops:
            yield from op.reqs()

    def put_file_from_filepath(
        self,
        pfs_path: str,
        local_path: str,
        datum: str = None,
        append: bool = False,
    ) -> None:
        """Uploads a PFS file from a local path at a specified path. This will
        lazily open files, which will prevent too many files from being
        opened, or too much memory being consumed, when atomically putting
        many files.

        Parameters
        ----------
        pfs_path : str
            The path in the repo the file will be written to.
        local_path : str
            The local file path.
        datum : str, optional
            A tag for the added file.
        append : bool, optional
            If true, appends the content of `local_path` to the file at
            `pfs_path`, if it already exists. Otherwise, overwrites the file.
        """
        self._ops.append(
            AtomicModifyFilepathOp(
                pfs_path,
                local_path,
                datum,
                append,
            )
        )

    def put_file_from_fileobj(
        self,
        path: str,
        value: BinaryIO,
        datum: str = None,
        append: bool = False,
    ) -> None:
        """Uploads a PFS file from a file-like object.

        Parameters
        ----------
        path : str
            The path in the repo the file will be written to.
        value : BinaryIO
            The file-like object.
        datum : str, optional
            A tag for the added file.
        append : bool, optional
            If true, appends the content of `value` to the file at `path`,
            if it already exists. Otherwise, overwrites the file.
        """
        self._ops.append(
            AtomicModifyFileobjOp(
                path,
                value,
                datum,
                append,
            )
        )

    def put_file_from_bytes(
        self,
        path: str,
        value: bytes,
        datum: str = None,
        append: bool = False,
    ) -> None:
        """Uploads a PFS file from a bytestring.

        Parameters
        ----------
        path : str
            The path in the repo the file will be written to.
        value : BinaryIO
            The file-like object.
        datum : str, optional
            A tag for the added file.
        append : bool, optional
            If true, appends the content of `value` to the file at `path`,
            if it already exists. Otherwise, overwrites the file.
        """
        self.put_file_from_fileobj(
            path,
            io.BytesIO(value),
            datum=datum,
            append=append,
        )

    def put_file_from_url(
        self,
        path: str,
        url: str,
        datum: str = None,
        append: bool = False,
        recursive: bool = False,
    ) -> None:
        """Uploads a PFSFile from the content found at a URL. The URL is
        sent to the server which performs the request.

        Parameters
        ----------
        path : str
            The path in the repo the file will be written to.
        url : str
            The URL of the file to upload.
        datum : str, optional
            A tag for the added file.
        append : bool, optional
            If true, appends the content to the file at `path`, if it
            already exists. Otherwise, overwrites the file.
        recursive : bool, optional
            If true, allows for recursive scraping on some types URLs, for
            example on s3:// URLs
        """
        self._ops.append(
            AtomicModifyFileURLOp(
                path,
                url,
                datum=datum,
                append=append,
                recursive=recursive,
            )
        )

    def delete_file(self, path: str, datum: str = None) -> None:
        """Deletes a file.

        Parameters
        ----------
        path : str
            The path to the file.
        datum : str, optional
            A tag that filters the files.
        """
        self._ops.append(AtomicDeleteFileOp(path, datum=datum))

    def copy_file(
        self,
        source_commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        source_path: str,
        dest_path: str,
        datum: str = None,
        append: bool = False,
    ) -> None:
        """Copy a file.

        Parameters
        ----------
        source_commit : Union[tuple, dict, Commit, pfs_proto.Commit]
            The commit the source file is in.
        source_path : str
            The path to the source file.
        dest_path : str
            The path to the destination file.
        datum : str, optional
            A tag for the added file.
        append : bool, optional
            If true, appends the content of the source file to the
            destination file, if it already exists. Otherwise, overwrites
            the file.
        """
        self._ops.append(
            AtomicCopyFileOp(
                source_commit,
                source_path,
                dest_path,
                datum=datum,
                append=append,
            )
        )


class AtomicOp:
    """Represents an operation in a `ModifyFile` call."""

    def __init__(self, path: str, datum: str):
        self.path = path
        self.datum = datum

    def reqs(self):
        """Yields one or more protobuf `ModifyFileRequests`, which are then
        enqueued into the request's channel.
        """
        pass


class AtomicModifyFilepathOp(AtomicOp):
    """A `ModifyFile` operation to put a file locally stored at a given path.
    This file is opened on-demand, which helps with minimizing the number of
    open files.
    """

    def __init__(
        self, pfs_path: str, local_path: str, datum: str = None, append: bool = False
    ):
        super().__init__(pfs_path, datum)
        self.local_path = local_path
        self.append = append

    def reqs(self) -> Iterator[pfs_proto.ModifyFileRequest]:
        if not self.append:
            yield _delete_file_req(self.path, self.datum)
        with open(self.local_path, "rb") as f:
            yield _add_file_req(path=self.path, datum=self.datum)
            for _, chunk in enumerate(f):
                yield _add_file_req(path=self.path, datum=self.datum, chunk=chunk)


class AtomicModifyFileobjOp(AtomicOp):
    """A `ModifyFile` operation to put a file from a file-like object."""

    def __init__(
        self, path: str, fobj: BinaryIO, datum: str = None, append: bool = False
    ):
        super().__init__(path, datum)
        self.fobj = fobj
        self.append = append

    def reqs(self) -> Iterator[pfs_proto.ModifyFileRequest]:
        if not self.append:
            yield _delete_file_req(self.path, self.datum)
        yield _add_file_req(path=self.path, datum=self.datum)
        for _ in itertools.count():
            chunk = self.fobj.read(BUFFER_SIZE)
            if len(chunk) == 0:
                return
            yield _add_file_req(path=self.path, datum=self.datum, chunk=chunk)


class AtomicModifyFileURLOp(AtomicOp):
    """A `ModifyFile` operation to put a file from a URL."""

    def __init__(
        self,
        path: str,
        url: str,
        datum: str = None,
        append: bool = False,
        recursive: bool = False,
    ):
        super().__init__(path, datum)
        self.url = url
        self.recursive = recursive
        self.append = append

    def reqs(self) -> Iterator[pfs_proto.ModifyFileRequest]:
        if not self.append:
            yield _delete_file_req(self.path, self.datum)
        yield pfs_proto.ModifyFileRequest(
            add_file=pfs_proto.AddFile(
                path=self.path,
                datum=self.datum,
                url=pfs_proto.AddFile.URLSource(
                    URL=self.url,
                    recursive=self.recursive,
                ),
            ),
        )


class AtomicCopyFileOp(AtomicOp):
    """A `ModifyFile` operation to copy a file."""

    def __init__(
        self,
        source_commit: Union[tuple, dict, Commit, pfs_proto.Commit],
        source_path: str,
        dest_path: str,
        datum: str = None,
        append: bool = False,
    ):
        super().__init__(dest_path, datum)
        self.source_commit = commit_from(source_commit)
        self.source_path = source_path
        self.dest_path = dest_path
        self.append = append

    def reqs(self) -> Iterator[pfs_proto.ModifyFileRequest]:
        yield pfs_proto.ModifyFileRequest(
            copy_file=pfs_proto.CopyFile(
                append=self.append,
                datum=self.datum,
                dst=self.dest_path,
                src=pfs_proto.File(commit=self.source_commit, path=self.source_path),
            ),
        )


class AtomicDeleteFileOp(AtomicOp):
    """A `ModifyFile` operation to delete a file."""

    def __init__(self, pfs_path: str, datum: str = None):
        super().__init__(pfs_path, datum)

    def reqs(self):
        yield _delete_file_req(self.path, self.datum)


def _add_file_req(path: str, datum: str = None, chunk: bytes = None):
    return pfs_proto.ModifyFileRequest(
        add_file=pfs_proto.AddFile(
            path=path, datum=datum, raw=wrappers_pb2.BytesValue(value=chunk)
        ),
    )


def _delete_file_req(path: str, datum: str = None):
    return pfs_proto.ModifyFileRequest(
        delete_file=pfs_proto.DeleteFile(path=path, datum=datum)
    )
