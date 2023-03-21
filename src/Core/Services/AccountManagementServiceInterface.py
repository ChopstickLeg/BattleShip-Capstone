from abc import ABC, abstractmethod
from uuid import uuid4
from ..Data import *

class AccountManagementServiceInterface(ABC):
    @abstractmethod
    def createAccount(self, user, passwd, conn):
        raise NotImplementedError()