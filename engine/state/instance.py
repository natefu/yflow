from abc import abstractmethod, ABCMeta


class InstanceState(metaclass=ABCMeta):

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
    def approve(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')


class InstanceReadyState(InstanceState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def approve(self):
        pass

    def deny(self):
        pass


class InstanceRunningState(InstanceState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def approve(self):
        pass

    def deny(self):
        pass


class InstanceFinishedState(InstanceState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def approve(self):
        pass

    def deny(self):
        pass


class InstanceFailedState(InstanceState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def approve(self):
        pass

    def deny(self):
        pass


class InstanceApprovedState(InstanceState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def approve(self):
        pass

    def deny(self):
        pass


class InstanceDeniedState(InstanceState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def approve(self):
        pass

    def deny(self):
        pass
