from abc import abstractmethod, ABCMeta


class NodeState(metadata=ABCMeta):

    def __init__(self, runtime):
        self.runtime = runtime

    @abstractmethod
    def run(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def complete(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def fail(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def wait(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def approved(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def skip(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def retry(self):
        raise NotImplementedError('NOT IMPLEMENT')


class NodeReadyState(NodeState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def wait(self):
        pass

    def approved(self):
        pass

    def deny(self):
        pass

    def skip(self):
        pass

    def retry(self):
        pass


class NodeRunningState(NodeState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def wait(self):
        pass

    def approved(self):
        pass

    def deny(self):
        pass

    def skip(self):
        pass

    def retry(self):
        pass


class NodeSkippedState(NodeState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def wait(self):
        pass

    def approved(self):
        pass

    def deny(self):
        pass

    def skip(self):
        pass

    def retry(self):
        pass


class NodeFailedState(NodeState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def wait(self):
        pass

    def approved(self):
        pass

    def deny(self):
        pass

    def skip(self):
        pass

    def retry(self):
        pass


class NodeApprovedState(NodeState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def wait(self):
        pass

    def approved(self):
        pass

    def deny(self):
        pass

    def skip(self):
        pass

    def retry(self):
        pass


class NodeDeniedState(NodeState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def wait(self):
        pass

    def approved(self):
        pass

    def deny(self):
        pass

    def skip(self):
        pass

    def retry(self):
        pass


class NodePendingState(NodeState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def wait(self):
        pass

    def approved(self):
        pass

    def deny(self):
        pass

    def skip(self):
        pass

    def retry(self):
        pass


class NodeFinishedState(NodeState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def wait(self):
        pass

    def approved(self):
        pass

    def deny(self):
        pass

    def skip(self):
        pass

    def retry(self):
        pass
